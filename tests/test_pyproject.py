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

import pyproject
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


class TestConfig(unittest.TestCase):
    '''Testing if config file was imported
    '''
    def test_get_config_dir(self):
        '''Test get_config_dir()
        '''
        username = os.getenv("SUDO_USER") or os.getenv("USER")
        homedir = os.path.expanduser('~'+username)
        configdir = os.path.join(homedir, ".config")
        self.assertEqual(configdir, pyproject.get_config_dir())

    def test_get_config_file(self):
        '''Test get_config_file()
        '''
        configdir = pyproject.get_config_dir()
        configfile = os.path.join(configdir, pyproject.CONFIG_FILE_NAME)
        self.assertEqual(configfile, pyproject.get_config_file())

    def test_create_config_inexisting(self):
        '''Test set_config() and read_config() when config file does not exist
        '''
        configdir = pyproject.get_config_dir()
        configfile = os.path.join(configdir, pyproject.CONFIG_FILE_NAME)

        author = 'Julien Spronck'
        author_email_prefix = 'github'
        author_email_suffix = 'frenetic.be'
        author_url = 'http://frenetic.be'

        old_config = {}

        if os.path.exists(configfile):
            old_config = pyproject.read_config()
            os.remove(configfile)

        config = pyproject.read_config()
        self.assertTrue(os.path.exists(configfile))
        self.assertEqual(config.AUTHOR, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_EMAIL_PREFIX, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_EMAIL_SUFFIX, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_URL, '<UNDEFINED>')
        os.remove(configfile)

        pyproject.set_config(author=author,
                             author_email_prefix=author_email_prefix,
                             author_email_suffix=author_email_suffix,
                             author_url=author_url)
        self.assertTrue(os.path.exists(configfile))
        config = pyproject.read_config()
        self.assertEqual(config.AUTHOR, author)
        self.assertEqual(config.AUTHOR_EMAIL_PREFIX, author_email_prefix)
        self.assertEqual(config.AUTHOR_EMAIL_SUFFIX, author_email_suffix)
        self.assertEqual(config.AUTHOR_URL, author_url)

        pyproject.set_config(overwrite=True)
        self.assertTrue(os.path.exists(configfile))
        config = pyproject.read_config()
        self.assertEqual(config.AUTHOR, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_EMAIL_PREFIX, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_EMAIL_SUFFIX, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_URL, '<UNDEFINED>')

        os.remove(configfile)

        if old_config:
            pyproject.set_config(
                author=old_config.AUTHOR,
                author_email_prefix=old_config.AUTHOR_EMAIL_PREFIX,
                author_email_suffix=old_config.AUTHOR_EMAIL_SUFFIX,
                author_url=old_config.AUTHOR_URL
            )


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

    def test_create_dirs(self):
        '''Test if dirs are created
        '''
        a_path = os.path.join(self.rootdir, 'a')
        b_path = os.path.join(self.rootdir, 'b')
        c_path = os.path.join(self.rootdir, 'c')
        pyproject.create_dirs(self.rootdir, a_path, b_path, c_path)
        self.assertTrue(os.path.exists(a_path))
        self.assertTrue(os.path.exists(b_path))
        self.assertTrue(os.path.exists(c_path))
        self.assertTrue(os.path.isdir(a_path))
        self.assertTrue(os.path.isdir(b_path))
        self.assertTrue(os.path.isdir(c_path))

    def test_create_file(self):
        '''Test if module file is created
        '''
        pyproject.create_file(self.project, self.rootdir)
        file_path = os.path.join(self.rootdir, self.project + '.py')
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path) as fil:
            lines = fil.readlines()
        content = list(pyproject.init_file_content(self.project))
        for j, line in enumerate(lines):
            self.assertEqual(line, content[j]+'\n')

    def test_create_init(self):
        '''Test if __init__.py is created
        '''
        pyproject.create_init_file(self.project, self.rootdir)
        file_path = os.path.join(self.rootdir, '__init__.py')
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path) as fil:
            lines = fil.readlines()
        content = list(pyproject.init_file_content(self.project))
        for j, line in enumerate(lines):
            self.assertEqual(line, content[j]+'\n')

    def test_create_gitignore(self):
        '''Test if .gitignore is created
        '''
        pyproject.create_gitignore_file(self.project, self.rootdir)
        file_path = os.path.join(self.rootdir, '.gitignore')
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path) as fil:
            lines = fil.readlines()
        content = list(pyproject.gitignore_file_content(self.project))
        for j, line in enumerate(lines):
            self.assertEqual(line, content[j]+'\n')

    def test_create_setup(self):
        '''Test if setup.py is created
        '''
        pyproject.create_setup_file(self.project, self.rootdir)
        file_path = os.path.join(self.rootdir, 'setup.py')
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path) as fil:
            lines = fil.readlines()
        content = list(pyproject.setup_file_content(self.project))
        for j, line in enumerate(lines):
            self.assertEqual(line, content[j]+'\n')

    def test_create_test(self):
        '''Test if test file is created
        '''
        pyproject.create_test_file(self.project, self.rootdir)
        file_path = os.path.join(self.rootdir,
                                 'test_{0}.py'.format(self.project))
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path) as fil:
            lines = fil.readlines()
        content = list(pyproject.test_file_content(self.project))
        for j, line in enumerate(lines):
            self.assertEqual(line, content[j]+'\n')

    def test_module_exists(self):
        '''Test what happens when module file already exists
        '''
        pyproject.create_file(self.project, self.rootdir)
        with self.assertRaises(IOError):
            pyproject.create_file(self.project, self.rootdir)

    def test_init_exists(self):
        '''Test what happens when __init__.py already exists
        '''
        pyproject.create_init_file(self.project, self.rootdir)
        with self.assertRaises(IOError):
            pyproject.create_init_file(self.project, self.rootdir)

    def test_gitignore_exists(self):
        '''Test what happens when .gitignore already exists
        '''
        pyproject.create_gitignore_file(self.project, self.rootdir)
        with self.assertRaises(IOError):
            pyproject.create_gitignore_file(self.project, self.rootdir)

    def test_setup_exists(self):
        '''Test what happens when setup.py already exists
        '''
        pyproject.create_setup_file(self.project, self.rootdir)
        with self.assertRaises(IOError):
            pyproject.create_setup_file(self.project, self.rootdir)

    def test_test_exists(self):
        '''Test what happens when test file already exists
        '''
        pyproject.create_test_file(self.project, self.rootdir)
        with self.assertRaises(IOError):
            pyproject.create_test_file(self.project, self.rootdir)

    def test_create_all_files_this_dir(self):
        '''Test that all files are created where they should be
        '''
        pyproject.create_all_files_and_dirs('.', self.project, '', '')
        gendir = os.path.join('.', self.project)

        self.assertTrue(os.path.exists(gendir))
        codedir = os.path.join(gendir, self.project)
        self.assertTrue(os.path.exists(codedir))
        initfile = os.path.join(codedir, '__init__.py')
        self.assertTrue(os.path.exists(initfile))
        gitignorefile = os.path.join(gendir, '.gitignore')
        self.assertTrue(os.path.exists(gitignorefile))
        setupfile = os.path.join(gendir, 'setup.py')
        self.assertTrue(os.path.exists(setupfile))
        docdir = os.path.join(gendir, 'docs')
        self.assertTrue(os.path.exists(docdir))
        testdir = os.path.join(gendir, 'tests')
        self.assertTrue(os.path.exists(testdir))
        testfile = os.path.join(testdir, 'test_{0}.py'.format(self.project))
        self.assertTrue(os.path.exists(testfile))

    def test_create_all_files_other_dir(self):
        '''Test that all files are created where they should be
        '''
        pyproject.create_all_files_and_dirs(self.rootdir, self.project, '', '')
        gendir = os.path.join(self.rootdir, self.project)

        self.assertTrue(os.path.exists(gendir))
        codedir = os.path.join(gendir, self.project)
        self.assertTrue(os.path.exists(codedir))
        initfile = os.path.join(codedir, '__init__.py')
        self.assertTrue(os.path.exists(initfile))
        gitignorefile = os.path.join(gendir, '.gitignore')
        self.assertTrue(os.path.exists(gitignorefile))
        setupfile = os.path.join(gendir, 'setup.py')
        self.assertTrue(os.path.exists(setupfile))
        docdir = os.path.join(gendir, 'docs')
        self.assertTrue(os.path.exists(docdir))
        testdir = os.path.join(gendir, 'tests')
        self.assertTrue(os.path.exists(testdir))
        testfile = os.path.join(testdir, 'test_{0}.py'.format(self.project))
        self.assertTrue(os.path.exists(testfile))

    def tearDown(self):
        '''Delete the randomly-created project name after testing
        '''
        if os.path.exists(self.project):
            shutil.rmtree(self.project)
        shutil.rmtree(self.rootdir)

if __name__ == '__main__':
    unittest.main()
