#!/usr/bin/env python

from setuptools import setup, find_packages

import buttshock

setup(name='buttshock',
      version="{}".format(buttshock.VERSION),
	  description='Python Libraries for Estim Unit (ErosTek ET312, Erostek ET232, Estim Systems 2B) Control',
      long_description="""Python Libraries for Estim Unit (ErosTek ET312, Erostek ET232, Estim Systems 2B) Control. Provides protocol implementations for serial communications, as well as utility functions for easily accessing features of estim equipment.""",
      author='qDot',
      author_email='kyle@machul.is',
      url='http://github.com/metafetish/buttshock-py',
      download_url='http://pypi.python.org/packages/source/b/buttshock',
      license='BSD License',
      packages=['buttshock'],
      keywords=['estim', 'buttshock', 'teledildonics', 'electrostim'],
      install_requires=['pyserial'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: System :: Hardware :: Hardware Drivers'
      ]
)