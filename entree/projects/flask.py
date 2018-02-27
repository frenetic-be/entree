'''
.. module:: entree.projects.flask
.. moduleauthor:: Julien Spronck
.. created:: Feb 2018

Module for Flask projects
'''

import os
from entree.projects.base import ProjectBase

__version__ = '0.0'

FILEPATH, FILEBASE = os.path.split(__file__)
BASENAME = os.path.splitext(FILEBASE)[0]
TEMPLATE_DIR = os.path.join(FILEPATH, 'templates/python-flask/')
REPLACE = None
DIRS = [
    'static',
    os.path.join('static', 'css'),
    os.path.join('static', 'js'),
    'templates',
]
FILES = [
    os.path.join('static', 'css', 'style.css'),
    os.path.join('static', 'js', 'app.js'),
    os.path.join('templates', 'index.html'),
    'app_py.template',
    '.gitignore'
]


class Flask(ProjectBase):
    '''Class for Flask projects

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
