# ErosOutsider - Base Module
#
# Contains base classes for communicating with the to the ErosTek ET-312B
# Electrostim Unit.


class ErosOutsiderError(Exception):
    """
    General exception class for ET312 errors
    """
    # TODO Should probably add some sort of error codes
    pass


class ErosOutsiderBase(object):
    """
    Base class for ET-312 communication. Should be inherited by other classes that
    implement specific communication types, such as RS-232.
    """
    def __init__(self):
        "Initialization function"
        # Set the crypto key to None, since it's used to tell whether or not we
        # should encrypt outgoing messages.
        self.key = None

    def _send_internal(self, data):
        """Internal send function, to be implemented by inheritors."""
        raise ErosOutsiderError("This should be overridden!")

    def _receive_internal(self, length):
        """Internal receive function, to be implemented by inheritors."""
        raise ErosOutsiderError("This should be overridden!")

    def _send_check(self, data):
        """Takes data, calculates checksum, encrypts if key is available."""
        # Append checksum before encrypting
        checksum = sum(data) % 256
        data.append(checksum)
        # Only encrypt if we have a key
        if self.key:
            data = map(lambda x: x ^ self.key, data)
        return self._send_internal(data)

    def _receive(self, length):
        """Receive function that handles type conversion and length checks, but does
        not calculate checksum.

        """
        data = map(ord, self._receive_internal(length))
        if len(data) < length:
            raise ErosOutsiderError("Received unexpected length %d, expected %d!" % (len(data), length))
        return data

    def _receive_check(self, length):
        """Receive function that handles type conversion and length checks, plus
        calculates and checks checksum

        """
        data = self._receive(length)
        # Test checksum
        checksum = data[-1]
        s = sum(data[:-1]) % 256
        if s != checksum:
            raise ErosOutsiderError("Checksum mismatch! 0x%.02x != 0x%.02x" % (s, checksum))
        return data[:-1]

    def read(self, address):
        """Read a byte from memory at the address given. Address corresponds to the
        table in the serial protocol documentation.

        """
        self._send_check([0x3c, address >> 8, address & 0xff])
        data = self._receive_check(3)
        return data[1]

    def write(self, address, data):
        """Write 1-8 bytes to memory at the address given. Address
        corresponds to the table in the serial protocol documentation.

        """
        if type(data) is not list:
            raise ErosOutsiderError("Must receive data as a list!")
        length = len(data)
        if 0 > length or length > 8:
            raise ErosOutsiderError("Can only write between 1-8 bytes!")
        self._send_check([((0x3 + length) << 0x4) | 0xd, address >> 8, address & 0xff] + data)
        data = self._receive(1)
        return data[0]

    def perform_handshake(self):
        """Performs the handshake and key exchange routine expected on box connection.

        Throws exception on connection issues, which can happen frequently with
        ET312 Firmware Versions 1.6 and below.

        """
        # TODO throw an exception if we just get a shitload of 0x7. Why does
        # this box suck so much.

        # Handshake. Do it twice, just 'cause.
        for i in range(2):
            self._send_internal([0x0])
            check = self._receive(1)[0]
            if check != 0x7:
                raise ErosOutsiderError("Handshake received 0x%.02x, expected 0x07!" % (check))

        # Send our chosen key over
        #
        # chosen by fair dice roll (oh fuck it no one cares about your xkcd
        # joke it's just 0)
        self._send_check([0x2f, 0x00])
        key_info = self._receive_check(3)
        if key_info[0] != 0x21:
            raise ErosOutsiderError("Handshake received 0x%.02x, expected 0x21!" % (key_info[0]))

        # Generate final key here. It's usually 0x55 ^ our_key ^ their_key, but
        # since our key is 0, we can shorten it to 0x55 ^ their_key
        self.key = 0x55 ^ key_info[1]
