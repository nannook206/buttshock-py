#!/usr/bin/env python

from setuptools import setup
import os
import buttshock

setup(name='buttshock',
      version="{}".format(buttshock.VERSION),
	  description='Python Libraries for Estim Unit (ErosTek ET312, Erostek ET232, Estim Systems 2B) Control',
      long_description=(open('README.rst').read() + '\n' + open(os.path.join('CHANGES.rst')).read()),
      author='qDot',
      author_email='kyle@machul.is',
      url='http://github.com/metafetish/buttshock-py',
      download_url='http://pypi.python.org/packages/source/b/buttshock',
      license='BSD License',
      packages=['buttshock'],
      keywords=['estim', 'buttshock', 'teledildonics', 'electrostim'],
      setup_requires=['pyserial', 'pytest-runner'],
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
