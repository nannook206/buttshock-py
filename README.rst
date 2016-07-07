buttshock-py
============

Python implementation of serial based control of the following devices:

- Erostek ET-312 Electrostimulation Device
- Erostek ET-232 Electrostimulation Device
- Estim Systems 2B Electrostimulation Device

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |travis| |coverage| |health|
    * - package
      - |license| |version| |pyversion|

.. |docs| image:: https://readthedocs.org/projects/buttshock-py/badge/?version=latest
   :target: http://buttshock-py.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |travis| image:: https://img.shields.io/travis/metafetish/buttplug-py/master.svg?label=build
   :target: https://travis-ci.org/metafetish/buttshock-py
   :alt: Travis CI build status

.. |health| image:: https://codeclimate.com/github/metafetish/buttshock-py/badges/gpa.svg
   :target: https://codeclimate.com/github/metafetish/buttshock-py
   :alt: Code coverage

.. |coverage| image:: https://codeclimate.com/github/metafetish/buttshock-py/badges/coverage.svg
   :target: https://codeclimate.com/github/metafetish/buttshock-py/coverage
   :alt: Code health

.. |license| image:: https://img.shields.io/pypi/l/buttshock.svg
   :target: https://pypi.python.org/pypi/buttshock/
   :alt: Latest PyPI version

.. |version| image:: https://img.shields.io/pypi/v/buttshock.svg
   :target: https://pypi.python.org/pypi/buttshock/
   :alt: Latest PyPI version
         
.. |pyversion| image:: https://img.shields.io/pypi/pyversions/buttshock.svg
   :target: https://pypi.python.org/pypi/buttshock/
   :alt: Latest PyPI version


.. end-badges
            
Using pyserial 3.1.1 (thought may work with pyserial 2.6+, but untested)

Buttshock Project Goals
-----------------------

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

Installation
------------

To install:

.. code:: shell

    $ pip install buttshock --upgrade

Package is also available on PyPi at http://pypi.python.org/pypi/buttshock

Python Implementation Details
-----------------------------

This is a python implementation of the RS-232 control protocol for the
ErosTek ET-312 electrostimulation box.

Documentation of the link cable, protocol, and other information is at:

https://buttshock.com/doc/et312

This library was developed and tested using a ET-312B running v1.6
firmware. The ET-232 and 2B libraries are untested, but please let us
know if you've used them and they do/don't work!

Requirements
------------

buttshock-py requires the pyserial library if you want to actually
connect via serial. However, it can pass packets for each box over
whatever medium you like.

Repo Contents
-------------

This repo contains the following:

- src - Source code for the library
- examples - Example code that uses the library

License
-------

tl;dr: BSD 3-Clause license

Copyright (c) 2016, Buttshock Project

See LICENSE file for full text.
