#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for entree
'''
import os
import shutil
import unittest

import entree.sqlalchemy_project as sqlalch
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
        sqlalch.create_all_files_and_dirs('.', self.project)
        gendir = os.path.join('.', self.project)

        fnames = ['tests', '__init__.py', 'models',
                  os.path.join('tests', 'test_{0}.py'.format(self.project)),
                  os.path.join('models', '__init__.py'.format(self.project)),
                  os.path.join('models', 'users.py'.format(self.project)),
                  os.path.join('models', 'statuses.py'.format(self.project)),
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
        sqlalch.create_all_files_and_dirs(self.rootdir, self.project)
        gendir = os.path.join(self.rootdir, self.project)

        fnames = ['tests', '__init__.py', 'models',
                  os.path.join('tests', 'test_{0}.py'.format(self.project)),
                  os.path.join('models', '__init__.py'.format(self.project)),
                  os.path.join('models', 'users.py'.format(self.project)),
                  os.path.join('models', 'statuses.py'.format(self.project)),
                  '.gitignore']

        for fname in fnames:
            path = os.path.join(gendir, fname)
            try:
                self.assertTrue(os.path.exists(path))
            except AssertionError:
                six.print_('Path does not exist: {0}'.format(path))
                raise

    def test_content_init(self):
        '''Test content of __init__.py
        '''

        sqlalch.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, '__init__.py')
        templatepath = os.path.join(sqlalch.TEMPLATE_DIR, '__init___py.template')
        content1, content2 = get_file_content(self.project, filepath,
                                              templatepath)

        self.assertEqual(content1, content2)

    def test_content_modelinit(self):
        '''Test content of models/__init__.py
        '''

        sqlalch.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, 'models', '__init__.py')
        templatepath = os.path.join(sqlalch.TEMPLATE_DIR, 'models',
                                    '__init___py.template')
        content1, content2 = get_file_content(self.project, filepath,
                                              templatepath)

        self.assertEqual(content1, content2)

    def test_content_modelusers(self):
        '''Test content of models/users.py
        '''

        sqlalch.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, 'models', 'users.py')
        templatepath = os.path.join(sqlalch.TEMPLATE_DIR, 'models',
                                    'users_py.template')
        content1, content2 = get_file_content(self.project, filepath,
                                              templatepath)

        self.assertEqual(content1, content2)

    def test_content_modelstatuses(self):
        '''Test content of models/statuses.py
        '''

        sqlalch.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, 'models', 'statuses.py')
        templatepath = os.path.join(sqlalch.TEMPLATE_DIR, 'models',
                                    'statuses_py.template')
        content1, content2 = get_file_content(self.project, filepath,
                                              templatepath)

        self.assertEqual(content1, content2)

    def test_content_gitignore(self):
        '''Test content of .gitignore
        '''
        sqlalch.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, '.gitignore')
        templatepath = os.path.join(sqlalch.TEMPLATE_DIR, '.gitignore')
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
