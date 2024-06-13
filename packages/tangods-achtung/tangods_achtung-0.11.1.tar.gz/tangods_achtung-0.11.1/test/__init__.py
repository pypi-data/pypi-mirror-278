from contextlib import contextmanager
from functools import partial
import multiprocessing
import os
import queue
import socket
import sys
import threading
import tempfile
import time

import tango
from tango import Database
from tango.test_context import get_host_ip, get_server_host_port, device
from tango.asyncio import DeviceProxy
from tango.server import run
from tango.utils import is_non_str_seq


def _device_class_from_field(field):
    # Also stolen from pytango 9.3.3, see GreenMultiDeviceTestContext below.
    device_cls_class = None
    if is_non_str_seq(field):
        try:
            (device_cls_class, device_class) = (field[0], field[1])
        except IndexError:
            device_class = field[0]["name"]
        if isinstance(device_cls_class, str):
            device_cls_class = device(device_cls_class)
    else:
        device_class = field
    if isinstance(device_class, str):
        device_class = device(device_class)
    return (device_cls_class, device_class)


class GreenMultiDeviceTestContext:

    """ Patched version of the device test context to pass on the green_mode argument. """

    # TODO submit this as a pytango MR!
    # TODO This class should be a subclass but since MultiDeviceTestContext is not available
    # until 9.3.2, I stole the entire class for now. Only the __init__ method is modified.

    nodb = "dbase=no"
    command = "{0} {1} -ORBendPoint giop:tcp:{2}:{3} -file={4}"

    thread_timeout = 3.
    process_timeout = 5.

    def __init__(self, devices_info, server_name=None, instance_name=None,
                 db=None, host=None, port=0, debug=3,
                 process=False, daemon=False, timeout=None, green_mode=None):
        if not server_name:
            _, first_device = _device_class_from_field(devices_info[0]["class"])
            server_name = first_device.__name__
        if not instance_name:
            instance_name = server_name.lower()
        if db is None:
            handle, db = tempfile.mkstemp()
            self.handle = handle
        else:
            self.handle = None
        if host is None:
            # IP address is used instead of the hostname on purpose (see #246)
            host = get_host_ip()
        if timeout is None:
            timeout = self.process_timeout if process else self.thread_timeout
        # Patch bug #819
        if process:
            os.environ['ORBscanGranularity'] = '0'
        # Attributes
        self.db = db
        self.host = host
        self.port = port
        self.timeout = timeout
        self.server_name = "/".join(("dserver", server_name, instance_name))
        self.queue = multiprocessing.Queue() if process else queue.Queue()
        self._devices = {}

        # Command args
        string = self.command.format(
            server_name, instance_name, host, port, db)
        string += " -v{0}".format(debug) if debug else ""
        cmd_args = string.split()

        class_list = []
        device_list = []
        tangoclass_list = []
        for device_info in devices_info:
            device_cls, device = _device_class_from_field(device_info["class"])
            tangoclass = device.__name__
            if tangoclass in tangoclass_list:
                self.delete_db()
                raise ValueError("multiple entries in devices_info pointing "
                                 "to the same Tango class")
            tangoclass_list.append(tangoclass)
            # File
            self.append_db_file(server_name, instance_name, tangoclass,
                                device_info["devices"], class_attributes=device_info["class"])
            if device_cls:
                class_list.append((device_cls, device, tangoclass))
            else:
                device_list.append(device)

        # Target and arguments
        if class_list and device_list:
            self.delete_db()
            raise ValueError("mixing HLAPI and classical API in devices_info "
                             "is not supported")
        if class_list:
            runserver = partial(run, class_list, cmd_args, green_mode=green_mode)
        elif len(device_list) == 1 and hasattr(device_list[0], "run_server"):
            runserver = partial(device.run_server, cmd_args, green_mode=green_mode)
        elif device_list:
            runserver = partial(run, device_list, cmd_args, green_mode=green_mode)
        else:
            raise ValueError("Wrong format of devices_info")

        cls = multiprocessing.Process if process else threading.Thread
        self.thread = cls(target=self.target, args=(runserver, process))
        self.thread.daemon = daemon

    # TODO The rest of this class is just copied from pytango, because the class
    # is not available before 9.3.2. When we no longer care about pytango 9.3.1 or older
    # we should remove it.

    def target(self, runserver, process=False):
        try:
            runserver(post_init_callback=self.post_init, raises=True)
        except Exception:
            # Put exception in the queue
            etype, value, tb = sys.exc_info()
            if process:
                tb = None  # Traceback objects can't be pickled
            self.queue.put((etype, value, tb))
        finally:
            # Put something in the queue just in case
            exc = RuntimeError("The server failed to report anything")
            self.queue.put((None, exc, None))
            # Make sure the process has enough time to send the items
            # because the it might segfault while cleaning up the
            # the tango resources
            if process:
                time.sleep(0.1)

    def post_init(self):
        try:
            host, port = get_server_host_port()
            self.queue.put((host, port))
        except Exception as exc:
            self.queue.put((None, exc, None))
        finally:
            # Put something in the queue just in case
            self.queue.put((None, RuntimeError("The post_init routine failed to report anything"), None))

    def append_db_file(self, server, instance, tangoclass, device_prop_info, class_attributes=None):
        """Generate a database file corresponding to the given arguments.
        """
        device_names = [info["name"] for info in device_prop_info]
        # Open the file
        with open(self.db, "a") as f:
            f.write("/".join((server, instance, "DEVICE", tangoclass)))
            f.write(": ")
            f.write(", ".join(device_names))
            f.write("\n")
        # Create database
        db = Database(self.db)
        # Write properties
        if is_non_str_seq(class_attributes):
            for class_property in class_attributes[0].get("properties", []):
                db.put_class_property(tangoclass, class_property)
        for info in device_prop_info:
            device_name = info["name"]
            properties = info.get("properties", {})
            # Patch the property dict to avoid a PyTango bug
            patched = dict((key, value if value != '' else ' ')
                           for key, value in properties.items())
            db.put_device_property(device_name, patched)

            memorized = info.get("memorized", {})
            munged = {
                attribute_name: {
                    "__value": memorized_value
                } for (attribute_name, memorized_value) in memorized.items()
            }
            db.put_device_attribute_property(device_name, munged)
        return db

    def delete_db(self):
        """ delete temporary database file only if it was created by this class """
        if self.handle is not None:
            os.close(self.handle)
            os.unlink(self.db)

    def get_server_access(self):
        """Return the full server name."""
        form = 'tango://{0}:{1}/{2}#{3}'
        return form.format(self.host, self.port, self.server_name, self.nodb)

    def get_device_access(self, device_name):
        """Return the full device name."""
        form = 'tango://{0}:{1}/{2}#{3}'
        return form.format(self.host, self.port, device_name, self.nodb)

    def get_device(self, device_name):
        """Return the device proxy corresponding to the given device name.

        Maintains previously accessed device proxies in a cache to not recreate
        then on every access.
        """
        if device_name not in self._devices:
            device = tango.DeviceProxy(self.get_device_access(device_name))
            self._devices[device_name] = device
        return self._devices[device_name]

    def start(self):
        """Run the server."""
        self.thread.start()
        self.connect()
        return self

    def connect(self):
        try:
            args = self.queue.get(timeout=self.timeout)
        except queue.Empty:
            if self.thread.is_alive():
                raise RuntimeError(
                    'The server appears to be stuck at initialization. '
                    'Check stdout/stderr for more information.')
            elif hasattr(self.thread, 'exitcode'):
                raise RuntimeError(
                    'The server process stopped with exitcode {}. '
                    'Check stdout/stderr for more information.'
                    ''.format(self.thread.exitcode))
            else:
                raise RuntimeError(
                    'The server stopped without reporting. '
                    'Check stdout/stderr for more information.')
        try:
            self.host, self.port = args
        except ValueError:
            raise
        # Get server proxy
        self.server = tango.DeviceProxy(self.get_server_access())
        self.server.ping()

    def stop(self):
        """Kill the server."""
        try:
            if self.server:
                self.server.command_inout('Kill')
            self.join(self.timeout)
        finally:
            self.delete_db()

    def join(self, timeout=None):
        self.thread.join(timeout)

    def __enter__(self):
        """Enter method for context support.

        :return:
          Instance of this test context.  Use `get_device` to get proxy
          access to any of the devices started by this context.
        :rtype:
          :class:`~tango.test_context.MultiDeviceTestContext`
        """
        if not self.thread.is_alive():
            self.start()
        return self

    def __exit__(self, exc_type, exception, trace):
        """Exit method for context support."""
        self.stop()


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def patch_device_proxy(mocker):

    """
    Patch DeviceProxy to work around a name-resolving issue when running
    without database.
    """

    host = get_host_ip()
    port = get_open_port()

    mocker.patch(
        'achtung.evaluator.DeviceProxy',
        wraps=lambda fqdn, *args, **kwargs: DeviceProxy(
            "tango://{0}:{1}/{2}#dbase=no".format(host, port, fqdn),
            *args,
            **kwargs
        )
    )

    return host, port


@contextmanager
def achtung_context(mocker, device_info):
    "Set up everythong for running device tests"
    host, port = patch_device_proxy(mocker)
    with GreenMultiDeviceTestContext(device_info,
                                     host=host, port=port, process=True,
                                     timeout=10,
                                     green_mode=tango.GreenMode.Asyncio) as context:
        yield context
