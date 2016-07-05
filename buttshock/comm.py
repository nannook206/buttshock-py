# Buttshock - Serial Module
#
# Contains classes for RS-232 implementations of the ET-312 communications
# protocol.


from .base import ButtshockET312Base
try:
    import serial
except:
    # Don't actually throw until we try to create a serial port. We may be
    # trying to mock otherwise.
    pass


class ButtshockET312SerialSync(ButtshockET312Base):
    """Synchronous serial implementation of Buttshock ET-312 protocol. All
    read/write calls will block. You have been warned.

    If you are looking to talk directly to the box, use this. At least, until
    there's an async one. If there is now and I forgot to update this comment,
    use that.

    """
    def __init__(self, port, key=None, shift_baud_rate=False):
        """Initialization function. Follows RAII, so creating the object opens the
        port."""
        super(ButtshockET312SerialSync, self).__init__(key)
        # Allow derived classes to set up a port to mock serial ports for
        # tests. There are cleaner ways to mock this, but this will do for now.
        if not hasattr(self, "port"):
            # Check argument validity
            if not port or type(port) is not str:
                raise ButtshockIOError("Serial port name is missing or is not string!")
            if not serial:
                # If we got here without importing serial, we have a problem.
                # Try again and throw this time.
                import serial
            self.port = serial.Serial(port, 19200, timeout=1,
                                      parity=serial.PARITY_NONE,
                                      bytesize=8, stopbits=1,
                                      xonxoff=0, rtscts=0)

        self.needs_bytes = False
        # Test for python 3
        if not isinstance(bytes([0]), str):
            self.needs_bytes = True
        self.shift_baud_rate = shift_baud_rate

    def __enter__(self):
        super(ButtshockET312SerialSync, self).__enter__()
        if self.shift_baud_rate:
            self.change_baud_rate(38400)
        return self

    def __exit__(self, type, value, traceback):
        if self.shift_baud_rate:
            self.change_baud_rate(19200)
        # Reset the key to zero as the last thing we do
        super(ButtshockET312SerialSync, self).__exit__(type, value, traceback)
        # Actually close the serial port
        self.close()

    def _send_internal(self, data):
        """Send data to ET-312 via serial port object."""
        return self.port.write(bytes(data) if self.needs_bytes else data)

    def _receive_internal(self, length, timeout=None):
        """Receive data from ET-312 via serial port object."""
        old_timeout = self.port.timeout
        if timeout is not None:
            self.port.timeout = timeout
        data = self.port.read(length)
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
        self.port.baudrate = rate

