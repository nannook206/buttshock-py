buttshock-py
============

Python implementation of serial based control of the following devices:

- `Erostek ET-312B Electrostimulation Device <http://shop.erostek.com/products/ET312B-Power-Unit.html>`_
- `Erostek ET-232 Electrostimulation Device <http://shop.erostek.com/products/ET232-Power-Unit.html>`_
- `Estim Systems 2B Electrostimulation Device <http://store.e-stim.co.uk/index.php?main_page=product_info&products_id=17>`_

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

Documentation for serial link cable construction and more information
about the ET-312B protocol is available at:

https://buttshock.com/doc/et312

This library was developed and tested using a ET-312B running v1.6
firmware. The ET-232 and 2B libraries are untested, but please let us
know if you've used them and they do/don't work!

Requirements
------------

buttshock-py requires the pyserial library if you want to actually
connect via serial. This dependency should be installed via setup.py.

However, the library is built to abstract the raw box protocols from
the communication medium, so it can pass packets for each box over
whatever medium you like. For instance, you could create a network
class that talks to a daemon that communicates with a serial port, if
needed.

Repo Contents
-------------

This repo contains the following:

- src - Source code for the library
- examples - Example code that uses the library

Development
-----------

buttshock-py uses the Tox library for test environment setup, test
execution, documentation building, and other automated tasks.

To run project tests:

.. code:: shell

    $ tox --skip-missing-interpreters

To create documentation:

.. code:: shell

    $ tox -e docs

License
-------

tl;dr: BSD 3-Clause license

Copyright (c) 2016, Buttshock Project

See LICENSE file for full text.
