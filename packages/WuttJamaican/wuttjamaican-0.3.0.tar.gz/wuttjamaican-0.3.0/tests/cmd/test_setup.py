# -*- coding: utf-8; -*-

from unittest import TestCase

from wuttjamaican.cmd import Command, setup


# nb. do this just for coverage
from wuttjamaican.commands.setup import Setup as legacy


class TestSetup(TestCase):

    def setUp(self):
        self.command = Command()
        self.subcommand = setup.Setup(self.command)

    def test_run(self):
        # TODO: this doesn't really test anything yet
        self.subcommand._run()
