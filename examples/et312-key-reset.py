# Demonstrate key persistence for ET-312
#
# Demonstrates reuse of keys for ET-312 sessions.

import sys

sys.path.append("..")

import buttshock
import argparse


def main():
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

    # Get the current mode
    try:
        mode = et312.read(0x407b)
        print("Current box mode: {0:#x}".format(mode))
    except Exception as e:
        print("Current mode read failed!")
        raise e
    et312.reset_key()
    et312.close()

if __name__ == "__main__":
    main()
