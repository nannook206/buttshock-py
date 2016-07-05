# Buttshock - Base Module
#
# Contains base classes for communicating with the to the ErosTek ET-312B
# Electrostim Unit.

ADDRS = {
    "BAUD_RATE_LOW": 0x4029,
    "BAUD_RATE_HIGH": 0x4020,
}

VALUES = {
    "BAUD_19200": 0x19,
    "BAUD_38400": 0x0c
}


class ButtshockError(Exception):
    """
    General exception class for ET312 errors
    """
    pass


class ButtshockChecksumError(ButtshockError):
    pass


class ButtshockIOError(ButtshockError):
    pass


class ButtshockET312Base(object):
    """Base class for ET-312 communication. Should be inherited by other classes
    that implement specific communication types, such as RS-232."""

    def __init__(self, key=None):
        "Initialization function"
        # Set the crypto key to None, since it's used to tell whether or not we
        # should encrypt outgoing messages.
        self.key = key

    def _send_internal(self, data):
        """Internal send function, to be implemented by inheritors."""
        raise RuntimeError("This should be overridden!")

    def _receive_internal(self, length, timeout=None):
        """Internal receive function, to be implemented by inheritors."""
        raise RuntimeError("This should be overridden!")

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

    def _receive(self, length, timeout=None, skip_len_check=False):
        """Receive function that handles type conversion and length checks, but does
        not calculate checksum.

        """
        data = self._receive_internal(length, timeout)
        if not skip_len_check and len(data) < length:
            raise ButtshockIOError("Received unexpected length {}, expected {}!".format(len(data), length))
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
            raise ButtshockChecksumError("Checksum mismatch! {:#02x} != {:#02x}".format(s, checksum))
        return data[:-1]

    def read(self, address):
        """Read a byte from memory at the address given. Address corresponds to the
        table in the serial protocol documentation.

        """
        self._send_check([0x3c, address >> 8, address & 0xff])
        data = self._receive_check(3)
        return data[1]

    def write(self, address, data, skip_receive=False):
        """Write 1-8 bytes to memory at the address given. Address
        corresponds to the table in the serial protocol documentation.

        """
        if type(data) is not list:
            raise TypeError("Must receive data as a list!")
        length = len(data)
        if 0 > length or length > 8:
            raise ButtshockIOError("Can only write between 1-8 bytes!")
        self._send_check([((0x3 + length) << 0x4) | 0xd, address >> 8,
                          address & 0xff] + data)
        if skip_receive:
            return None
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
            # Arbitrary timeouts are a horrible idea, but since we're syncing
            # here and not using coroutines, just deal with it.
            check = self._receive(1, timeout=0.1, skip_len_check=True)
            if len(check) == 0:
                continue
            if check[0] != 0x7:
                raise ButtshockIOError("Handshake received {:#02x}, expected 0x07!".format(check[-1]))
            else:
                break
        if len(check) == 0:
            raise ButtshockIOError("Handshake received no reply!")

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
            raise ButtshockIOError("Handshake received {:#02x}, expected 0x21!".format(key_info[0]))

        # Generate final key here. It's usually 0x55 ^ our_key ^ their_key, but
        # since our key is 0, we can shorten it to 0x55 ^ their_key
        self.key = 0x55 ^ key_info[1]

    def _change_baud_rate_internal(self, rate):
        """Internal baud rate change function, to be implemented by inheritors."""
        raise ButtshockError("This should be overridden!")

    def change_baud_rate(self, rate):
        # This will require sending over 2 bytes at the same time, as any
        # transmission after this will happen at the new baud rate.
        if rate == 38400:
            self.write(ADDRS["BAUD_RATE_LOW"], [VALUES["BAUD_38400"]],
                       skip_receive=True)
        elif rate == 19200:
            self.write(ADDRS["BAUD_RATE_LOW"], [VALUES["BAUD_19200"]],
                       skip_receive=True)
        else:
            raise ButtshockError("Baud rate {} not valid! Can only run at 19200 or 38400".format(rate))
        self._receive(1)
        self._change_baud_rate_internal(rate)

    def get_baud_rate(self):
        baud_lh = self.read(ADDRS["BAUD_RATE_LOW"])
        baud_uh = self.read(ADDRS["BAUD_RATE_HIGH"])
        return ((baud_uh & 0xf) << 0x8) | baud_lh

    def reset_box(self):
        self.write(0x4070, [0x17])

    def reset_key(self):
        self.write(0x4213, [0x0])

    def __enter__(self):
        # Handshake before anything else
        self.perform_handshake()
        return self

    def __exit__(self, type, value, traceback):
        # Reset the key to zero as the last thing we do
        self.reset_key()
