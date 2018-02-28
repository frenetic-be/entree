#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for entree.projects
'''
import os
import unittest

import entree.projects.base as base
from utilities import get_file_content, TMPFile, print_header

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
                with TMPFile(root=rootdir) as project:
                    print_header('Testing directory creation for class '
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
                with TMPFile(root=rootdir) as project:
                    print_header('Testing file creation for class '
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

    def test_common_file_creation(self):
        '''Test that all common files are created where they should be
        for all child classes of the ProjectBase class.
        '''
        # Loop through all classes available in entree.projects
        for project_cls in CLASSES:
            # Create temporary rootdir
            with TMPFile() as rootdir:
                # Create temporary project directory
                with TMPFile(root=rootdir) as project:
                    print_header('Testing common file creation for class '
                                 '`{0}`:'.format(project_cls.__name__))
                    project_cls.create_common_files(rootdir, project)
                    gendir = os.path.join(rootdir, project)

                    files = ['README.md', 'requirements.txt', 'License.md']

                    for fname in files:
                        six.print_('- Testing file `{0}`:'.format(fname))
                        path = os.path.join(gendir, fname)
                        try:
                            self.assertTrue(os.path.exists(path))
                        except AssertionError:
                            six.print_('\nERROR: Path does not exist: '
                                       '{0}'.format(path))
                            raise

    def test_single_file_creation(self):
        '''Test file creation in single-file mode
        for all child classes of the ProjectBase class.
        '''
        # Loop through all classes available in entree.projects
        for project_cls in CLASSES:
            if project_cls.single_file:
                # Create temporary rootdir
                with TMPFile() as rootdir:
                    # Create temporary project directory
                    with TMPFile(root=rootdir) as project:
                        print_header('Testing single-file creation for class '
                                     '`{0}`:'.format(project_cls.__name__))
                        gendir = os.path.join(rootdir, project)
                        project_cls.create_one(gendir, 'somefile.txt')
                        path = os.path.join(gendir, 'somefile.txt')
                        try:
                            self.assertTrue(os.path.exists(path))
                        except AssertionError:
                            six.print_('\nERROR: Path does not exist: '
                                       '{0}'.format(path))
                            raise

    def test_file_content(self):
        '''Test file content for all files for all child classes of the
        ProjectBase class.
        '''

        for project_cls in CLASSES:
            with TMPFile() as rootdir:
                with TMPFile(root=rootdir) as project:
                    print_header('Testing file content for class '
                                 '`{0}`:'.format(project_cls.__name__))
                    project_cls.create_all(rootdir, project)

                    gendir = os.path.join(rootdir, project)
                    filemap = project_cls.filemap(modname=project)
                    for tname, fname in filemap.items():
                        six.print_('- Testing file content for '
                                   '`{0}`:'.format(fname))
                        filepath = os.path.join(gendir, fname)
                        templatepath = project_cls.template_path()
                        templatepath = os.path.join(templatepath, tname)
                        content1, content2 = get_file_content(project,
                                                              filepath,
                                                              templatepath)
                        self.assertEqual(content1, content2)

    def test_single_file_content(self):
        '''Test file content in single-file mode
        for all child classes of the ProjectBase class.
        '''
        # Loop through all classes available in entree.projects
        for project_cls in CLASSES:
            if project_cls.single_file:
                # Create temporary rootdir
                with TMPFile() as rootdir:
                    # Create temporary project directory
                    with TMPFile(root=rootdir) as project:
                        print_header('Testing single-file content for class '
                                     '`{0}`:'.format(project_cls.__name__))
                        gendir = os.path.join(rootdir, project)
                        project_cls.create_one(gendir, 'somefile.txt')
                        filepath = os.path.join(gendir, 'somefile.txt')
                        templatepath = project_cls.single_file_path()
                        content1, content2 = get_file_content('somefile',
                                                              filepath,
                                                              templatepath)
                        self.assertEqual(content1, content2)

    def test_common_file_content(self):
        '''Test the content of the common files
        for all child classes of the ProjectBase class.
        '''
        # Loop through all classes available in entree.projects
        for project_cls in CLASSES:
            # Create temporary rootdir
            with TMPFile() as rootdir:
                # Create temporary project directory
                with TMPFile(root=rootdir) as project:
                    print_header('Testing common file content for class '
                                 '`{0}`:'.format(project_cls.__name__))

                    project_cls.create_common_files(rootdir, project)
                    gendir = os.path.join(rootdir, project)

                    files = ['README.md', 'requirements.txt', 'License.md']

                    for fname in files:
                        six.print_('- Testing file `{0}`:'.format(fname))
                        filepath = os.path.join(gendir, fname)
                        templatepath = os.path.join(
                            project_cls.common_template_path(),
                            fname
                        )
                        content1, content2 = get_file_content(project,
                                                              filepath,
                                                              templatepath)
                        self.assertEqual(content1, content2)

if __name__ == '__main__':
    unittest.main()
