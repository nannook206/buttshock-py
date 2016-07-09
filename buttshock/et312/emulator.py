from .comm import ET312SerialSync
import random


class ET312Emulator(object):
    def __init__(self):
        self.output_buffer = []
        self.rom = [0] * 512
        self.ram = [0] * 1024
        self.eeprom = [0] * 256
        self.wrong_checksum = False
        self.wrong_length_reply = False
        self.fail_handshake = False

    def command(self, data):
        if len(data) == 0:
            raise RuntimeError

        if self.ram[0x213] != 0:
            data = [x ^ self.ram[0x213] for x in data]
        # Handshake
        if data[0] == 0x0 and len(data) == 1:
            self.output_buffer.append(0x7)
            return

        # Key Exchange
        if data[0] == 0x2f and len(data) == 3:
            box_key = random.randint(0, 255)
            packet = [0x21, box_key]
            self.ram[0x213] = data[1] ^ box_key ^ 0x55
            self.output_buffer += packet
            self.output_buffer.append(sum(packet) % 0x100)
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
            # RAM write
            if write_location >= 0x4000 and write_location <= 0x8000:
                location = (write_location - 0x4000)
                if location > 1024:
                    location = location % 1024
                # TODO There has to be a more python way to do this but I'm
                # tired.
                for i in range(0, write_size):
                    self.ram[location + i] = data[3 + i]
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


class ET312SerialEmulator(object):
    def __init__(self):
        self.emu = ET312Emulator()
        self.timeout = 1
        self.baud = 19200

    def close(self):
        pass

    def read(self, length):
        return self.emu.read(length)

    def write(self, data):
        self.emu.command(data)


class ET312EmulatorSync(ET312SerialSync):
    def __init__(self, port=None, key=None, shift_baud_rate=False):
        """Initialization function. Follows RAII, so creating the object opens the
        port."""
        if port is None:
            self.port = ET312SerialEmulator()
        super(ET312EmulatorSync, self).__init__(port,
                                                key,
                                                shift_baud_rate)
