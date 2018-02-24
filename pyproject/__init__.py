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
                    create_general_file, create_dirs)

__version__ = '1.1'


def init_file_content(modname):
    '''
    init_file_content(modname): Returns a generator with the standard lines
    that should go into an empty python module.

    Args:
        modname (str): the module name
    '''
    config = read_config()
    import datetime
    yield '#!/usr/bin/env python'
    yield "# -*- coding: utf-8 -*-"
    yield ""
    yield "'''"
    yield ".. module:: {0}".format(modname)
    yield ".. moduleauthor:: {0}".format(config.AUTHOR)
    yield ".. created:: {0}".format(datetime.datetime.now().strftime('%B %Y'))
    yield "'''"
    yield ""
    yield "__version__ = '1.0'"
    yield ""
    yield "if __name__ == '__main__':"
    yield ""
    yield "#     import sys"
    yield "#     def usage(exit_status):"
    yield r"#         msg = '\n ... \n'"
    yield "#"
    yield "#         print(msg)"
    yield "#         sys.exit(exit_status)"
    yield "#"
    yield "#     import getopt"
    yield "#"
    yield "#    # parse command line options/arguments"
    yield "#     try:"
    yield "#         opts, args = getopt.getopt(sys.argv[1:],"
    yield "#                                    'hd:', ['help', 'dir='])"
    yield "#     except getopt.GetoptError:"
    yield "#         usage(2)"
    yield "#"
    yield "#     for opt, arg in opts:"
    yield "#         if opt in ('-h', '--help'):"
    yield "#             usage(0)"
    yield "#         if opt in ('-d', '--dir'):"
    yield "#             thedir = arg"
    yield ""
    yield "    pass"
    yield ""


def gitignore_file_content(modname):
    '''
    gitignore_file_content(modname): Returns a generator with .gitignore
    content

    Args:
        modname (str): the module name
    '''
    yield '.gitignore~'
    yield 'MANIFEST'
    yield '.DS_Store'
    yield 'dist/'
    yield 'dist/'+modname+'-1.0/*'
    yield 'dist/'+modname+'-1.0'
    yield 'dist/.DS_Store'
    yield 'build/'
    yield 'build/*'
    yield modname+'.egg-info/'
    yield modname+'.egg-info/*'
    yield '*.pyc'


def setup_file_content(modname):
    '''
    setup_file_content(modname): Returns a generator with setup.py content

    Args:
        modname (str): the module name
    '''
    config = read_config()
    yield '#!/usr/bin/env python'
    yield "# -*- coding: utf-8 -*-"
    yield ""
    yield "'''"
    yield "Setup script for {0}".format(modname)
    yield "'''"
#     yield 'import {0}'.format(modname)
    yield '# import os'
    yield '# _USERNAME = os.getenv("SUDO_USER") or os.getenv("USER")'
    yield '# _HOME = os.path.expanduser("~"+_USERNAME)'
    yield '# _CONFIGDIR = os.path.join(_HOME, ".config")'
    yield ''
    yield 'from setuptools import setup'
    yield ''
    yield 'setup(name="{0}",'.format(modname)
#     yield '      version={0}.__version__,'.format(modname)
    yield '      version="1.0",'
    yield '      description="",'
    yield '      long_description="""'
    yield '      Simple module to ...'
    yield '      """,'
    yield '      author="{0}",'.format(config.AUTHOR)
    yield '      author_email="{0}@{1}",'.format(config.AUTHOR_EMAIL_PREFIX,
                                                 config.AUTHOR_EMAIL_SUFFIX)
    yield '      url="{0}",'.format(config.AUTHOR_URL)
    yield '      packages=["{0}"],'.format(modname)
    yield '#       entry_points = {"console_scripts":["'+modname+' = "'
    yield ('#                                          '
           '"'+modname+':main"]},')
    yield ('#       data_files=[(_CONFIGDIR, '
           '["{0}/{0}_config.py"])],').format(modname)
    yield '      license="Free for non-commercial use",'
    yield '     )'
    yield ''


def test_file_content(modname):
    '''
    setup_file_content(modname): Returns a generator with content of test file

    Args:
        modname (str): the module name
    '''
    yield '#!/usr/bin/env python'
    yield "# -*- coding: utf-8 -*-"
    yield ""
    yield "'''"
    yield "Tests for {0}".format(modname)
    yield "'''"
    yield 'import sys'
    yield 'import os'
    yield 'sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))'
    yield ''
    yield 'import {0}'.format(modname)
    yield 'import unittest'
    yield ''
    yield 'class TestStringMethods(unittest.TestCase):'
    yield ''
    yield '    def test_upper(self):'
    yield '        self.assertEqual(\'foo\'.upper(), \'FOO\')'
    yield ''
    yield '    def test_isupper(self):'
    yield '        self.assertTrue(\'FOO\'.isupper())'
    yield '        self.assertFalse(\'Foo\'.isupper())'
    yield ''
    yield '    def test_split(self):'
    yield '        s = \'hello world\''
    yield '        with self.assertRaises(TypeError):'
    yield '            s.split(2)'
    yield ''
    yield 'if __name__ == \'__main__\':'
    yield '    unittest.main()'
    yield ''


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
