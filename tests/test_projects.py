#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for entree.projects
'''
import os
import unittest

import entree.utils
import entree.projects.base as base
from utilities import (
    get_file_content,
    TMPFile,
    print_header,
    get_all_dirs_and_files,
    filemap
)

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

                    tpath = project_cls.template_path()
                    dirs, _ = get_all_dirs_and_files(tpath)
                    dirmap = filemap(dirs, replace=project_cls.replace,
                                     modname=project)

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

                    tpath = project_cls.template_path()
                    _, files = get_all_dirs_and_files(tpath)
                    filmap = filemap(files, replace=project_cls.replace,
                                     modname=project)
                    for _, fname in filmap.items():
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

                    files = entree.utils.get_config_param(
                        'general_files', [],
                        project_type=project_cls.__name__
                    )

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
                    tpath = project_cls.template_path()
                    _, files = get_all_dirs_and_files(tpath)
                    filmap = filemap(files, replace=project_cls.replace,
                                     modname=project)
                    for tname, fname in filmap.items():
                        six.print_('- Testing file content for '
                                   '`{0}`:'.format(fname))
                        filepath = os.path.join(gendir, fname)
                        templatepath = project_cls.template_path()
                        templatepath = os.path.join(templatepath, tname)
                        content1, content2 = get_file_content(
                            project, filepath, templatepath,
                            project_cls=project_cls
                        )
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
                        content1, content2 = get_file_content(
                            'somefile', filepath, templatepath,
                            project_cls=project_cls
                        )
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

                    files = entree.utils.get_config_param(
                        'general_files', [],
                        project_type=project_cls.__name__
                    )

                    for fname in files:
                        six.print_('- Testing file `{0}`:'.format(fname))
                        filepath = os.path.join(gendir, fname)
                        templatepath = os.path.join(
                            project_cls.common_template_path(),
                            fname
                        )
                        content1, content2 = get_file_content(
                            project, filepath, templatepath,
                            project_cls=project_cls
                        )
                        self.assertEqual(content1, content2)


class TestProjectPaths(unittest.TestCase):
    '''Testing if the template path, the single-file path and the common files
    files path exists
    '''
    def test_common_template_path(self):
        '''Testing common template path
        '''
        # Loop through all classes available in entree.projects
        for project_cls in CLASSES:
            self.assertTrue(os.path.exists(project_cls.common_template_path()))

    def test_template_path(self):
        '''Testing template path
        '''
        # Loop through all classes available in entree.projects
        for project_cls in CLASSES:
            self.assertTrue(os.path.exists(project_cls.template_path()))

    def test_singlefile_path(self):
        '''Testing single-file path
        '''
        # Loop through all classes available in entree.projects
        for project_cls in CLASSES:
            if project_cls.single_file:
                self.assertTrue(os.path.exists(project_cls.single_file_path()))

if __name__ == '__main__':
    unittest.main()
