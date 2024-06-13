import asyncio
from unittest.mock import Mock

import pytest
from tango import AttrQuality, DevFailed, DevError, ConnectionFailed

from achtung.evaluator import AlarmEvaluator


def make_devfailed(desc, exc_class=DevFailed):
    err = DevError()
    err.desc = desc
    return exc_class(err)


class _FakeDeviceProxy:
    "Just a completely fake device proxy"

    VALUES = {
        "sys/tg_test/2/ampli": (0, AttrQuality.ATTR_VALID, None),
        "sys/tg_test/2/boolean_scalar": (True, AttrQuality.ATTR_VALID, None),
        "sys/tg_test/2/string_scalar": ("Default string", AttrQuality.ATTR_VALID, None),
        "tango://a.b.c.d.e.f.g:10000/sys/tg_test/2/ampli": (0, AttrQuality.ATTR_VALID, None),

        "some/broken/device/attr": (None, None, make_devfailed("Oh no!")),
        "some/disconnected/device/attr": (None, None, make_devfailed("Oh no!", ConnectionFailed)),
        "some/not/defined/device": (None, None, make_devfailed("blah API_DeviceNotDefined blah")),

    }

    def __init__(self, device):
        self.device = device

    async def read_attribute(self, attr):
        mock = Mock()
        full_name = f"{self.device}/{attr}"
        mock.value, mock.quality, raises_exc = self.VALUES[full_name]
        if raises_exc:
            raise raises_exc
        return mock

    def set_timeout_millis(self, timeout):
        pass


async def FakeDeviceProxy(attr):
    return _FakeDeviceProxy(attr)


def test_parse():
    formula = "apa:(flepp123 == 3.32) or (a/b/c/d != 123)"
    evaluator = AlarmEvaluator()
    evaluator.add_formula(formula)
    result = evaluator.formulas["apa"][0]
    assert result[0][0] == "flepp123"
    assert result[0][2] == 3.32
    assert result[1] == "or"
    assert result[2][0] == "a/b/c/d"
    assert result[2][2] == 123


def test_parse_state_with_extra_prop():
    formula = "B312A_VAC_PLC_01_FAULT:B312A/VAC/PLC-01/STATE.exception or B312A/VAC/PLC-01/STATE==FAULT"
    evaluator = AlarmEvaluator()
    evaluator.add_formula(formula)
    result = evaluator.formulas["B312A_VAC_PLC_01_FAULT"][0]
    assert result[0] == "B312A/VAC/PLC-01/STATE.exception"
    assert result[1] == "or"
    assert result[2][0] == "B312A/VAC/PLC-01/STATE"
    assert result[2][1] == "=="
    assert result[2][2] == "FAULT"


EVALUATE_FORMULAS = [

    # Basic math
    ("25", 25),
    ("abs(-17.5)", 17.5),
    ("(17.5-7.5)", 10),
    ("round(3.14)-2.3", 0.7),
    ("(1.0-2.0)*2", -2.0),
    ("-2", -2),
    ("1-2", -1),
    ("sin(pi) < 0.01", True),
    ("2**2 == 4", True),
    ("2^2 == 4", True),
    ("exp(1) > 2 and exp(1) < 3", True),
    ("10E-5 > -10e-4", True),
    ("10**5 > 10**-6", True),
    ("7.92e-4 > 6.48e-4", True),

    # Other types
    ("sys/tg_test/2/string_scalar == 'Default string'", True),
    ("'fault' in sys/tg_test/2/string_scalar", True),
    ('"flepp" in sys/tg_test/2/string_scalar', False),

    # Logic
    ("True or False", True),
    ("True and False", False),
    ("not True and False", False),
    ("not (True and False)", True),
    ("(not True) and False", False),
    ("!False", True),

    # Tango attributes
    ("sys/tg_test/2/ampli == 3", False),
    ("sys/tg_test/2/ampli < 5", True),
    ("sys/tg_test/2/ampli >= 5", False),
    ("sys/tg_test/2/ampli == sys/tg_test/2/ampli", True),
    ("sys/tg_test/2/ampli != sys/tg_test/2/ampli", False),
    ("!sys/tg_test/2/boolean_scalar", False),
    ("sys/tg_test/2/ampli == 3 and sys/tg_test/2/boolean_scalar == False", False),
    ("sys/tg_test/2/ampli/2 == 0", True),
    ("tango://a.b.c.d.e.f.g:10000/sys/tg_test/2/ampli/2 == 0", True),

    ("sys/tg_test/2/boolean_scalar.quality == ATTR_VALID", True),

    ("some/disconnected/device/attr.not_accessible", True),
    ("some/not/defined/device.not_accessible", True),
    ("some/broken/device/attr.not_readable", True),
    ("some/disconnected/device/attr.exception", True),
    ("some/not/defined/device.exception", True),
    ("some/broken/device/attr.exception", True),
    ("sys/tg_test/2/ampli.exception == False", True),
    ("sys/tg_test/2/ampli.not_readable", False),
    ("sys/tg_test/2/ampli.not_accessible", False),

    # Variables
    ("apa==4", True),
    ("sys/tg_test/2/ampli/2 + apa == 4", True),
    ("apa - sys/tg_test/2/ampli == 4", True),
    ("xyz == 3", True),
    ("sys/tg_test/2/ampli < xyz", True),

    # Complex
    ("((sys/tg_test/2/ampli<2.0 and bepa2<0) or (apa < 6 and False))", True),

    # PyAlarm compatibility
    ("ce_PA == False", True),
    ("ce_PA == false", True),
    ("ce_PA == FALSE", True),
    ("ce_PA != True", True),
    ("ce_PA != true", True),
    ("ce_PA != TRUE", True),
]

VARIABLES = {
    "apa": "4",
    "bepa2": "-10",
    "ce_PA": "False",
    "pi": "3.141592",
    "xyz": "1 + 2",  # Variables are formulas
}


@pytest.mark.parametrize("formula,expected", EVALUATE_FORMULAS)
@pytest.mark.asyncio
async def test_evaluate(formula, expected):
    evaluator = AlarmEvaluator(get_device_proxy=FakeDeviceProxy)
    name = "test"
    evaluator.add_formula(f"{name}:{formula}")
    for varname, varval in VARIABLES.items():
        evaluator.add_variable(f"{varname}:{varval}")
    result, sub_results = await evaluator.evaluate(name)
    assert expected == pytest.approx(result), \
        f"Formula '{formula}' gave unexpected result {result}; expected {expected}."


@pytest.mark.asyncio
async def test_evaluate_nonexistent_device():

    error_desc = "I am an error!"

    async def raise_devfailed(_):
        raise make_devfailed(error_desc)

    evaluator = AlarmEvaluator(get_device_proxy=raise_devfailed)
    name = "test"

    evaluator.add_formula(f"{name}:{'some/nonexistent/device/attr == 118'}")
    with pytest.raises(DevFailed) as ei:
        await evaluator.evaluate(name)
    assert ei.value.args[0].desc == error_desc


@pytest.mark.asyncio
async def test_evaluate_broken_attribute():
    evaluator = AlarmEvaluator(get_device_proxy=FakeDeviceProxy)
    name = "test"

    evaluator.add_formula(f"{name}:{'some/broken/device/attr == 7'}")
    with pytest.raises(DevFailed):
        await evaluator.evaluate(name)


@pytest.mark.asyncio
async def test_evaluate_broken_attribute_not_readable():
    evaluator = AlarmEvaluator(get_device_proxy=FakeDeviceProxy)
    name = "test"
    evaluator.add_formula(f"{name}:{'some/broken/device/attr.not_readable'}")
    assert await evaluator.evaluate(name)


@pytest.mark.asyncio
async def test_evaluate_disconnected_attribute_not_readable():
    evaluator = AlarmEvaluator(get_device_proxy=FakeDeviceProxy)
    name = "test"

    # device is not accessible and .not_readable doesn't catch connection errors
    evaluator.add_formula(f"{name}:{'some/disconnected/device/attr.not_readable'}")
    with pytest.raises(DevFailed):
        await evaluator.evaluate(name)


@pytest.mark.asyncio
async def test_evaluate_disconnected_attribute_not_accessible():
    evaluator = AlarmEvaluator(get_device_proxy=FakeDeviceProxy)
    name = "test"

    evaluator.add_formula(f"{name}:{'some/disconnected/device/attr.not_accessible'}")
    assert await evaluator.evaluate(name)


@pytest.mark.asyncio
async def test_evaluate_broken_attribute_not_accessible():
    evaluator = AlarmEvaluator(get_device_proxy=FakeDeviceProxy)
    name = "test"

    # device has broken attribute and .not_accessible catches only connection related errors
    evaluator.add_formula(f"{name}:{'some/broken/device/attr.not_accessible'}")
    with pytest.raises(DevFailed):
        await evaluator.evaluate(name)


@pytest.mark.asyncio
async def test_evaluate_missing_variable():
    evaluator = AlarmEvaluator(get_device_proxy=FakeDeviceProxy)
    name = "test"
    formula = "missing_var == 5"
    evaluator.add_formula(f"{name}:{formula}")
    with pytest.raises(ValueError) as e:
        await evaluator.evaluate(name)
        assert "missing_var" in str(e)


@pytest.mark.asyncio
async def test_evaluate_many():
    evaluator = AlarmEvaluator(get_device_proxy=FakeDeviceProxy)
    names = ["test1", "test2", "test3", "test4"]
    formulas = [
        "56",
        "sys/tg_test/2/ampli/2 == 4",
        "some/broken/device/attr == 7",
        "True",
    ]
    for name, formula in zip(names, formulas):
        evaluator.add_formula(f"{name}:{formula}")

    results = dict(zip(names, await evaluator.evaluate_many(names)))

    assert results["test1"][0] == 56
    assert results["test2"][0] is False
    assert isinstance(results["test3"], DevFailed)
    assert results["test4"][0] is True


@pytest.mark.asyncio
async def test_evaluate_many__nonexistent_device():

    error_desc = "I am an error!"

    called_times = 0

    async def raise_devfailed(_):
        nonlocal called_times
        called_times += 1
        raise make_devfailed(error_desc)

    evaluator = AlarmEvaluator(get_device_proxy=raise_devfailed)

    evaluator.add_formula(f"test1:{'some/nonexistent/device/attr == 118'}")
    evaluator.add_formula(f"test2:{'some/nonexistent/device/attr == 118'}")
    results = await evaluator.evaluate_many(["test1", "test2"])
    assert isinstance(results[0], DevFailed)
    assert results[0].args[0].desc == error_desc
    assert isinstance(results[1], DevFailed)
    assert results[1].args[0].desc == error_desc

    assert called_times == 1


@pytest.mark.asyncio
async def test_get_device_proxy():
    device_name = "sys/tg_test/2"
    fake_proxy = _FakeDeviceProxy(device_name)
    delay = 0.1

    called_times = 0

    async def slow_get_proxy(_):
        "Fake proxy getter that is also quite slow"
        # Should get called only once; the caching returns the same proxy twice
        nonlocal called_times
        called_times += 1
        await asyncio.sleep(delay)
        return fake_proxy

    evaluator = AlarmEvaluator(get_device_proxy=slow_get_proxy)

    evaluator.add_formula(f"test1:{'sys/tg_test/2/ampli == 118'}")
    evaluator.add_formula(f"test2:{'sys/tg_test/2/boolean_scalar == True'}")

    results = await evaluator.evaluate_many(["test1", "test2"])

    # Evaluation succeeded
    assert not isinstance(results[0], DevFailed)
    assert not isinstance(results[1], DevFailed)

    # Both evaluations had to wait for the same proxy
    assert evaluator.timers["test1"].total_time >= delay
    assert evaluator.timers["test2"].total_time >= delay

    # Only one proxy used for both attributes
    assert called_times == 1
