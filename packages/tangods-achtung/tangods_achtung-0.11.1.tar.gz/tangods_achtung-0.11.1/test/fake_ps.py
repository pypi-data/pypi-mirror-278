import asyncio
from tango import GreenMode
from tango.server import Device, attribute, command


class PowerSupply(Device):

    green_mode = GreenMode.Asyncio

    voltage = attribute(dtype=float,
                        fget="read_voltage",
                        fset="write_voltage")

    power = attribute(dtype=bool,
                      fget="read_power",
                      fset="write_power")

    slow = attribute(dtype=bool,
                     fget="read_slow", green_mode=GreenMode.Asyncio)

    exception = attribute(dtype=bool,
                          fget="read_exception")

    def init_device(self):
        self._voltage = 0
        self._power = False
        self._exception = False

    def read_voltage(self):
        return self._voltage if self._power else 0

    def write_voltage(self, value):
        self._voltage = value

    def read_power(self):
        return self._power

    def write_power(self, value):
        self._power = value

    async def read_slow(self):
        if self._power:
            await asyncio.sleep(0.2)
        return False

    def read_exception(self):
        if self._exception:
            raise RuntimeError()
        return True

    @command
    def toggle_exc(self):
        self._exception = not self._exception


if __name__ == "__main__":
    from tango.server import run
    run((PowerSupply,), green_mode=GreenMode.Asyncio)
