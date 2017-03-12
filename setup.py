#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setup script for pyproject
'''
import pyproject
import os

# from distutils.core import setup
from setuptools import setup

setup(name="pyproject",
      version=pyproject.__version__,
      description="",
      long_description="""
      Simple module to create files and directory structure necessary to 
      start a python project.
      """,
      author="Julien Spronck",
      author_email="github@frenetic.be",
      url="http://frenetic.be/",
      packages=["pyproject"],
      entry_points = {'console_scripts':['pyproject = pyproject:main']},
      data_files=[(os.path.join(os.path.expanduser("~"), '.config'),
                  ['pyproject/pyproject_config.py'])],
      license="Free for non-commercial use",
     )

