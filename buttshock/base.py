# Buttshock - Base Module
#
# Contains base classes for communicating with the to the ErosTek ET-312B
# Electrostim Unit.


class ButtshockError(Exception):
    """
    General exception class for ET312 errors
    """
    # TODO Should probably add some sort of error codes
    pass


class ButtshockET312Base(object):
    """
    Base class for ET-312 communication. Should be inherited by other classes that
    implement specific communication types, such as RS-232.
    """
    def __init__(self, key=None):
        "Initialization function"
        # Set the crypto key to None, since it's used to tell whether or not we
        # should encrypt outgoing messages.
        self.key = key

    def _send_internal(self, data):
        """Internal send function, to be implemented by inheritors."""
        raise ButtshockError("This should be overridden!")

    def _receive_internal(self, length):
        """Internal receive function, to be implemented by inheritors."""
        raise ButtshockError("This should be overridden!")

    def _encrypt(self, data):
        return [x ^ self.key for x in data]

    def _send_check(self, data):
        """Takes data, calculates checksum, encrypts if key is available."""
        # Append checksum before encrypting
        checksum = sum(data) % 256
        data.append(checksum)
        # Only encrypt if we have a key
        if self.key:
            data = self._encrypt(data)
        return self._send_internal(data)

    def _receive(self, length):
        """Receive function that handles type conversion and length checks, but does
        not calculate checksum.

        """
        data = self._receive_internal(length)
        if len(data) < length:
            raise ButtshockError("Received unexpected length {}, expected {}!".format(len(data), length))
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
            raise ButtshockError("Checksum mismatch! {:#02x} != {:#02x}".format(s, checksum))
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
            raise ButtshockError("Must receive data as a list!")
        length = len(data)
        if 0 > length or length > 8:
            raise ButtshockError("Can only write between 1-8 bytes!")
        self._send_check([((0x3 + length) << 0x4) | 0xd, address >> 8, address & 0xff] + data)
        data = self._receive(1)
        return data[0]

    def perform_handshake(self):
        """Performs the handshake and key exchange routine expected on box connection.

        Throws exception on connection issues, which can happen frequently with
        ET312 Firmware Versions 1.6 and below.

        """

        # Realign packet boundaries for the protocol.
        #
        # If another program has accessed the ET-312 before this session, we're
        # not sure what state it left the protocol in. Sending 0x0, possibly
        # encrypted with the key that the box established prior to this
        # session, should allow the box to realign the protocol. As the longest
        # command possible is 11 bytes (a command to write 8 bytes to an
        # address), we need to send up to 12 0s. Once we get back a 0x7, the
        # protocol is synced and we can move on.
        sync_byte = [0]
        # If a key was passed in on object construction, use it.
        if self.key is not None:
            sync_byte = self._encrypt(sync_byte)
        for i in range(12):
            self._send_internal(sync_byte)
        check = self._receive(12)
        if len(check) == 0 or check[-1] != 0x7:
            raise ButtshockError("Handshake received {:#02x}, expected 0x07!".format(check))

        # If we already have a key, stop here
        if self.key is not None:
            return

        # Send our chosen key over
        #
        # chosen by fair dice roll (oh fuck it no one cares about your xkcd
        # joke it's just 0)
        self._send_check([0x2f, 0x00])
        key_info = self._receive_check(3)
        if key_info[0] != 0x21:
            raise ButtshockError("Handshake received {:#02x}, expected 0x21!" % (key_info[0]))

        # Generate final key here. It's usually 0x55 ^ our_key ^ their_key, but
        # since our key is 0, we can shorten it to 0x55 ^ their_key
        self.key = 0x55 ^ key_info[1]

    def change_baud_rate(self):
        # This will require sending over 2 bytes at the same time, as any
        # transmission after this will happen at the new baud rate.
        self.write(0x4029, [0x0c])
        pass

    def get_baud_rate(self):
        baud_lh = self.read(0x4029)
        baud_uh = self.read(0x4020)
        return ((baud_uh & 0xf) << 0x8) & baud_lh

    def get_stack_ptr(self):
        return (self.read(0x405E) << 8) | self.read(0x405D)

    def set_stack_ptr(self):
        return self.write(0x405D, [0x80, 0x01])

    def get_mcucsr(self):
        return self.read(0x4054)

    def reset_box(self):
        self.write(0x4070, [0x17])

    def reset_key(self):
        self.write(0x4213, [0x0])
