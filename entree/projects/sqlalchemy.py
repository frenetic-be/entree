'''
.. module:: entree.projects.sqlalchemy
.. moduleauthor:: Julien Spronck
.. created:: Feb 2018

Module for SQLAlchemy projects
'''

import os
from entree.projects.base import ProjectBase

__version__ = '0.0'

FILEPATH, FILEBASE = os.path.split(__file__)
BASENAME = os.path.splitext(FILEBASE)[0]
TEMPLATE_DIR = os.path.join(FILEPATH, 'templates/python-sqlalchemy/')
REPLACE = {
    'unittest_py.template': 'test_{{ modname }}.py',
}
DIRS = [
    'models',
    'tests',
]
FILES = [
    os.path.join('models', '__init___py.template'),
    os.path.join('models', 'statuses_py.template'),
    os.path.join('models', 'users_py.template'),
    os.path.join('tests', 'unittest_py.template'),
    '__init___py.template',
    '.gitignore'
]


class SQLAlchemy(ProjectBase):
    '''Class for SQLAlchemy projects

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
