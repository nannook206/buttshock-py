# Cause screen to glitch
#
# Run this script, then press "Menu", then "Up", menu will glitch but still be
# usable. Demonstrates string offset hack for jumping around progmem.

import sys

sys.path.append("..")

import erosoutsider


def main():
    eo = erosoutsider.ErosOutsiderSerialSync("/dev/ttyUSB0")
    eo.perform_handshake()
    # Write over registers r14-17, though this doesn't seem to crash the ET312.
    # However, it does anger the box, making it try to print a "Shut off
    # power!!" message. It doesn't display right away, so instead we end up
    # with offset string indexes when it shows up when we go to the mode menu.
    eo.write(0x4014, [0x9, 0x4, 0x3, 0x24])
    eo.close()

if __name__ == "__main__":
    main()
