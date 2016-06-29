# Demonstrate key persistence for ET-312
#
# Demonstrates reuse of keys for ET-312 sessions.

import sys

sys.path.append("..")

import buttshock


def main():
    et312 = buttshock.ButtshockET312SerialSync("/dev/ttyS0")
    try:
        et312.perform_handshake()
        print("Key is {0:#x}".format(et312.key))
    except buttshock.ButtshockError as e:
        print(e)
    et312.close()

if __name__ == "__main__":
    main()
