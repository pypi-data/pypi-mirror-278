#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

__author__ = 'Carlo Ferrigno'
setup_requires = ['setuptools >= 30.3.3']

if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    setup_requires.append('pytest-runner')

setup(description="adslibraries",
      long_description=open('README.md').read(),
      version='0.2.2',
      include_package_data=True,
      setup_requires=setup_requires)
