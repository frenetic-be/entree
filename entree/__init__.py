#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: entree
.. moduleauthor:: Julien Spronck
.. created:: Apr 2015

Simple module to create files and directories in a python project
"""

import entree.projects

__version__ = '2.1'

CLASSES = entree.projects.CLASSES


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
        msg += "    entree [OPTIONS] <PROJECT_TYPE> [PROJECT_OPTIONS] ...\n\n"
        msg += "Arguments:\n\n"
        msg += "    PROJECT_TYPE: the type of the project you want to start\n"
        msg += "\n        Available project types:\n"
        for submodule in CLASSES:
            msg += "            - {0}: type `entree {0} -h`".format(submodule)
            msg += " for help\n"
        msg += "\nOPTIONS:\n\n"
        msg += "    -m, --modules: list available project types.\n\n"
        msg += "    -v, --version: diplays the version number.\n\n"
        msg += "PROJECT_OPTIONS:\n\n"
        msg += "    Available options are specific to each project type\n\n"

        six.print_(msg)
        sys.exit(exit_status)

    import getopt

    # Parse command line options/arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hmv",
                                   ["help", "modules", "version"])
    except getopt.GetoptError:
        usage(2)

    for opt, _ in opts:
        if opt in ("-h", "--help"):
            usage(0)
        if opt in ("-m", "--module"):
            six.print_('\nList of available modules:\n')
            for submodule in CLASSES:
                six.print_('- ' + submodule)
            six.print_()
            sys.exit()
        if opt in ("-v", "--version"):
            six.print_('entree {0}'.format(__version__))
            sys.exit()

    if not args:
        usage(2)

    submodule = args[0]

    if submodule in CLASSES:
        CLASSES[submodule].main()
    else:
        usage(3)

if __name__ == '__main__':
    main()
