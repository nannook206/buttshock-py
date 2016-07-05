from .comm import ButtshockET312SerialSync
import random


class ButtshockET312Emulator(object):
    def __init__(self):
        self.output_buffer = []
        self.rom = [0] * 512
        self.ram = [0] * 1024
        self.eeprom = [0] * 256
        self.wrong_checksum = False
        self.wrong_length_reply = False
        self.fail_handshake = False
        self.box_key = random.randint(0, 255)
        self.user_key = None

    def command(self, data):
        if len(data) == 0:
            raise RuntimeError

        if self.user_key is not None:
            data = [x ^ self.box_key ^ self.user_key ^ 0x55 for x in data]
        # Handshake
        if data[0] == 0x0 and len(data) == 1:
            self.output_buffer.append(0x7)
            return

        # Key Exchange
        if data[0] == 0x2f and len(data) == 3:
            self.user_key = data[1]
            packet = [0x21, self.box_key]
            self.output_buffer += packet
            self.output_buffer.append(sum(packet) % 0x100)
            print(["{:#02x}".format(x) for x in self.output_buffer])
            return

        # Read Command
        if data[0] & 0xf == 0xc:
            pass

        # Write Command
        if data[0] & 0xf == 0xd:
            write_size = ((data[0] & 0xf0) >> 4) - 0x3
            # TODO See what box does when this happens
            if len(data) != write_size + 4:
                raise RuntimeError("Incorrect write size! {} {}".format(len(data), write_size))
            write_location = (data[1] << 8) | (data[2])
            # Reset key
            if write_location == 0x4213 and data[3] == 0x0:
                self.user_key = None
            self.output_buffer.append(0x6)

        # If we don't know what it is, neither will the box. Just do nothing.

    def _write(self, data):
        pass

    def _read(self, data):
        pass

    def read(self, length):
        if length > len(self.output_buffer):
            raise RuntimeError("Cannot read {} bytes from output buffer of length {}!".format(length, len(self.output_buffer)))
        output = self.output_buffer[0:length]
        self.output_buffer = self.output_buffer[length:]
        return output


class ButtshockET312SerialEmulator(object):
    def __init__(self):
        self.emu = ButtshockET312Emulator()
        self.timeout = 1
        self.baud = 19200

    def close(self):
        pass

    def read(self, length):
        return self.emu.read(length)

    def write(self, data):
        self.emu.command(data)


class ButtshockET312EmulatorSync(ButtshockET312SerialSync):
    def __init__(self, port=None, key=None, shift_baud_rate=False):
        """Initialization function. Follows RAII, so creating the object opens the
        port."""
        if port is None:
            self.port = ButtshockET312SerialEmulator()
        super(ButtshockET312EmulatorSync, self).__init__(port,
                                                         key,
                                                         shift_baud_rate)
