#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for pyproject
'''
import os
import random
import shutil
import string
import unittest

import pyproject.flask_project as flp
import six

if six.PY2:
    six.print_('Testing with Python 2\n')
elif six.PY3:
    six.print_('Testing with Python 3\n')


def random_string(num_chars):
    '''Creates a random string of `num_chars` characters.

    Args:
        - num_chars (int): length of the desired string.

    Returns:
        randomly generated string of length `num_chars`
    '''
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(num_chars))


class TestFileCreation(unittest.TestCase):
    '''Testing if files are successfully created
    '''
    def setUp(self):
        '''Create a random project name before testing
        '''
        num_chars = 16

        self.rootdir = random_string(num_chars)
        while os.path.exists(self.rootdir):
            self.rootdir = random_string(num_chars)

        os.makedirs(self.rootdir)

        self.project = random_string(num_chars)

    def test_create_all_files_this_dir(self):
        '''Test that all files are created where they should be
        '''
        flp.create_all_files_and_dirs('.', self.project)
        gendir = os.path.join('.', self.project)

        fnames = ['static', os.path.join('static', 'css'),
                  os.path.join('static', 'css', 'style.css'),
                  os.path.join('static', 'js'),
                  os.path.join('static', 'js', 'app.js'),
                  'templates', os.path.join('templates', 'index.html'),
                  'app.py', '.gitignore']

        for fname in fnames:
            path = os.path.join(gendir, fname)
            try:
                self.assertTrue(os.path.exists(path))
            except AssertionError:
                six.print_('Path does not exist: {0}'.format(path))
                raise

    def test_create_all_files_other_dir(self):
        '''Test that all files are created where they should be
        '''
        flp.create_all_files_and_dirs(self.rootdir, self.project)
        gendir = os.path.join(self.rootdir, self.project)

        fnames = ['static', os.path.join('static', 'css'),
                  os.path.join('static', 'css', 'style.css'),
                  os.path.join('static', 'js'),
                  os.path.join('static', 'js', 'app.js'),
                  'templates', os.path.join('templates', 'index.html'),
                  'app.py', '.gitignore']

        for fname in fnames:
            path = os.path.join(gendir, fname)
            try:
                self.assertTrue(os.path.exists(path))
            except AssertionError:
                six.print_('Path does not exist: {0}'.format(path))
                raise

    def tearDown(self):
        '''Delete the randomly-created project name after testing
        '''
        if os.path.exists(self.project):
            shutil.rmtree(self.project)
        shutil.rmtree(self.rootdir)

if __name__ == '__main__':
    unittest.main()
