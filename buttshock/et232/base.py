# Buttshock - Base Module
#
# Contains base classes for communicating with the to the ErosTek ET-232B
# Electrostim Unit.

from ..errors import ButtshockChecksumError, ButtshockError, ButtshockIOError
import binascii
import struct


class ET232Base(object):
    """Base class for ET-232 communication. Should be inherited by other classes
    that implement specific communication types, such as RS-232."""

    def __init__(self, key=None, debug=False):
        "Initialization function"
        # Set the crypto key to None, since it's used to tell whether or not we
        # should encrypt outgoing messages.  The ET232 does not encrypt.
        self.key = None
        self.debug = debug

    def _debug_print(self, message):
        if self.debug:
            print('%s' % message)

    def _send_internal(self, data):
        """Internal send function, to be implemented by inheritors."""
        raise RuntimeError("This should be overridden!")

    def _receive_internal(self, length, timeout=None):
        """Internal receive function, to be implemented by inheritors."""
        raise RuntimeError("This should be overridden!")

    def _encrypt(self, data):
        return data

    def _send_check(self, data):
        """Takes data, calculates checksum, encrypts if key is available."""
        # Append checksum before encrypting
        checksum = sum(data) % 256
        data.append(self._highNib(checksum))
        data.append(self._lowNib(checksum))
        str = ''.join(chr(x) for x in data)
        str += '\r'
        self._debug_print('sending data: %s' % str)
        return self._send_internal(bytearray(str, 'utf8'))


    def _receive(self, length, timeout=None, skip_len_check=False):
        """Receive function that handles type conversion and length checks, but does
        not calculate checksum.

        """
        data = self._receive_internal(length, timeout)
        if not skip_len_check and len(data) < length:
            raise ButtshockIOError("Received unexpected length {}, expected {}!".format(len(data), length))
        if len(data) > 0:
            self._debug_print('received data: %s' % data)
        return data

    def _receive_check(self, length):
        """Receive function that trims the trailing newline

        """
        data = self._receive(length)
        return data[:-1]

    # Hex characters as integer values to allow checksumming
    hex_symbols = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65, 66, 67, 68, 69, 70]

    def _highNib(self, b):
        """Return high nibble of a byte as a digit
        """
        return int(self.hex_symbols[(b >> 4) & 0x0f])

    def _lowNib(self, b):
        """Return low nibble of a byte as a digit
        """
        return int(self.hex_symbols[b & 0x0f])

    def read(self, address):
        """Read a byte from memory at the address given. Address corresponds to the
        table in the serial protocol documentation.

        """
        self._send_check([72, self._highNib(address), self._lowNib(address)])
        data = self._receive_check(3)
        self._debug_print('read: len(data) = %d (%s)' % (len(data), data))
        value = int(data, base=16)
        self._debug_print('read: value is %d' % value)
        try:
            return value
        except Exception as e:
            print('read: reply unparsable')

    def write(self, address, data, skip_receive=False):
        """Write 1-8 bytes to memory at the address given. Address
        corresponds to the table in the serial protocol documentation.

        """
        if type(data) is not list:
            raise TypeError("Must receive data as a list!")
        length = len(data)
        if length != 1:
            raise ButtshockIOError("Can only write between 1 byte at a time!")
        self._send_check([0x49, self._highNib(address), self._lowNib(address), self._highNib(data[0]), self._lowNib(data[0])])
        if skip_receive:
            return None
        data = self._receive(2, timeout=3.0)
        return data[0]

    def perform_handshake(self):
        """Performs the handshake routine expected on box connection.

        Wait for 'CC'.  The startup sequence seems to send 0xff, 0x00, 'C', 'C'.
        Throws exception on connection issues
 
        """
        sync_string = '\0\r'
        str = bytearray()
        synced = False

        self._send_internal(bytearray(sync_string, 'utf8'))
        # Realign packet boundaries for the protocol.
        # Wait for a ?\r\n.
        for _ in range(5*10):
            # Arbitrary timeouts are a horrible idea, but since we're syncing
            # here and not using coroutines, just deal with it.
            resp = self._receive(1, timeout=0.2, skip_len_check=True)
            self._debug_print('Handshake received %s' % resp)
            if len(resp) == 0:
                continue
            str.append(resp[0])
            if str[-4:] == b'\377\000CC':
                # resend prompt
                self._debug_print('Handshake received startup preamble')
                self._send_internal(bytearray(sync_string, 'utf8'))
                continue
            if str[-3:] == b'?\r\n':
                self._debug_print('Handshake (startup) complete')
                synced = True
                break

        if synced == False:
            raise ButtshockIOError("Handshake received no reply!")

        return

    def _change_baud_rate_internal(self, rate):
        """Internal baud rate change function, to be implemented by inheritors."""
        raise ButtshockError('This should be overridden!')

    def __enter__(self):
        # Handshake before anything else
        self.perform_handshake()
        return self

    def __exit__(self, type, value, traceback):
        pass

    def get_current_mode(self):
        """ Get the current mode/pattern the box is running. """
        return self.read(0xa2)
