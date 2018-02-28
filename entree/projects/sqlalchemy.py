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
TEMPLATE_DIR = 'python-sqlalchemy'
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
    '__init___py.template']


class SQLAlchemy(ProjectBase):
    '''Class for SQLAlchemy projects

    Class attributes:
        project_type (str): project type (e.g. flask)
        template_dir (str): path to the project template directory relative to
            the template root directory
        common_dir (str): path to the common template directory relative to
            the template root directory
        single_file (str): path to a single file that you want to create in
            single-file mode relative to the template root directory
        replace (dict, default=None): dictionary mapping template file
            names that should be replaced when creating the files. For
            example, {'unittest_py.template': 'test_project.py'}
        version (str): version number
        directories (list): list of directories created by the class
            (only for unit testing)
        files (list): list of files created by the class
            (only for unit testing)
    '''
    project_type = BASENAME
    template_dir = TEMPLATE_DIR
    replace = REPLACE
    version = __version__
    directories = DIRS
    files = FILES
