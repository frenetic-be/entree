#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: pyproject.utils
.. moduleauthor:: Julien Spronck
.. created:: Feb 2018

Simple module to create files and directories in a programming project
"""
import os
import json
from jinja2 import Template

CONFIG_FILE_NAME = 'pyproject_config.json'


def get_config_dir():
    '''Returns path for the config directory.
    '''
    username = os.getenv("SUDO_USER") or os.getenv("USER")
    homedir = os.path.expanduser('~'+username)
    return os.path.join(homedir, ".config")


def get_config_file():
    '''Returns path of the config file.
    '''
    configdir = get_config_dir()
    configfile = os.path.join(configdir, CONFIG_FILE_NAME)
    return configfile


def read_config():
    '''Reads the config file

    Returns:
        config: namedtuple containing the configuration
    '''
    from collections import namedtuple

    def _json_object_hook(dic):
        '''Creates a named tuple from a dictionary dic
        '''
        return namedtuple('Config', dic.keys())(*dic.values())

    def json2obj(datafile):
        '''Reads a JSON file and convert response to a named tuple
        '''
        return json.load(datafile, object_hook=_json_object_hook)

    configfile = get_config_file()
    if not os.path.exists(configfile):
        set_config()
    with open(configfile) as fil:
        return json2obj(fil)


def set_config(author='<UNDEFINED>',
               author_email_prefix='<UNDEFINED>',
               author_email_suffix='<UNDEFINED>',
               author_url='<UNDEFINED>',
               overwrite=False):
    '''Sets the config parameters

    Keyword Args:
        author (str): author name,
        author_email_prefix (str): author email prefix,
        author_email_suffix (str): author email suffix,
        author_url (str): author url,
        overwrite (bool, default=False): Set to True to overwrite an existing
            config file.
    '''
    config = {'AUTHOR': author,
              'AUTHOR_EMAIL_PREFIX': author_email_prefix,
              'AUTHOR_EMAIL_SUFFIX': author_email_suffix,
              'AUTHOR_URL': author_url}
    configdir = get_config_dir()
    if not os.path.exists(configdir):
        os.makedirs(configdir)
    configfile = os.path.join(configdir, CONFIG_FILE_NAME)
    if not os.path.exists(configfile) or overwrite:
        with open(configfile, 'w') as fil:
            json.dump(config, fil)


def create_general_file(fname, dirname, file_content):
    '''Creates a file.

    Args:
        - fname (str): file name
        - dirname (str): directory name
        - file_content (iterator): generator/iterator containing
            the file content.
    '''
    if os.path.exists(fname):
        raise IOError('File already exists. Will not overwrite')

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(fname, 'w') as fil:
        for line in file_content:
            fil.write(line+'\n')


def create_dirs(rootdir, *dirs):
    '''
    Creates directories

    Args:
        modname (str): the module name
        dirs (str): directories to create
    '''
    if not os.path.exists(rootdir):
        raise IOError('Root directory not found: "'+rootdir+'"')

    for thedir in dirs:
        if not os.path.exists(thedir):
            os.makedirs(thedir)


def render_template(filename, **kwargs):
    '''Renders a template file given the variables defined in kwargs

    Args:
        filename (str): the filename

    Keyword args:
        **kwargs: dictionary containing the variables needed in the template

    Returns:
        string containing the content of the file after templating
    '''
    with open(filename) as fil:
        template = Template(fil.read())

    return template.render(**kwargs)
