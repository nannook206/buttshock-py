import serial
import time

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
        # Append checksum before encrypting
        checksum = sum(data) % 256
        data.append(checksum)
        # Only encrypt if we have a key
        if self.key:
            data = map(lambda x: x ^ self.key, data)
        return self._send_internal(data)

    def _receive(self, length):
        data = map(ord, self._receive_internal(length))
        if len(data) < length:
            raise ErosOutsiderError("Received unexpected length %d, expected %d!" % (len(data), length))
        return data

    def _receive_check(self, length):
        data = self._receive(length)
        # Test checksum
        checksum = data[-1]
        s = sum(data[:-1]) % 256
        if s != checksum:
            raise ErosOutsiderError("Checksum mismatch! 0x%.02x != 0x%.02x" % (s, checksum))
        return data[:-1]

    def read_sync(self, address):
        self._send_check([0x3c, address >> 8, address & 0xff])
        data = self._receive_check(3)
        return data[1]

    def write_sync(self, address, data):
        self._send_check([0x4d, address >> 8, address & 0xff, data])
        data = self._receive(1)
        return data[0]

    def perform_handshake(self):
        # TODO throw an exception if we just get a shitload of 0x7. Why does
        # this box suck so much.

        # Handshake portion
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

        # Generate final key here
        self.key = 0x55 ^ key_info[1]

    def glitch_menu(self):
        # Run these 4 commands then press "Menu", then "Up", menu will glitch
        # but still be usable.

        # Correct. Do not change
        # self.write_sync(0x4014, 0x09)
        # self.write_sync(0x4015, 0x04)
        # self.write_sync(0x4016, 0x03)
        # self.write_sync(0x4017, 0x24)

    def press_up_button(self):
        self.write_sync(0x4069, 0x40)

    def press_down_button(self):
        self.write_sync(0x4069, 0x40)

    def dump_rom(self):
        f = open("ram3.bin", "wb")
        # try:
        #     self.write_sync(0x4070, 0x0a)
        #     self.write_sync(0x4014, 0x09)
        #     self.write_sync(0x4015, 0x04)
        #     for i in range(0, 65536, 8):
        #         self.write_sync(0x4016, i >> 8)
        #         self.write_sync(0x4017, i & 0xff)
        #         # for i in range(0x4000, 0x4020):
        #         #     f.write(chr(self.read_sync(i)))
        #         # raw_input()
        # except KeyboardInterrupt:
        #     pass
        #

        #self.write_sync(0x4070, 0x02)
        # for i in range(0x4000, 0x4020):
        #     f.write(chr(self.read_sync(i)))
        f.close()
        # f = open("rom.bin", "wb")
        # for i in range(255):
        #     f.write(chr(self.read_sync(i)))
        # f.close()

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
    e = ErosOutsiderSerial("/dev/ttyUSB0")
    e.perform_handshake()
    #e.dump_rom()
    e.glitch_menu()
    while True:
        s = ""
        for i in range(0x4000, 0x4020):
            s += "0x%.02x " % (e.read_sync(i))
        print s
        raw_input()
    e.close()

if __name__ == "__main__":
    main()
