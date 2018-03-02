#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setup script for entree
'''
import os

# from distutils.core import setup
from setuptools import setup, find_packages

_USERNAME = os.getenv('SUDO_USER') or os.getenv('USER')
_HOME = os.path.expanduser('~'+_USERNAME)
_CONFIGDIR = os.path.join(_HOME, '.config')


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

TEMPLATE_PATHS = [os.path.join(directory, '*')
                  for directory in ['templates'] +
                  get_template_dirs('entree/projects/templates')]
TEMPLATE_PATHS += [os.path.join('templates', 'common', '.gitignore')]

if os.path.exists(os.path.join(_CONFIGDIR, 'entree_config.json')):
    DATA_FILES = []
else:
    DATA_FILES = [(_CONFIGDIR, ['entree/entree_config.json'])]
DATA_FILES += [(_CONFIGDIR, ['entree_autocomplete'])]

setup(
    name='entree',
    version='2.1',
    description='',
    long_description='''
    Simple module to create files and directory structure necessary to
    start a python project.
    ''',
    author='Julien Spronck',
    author_email='github@frenetic.be',
    url='http://frenetic.be/',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['entree = entree:main']
    },
    data_files=DATA_FILES,
    package_data={
        'entree.projects': TEMPLATE_PATHS,
    },
    install_requires=[
        'Jinja2==2.10',
        'MarkupSafe==1.0',
        'six==1.11.0',
    ],
    license='Free for non-commercial use'
)
