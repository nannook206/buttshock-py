# buttshock-py

[![Build Status](https://travis-ci.org/metafetish/buttshock-py.svg?branch=master)](https://travis-ci.org/metafetish/buttshock-py)
[![Code Climate](https://codeclimate.com/github/metafetish/buttshock-py/badges/gpa.svg)](https://codeclimate.com/github/metafetish/buttshock-py)
[![Test Coverage](https://codeclimate.com/github/metafetish/buttshock-py/badges/coverage.svg)](https://codeclimate.com/github/metafetish/buttshock-py/coverage)

Python implementation of serial based control of the following devices:

- Erostek ET-312 Electrostimulation Device
- Erostek ET-232 Electrostimulation Device
- Estim Systems 2B Electrostimulation Device

Tested with the following versions of Python

- Python 2.7
- Python 3.3
- Python 3.4
- Python 3.5
- Python 3.6

Using pyserial 3.1.1 (thought may work with pyserial 2.6+, but untested)

## Buttshock Project Goals

If you're going to shock yourself in the butt (or other places) for
sexual pleasure, don't you want to be able to know exactly what and
how you're doing it? Even if you can't understand it, wouldn't it be
nice for people that do to have access to the knowledge and data they
need to make sure things are safe? Why is the best encryption open
source, but electrostim toys are closed?

The Buttshock project exists to reverse engineer and document
eletrostim devices so that any developer that wants to control their
devices can, via their own code.

Some of the goals of this project include:

- Documenting the communications protocols (serial or otherwise)
- Reverse engineering the firmware (where possible)
- Mapping the circuit boards and creating schematics

## Python Implementation Details

This is a python implementation of the RS-232 control protocol for the
ErosTek ET-312 electrostimulation box.

Documentation of the protocol is kept in the main documentation repo
at:

https://github.com/metafetish/buttshock-protocol-docs

This library was developed and tested using a ET-312B running v1.6
firmware. The ET-232 and 2B libraries are untested, but please let us
know if you've used them and they do/don't work!

## Requirements

buttshock-py requires the pyserial library if you want to actually
connect via serial. However, it can pass packets for each box over
whatever medium you like.

## Repo Contents

This repo contains the following:

- src - Source code for the library
- examples - Example code that uses the library

## License

tl;dr: BSD 3-Clause license

All other portions of the Buttshock repository are covered under
the following BSD license:

    Copyright (c) 2016, Buttshock Project
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
        * Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in the
          documentation and/or other materials provided with the distribution.
        * Neither the name of the Buttshock Project nor the
          names of its contributors may be used to endorse or promote products
          derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY Buttshock Project ''AS IS'' AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
    THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Kyle
    Machulis/Nonpolynomial Labs BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
    OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
