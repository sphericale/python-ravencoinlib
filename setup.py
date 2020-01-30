#!/usr/bin/env python

from setuptools import setup, find_packages
import os

from version import __version__

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = ['x16r_hash','x16rv2_hash']

setup(name='python-ravencoinlib',
      version=__version__,
      description='Ravencoin fork of python-bitcoinlib',
      long_description=README,
      long_description_content_type='text/markdown',
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
      ],
      url='https://github.com/standard-error/python-ravencoinlib',
      keywords='ravencoin',
      packages=find_packages(),
      zip_safe=False,
      author = 'standard-error@github',
      author_email = 'ravencoinlib@gmail.com',
      install_requires=requires,
      test_suite="ravencoin.tests"
     )
