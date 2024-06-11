# -*- coding: utf-8; -*-

import os
import shutil
import tempfile
from unittest import TestCase
from unittest.mock import patch

from wuttjamaican.conf import WuttaConfig
from wuttjamaican.cmd import Command, make_appdir


# nb. do this just for coverage
from wuttjamaican.commands.make_appdir import MakeAppDir as legacy


class TestMakeAppDir(TestCase):

    def setUp(self):
        self.config = WuttaConfig(appname='wuttatest')
        self.command = Command(self.config, subcommands={
            'make-appdir': make_appdir.MakeAppDir,
        })

    def test_run(self):

        # appdir is created, and 3 subfolders added by default
        tempdir = tempfile.mkdtemp()
        appdir = os.path.join(tempdir, 'app')
        self.assertFalse(os.path.exists(appdir))
        self.command.run('make-appdir', '--path', appdir)
        self.assertTrue(os.path.exists(appdir))
        self.assertEqual(len(os.listdir(appdir)), 3)
        shutil.rmtree(tempdir)

        # subfolders still added if appdir already exists
        tempdir = tempfile.mkdtemp()
        self.assertTrue(os.path.exists(tempdir))
        self.assertEqual(len(os.listdir(tempdir)), 0)
        self.command.run('make-appdir', '--path', tempdir)
        self.assertEqual(len(os.listdir(tempdir)), 3)
        shutil.rmtree(tempdir)

        # mock out sys.prefix to get coverage
        with patch('wuttjamaican.cmd.make_appdir.sys') as sys:
            tempdir = tempfile.mkdtemp()
            appdir = os.path.join(tempdir, 'app')
            sys.prefix = tempdir
            self.assertFalse(os.path.exists(appdir))
            self.command.run('make-appdir')
            self.assertTrue(os.path.exists(appdir))
            self.assertEqual(len(os.listdir(appdir)), 3)
            shutil.rmtree(tempdir)
