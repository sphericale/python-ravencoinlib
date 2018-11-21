#!/usr/bin/env python

from setuptools import setup, find_packages
import os

from version import __version__

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = ['python-bitcoinlib']

setup(name='python-ravencoinlib',
      version=__version__,
      description='Ravencoin extension of the python-bitcoinlib library.',
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
      dependency_links=['git+https://github.com/petertodd/python-bitcoinlib.git@05cbb3c#python-bitcoinlib'],
      test_suite="tests"
     )
