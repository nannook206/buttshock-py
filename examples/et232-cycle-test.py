#!/usr/bin/python3
#
# Examples:
#    python3 et232-cycle-test.py -p /dev/ttyUSB0
#
# Port default is /dev/ttyUSB0

import sys
import fcntl
import argparse
from time import sleep

#sys.path.append("../")
sys.path.insert(0, "../")

import buttshock.et232

pass_count = 0

def print_modes(et232):
    global pass_count

    modes = {0x0b:"Waves",     0x0a:"Intense",   0x0e:"Random",
             0x06:"AudioSoft", 0x02:"AudioLoud", 0x03:"AudioWaves",
             0x07:"User",      0x05:"HiFreq",    0x01:"Climb",
             0x00:"Throb",     0x04:"Combo",     0x0c:"Thrust",
             0x08:"Thump",     0x09:"Ramp",      0x0d:"Stroke",
             0x0f:"Off",
            }

    print('Pass %d: Mode: %s, MA %d, chA %d, chB %d, D3 timer %d' % (
       pass_count, modes[et232.read(0xa3)], et232.read(0x89),
       et232.read(0x8c), et232.read(0x88), et232.read(0xd3)))
    pass_count += 1
    return

def set_modes(et232, i):
    modes = [0, 1, 2, 10, 11, 12]
    levels = [10, 20, 32]
    multiadjusts = [5, 32, 48, 145, 170]

    et232.write(0xa3, [modes[i%len(modes)]])
    #sleep(0.2)
    et232.write(0x89, [multiadjusts[i%len(multiadjusts)]])
    #sleep(0.2)
    et232.write(0x8c, [levels[i%len(levels)]])
    #sleep(0.2)
    et232.write(0x88, [levels[i%len(levels)]])

    if (i%4) == 3:
        et232.write(0xd3, [0])

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-p","--port",dest="port",help="Port for ET232 (default /dev/ttyUSB0)")    
    args = parser.parse_args()
    port = "/dev/ttyUSB0"  # lazy default
    if (args.port):
        port = args.port

    # Lock the serial port while we use it, wait a few seconds
    connected = False
    for _ in range(60*5):
        try:
            et232 = buttshock.et232.ET232SerialSync(port, debug=False)
            if et232.port.isOpen():
                fcntl.flock(et232.port.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                connected = True
        except Exception as e:
            print(e)
            et232.close()
            sleep(.2)
            continue

        if (not connected):
            print ("Connect Failed")
            continue

        print ("[+] connected")
        try:
            et232.perform_handshake()
            print ("[+] handshake ok")
            break
        except Exception as e:
            print(e)
            et232.close()
            sleep(1)

    print_modes(et232)
    sleep(0.2)

    # enable overrides for MA, chA, chB
    et232.write(0xa4, [0x13])
    sleep(0.2)

    i = 0
    while True:
        try:
            set_modes(et232, i)
        except Exception as e:
            print('write failure: %s' % e)
        try:
            print_modes(et232)
        except Exception as e:
            print('read failure: %s' % e)

        i += 1
        sleep(10)


if __name__ == "__main__":
    main()
                                                                        
