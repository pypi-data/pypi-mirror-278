#!/usr/bin/env python3

import re
import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 6, 0, 'final', 0):
    raise SystemExit('Python 3.6 or later is required!')

with open('README.rst', encoding='utf-8') as fd:
    long_description = fd.read()

with open('trainstation/__init__.py') as fd:
    lines = '\n'.join(fd.readlines())

version = re.search("__version__ = '(.*)'", lines).group(1)
url = re.search("__url__ = '(.*)'", lines).group(1)
license = re.search("__license__ = '(.*)'", lines).group(1)
description = re.search("__description__ = '(.*)'", lines).group(1)

# PyPI name
name = 'trainstation'

setup(name=name,
      version=version,
      description=description,
      long_description=long_description,
      url=url,
      platforms=['unix'],
      install_requires=['scipy',
                        'numpy>=1.12',
                        'scikit-learn'],
      packages=find_packages(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Topic :: Scientific/Engineering :: Physics'])
