# Buttshock - Serial Module
#
# Contains classes for RS-232 implementations of the ET-232 communications
# protocol.

from .base import ET232Base
from ..errors import ButtshockIOError


class ET232SerialSync(ET232Base):
    """Synchronous serial implementation of Buttshock ET-232 protocol. All
    read/write calls will block. You have been warned.

    If you are looking to talk directly to the box, use this. At least, until
    there's an async one. If there is now and I forgot to update this comment,
    use that.

    """
    def __init__(self, port, key=None, debug=False, shift_baud_rate=False):
        """Initialization function. Follows RAII, so creating the object opens the
        port."""
        super(ET232SerialSync, self).__init__(key, debug)
        # Allow derived classes to set up a port to mock serial ports for
        # tests. There are cleaner ways to mock this, but this will do for now.
        if not hasattr(self, "port"):
            # Check argument validity
            import serial
            if not port or type(port) is not str:
                raise ButtshockIOError("Serial port name is missing or is not string!")

            self.port = serial.Serial(port, 19200, timeout=2,
                                      parity=serial.PARITY_NONE,
                                      bytesize=8, stopbits=1,
                                      xonxoff=0, rtscts=0)

        self.needs_bytes = False
        # Test for python 3
        if not isinstance(bytes([0]), str):
            self.needs_bytes = True

    def __enter__(self):
        super(ET232SerialSync, self).__enter__()
        return self

    def __exit__(self, type, value, traceback):
        # Reset the key to zero as the last thing we do
        super(ET232SerialSync, self).__exit__(type, value, traceback)
        # Actually close the serial port
        self.close()

    def _send_internal(self, data):
        """Send data to ET-232 via serial port object."""
        self._debug_print('_send_internal %d bytes (%s)' % (len(bytes(data)), data))
        return self.port.write(bytes(data) if self.needs_bytes else data)

    def _receive_internal(self, length, timeout=None):
        """Receive data from ET-232 via serial port object."""
        old_timeout = self.port.timeout
        if timeout is not None:
            self.port.timeout = timeout
        data = self.port.read(length)
        self._debug_print('_receive_internal 2: data %s' % data)
        self.port.timeout = old_timeout
        # Make sure there's data to check
        if len(data) == 0:
            return []
        # Python 3
        if type(data[0]) is int:
            return data
        # Python 2
        return [ord(x) for x in data]

    def close(self):
        """Close port."""
        self.port.close()

    def _change_baud_rate_internal(self, rate):
        """No effect on ET232."""
        self.port.baudrate = rate

