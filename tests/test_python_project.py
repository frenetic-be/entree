#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for pyproject
'''
import os
import shutil
import unittest

import pyproject.python_project as pyp
from utilities import get_file_content, random_string

import six


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
        pyp.create_all_files_and_dirs('.', self.project)
        gendir = os.path.join('.', self.project)

        fnames = ['docs', 'tests', self.project,
                  os.path.join(self.project, '__init__.py'),
                  os.path.join('tests', 'test_{0}.py'.format(self.project)),
                  '.gitignore']

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
        pyp.create_all_files_and_dirs(self.rootdir, self.project)
        gendir = os.path.join(self.rootdir, self.project)

        fnames = ['docs', 'tests', self.project,
                  os.path.join(self.project, '__init__.py'),
                  os.path.join('tests', 'test_{0}.py'.format(self.project)),
                  '.gitignore']

        for fname in fnames:
            path = os.path.join(gendir, fname)
            try:
                self.assertTrue(os.path.exists(path))
            except AssertionError:
                six.print_('Path does not exist: {0}'.format(path))
                raise

    def test_content_setup(self):
        '''Test content of setup.py
        '''

        pyp.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, 'setup.py')
        templatepath = os.path.join(pyp.TEMPLATE_DIR, 'setup_py.template')
        content1, content2 = get_file_content(self.project, filepath,
                                              templatepath)

        self.assertEqual(content1, content2)

    def test_content_init(self):
        '''Test content of __init__.py
        '''
        pyp.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, self.project, '__init__.py')
        templatepath = os.path.join(pyp.TEMPLATE_DIR, 'src',
                                    '__init___py.template')
        content1, content2 = get_file_content(self.project, filepath,
                                              templatepath)

        self.assertEqual(content1, content2)

    def test_content_test(self):
        '''Test content of test_<project>.py
        '''
        pyp.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, 'tests',
                                'test_{0}.py'.format(self.project))
        templatepath = os.path.join(pyp.TEMPLATE_DIR, 'tests',
                                    'unittest_py.template')
        content1, content2 = get_file_content(self.project, filepath,
                                              templatepath)

        self.assertEqual(content1, content2)

    def test_content_gitignore(self):
        '''Test content of .gitignore
        '''
        pyp.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, '.gitignore')
        templatepath = os.path.join(pyp.TEMPLATE_DIR, '.gitignore')
        content1, content2 = get_file_content(self.project, filepath,
                                              templatepath)

        self.assertEqual(content1, content2)

    def tearDown(self):
        '''Delete the randomly-created project name after testing
        '''
        if os.path.exists(self.project):
            shutil.rmtree(self.project)
        shutil.rmtree(self.rootdir)

if __name__ == '__main__':
    unittest.main()
