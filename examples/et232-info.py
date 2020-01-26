#!/usr/bin/python3
#
# Examples:
#    python3 info.py -p /dev/ttyUSB0
#

import sys
import fcntl
import argparse
from time import sleep

#sys.path.append("../")
sys.path.insert(0, "../")

import buttshock.et232

def main():

    modes = {0x0b:"Waves",     0x0a:"Intense",   0x0e:"Random",
             0x06:"AudioSoft", 0x02:"AudioLoud", 0x03:"AudioWaves",
             0x07:"User",      0x05:"HiFreq",    0x01:"Climb",
             0x00:"Throb",     0x04:"Combo",     0x0c:"Thrust",
             0x08:"Thump",     0x09:"Ramp",      0x0d:"Stroke",
             0x0f:"Off",
            }

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
            et232 = buttshock.et232.ET232SerialSync(port)
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

    while True:
        sleep(1)
        try:
            print("Battery voltage\t\t: {0:#x}".format(et232.read(0x8a)))
            print("Battery scaled?\t\t: {0:.1f}%".format((et232.read(0x8a))*100/256))
            currentmode = et232.read(0xa2)
            print("Current mode\t\t: %d" % currentmode)
            print("Current Mode\t\t: "+modes[currentmode])
            print("Mode switch override\t: %d" % et232.read(0xa3))

            print("Channel A knob\t\t: {0:#x}".format(et232.read(0x8c)))
            print("Ampitude\t\t: {0:#x}".format(et232.read(0x0a)))
            # print("Power Compensation\t: {0:#x}".format(et232.read(0x0b)))
            print("Channel B knob\t\t: {0:#x}".format(et232.read(0x88)))
            print("Ampitude\t\t: {0:#x}".format(et232.read(0x10)))
            # print("Power Compensation\t: {0:#x}".format(et232.read(0x11)))
            print("MA knob\t\t\t: %d" % et232.read(0x89))
            print("D0 timer\t\t\t: %d" % et232.read(0xd0))
            print("D1 timer\t\t\t: %d" % et232.read(0xd1))
            print("D3 timer\t\t\t: %d" % et232.read(0xd3))
            return
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
                                                                        
