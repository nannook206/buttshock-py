import serial


class ErosOutsiderError(Exception):
    pass


class ErosOutsiderBase():
    def __init__(self, port):
        "docstring"
        self.key = None

    def _send_internal(self, data):
        raise RuntimeError("This should be overridden!")

    def _receive_internal(self, length):
        raise RuntimeError("This should be overridden!")

    def _send(self, data):
        return self._send_internal("".join(map(chr, data)))

    def _receive(self, length):
        data = map(ord, self._receive_internal(length))
        if len(data) < length:
            raise ErosOutsiderError("Received unexpected length %d, expected %d!" % (len(data), length))

    def _receive_check(self, length):
        # decrypt if encrypted
        data = self._receive_internal(length)
        if self.key:
            pass
        # Test checksum
        checksum = data[-1]
        s = sum(data[:-1]) % 256
        if s != checksum:
            raise ErosOutsiderError("Checksum mismatch! 0x%02x != 0x%02x" % (s, checksum))
        return data[:-1]

    def read(self, address):
        self._send()

    def write(self, address, data):
        self._send()

    def perform_handshake(self):
        # Handshake
        for i in range(3):
            self._send([0x0])
            check = self._receive(1)
            if check[0] != 0x7:
                raise ErosOutsiderError("Handshake received 0x%.02x, expected 0x07!" % (check[0]))
        # Key retreival
        self._send([0x2f, 0x00])
        key_info = self._receive_check(3)
        if key_info[0] != 0x21:
                raise ErosOutsiderError("Handshake received 0x%.02x, expected 0x21!" % (key_info[0]))
        self.key = key_info[1]


class ErosOutsiderSerial(ErosOutsiderBase):
    def __init__(self, port):
        "docstring"
        self.port = serial.Serial(port, 19200, timeout=1,
                                  parity=serial.PARITY_NONE,
                                  bytesize=8, stopbits=1)

    def _send_internal(self, data):
        return self.port.write(data)

    def _receive_internal(self, length):
        return self.port.read(length)

def main():
    e = ErosOutsiderSerial("/dev/ttyS0")
    e.perform_handshake()
    print e.key

if __name__ == "__main__":
    main()
