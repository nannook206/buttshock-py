import serial



    def glitch_menu(self):
        # Run these 4 commands then press "Menu", then "Up", menu will glitch
        # but still be usable.

        # Correct. Do not change
        self.write_sync(0x4014, 0x09)
        self.write_sync(0x4015, 0x04)
        self.write_sync(0x4016, 0x03)
        self.write_sync(0x4017, 0x24)

    def press_up_button(self):
        self.write_sync(0x4069, 0x40)

    def press_down_button(self):
        self.write_sync(0x4069, 0x40)

    def dump_ram(self, filename):
        f = open(filename, "wb")
        for i in range(0x4000, 0x4400):
            f.write(chr(self.read_sync(i)))
        f.close()

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
    # i = 0
    # while True:
    #     raw_input()
    #     print "Dumping"
    #     e.dump_ram("ram%d.bin" % (i))
    #     print "Dumped"
    #     i += 1
    e.close()

if __name__ == "__main__":
    main()
