'''
.. module:: entree.projects.python
.. moduleauthor:: Julien Spronck
.. created:: Feb 2018

Module for Python projects
'''

import os
from entree.projects.base import ProjectBase

__version__ = '0.0'

FILEPATH, FILEBASE = os.path.split(__file__)
BASENAME = os.path.splitext(FILEBASE)[0]
TEMPLATE_DIR = os.path.join(FILEPATH, 'templates/python/')
REPLACE = {
    'unittest_py.template': 'test_{{ modname }}.py',
    'src': '{{ modname }}'
}
DIRS = [
    'docs',
    'tests',
    'src'
]
FILES = [
    os.path.join('docs', 'README.md'),
    os.path.join('src', '__init___py.template'),
    os.path.join('tests', 'unittest_py.template'),
    'setup_py.template',
    '.gitignore'
]


class Python(ProjectBase):
    '''Class for Python projects

    Class attributes:
        project_type (str): project type (e.g. flask)
        template_dir (str): path to the template files
        replace (dict, default=None): dictionary mapping template file
            names that should be replaced when creating the files. For
            example, {'unittest_py.template': 'test_project.py'}
        version (str): version number
    '''
    project_type = BASENAME
    template_dir = TEMPLATE_DIR
    replace = REPLACE
    version = __version__
    directories = DIRS
    files = FILES
