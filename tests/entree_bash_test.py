#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for entree
"""

# import datetime
import os
import shutil
import subprocess

import unittest

# from jinja2.exceptions import UndefinedError
# import entree
import entree.projects.base as base

from utilities import TMPFile, random_string


def run_command(cmd):
    """Run a shell command and returns the exit code"""
    split_cmd = cmd.split(" ")
    process = subprocess.Popen(split_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, _ = process.communicate()

    # for line in out.splitlines():
    #     print(line)

    # if process.returncode:
    #     for line in err.splitlines():
    #         print(line)

    return process.returncode


CLASSES = base.ProjectBase.__subclasses__()
CLSNAMES = [class_.__name__.lower() for class_ in CLASSES]


class TestStatusSimple(unittest.TestCase):
    """Testing exit code status"""

    def test_simple(self):
        """check status code of `entree python blah`"""
        for project_cls in CLSNAMES:
            modname = random_string(16)
            code = run_command("entree {0} {1}".format(project_cls, modname))
            self.assertEqual(code, 0)
            if os.path.exists(modname):
                shutil.rmtree(modname)

    def test_dir(self):
        """check status code of `entree python -d rootdir blah`"""
        for project_cls in CLSNAMES:
            modname = random_string(16)
            with TMPFile() as rootdir:
                cmd = "entree {0} -d {1} {2}".format(project_cls, rootdir, modname)
                code = run_command(cmd)
                self.assertEqual(code, 0)

    def test_help(self):
        """check status code of `entree python -h`"""
        for project_cls in CLSNAMES:
            code = run_command("entree {0} -h".format(project_cls))
            self.assertEqual(code, 0)

    def test_version(self):
        """check status code of `entree python -v`"""
        for project_cls in CLSNAMES:
            code = run_command("entree {0} -v".format(project_cls))
            self.assertEqual(code, 0)

    def test_single(self):
        """check status code of `entree python -s blah`"""
        for project_cls in CLASSES:
            clsname = project_cls.__name__.lower()
            modname = random_string(16)
            cmd = "entree {0} -s {1}".format(clsname, modname)
            if project_cls.single_file:
                code = run_command(cmd)
                self.assertEqual(code, 0)
            if os.path.exists(modname):
                os.remove(modname)

    def test_add(self):
        """check status code of `entree python -a -d rootdir blah`"""
        for project_cls in CLSNAMES:
            modname = random_string(16)
            with TMPFile() as rootdir:
                cmd = "entree {0} -a -d {1} {2}".format(project_cls, rootdir, modname)
                code = run_command(cmd)
                self.assertEqual(code, 0)

    def test_partial(self):
        """check status code of `entree python -d dir -p partial blah`
        Status should be 1 if there is no `partial_builds` in the project
        config or if the partial name does not exist in `partial_builds`,
        should be 0 otherwise.
        """
        for project_cls in CLASSES:
            clsname = project_cls.__name__.lower()
            modname = random_string(16)
            with TMPFile() as rootdir:
                config = project_cls.get_config()
                if "partial_builds" in config:
                    for partial in config["partial_builds"]:
                        cmd = "entree {0} -d {1} -p {2} {3}".format(clsname, rootdir, partial, modname)
                        code = run_command(cmd)
                        self.assertEqual(code, 0)


class TestStatusMainSimple(unittest.TestCase):
    """Testing exit code status"""

    def test_help(self):
        """check status code of `entree -h`"""
        code = run_command("entree -h")
        self.assertEqual(code, 0)

    def test_version(self):
        """check status code of `entree -v`"""
        code = run_command("entree -v")
        self.assertEqual(code, 0)

    def test_modules(self):
        """check status code of `entree -m`"""
        code = run_command("entree -m")
        self.assertEqual(code, 0)

    def test_default_projtype(self):
        """check status code of `entree blah`"""
        modname = random_string(16)
        code = run_command("entree {0}".format(modname))
        self.assertEqual(code, 0)
        if os.path.exists(modname):
            shutil.rmtree(modname)

    def test_no_projtype_single(self):
        """check status code of `entree blah.py -s`"""
        modname = random_string(16)
        code = run_command("entree {0} -s".format(modname))
        self.assertEqual(code, 0)
        if os.path.exists(modname):
            os.remove(modname)

    def test_no_projtype_dir(self):
        """check status code of `entree blah.py -d blah`"""
        with TMPFile() as rootdir:
            modname = random_string(16)
            code = run_command("entree {0} -d {1}".format(modname, rootdir))
            self.assertEqual(code, 0)
            if os.path.exists(modname):
                os.remove(modname)


class TestStatusError(unittest.TestCase):
    """Testing exit code status with errors"""

    def test_no_args(self):
        """check status code of `entree python`"""
        for project_cls in CLSNAMES:
            code = run_command("entree {0}".format(project_cls))
            self.assertEqual(code, 4)

    def test_wrong_option(self):
        """check status code of `entree python -z`"""
        for project_cls in CLSNAMES:
            code = run_command("entree {0} -z".format(project_cls))
            self.assertEqual(code, 3)

    def test_single_rootdir_doesntexist(self):
        """`entree python -d blah -s blah.py`
        should raise an error if directory blah doesn't exist.
        """
        rootdir = random_string(16)
        code = run_command("entree python -d {0} -s blah.py".format(rootdir))
        self.assertEqual(code, 1)

    def test_rootdir_doesntexist(self):
        """`entree python -d blah -s blah.py`
        should raise an error if directory blah doesn't exist.
        """
        rootdir = random_string(16)
        code = run_command("entree python -d {0} blah".format(rootdir))
        self.assertEqual(code, 1)

    def test_toomany_args(self):
        """check status code of `entree python blah blah blah`"""
        for project_cls in CLSNAMES:
            modname = random_string(16)
            code = run_command("entree {0} {1} blah".format(project_cls, modname))
            self.assertEqual(code, 6)
            if os.path.exists(modname):
                shutil.rmtree(modname)

    def test_default_projtype_toomany_args(self):
        """check status code of `entree blah blah`"""
        modname = random_string(16)
        code = run_command("entree {0} {0}".format(modname))
        self.assertEqual(code, 6)
        if os.path.exists(modname):
            shutil.rmtree(modname)

    def test_partial(self):
        """check status code of `entree python -d dir -p partial blah`
        Status should be 1 if there is no `partial_builds` in the project
        config or if the partial name does not exist in `partial_builds`,
        should be 0 otherwise.
        """
        for project_cls in CLASSES:
            clsname = project_cls.__name__.lower()
            modname = random_string(16)
            with TMPFile() as rootdir:
                config = project_cls.get_config()
                if "partial_builds" not in config:
                    cmd = "entree {0} -d {1} -p blah {2}".format(clsname, rootdir, modname)
                    code = run_command(cmd)
                    self.assertEqual(code, 1)

    def test_partial2(self):
        """check status code of `entree python -d dir -p partial blah`
        Status should be 1 if there is no `partial_builds` in the project
        config or if the partial name does not exist in `partial_builds`,
        should be 0 otherwise.
        """
        for project_cls in CLASSES:
            clsname = project_cls.__name__.lower()
            modname = random_string(16)
            with TMPFile() as rootdir:
                config = project_cls.get_config()
                if "partial_builds" in config:
                    cmd = "entree {0} -d {1} -p {2} {2}".format(clsname, rootdir, modname)
                    code = run_command(cmd)
                    self.assertEqual(code, 1)


class TestStatusMainError(unittest.TestCase):
    """Testing exit code status from main script"""

    def test_no_args(self):
        """check status code of `entree`"""
        code = run_command("entree")
        self.assertEqual(code, 4)

    def test_wrong_option(self):
        """check status code of `entree -z`"""
        code = run_command("entree -z")
        self.assertEqual(code, 3)


class TestOutputSimple(unittest.TestCase):
    """Testing output os simple commands"""

    def setUp(self):
        """Setting up"""
        self.modname = random_string(16)

    def test_python(self):
        """check output of `entree python blah`"""
        run_command("entree python {0}".format(self.modname))
        files = [
            self.modname,
            os.path.join(self.modname, self.modname),
            os.path.join(self.modname, self.modname, "__init__.py"),
            os.path.join(self.modname, "tests"),
            os.path.join(self.modname, "tests", "test_{0}.py".format(self.modname)),
            os.path.join(self.modname, "setup.py"),
            os.path.join(self.modname, "License.md"),
            os.path.join(self.modname, "requirements.txt"),
            os.path.join(self.modname, "README.md"),
            os.path.join(self.modname, ".gitignore"),
        ]
        for name in files:
            self.assertTrue(os.path.exists(name))

    def test_python_dir(self):
        """check output of `entree python -d somedir blah`"""
        with TMPFile() as rootdir:
            run_command("entree python -d {0} {1}".format(rootdir, self.modname))
            files = [
                self.modname,
                os.path.join(self.modname, self.modname),
                os.path.join(self.modname, self.modname, "__init__.py"),
                os.path.join(self.modname, "tests"),
                os.path.join(self.modname, "tests", "test_{0}.py".format(self.modname)),
                os.path.join(self.modname, "setup.py"),
                os.path.join(self.modname, "License.md"),
                os.path.join(self.modname, "requirements.txt"),
                os.path.join(self.modname, "README.md"),
                os.path.join(self.modname, ".gitignore"),
            ]
            for name in files:
                self.assertTrue(os.path.exists(os.path.join(rootdir, name)))

    def test_python_single(self):
        """check output of `entree python -s blah`"""
        cmd = "entree python -s {0}".format(self.modname)
        run_command(cmd)
        self.assertTrue(os.path.exists(self.modname))
        if os.path.exists(self.modname):
            os.remove(self.modname)

    def test_add(self):
        """check output of `entree python -a -d rootdir blah`"""
        with TMPFile() as rootdir:
            cmd = "entree python -a -d {0} {1}".format(rootdir, self.modname)
            run_command(cmd)
            files = [
                self.modname,
                os.path.join(self.modname, "__init__.py"),
                "tests",
                os.path.join("tests", "test_{0}.py".format(self.modname)),
                "setup.py",
                "License.md",
                "requirements.txt",
                "README.md",
                ".gitignore",
            ]
            for name in files:
                self.assertTrue(os.path.exists(os.path.join(rootdir, name)))

    def tearDown(self):
        """Tearing down"""
        if os.path.exists(self.modname):
            shutil.rmtree(self.modname)


if __name__ == "__main__":
    unittest.main()
