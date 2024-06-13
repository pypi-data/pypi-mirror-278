import asyncio
import logging

import httpx
import pytest

from . import get_open_port
from achtung.consumer import http_consumer_task


async def wake_up(event):
    """
    Wake the task waiting for the event
    """
    event.set()
    await asyncio.sleep(0)
    event.clear()
    await asyncio.sleep(0.1)  # allow things to happen


@pytest.mark.asyncio
async def test_http_consumer_send_report(mocker, httpserver):
    # Set up mock HTTP server
    httpserver.expect_request("/alarms", method="POST").respond_with_data()

    url = httpserver.url_for("alarms")
    event = asyncio.Event()
    queues = {}
    errors = {}
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    task = asyncio.ensure_future(http_consumer_task(url, event, queues, errors, logger))
    await asyncio.sleep(0)
    queues[url] = [{"message": "just testing"}]
    await wake_up(event)

    await asyncio.sleep(0.1)

    # Cleanly stop the task
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    await asyncio.sleep(0.1)

    httpserver.check_assertions()
    assert len(httpserver.log) == 1

    request1, _ = httpserver.log[0]
    report1 = request1.get_json()
    assert len(report1) == 1
    assert report1[0]["message"] == "just testing"


@pytest.mark.asyncio
async def test_http_consumer_retries_on_error(mocker, httpserver):
    httpserver.expect_request("/alarms/", method="POST").respond_with_data()

    url = httpserver.url_for("alarms/")
    event = asyncio.Event()
    queues = {}
    errors = {}
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    max_errors = 3

    # Take consumer down
    httpserver.stop()

    task = asyncio.ensure_future(
        http_consumer_task(
            url, event, queues, errors, logger,
            max_errors=max_errors, timeout=0.01))

    queues[url] = [{"message": "just testing"}]
    for i in range(3):
        await wake_up(event)
    assert len(httpserver.log) == 0

    # We don't report errors until max errors reached
    assert not errors

    # Now bring the consumer back
    httpserver.start()

    await wake_up(event)

    # Cleanly stop the task
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert not errors
    httpserver.check_assertions()
    assert len(httpserver.log) == 1


@pytest.mark.asyncio
async def test_http_consumer_reports_failure(mocker):
    free_port = get_open_port()
    url = f"http://localhost:{free_port}"  # Should be unreachable as nothing is listening
    event = asyncio.Event()
    queues = {}
    errors = {}
    logger = logging.getLogger()
    max_errors = 3
    task = asyncio.ensure_future(http_consumer_task(url, event, queues, errors,
                                                    logger, max_errors=max_errors))
    await asyncio.sleep(0)
    queues[url] = [{"message": "just testing"}]
    for i in range(max_errors + 1):  # Retry too many times
        await wake_up(event)

    # Cleanly stop the task
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert errors[url]
    error = errors[url]
    assert isinstance(error, httpx.HTTPError)


@pytest.mark.asyncio
async def test_http_consumer_buffers_reports(mocker, httpserver):
    httpserver.expect_request("/alarms/", method="POST").respond_with_data()

    url = httpserver.url_for("alarms/")
    event = asyncio.Event()
    queues = {}
    errors = {}
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    max_errors = 3

    # Bring consumer down for a while
    httpserver.stop()

    task = asyncio.ensure_future(
        http_consumer_task(
            url, event, queues, errors, logger,
            max_errors=max_errors, timeout=0.01))

    queues[url] = [{"message": "test"}]
    for i in range(3):
        await wake_up(event)
        # more reports coming in while consumer is down
        queues[url].append({"message": f"test{i}"})
    assert len(httpserver.log) == 0

    # Consumer is back
    httpserver.start()

    await wake_up(event)

    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    # Check that only one report was sent
    assert not errors
    httpserver.check_assertions()
    assert len(httpserver.log) == 1

    # Check that the report contains the right messages, in the right order
    request, _ = httpserver.log[0]
    report = request.get_json()
    assert len(report) == 4
    assert report[0]["message"] == "test"
    assert report[1]["message"] == "test0"
    assert report[2]["message"] == "test1"
    assert report[3]["message"] == "test2"
