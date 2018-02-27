'''
.. module:: entree.projects.base
.. moduleauthor:: Julien Spronck
.. created:: Feb 2018

Module creating a base class for all projects
'''

import datetime
import getopt
import os
import sys

from jinja2 import Template
import six
from entree.utils import (
    copy_file_structure,
    create_dirs,
    create_single_file,
    read_config
)

__version__ = '0.0'


class ProjectBase(object):
    '''Class for each project.

    Class attributes:
        project_type (str): project type (e.g. flask)
        template_dir (str): path to the template files
        replace (dict, default=None): dictionary mapping template file
            names that should be replaced when creating the files. For
            example, {'unittest_py.template': 'test_project.py'}
        version (str): version number
    '''

    # Project type (typically the python module containing the class)
    project_type = ''

    # Path to the template directory
    template_dir = ''

    # Path to a single file that you want to create in single-file mode
    single_file = None

    # Dictionary for mapping template file names to project file names
    replace = None

    # Project version
    version = __version__

    # List of directories created by the class (only for unit testing)
    directories = []

    # List of files created by the class (only for unit testing)
    files = []

    @classmethod
    def usage(cls, exit_status):
        '''
        Displays the usage/help for this project
        '''
        msg = "\nSets up a project by creating the "
        msg += "directories and starter files.\n"
        msg += "\nUsage: \n\n"
        msg += "    entree {0} ".format(cls.project_type)
        msg += "[OPTIONS] <modname>\n\n"
        msg += "Arguments:\n\n"
        msg += "    modname: the name of the project you want to start or "
        msg += "modify\n\n"
        msg += "Options:\n\n"
        msg += "    -h, --help: prints the usage of the program with possible"
        msg += "\n                options.\n\n"
        msg += "    -a, --add: adds the files to the directory specified \n"
        msg += "                with the -d option or current directory\n"
        msg += "                without creating a project directory.\n\n"
        msg += "    -d, --dir: Specifies the directory where to save create\n"
        msg += "               the project files. By default, it is the\n"
        msg += "               current directory.\n\n"
        if cls.single_file:
            msg += "    -s, --single-file: creates a single file instead of\n"
            msg += "                       a complete package.\n\n"
        msg += "    -v, --version: diplays the version number.\n\n"

        six.print_(msg)
        sys.exit(exit_status)

    @classmethod
    def dirmap(cls, **kwargs):
        '''Mapping between directory names and their template
        for testing purposes.
        '''
        out = {}
        for dirname in cls.directories:
            if cls.replace and dirname in cls.replace:
                template = Template(cls.replace[dirname])
                out[dirname] = template.render(**kwargs)
            else:
                out[dirname] = dirname
        return out

    @classmethod
    def filemap(cls, **kwargs):
        '''Mapping between file names and their template
        for testing purposes.
        '''
        out = {}
        for filename in cls.files:
            path, basename = os.path.split(filename)
            if cls.replace and path in cls.replace:
                path = Template(cls.replace[path]).render(**kwargs)
            if cls.replace and basename in cls.replace:
                template = Template(cls.replace[basename])
                out[filename] = os.path.join(path, template.render(**kwargs))
            elif filename.endswith('_py.template'):
                out[filename] = os.path.join(path, basename[:-12]+'.py')
            else:
                out[filename] = os.path.join(path, basename)
        return out

    @classmethod
    def create_one(cls, rootdir, modname):
        '''Creates a single-file project

        Args:
            rootdir (str): the root directory
            modname (str): the project name
        '''
        if cls.create_one:
            # Read config file and set creation_date
            config = read_config()
            creation_date = datetime.datetime.now().strftime('%B %Y')
            create_single_file(rootdir, modname, cls.single_file,
                               config=config, creation_date=creation_date,
                               modname=modname)

    @classmethod
    def create_all(cls, rootdir, modname, add_to_existing=False):
        '''Creates all project files and directories

        Args:
            rootdir (str): the root directory
            modname (str): the module name

        Keyword args:
            add_to_existing (bool, default=False): True if you want to add
                files without creating a project directory (add to existing
                project)
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
        copy_file_structure(projectdir, cls.template_dir,
                            replace=cls.replace,
                            modname=modname, config=config,
                            creation_date=creation_date)

    @classmethod
    def main(cls):
        '''Main program
        '''

        # Parse command line options/arguments
        options = [
            ('h', 'help'),
            ('a:', 'add='),
            ('d:', 'dir='),
            ('v', 'version')
        ]
        if cls.single_file:
            options.append(('s', 'single-file'))

        short_options = ''.join(option[0] for option in options)
        long_options = [option[1] for option in options]

        try:
            opts, args = getopt.getopt(sys.argv[2:], short_options,
                                       long_options)

        except getopt.GetoptError:
            cls.usage(2)

        add_to_existing = False
        rootdir = './'
        single_file = False
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                cls.usage(0)
            if opt in ("-a", "--add"):
                add_to_existing = True
            if opt in ("-d", "--dir"):
                rootdir = arg
            if opt in ("-s", "--single-file"):
                single_file = True
            if opt in ("-v", "--version"):
                six.print_('entree.projects.{0} {1}'.format(cls.project_type,
                                                            cls.version))
                sys.exit()

        if not args:
            if not add_to_existing:
                cls.usage(2)
            else:
                modname = ''
        else:
            modname = args[0]

        if single_file:
            cls.create_one(rootdir, modname)
        else:
            cls.create_all(rootdir, modname, add_to_existing=add_to_existing)
