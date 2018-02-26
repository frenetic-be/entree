#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for pyproject
'''
import os
import shutil
import unittest

import pyproject.flask_project as flp
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

    def test_content_app(self):
        '''Test content of app.py
        '''

        flp.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, 'app.py')
        templatepath = os.path.join(flp.TEMPLATE_DIR, 'app_py.template')
        content1, content2 = get_file_content(self.project, filepath,
                                              templatepath)

        self.assertEqual(content1, content2)

    def test_content_index(self):
        '''Test content of index.html
        '''
        flp.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, 'templates', 'index.html')
        templatepath = os.path.join(flp.TEMPLATE_DIR, 'templates',
                                    'index.html')
        content1, content2 = get_file_content(self.project, filepath,
                                              templatepath)

        self.assertEqual(content1, content2)

    def test_content_style(self):
        '''Test content of style.css
        '''
        flp.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, 'static', 'css', 'style.css')
        templatepath = os.path.join(flp.TEMPLATE_DIR, 'static', 'css',
                                    'style.css')
        content1, content2 = get_file_content(self.project, filepath,
                                              templatepath)

        self.assertEqual(content1, content2)

    def test_content_js(self):
        '''Test content of app.js
        '''
        flp.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, 'static', 'js', 'app.js')
        templatepath = os.path.join(flp.TEMPLATE_DIR, 'static', 'js',
                                    'app.js')
        content1, content2 = get_file_content(self.project, filepath,
                                              templatepath)

        self.assertEqual(content1, content2)

    def test_content_gitignore(self):
        '''Test content of .gitignore
        '''
        flp.create_all_files_and_dirs(self.rootdir, self.project)

        gendir = os.path.join(self.rootdir, self.project)
        filepath = os.path.join(gendir, '.gitignore')
        templatepath = os.path.join(flp.TEMPLATE_DIR, '.gitignore')
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
