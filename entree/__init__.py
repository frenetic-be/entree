#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: entree
.. moduleauthor:: Julien Spronck
.. created:: Apr 2015

Simple module to create files and directories in a python project
"""

import entree.python_project
import entree.flask_project

__version__ = '2.0'

KNOWN_MODULES = ['python', 'flask']


def main():
    '''Main program
    '''
    import six
    import sys

    def usage(exit_status):
        '''
        Displays the usage/help of this script
        '''
        msg = "\nentree sets up starter files for different types of \n"
        msg += "programming projects.\n\n"
        msg += "\nUsage: \n\n"
        msg += "    entree <PROJECT_TYPE> [OPTIONS] ...\n\n"
        msg += "Arguments:\n\n"
        msg += "    PROJECT_TYPE: the type of the project you want to start\n"
        msg += "\n        Available project types:\n"
        msg += "            - python: type `entree python -h` for help\n"
        msg += "            - flask: type `entree flask -h` for help\n"
        msg += "\nOptions:\n\n"
        msg += "    Available options are specific to each project type\n\n"

        six.print_(msg)
        sys.exit(exit_status)

    import getopt

    # Parse command line options/arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hv",
                                   ["help", "version"])
    except getopt.GetoptError:
        usage(2)

    for opt, _ in opts:
        if opt in ("-h", "--help"):
            usage(0)
        if opt in ("-v", "--version"):
            six.print_('entree {0}'.format(__version__))
            sys.exit()

    if not args:
        usage(2)

    submodule = args[0]

    if submodule not in KNOWN_MODULES:
        usage(3)

    if submodule == 'python':
        entree.python_project.main()
    elif submodule == 'flask':
        entree.flask_project.main()


if __name__ == '__main__':
    main()
