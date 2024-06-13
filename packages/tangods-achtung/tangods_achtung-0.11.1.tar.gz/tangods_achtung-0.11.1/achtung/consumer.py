import asyncio
import httpx


async def check_http_consumers(urls, logger, timeout=2):
    # Do a simple get to ensure something is there
    errors = []
    for url in urls:
        async with httpx.AsyncClient() as client:
            try:
                result = await client.get(url, timeout=timeout)
                result.raise_for_status()
            except httpx.HTTPError as e:
                logger.error("Failed to talk to consumer %r: %s", url, e)
                msg = f"HttpConsumers[{url}]: {e}"
                errors.append(msg)
    return errors


async def http_consumer_task(url, event, queues, errors, logger,
                             retry=1, max_errors=5, timeout=3, extras=None):
    """Task that handles sending reports to one HTTP consumer."""

    n_errors = 0
    logger.info("HTTP consumer task for %r starting.", url)
    while True:
        try:
            # Wait for any new reports, but max X s (for retries)
            await asyncio.wait_for(event.wait(), timeout=retry)
        except asyncio.TimeoutError:
            pass
        if not queues.get(url):
            # No new reports, and nothing to retry. Never mind!
            continue

        # We have reports to send
        reports = list(queues[url])  # make a copy
        logger.debug("HTTP consumer task for %r sending %d reports.",
                     url, len(reports))
        if extras:
            reports = [{**extras, **report} for report in reports]
        try:
            async with httpx.AsyncClient() as client:
                result = await client.post(url, json=reports, timeout=timeout)
                result.raise_for_status()
        except httpx.HTTPError as e:
            n_errors += 1
            if n_errors > max_errors:
                # Too many errors; put the device into FAULT
                logger.error("Too many failures (%d) with HTTP consumer %r!",
                             n_errors, url)
                errors[url] = e
            else:
                logger.warn("Failed to send reports to HTTP consumer %r: %r, retrying...",
                            e, url)
        else:
            # All is well; all is forgiven!
            errors.pop(url, None)
            n_errors = 0

            # Remove the sent reports from queue
            n = len(reports)
            queues[url] = queues[url][n:]
