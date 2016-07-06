# Demonstrate baud rate shifting for ET-312

import sys
import buttshock.et312
import argparse
import timeit

et312 = None
i = 0


def read_mode():
    global et312, i
    try:
        et312.read(0x407b)
        print(i)
        i += 1
    except Exception:
        print("Current mode read failed!")


def main():
    global et312
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", dest="serial_port",
                        help="Serial Port to use")

    args = parser.parse_args()

    if not args.serial_port:
        print("Serial port argument is required!")
        sys.exit(1)

    with buttshock.et312.ET312SerialSync(args.serial_port) as et312:
        et312.perform_handshake()
        key = et312.key
        print("Key is {0:#x} ({0})".format(et312.key, et312.key))

        current_baud_rate = et312.get_baud_rate()
        print("Current baud flag: {:#02x}".format(current_baud_rate))
        print("Running 1000 mode gets test")
        # Get the current mode
        print("Total time: {}", timeit.timeit(stmt=read_mode, number=1000))
    print("Shifting baud rate")
    with buttshock.et312.ET312SerialSync(args.serial_port,
                                         key=key,
                                         shift_baud_rate=True) as et312:
        print("Running 1000 mode gets test")
        print("Total time: {}", timeit.timeit(stmt=read_mode, number=1000))

if __name__ == "__main__":
    main()
