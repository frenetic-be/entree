#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: entree.flask_project
.. moduleauthor:: Julien Spronck
.. created:: February 2017

Simple module to create files and directories to start a Python Flask project
"""

import datetime
import os
import sys
import six
from entree.utils import (read_config, copy_file_structure, create_dirs)

__version__ = '1.0'

# Template directory
TEMPLATE_DIR = 'templates/python-flask/'
TEMPLATE_DIR = os.path.join(os.path.split(__file__)[0],
                            TEMPLATE_DIR)


def create_all_files_and_dirs(rootdir, modname, add_to_existing=False):
    '''Creates all project files and directories

    Args:
        rootdir (str): the root directory
        modname (str): the module name

    Keyword args:
        add_to_existing (bool, default=False): True if you want to add files
            without creating a project directory (add to existing project)
    '''
    if add_to_existing:
        projectdir = rootdir
    else:
        # Create project directory
        projectdir = os.path.join(rootdir, modname)
        create_dirs(rootdir, projectdir)

    # Read config file and set creation_date
    config = read_config()
    creation_date = datetime.datetime.now().strftime('%B %Y')

    # Copy entire file structure from template directory to the project
    # directory
    copy_file_structure(projectdir, TEMPLATE_DIR,
                        replace={'app_py.template': 'app.py'},
                        modname=modname, config=config,
                        creation_date=creation_date)


def main():
    '''Main program
    '''

    def usage(exit_status):
        '''
        Displays the usage/help of this script
        '''
        msg = "\nSets up a Python Flask project by creating the "
        msg += "directories and files necessary to start new project.\n"
        msg += "\nUsage: \n\n"
        msg += "    entree_flask[OPTIONS] modname\n\n"
        msg += "Arguments:\n\n"
        msg += "    modname: the name of the project you want to start or "
        msg += "modify\n\n"
        msg += "Options:\n\n"
        msg += "    -h, --help: prints the usage of the program with possible"
        msg += "\n                options.\n\n"
        msg += "    -a, --add: adds the files to the directory specified \n"
        msg += "                with the -d option or current directory.\n\n"
        msg += "    -d, --dir: Specifies the directory where to save create\n"
        msg += "               the project files. By default, it is the\n"
        msg += "               current directory.\n"

        six.print_(msg)
        sys.exit(exit_status)

    import getopt

    # Parse command line options/arguments
    try:
        opts, args = getopt.getopt(sys.argv[2:],
                                   "ha:d:v",
                                   ["help", "add=", "dir=",
                                    "version"])
    except getopt.GetoptError:
        usage(2)

    add_to_existing = False
    rootdir = './'
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(0)
        if opt in ("-a", "--add"):
            add_to_existing = True
        if opt in ("-d", "--dir"):
            rootdir = arg
        if opt in ("-v", "--version"):
            six.print_('entree.flask_project {0}'.format(__version__))
            sys.exit()

    if not args:
        if not add_to_existing:
            usage(2)
        else:
            modname = ''
    else:
        modname = args[0]

    create_all_files_and_dirs(rootdir, modname,
                              add_to_existing=add_to_existing)

if __name__ == '__main__':
    main()
