#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setup script for pyproject
'''
import os

# from distutils.core import setup
from setuptools import setup

_USERNAME = os.getenv("SUDO_USER") or os.getenv("USER")
_HOME = os.path.expanduser('~'+_USERNAME)
_CONFIGDIR = os.path.join(_HOME, ".config")

setup(name="pyproject",
      version="1.0",
      description="",
      long_description="""
      Simple module to create files and directory structure necessary to
       start a python project.
      """,
      author="Julien Spronck",
      author_email="github@frenetic.be",
      url="http://frenetic.be/",
      packages=["pyproject"],
      entry_points={'console_scripts': ['pyproject = pyproject:main']},
      data_files=[(_CONFIGDIR, ['pyproject/pyproject_config.json'])],
      license="Free for non-commercial use")
