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

import six
import entree.utils


def get_file_content(project, filepath, templatepath):
    ''' Get the content of a file and of its template

    Args:
        rootdir (str): root directory where the project will be saved
        project (str): project name
        filepath (str): path for the file to check
        templatepath (str): path for the template file

    Returns:
        tuple with content of both files
    '''
    modname = project
    config = entree.utils.read_config()
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
