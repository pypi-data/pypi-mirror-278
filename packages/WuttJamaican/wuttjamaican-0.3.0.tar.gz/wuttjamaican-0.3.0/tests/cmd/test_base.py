# -*- coding: utf-8; -*-

import argparse
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

from wuttjamaican.cmd import base
from wuttjamaican.cmd.setup import Setup
from wuttjamaican.testing import FileConfigTestCase


# nb. do this just for coverage
from wuttjamaican.commands.base import Command as legacy


class TestCommand(FileConfigTestCase):

    def test_base(self):
        # base command is for 'wutta' and has a 'setup' subcommand
        cmd = base.Command()
        self.assertEqual(cmd.name, 'wutta')
        self.assertIn('setup', cmd.subcommands)
        self.assertEqual(str(cmd), 'wutta')

    def test_subcommand_entry_points(self):
        with patch('wuttjamaican.cmd.base.load_entry_points') as load_entry_points:

            # empty entry points
            load_entry_points.side_effect = lambda group: {}
            cmd = base.Command()
            self.assertEqual(cmd.subcommands, {})

            # typical entry points
            load_entry_points.side_effect = lambda group: {'setup': Setup}
            cmd = base.Command()
            self.assertEqual(cmd.subcommands, {'setup': Setup})
            self.assertEqual(cmd.subcommands['setup'].name, 'setup')

            # legacy entry points
            # nb. mock returns entry points only when legacy name is used
            load_entry_points.side_effect = lambda group: {} if 'subcommands' in group else {'setup': Setup}
            cmd = base.Command()
            self.assertEqual(cmd.subcommands, {'setup': Setup})
            self.assertEqual(cmd.subcommands['setup'].name, 'setup')

    def test_sorted_subcommands(self):
        cmd = base.Command(subcommands={'foo': 'FooSubcommand',
                                        'bar': 'BarSubcommand'})

        srtd = cmd.sorted_subcommands()
        self.assertEqual(srtd, ['BarSubcommand', 'FooSubcommand'])

    def test_run_may_print_help(self):

        class Hello(base.Subcommand):
            name = 'hello'

        cmd = base.Command(subcommands={'hello': Hello})

        # first run is not "tested" per se but gives us some coverage.
        # (this will *actually* print help, b/c no args specified)
        try:
            cmd.run()
        except SystemExit:
            pass

        # from now on we mock the help
        print_help = MagicMock()
        cmd.print_help = print_help

        # help is shown if no subcommand is given
        try:
            cmd.run()
        except SystemExit:
            pass
        print_help.assert_called_once_with()

        # help is shown if -h is given
        print_help.reset_mock()
        try:
            cmd.run('-h')
        except SystemExit:
            pass
        print_help.assert_called_once_with()

        # help is shown if --help is given
        print_help.reset_mock()
        try:
            cmd.run('--help')
        except SystemExit:
            pass
        print_help.assert_called_once_with()

        # help is shown if bad arg is given
        print_help.reset_mock()
        try:
            cmd.run('--this-means-nothing')
        except SystemExit:
            pass
        print_help.assert_called_once_with()

        # help is shown if bad subcmd is given
        print_help.reset_mock()
        try:
            cmd.run('make-sandwich')
        except SystemExit:
            pass
        print_help.assert_called_once_with()

        # main help is *not* shown if subcommand *and* -h are given
        # (sub help is shown instead in that case)
        print_help.reset_mock()
        try:
            cmd.run('hello', '-h')
        except SystemExit:
            pass
        print_help.assert_not_called()

    def test_run_invokes_subcommand(self):

        class Hello(base.Subcommand):
            name = 'hello'
            def add_args(self):
                self.parser.add_argument('--foo', action='store_true')
            def run(self, args):
                self.run_with(foo=args.foo)

        run_with = Hello.run_with = MagicMock()
        cmd = base.Command(subcommands={'hello': Hello})

        # omit --foo in which case that is false by default
        cmd.run('hello')
        run_with.assert_called_once_with(foo=False)

        # specify --foo in which case that is true
        run_with.reset_mock()
        cmd.run('hello', '--foo')
        run_with.assert_called_once_with(foo=True)

    def test_run_uses_stdout_stderr_params(self):
        myout = self.write_file('my.out', '')
        myerr = self.write_file('my.err', '')

        class Hello(base.Subcommand):
            name = 'hello'
            def run(self, args):
                self.stdout.write("hello world")
                self.stderr.write("error text")

        with patch('wuttjamaican.cmd.base.sys') as sys:

            cmd = base.Command(subcommands={'hello': Hello})

            # sys.stdout and sys.stderr should be used by default
            cmd.run('hello')
            sys.exit.assert_not_called()
            sys.stdout.write.assert_called_once_with('hello world')
            sys.stderr.write.assert_called_once_with('error text')

            # but our files may be used instead if specified
            sys.reset_mock()
            cmd.run('hello', '--stdout', myout, '--stderr', myerr)
            sys.exit.assert_not_called()
            sys.stdout.write.assert_not_called()
            sys.stderr.write.assert_not_called()
            with open(myout, 'rt') as f:
                self.assertEqual(f.read(), 'hello world')
            with open(myerr, 'rt') as f:
                self.assertEqual(f.read(), 'error text')


class TestCommandArgumentParser(TestCase):

    def test_parse_args(self):

        kw = {
            'prog': 'wutta',
            'add_help': False,
        }

        # nb. examples below assume a command line like:
        #     bin/wutta foo --bar

        # first here is what default parser does
        parser = argparse.ArgumentParser(**kw)
        parser.add_argument('subcommand', nargs='*')
        try:
            args = parser.parse_args(['foo', '--bar'])
        except SystemExit:
            # nb. parser was not happy, tried to exit process
            args = None
        else:
            self.assertEqual(args.subcommand, ['foo', '--bar'])
        self.assertFalse(hasattr(args, 'argv'))

        # now here is was custom parser does
        # (moves extras to argv for subcommand parser)
        parser = base.CommandArgumentParser(**kw)
        parser.add_argument('subcommand', nargs='*')
        args = parser.parse_args(['foo', '--bar'])
        self.assertEqual(args.subcommand, ['foo'])
        self.assertEqual(args.argv, ['--bar'])


class TestSubcommand(TestCase):

    def test_basic(self):
        cmd = base.Command()
        subcmd = base.Subcommand(cmd)
        subcmd.name = 'foobar'
        self.assertEqual(repr(subcmd), 'Subcommand(name=foobar)')
        # TODO: this doesn't really test anything per se, but at least
        # gives us the coverage..
        subcmd._run()


class TestMain(TestCase):

    # nb. this doesn't test anything per se but gives coverage

    def test_explicit_args(self):
        try:
            base.main('--help')
        except SystemExit:
            pass

    def test_implicit_args(self):

        def true_exit(*args):
            sys.exit(*args)

        with patch('wuttjamaican.cmd.base.sys') as mocksys:
            mocksys.argv = ['wutta', '--help']
            mocksys.exit = true_exit

            try:
                base.main()
            except SystemExit:
                pass
