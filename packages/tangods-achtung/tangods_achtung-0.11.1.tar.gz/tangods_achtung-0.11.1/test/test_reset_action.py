import pytest
import tango

from achtung.alarm import Action

ARGS = [
    ("", None),
    (";0", 0),
    (";1", 1),
    (";true", True),
    (";false", False),
    (";1.2", 1.2),
    (";0.2", 0.2),
    (";-0.2", -0.2),
    (";1e5", 100000),
    (";1e-3", 0.001),
    (';"test"', "test"),
    (";[1, 2, 3]", [1, 2, 3]),
    (';["a"]', ["a"]),

    (";test", ValueError),
    (";test23113", ValueError),
    (";1,2", ValueError),
    (";;;;;", ValueError),
]


class FakeProxy:
    last_call = ()

    def __init__(self, *args, **kwargs):
        pass

    async def write(arg):
        FakeProxy.last_call = "write", arg

    async def command_inout(command, arg=[]):
        FakeProxy.last_call = "command_inout", command, arg


@pytest.mark.asyncio
async def test_execute(mocker):
    mocker.patch.object(tango.device_proxy, 'DeviceProxy', return_value=FakeProxy)
    mocker.patch.object(tango.attribute_proxy, 'AttributeProxy', return_value=FakeProxy)

    command_with_args = Action(Action.RUN_COMMAND, "sys/tg_test/11/switchstates", [0])
    command_without_args = Action(Action.RUN_COMMAND, "sys/tg_test/11/switchstates", [])
    write_attribute = Action(Action.WRITE_ATTRIBUTE, "sys/tg_test/11/double_scalar", 12.12)

    await command_with_args.execute()
    assert FakeProxy.last_call == ("command_inout", "switchstates", [0])

    await command_without_args.execute()
    assert FakeProxy.last_call == ("command_inout", "switchstates", [])

    await write_attribute.execute()
    assert FakeProxy.last_call == ("write", 12.12)


@pytest.mark.parametrize("arg,expected", ARGS)
def test_attribute_from_string(arg, expected):
    s = f"write_attribute; sys/tg_test/1/boolean_spectrum{arg}"
    if expected != ValueError:
        action = Action.from_string(s)
        assert action.action_type == Action.WRITE_ATTRIBUTE
        assert action.target == "sys/tg_test/1/boolean_spectrum"
        assert action.args == expected
    else:
        with pytest.raises(ValueError):
            Action.from_string(s)


@pytest.mark.parametrize("arg,expected", ARGS)
def test_command_from_string(arg, expected):
    s = f"run_command; sys/tg_test/1/switchstates{arg}"
    if expected != ValueError:
        action = Action.from_string(s)
        assert action.action_type == Action.RUN_COMMAND
        assert action.target == "sys/tg_test/1/switchstates"
        assert action.args == expected
    else:
        with pytest.raises(ValueError, match=".*bad args.*"):
            Action.from_string(s)


def test_bad_format_type_from_string():
    s = "this is just a string"
    with pytest.raises(ValueError, match=".*bad format.*"):
        Action.from_string(s)


def test_bad_action_type_from_string():
    s = "run_bananas; sys/tg_test/1/switchstates;56"
    with pytest.raises(ValueError, match=".*bad action.*"):
        Action.from_string(s)


def test_bad_target_from_string():
    s = "run_command;notatangodevice;56"
    with pytest.raises(ValueError, match=".*bad target.*"):
        Action.from_string(s)
