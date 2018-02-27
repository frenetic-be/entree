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

import entree.utils as pyutils


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
    config = pyutils.read_config()
    creation_date = datetime.datetime.now().strftime('%B %Y')
    data = {
        'modname': modname,
        'config': config,
        'creation_date': creation_date
    }

    with open(filepath) as file1:
        content1 = file1.read()
    content2 = pyutils.render_template(templatepath, **data)
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

    def __init__(self):
        '''Initialization

        Args:
            dirname (str): directlory name
        '''
        num_chars = 16
        self.rootdir = random_string(num_chars)
        while os.path.exists(self.rootdir):
            self.rootdir = random_string(num_chars)

    def __enter__(self):
        '''Create a random directory
        '''
        os.makedirs(self.rootdir)
        return self.rootdir

    def __exit__(self, *args):
        '''Deletes the random directory
        '''
        if os.path.exists(self.rootdir):
            shutil.rmtree(self.rootdir)
