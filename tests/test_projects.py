#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for entree.projects
'''
import os
import unittest

import entree.projects.base as base
from utilities import get_file_content, TMPFile

import six

CLASSES = base.ProjectBase.__subclasses__()


class TestFileCreation(unittest.TestCase):
    '''Testing if files are successfully created
    '''

    def test_directory_creation(self):
        '''Test that all directories are created where they should be
        for all child classes of the ProjectBase class.
        '''
        # Loop through all classes available in entree.projects
        for project_cls in CLASSES:
            # Create temporary rootdir
            with TMPFile() as rootdir:
                # Create temporary project directory
                with TMPFile() as project:
                    six.print_('\n-------------------------------------------')
                    six.print_('Testing directories for class '
                               '`{0}`:'.format(project_cls.__name__))
                    project_cls.create_all(rootdir, project)
                    gendir = os.path.join(rootdir, project)

                    dirmap = project_cls.dirmap(modname=project)

                    for _, dname in dirmap.items():
                        six.print_('- Testing directory `{0}`:'.format(dname))
                        path = os.path.join(gendir, dname)
                        try:
                            self.assertTrue(os.path.exists(path))
                        except AssertionError:
                            six.print_('\nERROR: Path does not exist: '
                                       '{0}'.format(path))
                            raise

    def test_file_creation(self):
        '''Test that all files are created where they should be
        for all child classes of the ProjectBase class.
        '''
        # Loop through all classes available in entree.projects
        for project_cls in CLASSES:
            # Create temporary rootdir
            with TMPFile() as rootdir:
                # Create temporary project directory
                with TMPFile() as project:
                    six.print_('\n-------------------------------------------')
                    six.print_('Testing files for class '
                               '`{0}`:'.format(project_cls.__name__))
                    project_cls.create_all(rootdir, project)
                    gendir = os.path.join(rootdir, project)

                    filemap = project_cls.filemap(modname=project)

                    for _, fname in filemap.items():
                        six.print_('- Testing file `{0}`:'.format(fname))
                        path = os.path.join(gendir, fname)
                        try:
                            self.assertTrue(os.path.exists(path))
                        except AssertionError:
                            six.print_('\nERROR: Path does not exist: '
                                       '{0}'.format(path))
                            raise

    def test_content_app(self):
        '''Test file content for all files for all child classes of the
        ProjectBase class.
        '''

        for project_cls in CLASSES:
            with TMPFile() as rootdir:
                with TMPFile() as project:
                    six.print_('\n-------------------------------------------')
                    six.print_('Testing file content for class '
                               '`{0}`:'.format(project_cls.__name__))
                    project_cls.create_all(rootdir, project)

                    gendir = os.path.join(rootdir, project)
                    filemap = project_cls.filemap(modname=project)
                    for tname, fname in filemap.items():
                        six.print_('- Testing file content for '
                                   '`{0}`:'.format(fname))
                        filepath = os.path.join(gendir, fname)
                        templatepath = os.path.join(project_cls.template_dir,
                                                    tname)
                        content1, content2 = get_file_content(project,
                                                              filepath,
                                                              templatepath)
                        self.assertEqual(content1, content2)

if __name__ == '__main__':
    unittest.main()
