#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for pyproject
'''
import os
import random
# import shutil
import string
import unittest

import pyproject
# import six


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
        self.assertEqual(configdir, pyproject.utils.get_config_dir())

    def test_get_config_file(self):
        '''Test get_config_file()
        '''
        configdir = pyproject.utils.get_config_dir()
        configfile = os.path.join(configdir, pyproject.utils.CONFIG_FILE_NAME)
        self.assertEqual(configfile, pyproject.utils.get_config_file())

    def test_create_config_inexisting(self):
        '''Test set_config() and read_config() when config file does not exist
        '''
        configdir = pyproject.utils.get_config_dir()
        configfile = os.path.join(configdir, pyproject.utils.CONFIG_FILE_NAME)

        author = 'Julien Spronck'
        author_email_prefix = 'github'
        author_email_suffix = 'frenetic.be'
        author_url = 'http://frenetic.be'

        old_config = {}

        if os.path.exists(configfile):
            old_config = pyproject.utils.read_config()
            os.remove(configfile)

        config = pyproject.utils.read_config()
        self.assertTrue(os.path.exists(configfile))
        self.assertEqual(config.AUTHOR, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_EMAIL_PREFIX, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_EMAIL_SUFFIX, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_URL, '<UNDEFINED>')
        os.remove(configfile)

        pyproject.utils.set_config(author=author,
                                   author_email_prefix=author_email_prefix,
                                   author_email_suffix=author_email_suffix,
                                   author_url=author_url)
        self.assertTrue(os.path.exists(configfile))
        config = pyproject.utils.read_config()
        self.assertEqual(config.AUTHOR, author)
        self.assertEqual(config.AUTHOR_EMAIL_PREFIX, author_email_prefix)
        self.assertEqual(config.AUTHOR_EMAIL_SUFFIX, author_email_suffix)
        self.assertEqual(config.AUTHOR_URL, author_url)

        pyproject.utils.set_config(overwrite=True)
        self.assertTrue(os.path.exists(configfile))
        config = pyproject.utils.read_config()
        self.assertEqual(config.AUTHOR, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_EMAIL_PREFIX, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_EMAIL_SUFFIX, '<UNDEFINED>')
        self.assertEqual(config.AUTHOR_URL, '<UNDEFINED>')

        os.remove(configfile)

        if old_config:
            pyproject.utils.set_config(
                author=old_config.AUTHOR,
                author_email_prefix=old_config.AUTHOR_EMAIL_PREFIX,
                author_email_suffix=old_config.AUTHOR_EMAIL_SUFFIX,
                author_url=old_config.AUTHOR_URL
            )

if __name__ == '__main__':
    unittest.main()
