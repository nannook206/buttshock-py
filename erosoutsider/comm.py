# ErosOutsider - Serial Module
#
# Contains classes for RS-232 implementations of the ET-312 communications
# protocol.


from .base import ErosOutsiderBase
import serial


class ErosOutsiderSerialSync(ErosOutsiderBase):
    """Synchronous serial implementation of ErosOutsider protocol. All read/write
    calls will block. You have been warned.

    If you are looking to talk directly to the box, use this. At least, until
    there's an async one. If there is now and I forgot to update this comment,
    use that.

    """
    def __init__(self, port):
        """Initialization function. Follows RAII, so creating the object opens the port."""
        super(ErosOutsiderSerialSync, self).__init__()
        self.port = serial.Serial(port, 19200, timeout=1,
                                  parity=serial.PARITY_NONE,
                                  bytesize=8, stopbits=1,
                                  xonxoff=0, rtscts=0)

    def _send_internal(self, data):
        """Send data to ET-312 via serial port object."""
        return self.port.write(data)

    def _receive_internal(self, length):
        """Receive data from ET-312 via serial port object."""
        return self.port.read(length)

    def close(self):
        """Close port."""
        self.port.close()
