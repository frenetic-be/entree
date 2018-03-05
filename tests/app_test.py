#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for entree
'''
# import datetime
# import os
import unittest

import requests

SUBMIT_URL = 'http://localhost:5000/submit'


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

if __name__ == '__main__':
    unittest.main()
