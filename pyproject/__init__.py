#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: pyproject
.. moduleauthor:: Julien Spronck
.. created:: Apr 2015

Simple module to create files and directories in a python project
"""

import os
import sys
import six
from .utils import (CONFIG_FILE_NAME, get_config_dir,
                    get_config_file, read_config, set_config,
                    create_general_file, create_dirs,
                    render_template)

__version__ = '1.1'

TEMPLATE_DIR = 'templates/python/'


def init_file_content(modname):
    '''
    init_file_content(modname): Returns the content of a standard empty
    python module.

    Args:
        modname (str): the module name
    '''
    config = read_config()
    import datetime
    creation_date = datetime.datetime.now().strftime('%B %Y')

    template_file = os.path.join(os.path.split(__file__)[0],
                                 TEMPLATE_DIR, '__init__.py')
    return render_template(template_file, modname=modname, config=config,
                           creation_date=creation_date)


def gitignore_file_content(modname):
    '''
    gitignore_file_content(modname): Returns a generator with .gitignore
    content

    Args:
        modname (str): the module name
    '''
    template_file = os.path.join(os.path.split(__file__)[0],
                                 TEMPLATE_DIR, 'gitignore')
    return render_template(template_file, modname=modname)


def setup_file_content(modname):
    '''
    setup_file_content(modname): Returns a generator with setup.py content

    Args:
        modname (str): the module name
    '''
    config = read_config()
    template_file = os.path.join(os.path.split(__file__)[0],
                                 TEMPLATE_DIR, 'setup.py')
    return render_template(template_file, modname=modname, config=config)


def test_file_content(modname):
    '''
    setup_file_content(modname): Returns a generator with content of test file

    Args:
        modname (str): the module name
    '''
    template_file = os.path.join(os.path.split(__file__)[0],
                                 TEMPLATE_DIR, 'unittest.py')
    return render_template(template_file, modname=modname)


def create_init_file(modname, dirname):
    '''
    Creates __init__.py

    Args:
        modname (str): the module name
        dirname (str): the directory where to save the file.
    '''
    fname = os.path.join(dirname, '__init__.py')
    create_general_file(fname, dirname, init_file_content(modname))


def create_file(modname, dirname):
    '''
    Creates a module file

    Args:
        modname (str): the module name
        dirname (str): the directory where to save the file.
    '''
    fname = os.path.join(dirname, modname+'.py')
    create_general_file(fname, dirname, init_file_content(modname))


def create_gitignore_file(modname, dirname):
    '''
    Creates .gitignore

    Args:
        modname (str): the module name
        dirname (str): the directory where to save the file.
    '''
    fname = os.path.join(dirname, '.gitignore')
    create_general_file(fname, dirname, gitignore_file_content(modname))


def create_setup_file(modname, dirname):
    '''
    Creates setup.py

    Args:
        modname (str): the module name
        dirname (str): the directory where to save the file.
    '''
    fname = os.path.join(dirname, 'setup.py')
    create_general_file(fname, dirname, setup_file_content(modname))


def create_test_file(modname, dirname):
    '''
    Creates test file

    Args:
        modname (str): the module name
        dirname (str): the directory where to save the file.
    '''
    fname = os.path.join(dirname, 'test_'+modname+'.py')
    create_general_file(fname, dirname, test_file_content(modname))


def create_all_files_and_dirs(rootdir, modname, other_module, submodule):
    '''Creates all project files and directories

    Args:
        rootdir (str): the root directory
        modname (str): the module name
        other_module (str): the module name where you wish to add a project
            file
        submodule (str): the submodule name
    '''
    gendir = os.path.join(rootdir, modname)
    codedir = os.path.join(gendir, modname)

    if other_module:
        create_file(other_module, codedir)
        return

    if submodule:
        subdir = os.path.join(codedir, submodule)
        if os.path.exists(subdir):
            raise IOError('Submodule directory already exists')
        create_init_file(submodule, subdir)
        return

    if os.path.exists(gendir):
        raise IOError('Project directory already exists. Will not overwrite')

    testdir = os.path.join(gendir, 'tests')
    docdir = os.path.join(gendir, 'docs')

    create_dirs(rootdir, gendir, codedir, testdir, docdir)
    create_init_file(modname, codedir)
    create_gitignore_file(modname, gendir)
    create_setup_file(modname, gendir)
    create_test_file(modname, testdir)


def main():
    '''Main program
    '''

    def usage(exit_status):
        '''
        Displays the usage/help of this script
        '''
        msg = "\npyproject sets up a python project by creating the "
        msg += "directories and files necessary to start new python project.\n"
        msg += "\nUsage: \n\n"
        msg += "    pyproject [OPTIONS] modname\n\n"
        msg += "Arguments:\n\n"
        msg += "    modname: the name of the project you want to start or "
        msg += "modify\n\n"
        msg += "Options:\n\n"
        msg += "    -h, --help: prints the usage of the program with possible"
        msg += "\n                options.\n\n"
        msg += "    -a, --add: adds a .py file to the module or current \n"
        msg += "                directory.\n\n"
        msg += "    -d, --dir: Specifies the directory where to save create\n"
        msg += "               the project files. By default, it is the\n"
        msg += "               current directory.\n"
        msg += "    -s, --submodules: adds a submodule directory and\n"
        msg += "                __init__.py file.\n\n"

        six.print_(msg)
        sys.exit(exit_status)

    import getopt

    # Parse command line options/arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "ha:d:s:",
                                   ["help", "add=", "dir=", "submodule="])
    except getopt.GetoptError:
        usage(2)

    other_module = ''
    submodule = ''
    rootdir = './'
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(0)
        if opt in ("-a", "--add"):
            other_module = arg
        if opt in ("-d", "--dir"):
            rootdir = arg
        if opt in ("-s", "--submodule"):
            submodule = arg

    if not args:
        if not other_module and not submodule:
            usage(2)
        else:
            modname = ''
    else:
        modname = args[0]

    create_all_files_and_dirs(rootdir, modname, other_module, submodule)

if __name__ == '__main__':
    main()
