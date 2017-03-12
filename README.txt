NAME
    pyproject

DESCRIPTION
    .. module:: pyproject
    .. moduleauthor:: Julien Spronck
    .. created:: Apr 2015
    
    Simple script to create files and directories in a python project. 
    
    This program is meant to be used as a console script, rather than as a
    python module. The author information (name, e-mail address and URL) can
    be configured in the config file located at `~/.config/pyproject_config.py`.
    
 USAGE
    
    pyproject [OPTIONS] modname

    Arguments:

        modname: the name of the project you want to start or modify

    Options:

        -h, --help: prints the usage of the program with possible
                    options.

        -a, --add: adds a .py file to the module or current 
                    directory.

        -d, --dir: Specifies the directory where to save create
                   the project files. By default, it is the
                   current directory.
        -s, --submodules: adds a submodule directory and
                    __init__.py file.


VERSION
    1.0


MODULES
    os


FUNCTIONS

    create_dirs(rootdir)
     |  Creates directories
     |  
     |  Args:
     |      modname (str): the module name
     |      the_dir (str): the directory where to save the file.

    create_file(modname, the_dir)
     |  Creates a module file
     |  
     |  Args:
     |      modname (str): the module name
     |      the_dir (str): the directory where to save the file.

    create_gitignore_file(modname, the_dir)
     |  Creates .gitignore
     |  
     |  Args:
     |      modname (str): the module name
     |      the_dir (str): the directory where to save the file.

    create_init_file(modname, the_dir)
     |  Creates __init__.py
     |  
     |  Args:
     |      modname (str): the module name
     |      the_dir (str): the directory where to save the file.

    create_setup_file(modname, the_dir)
     |  Creates setup.py
     |  
     |  Args:
     |      modname (str): the module name
     |      the_dir (str): the directory where to save the file.

    create_test_file(modname, the_dir)
     |  Creates test file
     |  
     |  Args:
     |      modname (str): the module name
     |      the_dir (str): the directory where to save the file.

    gitignore_file_content(modname)
     |  gitignore_file_content(modname): Returns a generator with .gitignore content
     |  
     |  Args:
     |      modname (str): the module name

    init_file_content(modname)
     |  init_file_content(modname): Returns a generator with the standard lines that
     |      should go into an empty python module.
     |  
     |  Args:
     |      modname (str): the module name

    setup_file_content(modname)
     |  setup_file_content(modname): Returns a generator with setup.py content
     |  
     |  Args:
     |      modname (str): the module name

    test_file_content(modname)
     |  setup_file_content(modname): Returns a generator with content of test file
     |  
     |  Args:
     |      modname (str): the module name


