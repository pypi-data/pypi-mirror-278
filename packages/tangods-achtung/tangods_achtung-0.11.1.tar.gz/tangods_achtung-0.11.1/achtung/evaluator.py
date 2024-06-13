import asyncio
from collections import defaultdict
from functools import lru_cache, reduce
import logging
import math
import operator
import re
from time import perf_counter
from typing import Mapping, Any, Set, Iterator

from pyparsing import (  # type: ignore
    Regex,
    Literal,
    oneOf,
    ZeroOrMore,
    Char,
    infixNotation,
    opAssoc,
    nums,
    alphas,
    quoted_string,
    ParseResults,
    ParserElement,
    pyparsing_common,
    Combine
)
import tango  # type: ignore
from tango.asyncio import DeviceProxy  # type: ignore

from .util import Timer


ParserElement.enablePackrat()


def invert(nbr):
    return -nbr


def _generate_named_results(results: ParseResults, key: str) -> Iterator[Any]:
    if isinstance(results, ParseResults):
        value = results.get(key)
        if value is not None:
            yield value
        for res in results:
            yield from _generate_named_results(res, key)


def get_named_results(results: ParseResults, name: str) -> Set[Any]:
    "Return the set of named results, recursively."
    return set(_generate_named_results(results, name))


class AlarmEvaluator:

    """Handles parsing and evaluation of alarms"""

    ATTRIBUTE_PREFIX_RE = r"tango://[^:]+:\d+/"
    ATTRIBUTE_RE = fr"(?:{ATTRIBUTE_PREFIX_RE})?[\-\w.@_]+/[\-\w.@_]+/[\-\w.@_]+/[\-\w.@_]+"
    STATE_ATTRIBUTE_RE = fr"(?:{ATTRIBUTE_PREFIX_RE})?[\-\w.@_]+/[\-\w.@_]+/[\-\w.@_]+/state(\.[_a-z]+)?"

    nbr_float = pyparsing_common.sci_real
    nbr_int = pyparsing_common.signed_integer
    variable = (Combine((Char(alphas) | "_") - ZeroOrMore(Char(alphas) | Char(nums) | "_")))
    state_attribute = Regex(STATE_ATTRIBUTE_RE, flags=re.IGNORECASE).set_results_name("state_attribute")
    attribute = Regex(ATTRIBUTE_RE).set_results_name("attribute")

    keywords = {
        "False": False,
        "false": False,
        "FALSE": False,
        "True": True,
        "true": True,
        "TRUE": True,
        "ATTR_VALID": tango._tango.AttrQuality.ATTR_VALID,
        "ATTR_ALARM": tango._tango.AttrQuality.ATTR_ALARM,
        "ATTR_INVALID": tango._tango.AttrQuality.ATTR_INVALID,
        "ATTR_CHANGING": tango._tango.AttrQuality.ATTR_CHANGING,
        "ATTR_WARNING": tango._tango.AttrQuality.ATTR_WARNING,
        "ALARM": tango.DevState.ALARM,
        "EXTRACT": tango.DevState.EXTRACT,
        "INSERT": tango.DevState.INSERT,
        "ON": tango.DevState.ON,
        "STANDBY": tango.DevState.STANDBY,
        "CLOSE": tango.DevState.CLOSE,
        "FAULT": tango.DevState.FAULT,
        "MOVING": tango.DevState.MOVING,
        "OPEN": tango.DevState.OPEN,
        "UNKNOWN": tango.DevState.UNKNOWN,
        "DISABLE": tango.DevState.DISABLE,
        "INIT": tango.DevState.INIT,
        "OFF": tango.DevState.OFF,
        "RUNNING": tango.DevState.RUNNING,
    }

    operand = reduce(operator.or_, [quoted_string, nbr_float, nbr_int,
                                    *keywords.keys(),
                                    state_attribute, attribute, variable])

    powop = Literal("^") | Literal("**")
    signop = oneOf("+ -")
    notop = Literal("!") | Literal("not")
    multop = oneOf("* /")
    plusop = oneOf("+ -")
    compop = oneOf("< >")
    lesseqop = Literal("<=")
    gteqop = Literal(">=")
    equalop = Literal("==")
    nequalop = Literal("!=")
    inop = Literal("in")
    andop = Literal("and")
    orop = Literal("or")
    absop = Literal("abs")
    sinop = Literal("sin")
    cosop = Literal("cos")
    # tanop = Literal("tan")  # TODO collides with "tango" URLs
    expop = Literal("exp")
    roundop = Literal("round")

    operations = {
        "+": operator.add,
        "-": operator.sub,
        "**": operator.pow,
        "*": operator.mul,
        "/": operator.truediv,
        "and": operator.and_,
        "or": operator.or_,
        "<": operator.lt,
        ">": operator.gt,
        "<=": operator.le,
        ">=": operator.ge,
        "!=": operator.ne,
        "==": operator.eq,
        "^": operator.pow,
        "in": lambda a, b: operator.contains(b, a),
    }

    operations_single = {
        "!": operator.not_,
        "not": operator.not_,
        "-": invert,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "exp": math.exp,
        "abs": abs,
        "round": round,
    }

    expr = infixNotation(
        operand,
        [
            ("**", 2, opAssoc.RIGHT),
            ("^", 2, opAssoc.RIGHT),
            (sinop, 1, opAssoc.RIGHT),
            (cosop, 1, opAssoc.RIGHT),
            # (tanop, 1, opAssoc.RIGHT),
            (expop, 1, opAssoc.RIGHT),
            (absop, 1, opAssoc.RIGHT),
            (roundop, 1, opAssoc.RIGHT),
            (notop, 1, opAssoc.RIGHT),
            (signop, 1, opAssoc.RIGHT),
            (multop, 2, opAssoc.LEFT),
            (plusop, 2, opAssoc.LEFT),
            (compop, 2, opAssoc.LEFT),
            (gteqop, 2, opAssoc.LEFT),
            (lesseqop, 2, opAssoc.LEFT),
            (equalop, 2, opAssoc.LEFT),
            (nequalop, 2, opAssoc.LEFT),
            (andop, 2, opAssoc.LEFT),
            (orop, 2, opAssoc.LEFT),
            (inop, 2, opAssoc.RIGHT),
        ],
    )

    def __init__(self, logger=None, get_device_proxy=None, timeout: int = 1):
        self.formulas: Mapping[str, ParseResults] = {}
        self.variables: Mapping[str, ParserElement] = {}
        self.timers: Mapping[str, Timer] = defaultdict(Timer)
        self.timeout = timeout
        self._device_proxies: Mapping[str, DeviceProxy] = {}
        self.attr_read: Mapping[str, Any] = {}
        self.logger = logger or logging.getLogger(__name__)
        self._get_device_proxy = get_device_proxy or DeviceProxy
        self.logger.info("Created new evaluator")

    async def get_device_proxy(self, device_name):
        """Simple cache for device proxies."""
        result = self._device_proxies.get(device_name)
        if isinstance(result, tango.DeviceProxy):
            # proxy already exists, just return it
            return result
        if isinstance(result, asyncio.Event):
            # Someone else already started creating a proxy, let's
            # wait for that and then return it.
            await result.wait()
            return self._device_proxies[device_name]
        if isinstance(result, tango.DevFailed):
            # Proxy could not be created, we raise the same error
            # until restart/Init. See below.
            raise result
        # No proxy exists for this device, let us create it.
        event = asyncio.Event()
        self._device_proxies[device_name] = event
        try:
            proxy = await self._get_device_proxy(device_name)
            proxy.set_timeout_millis(int(self.timeout * 1000))
            self._device_proxies[device_name] = proxy
            event.set()
            return proxy
        except tango.DevFailed as e:
            # Failed to create proxy. This should only happen if the device
            # doesn't exist in the DB (?), and therefore it's unlikely to recover
            # by itself. So we store the error and raise it.
            self.logger.warn("Failed to create proxy to %r: %s",
                             device_name, e.args[0].desc)
            self._device_proxies[device_name] = e
            event.set()
            raise

    def add_formula(self, formula):
        name, formula = formula.split(":", 1)
        start = perf_counter()
        parsed = self.expr.parseString(formula, True)
        self.logger.debug("parse {} took {}s".format(formula, perf_counter() - start))
        self.logger.debug("parsed result: %r", parsed)
        self.formulas[name] = parsed
        return get_named_results(parsed, "state_attribute")

    def add_variable(self, formula):
        name, formula = formula.split(":", 1)
        start = perf_counter()
        parsed = self.expr.parseString(formula)
        self.logger.debug("parse %r took %fs", formula, perf_counter() - start)
        self.variables[name] = parsed

    async def _read_attr(self, attr):
        # TODO perhaps we could gain some performance by batching this,
        # to read all attributes from the same device in one call.
        device, attribute = attr.rsplit("/", 1)
        self.logger.debug("Getting proxy for %r", device)
        proxy = await self.get_device_proxy(device)
        # TODO handle errors
        return await proxy.read_attribute(attribute)

    @lru_cache()
    def _get_attr_prop(self, formula):
        if formula.endswith((".value", ".quality", ".not_readable", ".not_accessible", ".exception")):
            attr, prop = formula.rsplit(".", 1)
        else:
            attr = formula
            prop = "value"
        return attr, prop

    @lru_cache()
    def _check_attr(self, formula):
        return re.match(self.ATTRIBUTE_RE, formula)

    async def get_value(self, formula):
        if isinstance(formula, (float, int, bool)):
            # Simple value
            return formula, {}
        elif isinstance(formula, str) and formula.startswith(("'", '"')):
            # Value is a string, which includes quotes
            return formula.strip(formula[0]), {}
        elif formula in self.keywords:
            return self.keywords[formula], {}
        elif formula in self.variables:
            value, sub_values = await self._evaluate_formula(self.variables[formula])
            sub_values[formula] = value
            return value, sub_values
        elif self._check_attr(formula):
            attr, prop = self._get_attr_prop(formula)

            if prop in ("not_readable", "not_accessible", "exception"):
                try:
                    await self._read_attr(attr)
                    value = False
                except tango.DevFailed as exc:
                    connection_error = isinstance(exc, tango.ConnectionFailed) or "API_DeviceNotDefined" in str(exc)
                    # checking string to avoid another db call to check if the device exists
                    if prop == "not_accessible" and connection_error:
                        value = True
                    elif prop == "not_readable" and not connection_error:
                        value = True
                    elif prop == "exception":
                        value = True
                    else:
                        raise  # probably a bug with DS. We don't want to catch that (?)

            else:
                self.logger.debug("Reading attribute %r", attr)
                attr_data = await self._read_attr(attr)
                value = getattr(attr_data, prop)
                self.attr_read[formula] = value

            return value, {attr: value}
        raise ValueError(f"Can't find value for '{formula}'! Check spelling?")

    async def _evaluate_formula(self, formula, sub_values=None):
        f = []
        sub_values = sub_values or {}
        value = None
        for part in formula:
            if isinstance(part, ParseResults):
                value, sub_values_ = await self._evaluate_formula(part, sub_values)
                sub_values.update(sub_values_)
                f.append(value)
            else:
                f.append(part)
        n_parts = len(f)
        if n_parts == 3:
            left, l_sub_values = await self.get_value(f[0])
            sub_values.update(l_sub_values)
            right, r_sub_values = await self.get_value(f[2])
            sub_values.update(r_sub_values)
            value = self.operations[f[1]](left, right)
        elif n_parts == 2:
            if f[0] in self.operations_single:
                arg, sub_values_ = await self.get_value(f[1])
                sub_values.update(sub_values_)
                value = self.operations_single[f[0]](arg)
            # elif f[1] in self.operations_single:
            #    value = self.operations_single[f[1]](self.get_value(f[2]))
            else:
                value = None
        elif n_parts == 1:
            value, sub_values_ = await self.get_value(f[0])
            sub_values.update(sub_values_)

        return value, sub_values

    async def evaluate(self, name):
        formula = self.formulas[name]
        start = perf_counter()
        try:
            # This wait_for should not be needed since we set a timeout on the proxies.
            # It's here for safety.
            # TODO check performance impact of wait_for creating tasks for each eval
            value, sub_values = await asyncio.wait_for(self._evaluate_formula(formula),
                                                       timeout=self.timeout * 1.1)
        except asyncio.TimeoutError:
            t = perf_counter() - start
            self.timers[name].add(t)
            self.logger.warn("Evaluation of formula %r took too long (%f s)", name, t)
            raise RuntimeError(f"Evaluation took longer than the timeout setting ({self.timeout} s).")
        except tango.DevFailed as e:
            t = perf_counter() - start
            self.timers[name].add(t)
            self.logger.warn("Failed to evaluate formula %r: %r (took %f s)", name, e.args[0].desc, t)
            raise

        t = perf_counter() - start
        self.timers[name].add(t)
        self.logger.debug("Evaluated formula %r => %r (took %f s)", name, value, t)
        return value, sub_values

    async def evaluate_many(self, names):
        self.attr_read.clear()
        return await asyncio.gather(*(self.evaluate(name) for name in names),
                                    return_exceptions=True)
