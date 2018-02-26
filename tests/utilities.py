#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Test utilities for entree
'''
import datetime
# import os
import random
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
