#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: pyproject
.. moduleauthor:: Julien Spronck
.. created:: Apr 2015

Simple module to create files and directories in a python project
"""

__version__ = '1.0'

import os

def init_file_content(modname):
    '''
    init_file_content(modname): Returns a generator with the standard lines that
        should go into an empty python module.

    Args:
        modname (str): the module name
    '''
    import datetime
    yield '#!/usr/bin/env python'
    yield "# -*- coding: utf-8 -*-"
    yield ""
    yield "'''"
    yield ".. module:: {0}".format(modname)
    yield ".. moduleauthor:: Julien Spronck"
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
    yield "#         print msg"
    yield "#         sys.exit(exit_status)"
    yield "#"
    yield "#     import getopt"
    yield "#"
    yield "#    # parse command line options/arguments"
    yield "#     try:"
    yield "#         OPTS, ARGS = getopt.getopt(sys.argv[1:],"
    yield "#                                    'hd:', ['help', 'dir='])"
    yield "#     except getopt.GetoptError:"
    yield "#         usage(2)"
    yield "#"
    yield "#     for o, a in OPTS:"
    yield "#         if o in ('-h', '--help'):"
    yield "#             usage(0)"
    yield "#         if o in ('-d', '--dir'):"
    yield "#             thedir = a"
    yield ""
    yield "    pass"
    yield ""

def gitignore_file_content(modname):
    '''
    gitignore_file_content(modname): Returns a generator with .gitignore content

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

def setup_file_content(modname):
    '''
    setup_file_content(modname): Returns a generator with setup.py content

    Args:
        modname (str): the module name
    '''
    yield '#!/usr/bin/env python'
    yield "# -*- coding: utf-8 -*-"
    yield ""
    yield "'''"
    yield "Setup script for {0}".format(modname)
    yield "'''"
    yield 'import {0}'.format(modname)
    yield ''
    yield 'from distutils.core import setup'
    yield ''
    yield 'setup(name="{0}",'.format(modname)
    yield '      version={0}.__version__,'.format(modname)
    yield '      description="",'
    yield '      long_description="""'
    yield '      Simple module to ...'
    yield '      """,'
    yield '      author="Julien Spronck",'
    yield '      author_email="frenticb@hotmail.com",'
    yield '      url="http://frenticb.com/",'
    yield '      packages=["{0}"],'.format(modname)
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

def create_init_file(modname, the_dir):
    '''
    Creates __init__.py

    Args:
        modname (str): the module name
        the_dir (str): the directory where to save the file.
    '''
    fname = os.path.join(the_dir, '__init__.py')
    if os.path.exists(fname):
        raise IOError('File already exists. Will not overwrite')

    if not os.path.exists(the_dir):
        os.makedirs(the_dir)

    with open(fname, 'w') as fil:
        for line in init_file_content(modname):
            fil.write(line+'\n')

def create_file(modname, the_dir):
    '''
    Creates a module file

    Args:
        modname (str): the module name
        the_dir (str): the directory where to save the file.
    '''
    fname = os.path.join(the_dir, modname+'.py')
    if os.path.exists(fname):
        raise IOError('File already exists. Will not overwrite')

    if not os.path.exists(the_dir):
        os.makedirs(the_dir)

    with open(fname, 'w') as fil:
        for line in init_file_content(modname):
            fil.write(line+'\n')

def create_gitignore_file(modname, the_dir):
    '''
    Creates .gitignore

    Args:
        modname (str): the module name
        the_dir (str): the directory where to save the file.
    '''
    fname = os.path.join(the_dir, '.gitignore')
    if os.path.exists(fname):
        raise IOError('File already exists. Will not overwrite')

    if not os.path.exists(the_dir):
        os.makedirs(the_dir)

    with open(fname, 'w') as fil:
        for line in gitignore_file_content(modname):
            fil.write(line+'\n')

def create_setup_file(modname, the_dir):
    '''
    Creates setup.py

    Args:
        modname (str): the module name
        the_dir (str): the directory where to save the file.
    '''
    fname = os.path.join(the_dir, 'setup.py')
    if os.path.exists(fname):
        raise IOError('File already exists. Will not overwrite')

    if not os.path.exists(the_dir):
        os.makedirs(the_dir)

    with open(fname, 'w') as fil:
        for line in setup_file_content(modname):
            fil.write(line+'\n')

def create_test_file(modname, the_dir):
    '''
    Creates test file

    Args:
        modname (str): the module name
        the_dir (str): the directory where to save the file.
    '''
    fname = os.path.join(the_dir, 'test_'+modname+'.py')
    if os.path.exists(fname):
        raise IOError('File already exists. Will not overwrite')

    if not os.path.exists(the_dir):
        os.makedirs(the_dir)

    with open(fname, 'w') as fil:
        for line in test_file_content(modname):
            fil.write(line+'\n')

def create_dirs(rootdir, *dirs):
    '''
    Creates directories

    Args:
        modname (str): the module name
        the_dir (str): the directory where to save the file.
    '''
    if not os.path.exists(rootdir):
        raise IOError('Root directory not found: "'+rootdir+'"')

    for thedir in dirs:
        if not os.path.exists(thedir):
            os.makedirs(thedir)

if __name__ == '__main__':

    import sys
    def usage(exit_status):
        '''
        Displays the usage/help of this script
        '''
        msg = "\npyproject sets up a python project by creating the directories"
        msg += " and files necessary to start new python project.\n\n"
        msg += "Usage: \n\n"
        msg += "    [python] pyproject.py [OPTIONS]\n\n"
        msg += "Options:\n\n"
        msg += "    -h, --help: prints the usage of the program with possible\n"
        msg += "                options.\n\n"
        msg += "    -a, --add: adds a .py file to the module or current \n"
        msg += "                directory.\n\n"
        msg += "    -d, --dir: Specifies the directory where to save create\n"
        msg += "               the project files. By default, it is the\n"
        msg += "               current directory.\n"
        msg += "    -s, --submodules: adds a submodule directory and\n"
        msg += "                __init__.py file.\n\n"

        print msg
        sys.exit(exit_status)

    import getopt

   # parse command line options/arguments
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:],
                                   "ha:d:s:", ["help", "add=", "dir=", "submodule="])
    except getopt.GetoptError:
        usage(2)

    OTHERMODULE = ''
    SUBMODULE = ''
    ROOTDIR = './'
    for o, a in OPTS:
        if o in ("-h", "--help"):
            usage(0)
        if o in ("-a", "--add"):
            OTHERMODULE = a
        if o in ("-d", "--dir"):
            ROOTDIR = a
        if o in ("-s", "--submodule"):
            SUBMODULE = a

    if len(ARGS) == 0:
        if not OTHERMODULE and not SUBMODULE:
            usage(2)
        else:
            MODNAME = ''
    else:
        MODNAME = ARGS[0]

    CODEDIR = os.path.join(ROOTDIR, MODNAME, MODNAME)
    GENDIR = os.path.join(ROOTDIR, MODNAME)

    if OTHERMODULE:
        create_file(OTHERMODULE, CODEDIR)
        sys.exit()

    if SUBMODULE:
        SUBDIR = os.path.join(CODEDIR, SUBMODULE)
        if os.path.exists(SUBDIR):
            raise IOError('Submodule directory already exists')
        create_init_file(SUBMODULE, SUBDIR)
        sys.exit()

    if os.path.exists(GENDIR):
        raise IOError('Project directory already exists. Will not overwrite')


    TESTDIR = os.path.join(ROOTDIR, MODNAME, 'tests')
    DOCDIR = os.path.join(ROOTDIR, MODNAME, 'docs')

    create_dirs(ROOTDIR, GENDIR, CODEDIR, TESTDIR, DOCDIR)
    create_init_file(MODNAME, CODEDIR)
    create_gitignore_file(MODNAME, GENDIR)
    create_setup_file(MODNAME, GENDIR)
    create_test_file(MODNAME, TESTDIR)
