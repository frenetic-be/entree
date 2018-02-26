#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setup script for pyproject
'''
import os

# from distutils.core import setup
from setuptools import setup, find_packages

_USERNAME = os.getenv("SUDO_USER") or os.getenv("USER")
_HOME = os.path.expanduser('~'+_USERNAME)
_CONFIGDIR = os.path.join(_HOME, ".config")


def get_template_dirs(path, basename='templates'):
    '''Get all path names for template directories
    '''
    dirs = []
    for fname in os.listdir(path):
        subpath = os.path.join(path, fname)
        if os.path.isdir(subpath):
            newbasename = os.path.join(basename, fname)
            dirs.append(newbasename)
            dirs.extend(get_template_dirs(subpath, basename=newbasename))
    return dirs
TEMPLATE_PATHS = [os.path.join(directory, '*') for directory in ['templates'] +
                  get_template_dirs('pyproject/templates')]

setup(name="pyproject",
      version="2.0",
      description="",
      long_description="""
      Simple module to create files and directory structure necessary to
       start a python project.
      """,
      author="Julien Spronck",
      author_email="github@frenetic.be",
      url="http://frenetic.be/",
      packages=find_packages(),
      entry_points={
          'console_scripts': ['pyproject = pyproject:main']
      },
      data_files=[(_CONFIGDIR, ['pyproject/pyproject_config.json'])],
      package_data={
          'pyproject': TEMPLATE_PATHS,
      },
      install_requires=[
          'Jinja2==2.10',
          'MarkupSafe==1.0',
          'six==1.11.0',
      ],
      license="Free for non-commercial use")
