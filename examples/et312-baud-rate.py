# Demonstrate baud rate shifting for ET-312

import sys

sys.path.append("..")

import buttshock
import argparse
import timeit

et312 = None


def read_mode():
    global et312
    try:
        mode = et312.read(0x407b)
    except Exception as e:
        print("Current mode read failed!")
        raise e


def main():
    global et312
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", dest="serial_port",
                        help="Serial Port to use")

    args = parser.parse_args()

    if not args.serial_port:
        print("Serial port argument is required!")
        sys.exit(1)

    et312 = buttshock.ButtshockET312SerialSync(args.serial_port)

    et312.perform_handshake()
    print("Key is {0:#x} ({0})".format(et312.key, et312.key))

    current_baud_rate = et312.get_baud_rate()
    print("Current baud flag: {:#02x}".format(current_baud_rate))
    print("Running 1000 mode gets test")
    # Get the current mode
    print("Total time: {}", timeit.timeit(stmt=read_mode, number=1000))
    print("Shifting baud rate")
    et312.change_baud_rate()
    print("Running 1000 mode gets test")
    print("Total time: {}", timeit.timeit(stmt=read_mode, number=1000))
    et312.reset_key()
    et312.close()

if __name__ == "__main__":
    main()
