#!/bin/python3
#
# ** Implement a GAME mode **
#
# We want a training mode for the ET312 that works similarly to the modes
# that the ET302R has.  You can already put the ET312 box into audio mode
# and use audio signals to trigger, but what if we want to trigger via
# serial instead without adding/configuring an extra sound card.
#
# This script works with any ET312 box with a serial connection.  You
# set your A and B levels using the POTs on the device as you wish.
# It changes the display to show the word "Game" to show it's in this game
# mode.
#
# First time you run this if you're not already in GAME mode it turns the box
# into game mode, turns the outputs off, then handles any commands given.
#
# pass a channel name "a" or "b" and either the level you want it at (255 is max,
# 128 is min) or the level to ramp down from (255 is max again).  Ramp takes just
# a few seconds and is currently hardcoded.   Script exits and ramp continues
# or level remains set.  No channel name? a and b get affected.
#
# Examples:
#    python3 etgame.py -c a -l 255 -p /dev/ttyUSB0
#
#    this turns on Game mode if not on already, then sets channel A to full
#    itensity.  Script exits (with channel left on full)
#
#    python3 etgame.py -r 240 -p /dev/ttyUSB0
#
#    this turns on Game mode if not on already, then sets channel A and B
#    to level 240 intensity.  Script exists (while A and B ramps down to 0
#    over a few seconds).
#
# There's no end; just change mode manually to finish game mode.
#
# July 2016

import sys
import fcntl
import argparse
from time import sleep

sys.path.append("../../")

import buttshock

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--channel",dest="channel",help="Channel a or b or empty for both")
    parser.add_argument("-l","--level",dest="level",help="Set output to given level")
    parser.add_argument("-p","--port",dest="port",help="Port for ET312 (default /dev/ttyUSB0)")    
    parser.add_argument("-r","--ramp",dest="ramp",help="Ramp down from given level")    
    args = parser.parse_args()
    port = "/dev/ttyUSB0"  # lazy default
    if (args.port):
        port = args.port

    # Lock the serial port while we use it, wait a few seconds
    connected = False
    for _ in range(10):
        try:
            et312 = buttshock.ButtshockET312SerialSync(port)
            if et312.port.isOpen():
                fcntl.flock(et312.port.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                connected = True
            break
        except Exception as e:
            print(e)
            sleep(.2)

    if (not connected):
        print ("Failed")
        return

    try:
        et312.perform_handshake()

        # this location gets written a 0 when any mode starts, but otherwise unused
        arewerunning = et312.read(0x4093)
        
        if (arewerunning != 42):
            # so let's get it into a blank empty mode. easiest way is calltable 18
            et312.write(0x4078, [0x90]) # mode 90 doesn't exist
            et312.write(0x4070, [18]) # execute mode 90
            while (et312.read(0x4070) != 0xff):
                pass            

            # Overwrite name of current mode with spaces, then display "Game"
            et312.write(0x4180, [0x64])
            et312.write(0x4070, [0x15])
            while (et312.read(0x4070) != 0xff):
                pass
            for pos, char in enumerate('Game'):
                et312.write(0x4180, [ord(char),pos+9])
                et312.write(0x4070, [0x13])
                while (et312.read(0x4070) != 0xff):
                    pass

            for base in [0x4000,0x4100]:
                et312.write(base+0xa8, [0,0]) # don't increment channel A intensity
                et312.write(base+0xa5, [128]) # A intensity mod value = min
                et312.write(base+0xac, [0]) # no select
            
                et312.write(base+0xb1, [0]) # rate        
                et312.write(base+0xae, [0x64]) # freq mod
                et312.write(base+0xb5, [4]) # select normal parms

                et312.write(base+0xb7, [0xc8]) # width mod value
                et312.write(base+0xba, [0]) # width mod value        
                et312.write(base+0xbe, [4]) # select normal parms

                et312.write(base+0x9c, [255]) # ramp off

                #et312.write(0x4098,[5,5,1]) # gate it!

            et312.write(0x4093,[42]) # we're provisioned
                
        for base in [0x4000,0x4100]:
            if ( (not args.channel) or (base == 0x4000 and args.channel == "a") or ( base == 0x4100 and args.channel == "b")):
                    
                et312.write(base+0xac, [0]) # no select
                
                if (args.level):
                    level = int(args.level)
                    et312.write(base+0xa8, [0, 0])   # rate, direction
                    et312.write(base+0xa5, [level])
                    
                elif (args.ramp):
                    level = int(args.ramp)
                    # let it drop down to nothing
                    et312.write(base+0xa5, [level])
                    et312.write(base+0xa6, [128,level]) # Min, Max
                    et312.write(base+0xa8, [10, 255])   # rate, direction
                    et312.write(base+0xaa, [0xfc]) # at min? then stop!
                    et312.write(base+0xac, [1])  # use fast timer
                    
    except Exception as e:
        print(e)

    if (et312):
        et312.reset_key()  # reset cipher key so easy resync next time
        et312.close()

if __name__ == "__main__":
    main()
                                                                        
