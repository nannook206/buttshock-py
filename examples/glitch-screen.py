# Cause screen to glitch

import sys

sys.path.append("..")

import erosoutsider


def main():
    eo = erosoutsider.ErosOutsiderSerialSync("/dev/ttyUSB0")
    eo.perform_handshake()
    # Run these 4 commands then press "Menu", then "Up", menu will glitch but
    # still be usable. Demonstrates string offset hack for jumping around
    # progmem.
    eo.write(0x4014, [0x09])
    eo.write(0x4015, [0x04])
    eo.write(0x4016, [0x03])
    eo.write(0x4017, [0x24])
    eo.close()

if __name__ == "__main__":
    main()
