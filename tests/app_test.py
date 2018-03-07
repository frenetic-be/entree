#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for entree
'''
# import datetime
# import os
import unittest

import requests

BASE_URL = 'http://localhost:5000'
SUBMIT_URL = BASE_URL + '/submit'


class TestStatus(unittest.TestCase):
    '''Testing http status code
    '''
    def test_simple(self):
        '''check http status code
        '''
        data = {
            'email': 'j@f',
            'name': 'J',
            'projectname': 'BOB',
            'projecttype': 'Python',
            'url': 'frenetic.be'
        }
        response = requests.post(SUBMIT_URL, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Content-Type' in response.headers)
        self.assertTrue('Content-Disposition' in response.headers)
        self.assertEqual(response.headers.get('Content-Type'),
                         'application/zip')
        self.assertEqual(response.headers.get('Content-Disposition'),
                         'attachment; filename=BOB.zip')

    def test_invalid_projectname(self):
        '''check http response
        '''
        data = {
            'email': 'j@f',
            'name': 'J',
            'projectname': 'BOB BOBBY',
            'projecttype': 'Python',
            'url': 'frenetic.be'
        }
        response = requests.post(SUBMIT_URL, data=data)
        self.assertEqual(response.url,
                         'http://localhost:5000/?'
                         'error=Wrong+format+for+project+name')

    def test_invalid_projecttype(self):
        '''check http response
        '''
        data = {
            'email': 'j@f',
            'name': 'J',
            'projectname': 'BOBBOBBY',
            'projecttype': 'PythonZ',
            'url': 'frenetic.be'
        }
        response = requests.post(SUBMIT_URL, data=data)
        self.assertEqual(response.url,
                         'http://localhost:5000/?'
                         'error=Project+type+unsupported')


class TestFileStructure(unittest.TestCase):
    '''Testing filestructure endpoint
    '''
    def test_python(self):
        '''check http status code
        '''
        url = BASE_URL + '/filestructure/Python?projectname=blahblah'
        expected = {
            'dirs': {
                'src': 'blahblah',
                'tests': 'tests'
            },
            'files': {
                '.gitignore': '.gitignore',
                'License.md': 'License.md',
                'README.md': 'README.md',
                'requirements.txt': 'requirements.txt',
                'setup_py.template': 'setup.py',
                'src/__init___py.template': 'blahblah/__init__.py',
                'tests/unittest_py.template': 'tests/test_blahblah.py'
            },
        }
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertDictEqual(response, expected)

if __name__ == '__main__':
    unittest.main()
