#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Test utilities for entree
'''
import datetime
import os
import random
import shutil
import string

from jinja2 import Template
import six
import entree.utils


def get_file_content(project, filepath, templatepath, project_cls=None):
    ''' Get the content of a file and of its template

    Args:
        rootdir (str): root directory where the project will be saved
        project (str): project name
        filepath (str): path for the file to check
        templatepath (str): path for the template file

    Keyword args:
        project_cls (ProjectBase class, default=None): project class

    Returns:
        tuple with content of both files
    '''
    modname = project
    if project_cls is None:
        config = entree.utils.read_config()
    else:
        config = project_cls.get_config()
    creation_date = datetime.datetime.now()
    data = {
        'modname': modname,
        'config': config,
        'creation_date': creation_date
    }

    with open(filepath) as file1:
        content1 = file1.read()
    content2 = entree.utils.render_template(templatepath, **data)
    return content1, content2


def random_string(num_chars):
    '''Creates a random string of `num_chars` characters.

    Args:
        - num_chars (int): length of the desired string.

    Returns:
        randomly generated string of length `num_chars`
    '''
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(num_chars))


class TMPFile(object):
    '''Creates a context manager to create a temporary folder and delete it
    afterwards.
    '''

    def __init__(self, root=None):
        '''Initialization

        Args:
            dirname (str): directlory name
        '''
        num_chars = 16
        self.rootdir = random_string(num_chars)
        if root:
            self.fulldir = os.path.join(root, self.rootdir)
        else:
            self.fulldir = self.rootdir

        while os.path.exists(self.fulldir):
            self.rootdir = random_string(num_chars)
            if root:
                self.fulldir = os.path.join(root, self.rootdir)
            else:
                self.fulldir = self.rootdir

    def __enter__(self):
        '''Create a random directory
        '''
        os.makedirs(self.fulldir)
        return self.rootdir

    def __exit__(self, *args):
        '''Deletes the random directory
        '''
        if os.path.exists(self.rootdir):
            shutil.rmtree(self.rootdir)


def print_header(msg):
    '''Prints a header
    '''
    six.print_('\n' + '-' * len(msg))
    six.print_(msg)
    six.print_('-' * len(msg))


def replace_pathname(pathname, replace=None, **kwargs):
    '''Replaces a directory name based on patterns defined in a dictionary

    Args:
        replace (dict, default=None): dictionary with replacement patterns

    Returns:
        new directory name (str)
    '''
    if not replace:
        if pathname.endswith('_py.template'):
            return pathname[:-12]+'.py'
        return pathname

    dirsplit = pathname.split(os.sep)
    if len(dirsplit) > 1:
        # Apply this function to all directory names in the path
        dirsplit = [replace_pathname(dname, replace=replace, **kwargs)
                    for dname in dirsplit]
        return os.path.join(*dirsplit)
    else:
        if pathname in replace:
            template = Template(replace[pathname])
            return template.render(**kwargs)
        if pathname.endswith('_py.template'):
            return pathname[:-12]+'.py'
        # No match in `replace` => returns the orginal name
        return pathname


def get_all_dirs_and_files(rootdir, basename=''):
    '''Get all path names for template directories
    '''
    dirs = []
    files = []

    files_to_ignore = entree.utils.get_config_param('files_to_ignore', [])

    for fname in os.listdir(rootdir):
        subpath = os.path.join(rootdir, fname)
        newbasename = os.path.join(basename, fname)
        if os.path.isdir(subpath):
            dirs.append(newbasename)
            newdirs, newfiles = get_all_dirs_and_files(subpath,
                                                       basename=newbasename)
            dirs += newdirs
            files += newfiles
        elif (os.path.isfile(subpath) and
              fname not in files_to_ignore):
            files.append(newbasename)
    return dirs, files


def filemap(files, replace=None, **kwargs):
    '''Mapping between file/dir names and their template
    for testing purposes.
    '''
    return {name: replace_pathname(name, replace=replace, **kwargs)
            for name in files}
