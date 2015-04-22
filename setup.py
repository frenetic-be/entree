#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setup script for pyproject
'''
import pyproject

from distutils.core import setup

setup(name="pyproject",
      version=pyproject.__version__,
      description="",
      long_description="""
      Simple module to ...
      """,
      author="Julien Spronck",
      author_email="frenticb@hotmail.com",
      url="http://frenticb.com/",
      packages=["pyproject"],
      scripts=['bin/pyproject'],
      license="Free for non-commercial use",
     )

