##############################################################################
#     Achtung
#
#     Copyright (C) 2019  MAX IV Laboratory, Lund Sweden.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see [http://www.gnu.org/licenses/].
###############################################################################

import asyncio
import json
from logging.handlers import RotatingFileHandler
from time import perf_counter, time
from typing import Dict, Set, Optional, List

import httpx
from pyparsing import ParseException  # type: ignore
import tango  # type: ignore
from tango import AttrWriteType, DispLevel, Attr, UserDefaultAttrProp, GreenMode
from tango.server import (  # type: ignore
    Device,
    attribute,
    command,
    device_property,
    class_property,
    run
)

from .evaluator import AlarmEvaluator
from .alarm import Alarm, Action
from .util import Timer, JsonFormatter
from .consumer import check_http_consumers, http_consumer_task


class PyAlarm(Device):
    # ========== properties ==========
    AlarmList = device_property(
        dtype=[str],
        default_value=[],
        doc="List of alarms with formulas e.g. TAG:FORMULA")
    AlarmDescriptions = device_property(
        dtype=[str],
        default_value=[],
        doc="List of alarms with descriptions e.g. TAG:DESCRIPTION")
    AlarmSeverities = device_property(
        dtype=[str],
        default_value=[],
        doc="List of alarms with severities e.g. TAG:SEVERITY")
    AlarmThreshold = device_property(
        dtype=int,
        default_value=1,
        doc="Number of cycles that an alarm must evaluate to True to be considered as active")
    EvalTimeout = device_property(
        dtype=float,
        default_value=2,
        doc="Any read attribute slower than timeout will raise exception")
    PollingPeriod = device_property(
        dtype=float,
        default_value=5,
        doc="Period in seconds in which all attributes are polled")
    AutoReset = device_property(
        dtype=float,
        default_value=0,
        doc="Alarm will reset if the conditions are no longer active after the given interval")
    StartupDelay = device_property(
        dtype=float,
        default_value=0,
        doc="the device will wait before starting to evaluate alarms"
        + " (e.g. giving some time to the system to recover from a power-cut)")
    Variables = class_property(
        dtype=[str],
        default_value=[],
        doc="Place for declare variables which can be used in formulas")
    HttpConsumers = device_property(
        dtype=[str],
        default_value=[],
        doc="Any number of HTTP URLs to push updates to.")
    ResetActions = device_property(
        dtype=[str],
        default_value=[],
        doc="List of alarms with action. Run on manual reset of an alarm."
        + " E.g. TAG:[write_attribute/run_command];NAME_OF_ATTRIBUTE/COMMAND;JSON_ARGS")
    ReportExtras = device_property(
        dtype=str,
        default_value="{}",
        doc="JSON encoded dict of static values to add to all reports.")
    AlarmAttributeSeparator = device_property(
        dtype=str,
        default_value=":",
        doc="Separator to use in e.g. ActiveAlarms. Defaults to ':'.")

    ReportLogfile = device_property(
        dtype=str,
        default_value="",
        doc="Path to optional alarm report logfile."
    )
    ReportLogfileMaxBytes = device_property(
        dtype=int,
        default_value=1_000_000,
        doc="Max size of report logfile, before rotation"
    )
    ReportLogfileBackupCount = device_property(
        dtype=int,
        default_value=1,
        doc="Number of rotated report logfiles to keep."
    )

    # ========== attributes ==========

    nbr_alarms = attribute(
        label="nbr_alarms",
        dtype=int,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ,
        unit="",
        format="d",
        fget="get_nbr_alarms",
        fisallowed="is_device_operational",
        doc="Number of alarms",
    )

    ActiveAlarms = attribute(
        label="active_alarms",
        dtype=[tango.DevString],
        max_dim_x=10000,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ,
        fget="get_active_alarms",
        fisallowed="is_device_operational",
        doc="Active alarms",
    )

    AcknowledgedAlarms = attribute(
        label="acknowledged_alarms",
        dtype=[tango.DevString],
        max_dim_x=10000,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ,
        fget="get_acknowledged_alarms",
        fisallowed="is_device_operational",
        doc="Acknowledged alarms",
    )

    FailedAlarms = attribute(
        label="failed_alarms",
        dtype=[tango.DevString],
        max_dim_x=10000,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ,
        fget="get_failed_alarms",
        fisallowed="is_device_operational",
        doc="Failed alarms",
    )

    DisabledAlarms = attribute(
        label="disabled_alarms",
        dtype=[tango.DevString],
        max_dim_x=10000,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ,
        fget="get_disabled_alarms",
        fisallowed="is_device_operational",
        doc="Disabled alarms",
    )

    AlarmsList = attribute(
        label="AlarmsList",
        dtype=[tango.DevString],
        max_dim_x=10000,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ,
        fget="get_alarm_list",
        fisallowed="is_device_operational",
        doc="List of alarms",
    )

    AlarmSummary = attribute(
        label="AlarmSummary",
        dtype=[tango.DevString],
        max_dim_x=10000,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ,
        fget="get_alarm_summary",
        fisallowed="is_device_operational",
        doc="Summary of alarms",
    )

    VersionNumber = attribute(
        label="VersionNumber",
        dtype=tango.DevString,
        display_level=DispLevel.EXPERT,
        access=AttrWriteType.READ,
        fget="get_version",
        doc="PyAlarm version number for PANIC",
    )

    green_mode = GreenMode.Asyncio

    # TODO maybe these could be properties
    HTTP_CONSUMER_MAX_BUFFER_SIZE = 10000
    HTTP_CONSUMER_RETRY_PERIOD = 3  # seconds
    HTTP_CONSUMER_MAX_ERRORS = 5
    # PyAlarm version is needed for PANIC compatibility.
    # Needs to be above 6.2.0 for PANIC GUI to work properly with Achtung and 9.1.4 is the current version of
    # PyAlarm installed together with PANIC GUI. No need to change that every PANIC update.
    CURRENT_PYALARM_VERSION = "9.1.4"

    async def init_device(self):

        self.logger = self.get_logger()
        self.logger.info("Starting up")

        self.get_device_properties()

        self.alarms: Dict[str, Alarm] = {}

        self.timer = Timer()
        self.start_time = time()
        self._update_lock = asyncio.Lock()
        self._stopped = asyncio.Event()
        self.update_task: Optional[asyncio.Task] = None
        self.http_consumer_tasks: Set[asyncio.Task] = set()

        self._http_consumer_event = asyncio.Event()
        self._http_consumer_reports: Dict[httpx.AsyncClient, List[Dict]] = {}
        self._http_consumer_errors: Dict[httpx.AsyncClient, Exception] = {}

        self.eval = AlarmEvaluator(self.logger, timeout=self.EvalTimeout)

        # Configuration

        formulas = {}
        severities = {}
        descriptions = {}
        reset_actions = {}

        # Collect all errors as we go.
        config_error_report = []

        self.autoreset = self.AutoReset

        for i, rawformula in enumerate(self.AlarmList):
            try:
                tag, formula = [word.strip() for word in rawformula.split(":", 1)]
            except ValueError as e:  # TODO check exception
                msg = f"AlarmList[{i}]: incomplete alarm {rawformula}, reason: {e}"
                config_error_report.append(msg)
                continue
            formulas[tag] = i, formula, rawformula

        def check_property(prop):
            "Parse a string property on format 'tag:value'."
            try:
                tag, value = [word.strip() for word in prop.split(":", 1)]
            except ValueError:
                msg = f"bad format '{prop}'. Expected <tag>:<value>"
                raise ValueError(msg)
            if tag not in formulas:
                msg = f"unknown alarm tag {tag}."
                raise ValueError(msg)
            return tag, value

        for i, sev in enumerate(self.AlarmSeverities):
            try:
                tag, severity = check_property(sev)
            except ValueError as e:
                config_error_report.append(f"AlarmSeverities[{i}]: {e}")
                continue
            severity = severity.upper()
            if severity not in Alarm.ALARM_PRIORITIES:
                msg = f"AlarmSeverities[{i}]: invalid severity {severity}"
                continue
            severities[tag] = severity
            # TODO missing severities

        for i, desc in enumerate(self.AlarmDescriptions):
            try:
                tag, description = check_property(desc)
            except ValueError as e:
                config_error_report.append(f"AlarmDescriptions[{i}]: {e}")
                continue
            descriptions[tag] = description

        for i, property_ in enumerate(self.ResetActions):
            try:
                tag, value = check_property(property_)
                if tag not in reset_actions:
                    reset_actions[tag] = Action.from_string(value)
                else:
                    raise ValueError(f"Multiple actions defined for {tag}. Achtung supports one action per alarm")
            except ValueError as e:
                config_error_report.append(f"ResetActions[{i}]: {e}")
                continue

        # Now we should have all the info and can build the alarms
        device = self.get_name()
        for tag, (i, formula, rawformula) in formulas.items():
            try:
                state_attrs = self.eval.add_formula(rawformula)
            except ParseException as e:
                msg = f"AlarmList[{i}]: failed to parse '{rawformula}' reason={e}"
                config_error_report.append(msg)
                continue
            alarm = Alarm(
                formula=formula,
                rawformula=rawformula,
                name=tag,
                severity=severities.get(tag, "ALARM"),
                desc=descriptions.get(tag, ""),
                device=device,
                autoreset=self.AutoReset,
                logger=self.logger,
                reset_action=reset_actions.get(tag, None),
                checks_state=bool(state_attrs)
            )
            self.alarms[tag] = alarm

        for i, rawvariable in enumerate(self.Variables):
            try:
                self.eval.add_variable(rawvariable)
            except ParseException as e:
                msg = f"Variables[{i}]: failed to parse {rawvariable}, reason: {e}"
                config_error_report.append(msg)
            # TODO we could check that all used variables are also defined

        try:
            self.report_extras = json.loads(self.ReportExtras)
        except ValueError as e:
            config_error_report.append(f"ReportExtras property must be valid JSON: {e}")

        # HTTP consumers
        if self.HttpConsumers:
            self.logger.info("Checking HTTPConsumers property: %r", self.HttpConsumers)
            errors = await check_http_consumers(self.HttpConsumers, self.logger)
            if errors:
                config_error_report.extend(errors)

        # Check if we had errors
        # Any errors in config will put the device in FAULT and prevent it from starting.
        if config_error_report:
            self.set_status(
                "Device in FAULT because of errors in configuration properties:\n"
                + "\n".join(config_error_report))
            self.set_state(tango.DevState.FAULT)
            self.logger.fatal("Device did not start up because of configuration errors.")
            for msg in config_error_report:
                self.logger.error(msg.replace("%", "%%"))  # To be safe; % can break logging
            return

        # Everything is fine, let's start up

        def log_task_exception(task):
            "Helper to log tasks that exit due to uncaught exceptions"
            try:
                task.result()
            except Exception as e:
                self.logger.error("Task %r exited with exception: %r", task, e)
            else:
                self.logger.info("Task %r exited normally", task)

        # we're doing sequential evaluation to give enough time for Achtung to create connections. Dry run
        for alarm in [name for name, alarm in self.alarms.items() if alarm.enabled]:
            try:
                await self.eval.evaluate(alarm)
            except Exception:
                pass

        if self.PollingPeriod > 0:
            self.update_task = asyncio.ensure_future(self._alarm_updater())
            self.update_task.add_done_callback(log_task_exception)
        else:
            self.set_status("Device off because PollingPeriod is 0.")
            self.set_state(tango.DevState.OFF)
            return

        for url in self.HttpConsumers:
            queue = []
            self._http_consumer_reports[url] = queue
            task = asyncio.ensure_future(
                http_consumer_task(
                    url,
                    self._http_consumer_event,
                    self._http_consumer_reports,
                    self._http_consumer_errors,
                    self.logger,
                    retry=self.HTTP_CONSUMER_RETRY_PERIOD,
                    max_errors=self.HTTP_CONSUMER_MAX_ERRORS,
                    extras=self.report_extras))
            self.http_consumer_tasks.add(task)
            task.add_done_callback(log_task_exception)

        if self.ReportLogfile:
            self.logger.info(f"Setting up report logfile at {self.ReportLogfile}")
            self.report_log_handler = RotatingFileHandler(
                self.ReportLogfile,
                maxBytes=self.ReportLogfileMaxBytes,
                backupCount=self.ReportLogfileBackupCount
            )
            json_formatter = JsonFormatter()
            self.report_log_handler.setFormatter(json_formatter)
        else:
            self.report_log_handler = None

        self.set_state(tango.DevState.ON)

    async def delete_device(self):
        self._stopped.set()
        for task in self.http_consumer_tasks:
            task.cancel()

    async def dev_state(self):
        if self._http_consumer_errors:
            return tango.DevState.FAULT
        return self.get_state()

    async def dev_status(self):
        self._status = self.get_status()
        if self._http_consumer_errors:
            self._status += "\n".join(
                ["Error sending alarm reports:",
                 *[f"{client.base_url}: {error}"
                   for client, error in self._http_consumer_errors.items()]])
        return self._status

    async def _update_alarms(self):
        "Update all alarms once."
        if not self.update_task:
            raise RuntimeError("Device is not operational; check Status for errors.")
        try:
            await asyncio.wait_for(self._update_lock.acquire(), 0.1)
        except asyncio.TimeoutError:
            # Evaluation already in progress, maybe someone ran the "update" command
            self.logger.warn("Skip evaluating alarms; evaluation already in progress.")
            return
        else:
            enabled_alarms = [name
                              for name, alarm in self.alarms.items()
                              if alarm.enabled]
            start = perf_counter()
            results = await self.eval.evaluate_many(enabled_alarms)
            t = perf_counter() - start
            self.logger.debug("Evaluation of %d alarms took %f s", len(enabled_alarms), t)
            self.timer.add(t)
            reports = []
            n_active = 0
            failed_alarms = []  # list of failed alarms that check device state in formula
            for tag, result in zip(enabled_alarms, results):
                alarm = self.alarms[tag]
                if isinstance(result, Exception):
                    # Evaluation failed
                    if isinstance(result, tango.DevFailed):
                        error = result.args[-1].desc
                    else:
                        error = str(result)
                    self.logger.error(
                        "Error processing alarm %r. Error: %s", tag, error
                    )
                    alarm.fail(result)
                    failed_alarms.append(alarm)
                else:
                    # Evaluation succeeded
                    value, sub_values = result
                    alarm.update(value, sub_values, self.AlarmThreshold)
                reports.extend(alarm.get_reports())
                if alarm.active:
                    n_active += 1

            # TODO should we sync up with whatever pyalarm does for status?
            if n_active > 0:
                status = f"There are {n_active} alarms currently active."
                self.set_state(tango.DevState.ALARM)
            else:
                status = "No active alarms."
                self.set_state(tango.DevState.ON)
            if len(failed_alarms) > 0:
                status += f"\n{len(failed_alarms)} alarms could not be evaluated:\n"
                for alarm in failed_alarms:
                    status += f" - {alarm.tag}: {str(alarm.get_exception_string())}\n"
            self.set_status(status)

            # Handle alarm reports
            if reports and self.HttpConsumers:
                self.logger.debug("Got %d new reports", len(reports))
                for url in self.HttpConsumers:
                    client_reports = self._http_consumer_reports.setdefault(url, [])
                    client_reports.extend(reports)
                    if len(client_reports) > self.HTTP_CONSUMER_MAX_BUFFER_SIZE:
                        # We don't want the reports buffer to grow indefinitely
                        self.logger.warn(
                            "Too many reports buffered for client %r; dropping some!",
                            url)
                        self._http_consumer_reports[url] = client_reports[-self.HTTP_CONSUMER_MAX_BUFFER_SIZE:]
                # Wake consumer tasks up
                self._http_consumer_event.set()
                await asyncio.sleep(0)
                self._http_consumer_event.clear()

            if reports and self.report_log_handler:
                self.logger.debug(f"Writing {len(reports)} reports to alarm logfile")
                for report in reports:
                    self.report_log_handler.emit({**report, **self.report_extras})

            self._update_lock.release()

    async def _alarm_updater(self):
        """Task that updates alarms continually."""
        self.logger.info("Update task starting")
        if self.StartupDelay > 0:
            self.set_state(tango.DevState.INIT)
            self.set_status(f"Alarms evaluation not started yet, waiting {self.StartupDelay} seconds.")
            await asyncio.sleep(self.StartupDelay)
            self.set_state(tango.DevState.ON)
        await self._sleep(self.PollingPeriod)
        while not self._stopped.is_set():
            start = perf_counter()
            try:
                await self._update_alarms()
            except Exception as e:
                print(e)
            # Adjust the sleep time according to how long the alarm evaluation took
            dt = perf_counter() - start
            if dt > self.PollingPeriod:
                self.logger.warn("Alarm evaluaton too slow; took %f s while PollingPeriod is %f s.",
                                 dt, self.PollingPeriod)
            await self._sleep(max(0, self.PollingPeriod - dt))
        self.logger.info("Update task exiting")

    async def _sleep(self, secs):
        "Sleep task that wakes up if the device is stopped."
        try:
            await asyncio.wait_for(self._stopped.wait(), secs)
        except asyncio.TimeoutError:
            pass

    def is_device_operational(self, attr):
        "Whether the device is currently running normally."
        return self.update_task and not self.update_task.done()

    def initialize_dynamic_attributes(self):

        self.logger.info("Create dynamic attributes")
        for name, alarm in self.alarms.items():
            # self.eval.add_formula(alarm.rawformula)
            self.logger.debug("Create dynamic attribute for alarm {}".format(name))
            attr = Attr(name, tango.DevBoolean, tango.READ)
            attr.set_disp_level(DispLevel.OPERATOR)
            attrprops = UserDefaultAttrProp()
            attrprops.set_description("Status of alarm {}".format(name))
            attr.set_default_properties(attrprops)
            self.add_attribute(
                attr, r_meth=self.read_alarm,
            )
        self.logger.info("Create dynamic attributes done")

    # ========== read methods ==========

    @tango.DebugIt()
    def read_alarm(self, attr):
        name = attr.get_name()
        alarm = self.alarms[name]
        value = alarm.enabled and alarm.active
        attr.set_value(value)
        self.logger.debug("Read alarm %r, value %r", attr, value)

    @tango.DebugIt()
    def get_nbr_alarms(self):
        return len(self.alarms)

    def join_sep(self, *fields):
        sep = self.AlarmAttributeSeparator
        return sep.join(fields)

    @tango.DebugIt()
    def get_active_alarms(self):
        active = (alarm
                  for alarm in self.alarms.values()
                  if alarm.active and alarm.enabled)
        # TODO pyalarm uses time.ctime to format the timestamp...?
        active_alarm_template = self.join_sep(
            "{alarm.tag}",
            "{alarm.active_since_isoformat}",
            "{alarm.formula}")
        return [active_alarm_template.format(alarm=a) for a in active]

    @tango.DebugIt()
    def get_disabled_alarms(self):
        disabled = (alarm
                    for alarm in self.alarms.values()
                    if not alarm.enabled)
        disabled_alarm_template = self.join_sep("{alarm.tag}", "{alarm.disabled_since_isoformat}")
        return [disabled_alarm_template.format(alarm=a) for a in disabled]

    @tango.DebugIt()
    def get_acknowledged_alarms(self):
        acked = (alarm
                 for alarm in self.alarms.values()
                 if alarm.enabled and alarm.acked)
        acked_alarm_template = "{alarm.tag}"
        return [acked_alarm_template.format(alarm=a) for a in acked]

    @tango.DebugIt()
    def get_failed_alarms(self):
        "Alarms that currently can't be evaluated, e.g. because they can't read an attribute."
        failed = (alarm
                  for alarm in self.alarms.values()
                  if alarm.failed)
        failed_alarm_template = self.join_sep("{alarm.tag}", "{alarm.failed_since_isoformat}")
        return [failed_alarm_template.format(alarm=a) for a in failed]

    @tango.DebugIt()
    def get_alarm_list(self):
        return [v.rawformula for v in self.alarms.values()]

    @tango.DebugIt()
    def get_alarm_summary(self):
        separator = ";"
        alarm_summary_template = separator.join([
            "tag={alarm.tag}",
            "state={alarm.state}",
            "priority={alarm.severity}",
            "time={alarm.active_since_isoformat}",
            "formula={alarm.formula}",
            "message={alarm.description}"
        ])
        return [alarm_summary_template.format(alarm=alarm)
                for alarm in self.alarms.values()]

    @tango.DebugIt()
    def get_version(self):
        return self.CURRENT_PYALARM_VERSION

    # ========== commands ==========

    @command()
    async def update(self):
        await self._update_alarms()

    @tango.DebugIt(show_args=True, show_ret=True)
    @command(dtype_in=str, dtype_out=str, doc_in="Alarm to enable")
    def Enable(self, name):
        self.alarms[name].enable()
        return "DONE"

    @tango.DebugIt(show_args=True, show_ret=True)
    @command(dtype_in=[str], dtype_out=str, doc_in="Alarms to disable")
    def Disable(self, names):
        name = names[0]
        comment = names[1]
        self.alarms[name].disable(comment)
        return "DONE"

    @tango.DebugIt(show_args=True, show_ret=True)
    @command(dtype_in=str, dtype_out=str, doc_in="Evaluate a formula")
    async def EvaluateFormula(self, formula):
        if formula in self.alarms.keys():
            self.logger.debug("Returning existing value")
            return str(self.alarms[formula].value)
        temp_eval = AlarmEvaluator()
        for rawvariable in self.Variables:
            temp_eval.add_variable(rawvariable)
        temp_eval.add_formula("test:" + formula)
        value, subvalues = await temp_eval.evaluate("test")
        return str(value)

    @tango.DebugIt(show_args=True, show_ret=True)
    @command(dtype_in=str, dtype_out=str, doc_in="Evaluate a formula")
    async def EvaluateFormulaExpert(self, formula):
        if formula in self.alarms.keys():
            self.logger.debug("Returning existing value")
            return str(self.alarms[formula].value)
        temp_eval = AlarmEvaluator()
        for rawvariable in self.Variables:
            temp_eval.add_variable(rawvariable)
        temp_eval.add_formula("test:" + formula)
        result = await temp_eval.evaluate("test")
        return json.dumps(result)

    @tango.DebugIt(show_args=True, show_ret=True)
    @command(dtype_in=str, dtype_out=bool, doc_in="Check if disabled")
    def CheckDisabled(self, name):
        return not self.alarms[name].enabled

    @tango.DebugIt(show_args=True, show_ret=True)
    @command(dtype_in=str, dtype_out=bool, doc_in="Check if acknowledged")
    def CheckAcknowledged(self, name):
        return not self.alarms[name].acked

    @tango.DebugIt(show_args=True, show_ret=True)
    @command(dtype_in=[str], dtype_out=[str], doc_in="Acknowledge an alarm")
    def Acknowledge(self, args):
        name = args[0]
        if len(args) > 1:
            comment = args[1]
        else:
            comment = ""
        self.alarms[name].acknowledge(comment)
        return []

    @tango.DebugIt(show_args=True, show_ret=True)
    @command(dtype_in=[str], dtype_out=[str], doc_in="Reset an alarm")
    async def ResetAlarm(self, args):
        try:
            name, comment = args
        except ValueError:
            raise RuntimeError("Wrong number of arguments; should be <tag>, <comment>")
        await self.alarms[name].reset(comment)
        return []

    @tango.DebugIt(show_args=True, show_ret=True)
    @command(dtype_in=str, dtype_out=[str], doc_in="Reset all alarms")
    async def ResetAll(self, comment):
        active_alarms = [alarm for alarm in self.alarms.values() if alarm.active]
        reset_actions = (alarm.reset(comment) for alarm in active_alarms)
        results = await asyncio.gather(*reset_actions, return_exceptions=True)
        failed_tags = []
        for alarm, result in zip(active_alarms, results):
            if result:
                self.logger.error("Failed to execute reset action %r: %s", alarm, result)
                failed_tags.append(alarm.tag)
        if failed_tags:
            raise RuntimeError(f"Reset actions for alarms {', '.join(failed_tags)} failed. Check logs!")
        return [alarm.tag for alarm in active_alarms]

    @tango.DebugIt(show_args=True, show_ret=True)
    @command(dtype_in=[str], dtype_out=int, doc_in="Evaluate a formula")  # TODO ?
    def CreateAlarmContext(self, values):
        return 1

    @command(dtype_out=str, doc_in="")
    def GetRelease(self):
        return self.CURRENT_PYALARM_VERSION

    @command(dtype_out=str, doc_in="Get evaluation statistics in JSON format.")
    def GetStatistics(self):
        return json.dumps(dict(
            device=self.timer.as_dict(),
            alarms={
                name: timer.as_dict()
                for name, timer in self.eval.timers.items()
            }
        ), indent=4)

    def get_fields(self, name, fields):
        mapping = {
            "tag": "name",
            "annunciators": "receiver",
            "priority": "severity",
            "message": "description",
            "acknowledged": "acked",
            "active": "active_since",
        }
        alarm = self.alarms[name]
        result = {}
        for field in fields:
            if field == "state":
                result[field] = alarm.state
            else:
                if field in mapping:
                    f = mapping[field]
                else:
                    f = field
                result[field] = getattr(alarm, f, None)
        return result

    @tango.DebugIt(show_args=True, show_ret=True)
    @command(dtype_in=[str], dtype_out=[str], doc_in="Get alarm info")
    def GetAlarmInfo(self, argin):
        DATA_FIELDS = (
            "tag",
            "device",
            "priority",
            "formula",
            "message",
            "annunciators",
        )
        STATE_FIELDS = (
            "state",
            "time",
            "counter",
            "active",
            "disabled",
            "acknowledged",
            "updated",
            "last_sent",
            "last_error",
        )
        name = argin[0]
        request = argin[1:] or ("SETTINGS", "VALUES")

        result = []
        for req in request:

            if req in DATA_FIELDS + STATE_FIELDS:
                val = self.get_fields(name, [req])[req]
                result.append("{}={}".format(req, val))

            if req == "SETTINGS":
                values = self.get_fields(name, DATA_FIELDS)
                for key, val in values.items():
                    if key == "message":
                        val = json.dumps(val)
                    result.append("{}={}".format(key, val))

        return result

    @tango.DebugIt(show_args=True, show_ret=True)
    @command(dtype_in=str, dtype_out=str, doc_in="Send test report to HTTP consumers")
    async def SendTestReport(self, msg):
        if self.HttpConsumers:
            report = {
                "description": "This just a test.",
                "user_comment": msg,
                "timestamp": time(),
                "priority": 100,
                "values": [],
                "device": self.get_name(),
                "formula": "False",
                "alarm_tag": "some_fake_test_tag",
                "severity": "DEBUG",
                "message": "ACTIVE",
            }
            for url in self.HttpConsumers:
                self._http_consumer_reports.setdefault(url, []).append(report)
            self._http_consumer_event.set()
            await asyncio.sleep(0)
            self._http_consumer_event.clear()
            return "Test message sent. Check logs for errors."
        else:
            raise RuntimeError("There are no consumers. Set HttpConsumers property.")


def main():
    run((PyAlarm,), green_mode=GreenMode.Asyncio)


if __name__ == "__main__":
    main()
