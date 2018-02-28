#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for entree
'''
import datetime
import os
import shutil
import unittest

from jinja2.exceptions import UndefinedError
import entree
# import six
from utilities import TMPFile, random_string


class TestConfig(unittest.TestCase):
    '''Testing if config file was imported
    '''
    def test_get_config_dir(self):
        '''Test get_config_dir()
        '''
        username = os.getenv("SUDO_USER") or os.getenv("USER")
        homedir = os.path.expanduser('~'+username)
        configdir = os.path.join(homedir, ".config")
        self.assertEqual(configdir, entree.utils.get_config_dir())

    def test_get_config_file(self):
        '''Test get_config_file()
        '''
        configdir = entree.utils.get_config_dir()
        configfile = os.path.join(configdir, entree.utils.CONFIG_FILE_NAME)
        self.assertEqual(configfile, entree.utils.get_config_file())

    def test_create_config_inexisting(self):
        '''Test set_config() and read_config() when config file does not exist
        '''
        configdir = entree.utils.get_config_dir()
        configfile = os.path.join(configdir, entree.utils.CONFIG_FILE_NAME)

        author = 'Julien Spronck'
        author_email_prefix = 'github'
        author_email_suffix = 'frenetic.be'
        author_url = 'http://frenetic.be'

        old_config = {}

        if os.path.exists(configfile):
            old_config = entree.utils.read_config()
            os.remove(configfile)

        config = entree.utils.read_config()
        self.assertTrue(os.path.exists(configfile))
        self.assertEqual(config.AUTHOR, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_EMAIL_PREFIX, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_EMAIL_SUFFIX, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_URL, '<UNDEFINED>')
        os.remove(configfile)

        entree.utils.set_config(author=author,
                                author_email_prefix=author_email_prefix,
                                author_email_suffix=author_email_suffix,
                                author_url=author_url)
        self.assertTrue(os.path.exists(configfile))
        config = entree.utils.read_config()
        self.assertEqual(config.AUTHOR, author)
        self.assertEqual(config.AUTHOR_EMAIL_PREFIX, author_email_prefix)
        self.assertEqual(config.AUTHOR_EMAIL_SUFFIX, author_email_suffix)
        self.assertEqual(config.AUTHOR_URL, author_url)

        entree.utils.set_config(overwrite=True)
        self.assertTrue(os.path.exists(configfile))
        config = entree.utils.read_config()
        self.assertEqual(config.AUTHOR, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_EMAIL_PREFIX, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_EMAIL_SUFFIX, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_URL, '<UNDEFINED>')

        os.remove(configfile)

        if old_config:
            entree.utils.set_config(
                author=old_config.AUTHOR,
                author_email_prefix=old_config.AUTHOR_EMAIL_PREFIX,
                author_email_suffix=old_config.AUTHOR_EMAIL_SUFFIX,
                author_url=old_config.AUTHOR_URL
            )


class TestCreateDirsAndFiles(unittest.TestCase):
    '''Testing file and directory creation
    '''
    def test_create_general_file(self):
        '''Test create_dirs()
        '''
        with TMPFile() as rootdir:
            path_a = os.path.join(rootdir, 'a')
            entree.utils.create_general_file(path_a, "AAAAA")
            self.assertTrue(os.path.exists(path_a))
            with open(path_a) as fil:
                content = fil.read()
                self.assertEqual(content, "AAAAA")

    def test_create_general_file_nofile(self):
        '''Test create_dirs()
        '''
        rootdir = random_string(16)
        path_a = os.path.join(rootdir, 'a')
        with self.assertRaises(IOError):
            entree.utils.create_general_file(path_a, "AAAAA")
        self.assertFalse(os.path.exists(path_a))

    def test_create_dirs(self):
        '''Test create_dirs()
        '''
        with TMPFile() as rootdir:
            path_a = os.path.join(rootdir, 'a')
            path_b = os.path.join(rootdir, 'b')
            path_c = os.path.join(rootdir, 'c')
            entree.utils.create_dirs(rootdir, path_a, path_b, path_c)
            self.assertTrue(os.path.exists(rootdir))
            self.assertTrue(os.path.exists(path_a))
            self.assertTrue(os.path.exists(path_b))
            self.assertTrue(os.path.exists(path_c))

    def test_create_dirs_norootdir(self):
        '''Test create_dirs()
        '''
        rootdir = random_string(16)
        path_a = os.path.join(rootdir, 'a')
        path_b = os.path.join(rootdir, 'b')
        path_c = os.path.join(rootdir, 'c')
        with self.assertRaises(IOError):
            entree.utils.create_dirs(rootdir, path_a, path_b, path_c)
        self.assertFalse(os.path.exists(rootdir))
        self.assertFalse(os.path.exists(path_a))
        self.assertFalse(os.path.exists(path_b))
        self.assertFalse(os.path.exists(path_c))

    def test_render_template(self):
        '''Test render_template()
        '''
        with TMPFile() as rootdir:
            path_a = os.path.join(rootdir, 'a')
            template_string = ("My name is {{ name }}, I'm {{ blah['age'] }} "
                               "years old. This is year "
                               "{{ date.strftime('%Y') }}.")
            entree.utils.create_general_file(path_a, template_string)
            date = datetime.datetime(2018, 1, 1)
            content = entree.utils.render_template(path_a, name="Lily",
                                                   blah={'age': 19},
                                                   date=date)
            self.assertEqual(content, 'My name is Lily, I\'m 19 years old. '
                             'This is year 2018.')

    def test_create_single_file(self):
        '''Test create_single_file()
        '''
        with TMPFile() as rootdir:
            newfilename = 'newfilename'
            template_path = os.path.join(rootdir, 'template_path')

            template_string = ("My name is {{ name }}, I'm {{ blah['age'] }} "
                               "years old")
            entree.utils.create_general_file(template_path, template_string)
            entree.utils.create_single_file(rootdir, newfilename,
                                            template_path, name="Lily",
                                            blah={'age': 19})
            self.assertTrue(os.path.exists(os.path.join(rootdir, newfilename)))
            with open(os.path.join(rootdir, newfilename)) as fil:
                content = fil.read()
                self.assertEqual(content, 'My name is Lily, I\'m 19 years old')

    def test_create_single_file_nofile(self):
        '''Test create_single_file()
        '''
        rootdir = random_string(16)
        path_a = os.path.join(rootdir, 'a')
        with self.assertRaises(IOError):
            entree.utils.create_single_file(path_a, '', '')


class TestCopyFileStructure(unittest.TestCase):
    '''Testing copy_file_structure
    '''
    def setUp(self):
        '''Create a fake file structure to test
        '''
        self.template_dir = random_string(16)
        os.makedirs(self.template_dir)

        self.path_a = os.path.join(self.template_dir, 'a')
        self.path_b = os.path.join(self.template_dir, 'b')
        self.path_c = os.path.join(self.template_dir, 'c')

        entree.utils.create_dirs(self.template_dir, self.path_a, self.path_b,
                                 self.path_c)

        self.file_a = os.path.join(self.path_a, 'a.txt')
        self.file_b = os.path.join(self.path_b, 'b.md')
        self.file_c = os.path.join(self.path_c, 'c_py.template')

        entree.utils.create_general_file(self.file_a, "My name is")
        entree.utils.create_general_file(self.file_b, "{{ name }}")
        entree.utils.create_general_file(self.file_c,
                                         "I'm {{ blah['age'] }} years old.")

    def test_cfs_missing_dictionary(self):
        '''Test create_dirs()
        '''
        with TMPFile() as rootdir:
            with self.assertRaises(UndefinedError):
                entree.utils.copy_file_structure(rootdir, self.template_dir)

    def test_cfs_with_blah_dictionary(self):
        '''Test create_dirs()
        '''
        with TMPFile() as rootdir:
            path_a = os.path.join(rootdir, 'a')
            path_b = os.path.join(rootdir, 'b')
            path_c = os.path.join(rootdir, 'c')
            file_a = os.path.join(path_a, 'a.txt')
            file_b = os.path.join(path_b, 'b.md')
            file_c = os.path.join(path_c, 'c.py')
            entree.utils.copy_file_structure(rootdir, self.template_dir,
                                             blah={'age': 19})
            self.assertTrue(os.path.exists(path_a))
            self.assertTrue(os.path.exists(path_b))
            self.assertTrue(os.path.exists(path_c))
            self.assertTrue(os.path.exists(file_a))
            self.assertTrue(os.path.exists(file_b))
            self.assertTrue(os.path.exists(file_c))
            with open(file_a) as fil:
                content = fil.read()
                self.assertEqual(content, "My name is")
            with open(file_b) as fil:
                content = fil.read()
                self.assertEqual(content, "")
            with open(file_c) as fil:
                content = fil.read()
                self.assertEqual(content, "I'm 19 years old.")

    def test_cfs_with_blah_and_name(self):
        '''Test create_dirs()
        '''
        with TMPFile() as rootdir:
            path_a = os.path.join(rootdir, 'a')
            path_b = os.path.join(rootdir, 'b')
            path_c = os.path.join(rootdir, 'c')
            file_a = os.path.join(path_a, 'a.txt')
            file_b = os.path.join(path_b, 'b.md')
            file_c = os.path.join(path_c, 'c.py')
            entree.utils.copy_file_structure(rootdir, self.template_dir,
                                             blah={'age': 19},
                                             name="Lily")
            self.assertTrue(os.path.exists(path_a))
            self.assertTrue(os.path.exists(path_b))
            self.assertTrue(os.path.exists(path_c))
            self.assertTrue(os.path.exists(file_a))
            self.assertTrue(os.path.exists(file_b))
            self.assertTrue(os.path.exists(file_c))
            with open(file_a) as fil:
                content = fil.read()
                self.assertEqual(content, "My name is")
            with open(file_b) as fil:
                content = fil.read()
                self.assertEqual(content, "Lily")
            with open(file_c) as fil:
                content = fil.read()
                self.assertEqual(content, "I'm 19 years old.")

    def test_cfs_with_replace(self):
        '''Test create_dirs()
        '''
        with TMPFile() as rootdir:
            path_a = os.path.join(rootdir, 'a')
            path_b = os.path.join(rootdir, 'b')
            path_c = os.path.join(rootdir, 'c')
            file_a = os.path.join(path_a, 'new.txt')
            file_b = os.path.join(path_b, 'b.md')
            file_c = os.path.join(path_c, 'c.py')
            entree.utils.copy_file_structure(rootdir, self.template_dir,
                                             replace={'a.txt': 'new.txt'},
                                             blah={'age': 19},
                                             name="Lily")
            self.assertTrue(os.path.exists(path_a))
            self.assertTrue(os.path.exists(path_b))
            self.assertTrue(os.path.exists(path_c))
            self.assertTrue(os.path.exists(file_a))
            self.assertTrue(os.path.exists(file_b))
            self.assertTrue(os.path.exists(file_c))
            with open(file_a) as fil:
                content = fil.read()
                self.assertEqual(content, "My name is")
            with open(file_b) as fil:
                content = fil.read()
                self.assertEqual(content, "Lily")
            with open(file_c) as fil:
                content = fil.read()
                self.assertEqual(content, "I'm 19 years old.")

    def test_cfs_with_replace_dir(self):
        '''Test create_dirs()
        '''
        with TMPFile() as rootdir:
            path_a = os.path.join(rootdir, 'a')
            path_b = os.path.join(rootdir, 'b')
            path_c = os.path.join(rootdir, 'newdir')
            file_a = os.path.join(path_a, 'new.txt')
            file_b = os.path.join(path_b, 'b.md')
            file_c = os.path.join(path_c, 'c.py')
            entree.utils.copy_file_structure(rootdir, self.template_dir,
                                             replace={'a.txt': 'new.txt',
                                                      'c': 'newdir'},
                                             blah={'age': 19},
                                             name="Lily")
            self.assertTrue(os.path.exists(path_a))
            self.assertTrue(os.path.exists(path_b))
            self.assertTrue(os.path.exists(path_c))
            self.assertTrue(os.path.exists(file_a))
            self.assertTrue(os.path.exists(file_b))
            self.assertTrue(os.path.exists(file_c))
            with open(file_a) as fil:
                content = fil.read()
                self.assertEqual(content, "My name is")
            with open(file_b) as fil:
                content = fil.read()
                self.assertEqual(content, "Lily")
            with open(file_c) as fil:
                content = fil.read()
                self.assertEqual(content, "I'm 19 years old.")

    def test_cfs_with_replace_dir_templ(self):
        '''Test create_dirs()
        '''
        with TMPFile() as rootdir:
            path_a = os.path.join(rootdir, 'a')
            path_b = os.path.join(rootdir, 'b')
            path_c = os.path.join(rootdir, 'Lily')
            file_a = os.path.join(path_a, 'new.txt')
            file_b = os.path.join(path_b, 'b.md')
            file_c = os.path.join(path_c, 'c.py')
            entree.utils.copy_file_structure(rootdir, self.template_dir,
                                             replace={'a.txt': 'new.txt',
                                                      'c': '{{ name }}'},
                                             blah={'age': 19},
                                             name="Lily")
            self.assertTrue(os.path.exists(path_a))
            self.assertTrue(os.path.exists(path_b))
            self.assertTrue(os.path.exists(path_c))
            self.assertTrue(os.path.exists(file_a))
            self.assertTrue(os.path.exists(file_b))
            self.assertTrue(os.path.exists(file_c))
            with open(file_a) as fil:
                content = fil.read()
                self.assertEqual(content, "My name is")
            with open(file_b) as fil:
                content = fil.read()
                self.assertEqual(content, "Lily")
            with open(file_c) as fil:
                content = fil.read()
                self.assertEqual(content, "I'm 19 years old.")

    def tearDown(self):
        '''Get rid of the temporary file structure
        '''
        if os.path.exists(self.template_dir):
            shutil.rmtree(self.template_dir)

if __name__ == '__main__':
    unittest.main()
