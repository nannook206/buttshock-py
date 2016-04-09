import serial


class ErosOutsiderError(Exception):
    pass


class ErosOutsiderBase(object):
    def __init__(self):
        "docstring"
        self.key = None

    def _send_internal(self, data):
        raise RuntimeError("This should be overridden!")

    def _receive_internal(self, length):
        raise RuntimeError("This should be overridden!")

    def _send_check(self, data):
        checksum = sum(data) % 256
        data.append(checksum)
        print data
        return self._send_internal(data)

    def _receive(self, length):
        data = map(ord, self._receive_internal(length))
        if len(data) < length:
            raise ErosOutsiderError("Received unexpected length %d, expected %d!" % (len(data), length))
        return data

    def _receive_check(self, length):
        # decrypt if encrypted
        data = self._receive(length)
        if self.key:
            pass
        # Test checksum
        checksum = data[-1]
        s = sum(data[:-1]) % 256
        if s != checksum:
            raise ErosOutsiderError("Checksum mismatch! 0x%.02x != 0x%.02x" % (s, checksum))
        return data[:-1]

    def read(self, address):
        pass

    def write(self, address, data):
        pass

    def perform_handshake(self):
        # Handshake
        for i in range(4):
            self._send_internal([0x0])
            check = self._receive(1)[0]
            if check != 0x7:
                raise ErosOutsiderError("Handshake received 0x%.02x, expected 0x07!" % (check))
        # Key retreival
        self._send_check([0x2f, 0x29])
        key_info = self._receive_check(3)
        if key_info[0] != 0x21:
                raise ErosOutsiderError("Handshake received 0x%.02x, expected 0x21!" % (key_info[0]))
        self.key = key_info[1]


class ErosOutsiderSerial(ErosOutsiderBase):
    def __init__(self, port):
        "docstring"
        super(ErosOutsiderSerial, self).__init__()
        self.port = serial.Serial(port, 19200, timeout=1,
                                  parity=serial.PARITY_NONE,
                                  bytesize=8, stopbits=1,
                                  xonxoff=0, rtscts=0)

    def _send_internal(self, data):
        return self.port.write(data)

    def _receive_internal(self, length):
        return self.port.read(length)

    def close(self):
        self.port.close()

def main():
    e = ErosOutsiderSerial("/dev/ttyS0")
    try:
        e.perform_handshake()
    except ErosOutsiderError, b:
        e.close()
        raise b
    e.close()

if __name__ == "__main__":
    main()
