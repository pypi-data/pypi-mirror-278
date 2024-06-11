# -*- coding: utf-8; -*-
################################################################################
#
#  WuttJamaican -- Base package for Wutta Framework
#  Copyright © 2023 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
WuttJamaican - command framework
"""

import argparse
import logging
import sys
import warnings

from wuttjamaican import __version__
from wuttjamaican.conf import make_config
from wuttjamaican.util import load_entry_points


log = logging.getLogger(__name__)


class Command:
    """
    Primary command for the application.

    A primary command will usually have multiple subcommands it can
    run.  The typical command line interface is like:

    .. code-block:: none

       <command> [command-options] <subcommand> [subcommand-options]

    :class:`Subcommand` will contain most of the logic, in terms of
    what actually happens when it runs.  Top-level commands are mostly
    a stub for sake of logically grouping the subcommands.

    :param config: Optional config object to use.

       Usually a command is being ran via actual command line, and
       there is no config object yet so it must create one.  (It does
       this within its :meth:`run()` method.)

       But if you already have a config object you can specify it here
       and it will be used instead.

    :param name: Optional value to assign to :attr:`name`.  Usually
       this is declared within the command class definition, but if
       needed it can be provided dynamically.

    :param stdout: Optional replacement to use for :attr:`stdout`.

    :param stderr: Optional replacement to use for :attr:`stderr`.

    :param subcommands: Optional dictionary to use for
       :attr:`subcommands`, instead of loading those via entry points.

    This base class also serves as the primary ``wutta`` command for
    WuttJamaican.  Most apps will subclass this and register their own
    top-level command, then create subcommands as needed.

    For more info see :doc:`/narr/cli/commands`.

    .. attribute::  name

       Name of the primary command, e.g. ``wutta``

    .. attribute:: description

       Description of the app itself or the primary command.

    .. attribute:: version

       Version string for the app or primary command.

    .. attribute:: stdout

       Reference to file-like object which should be used for writing
       to STDOUT.  By default this is just ``sys.stdout``.

    .. attribute:: stderr

       Reference to file-like object which should be used for writing
       to STDERR.  By default this is just ``sys.stderr``.

    .. attribute:: subcommands

       Dictionary of available subcommand classes, keyed by subcommand
       name.  These are usually loaded from setuptools entry points.
    """
    name = 'wutta'
    version = __version__
    description = "Wutta Software Framework"

    def __init__(
            self,
            config=None,
            name=None,
            stdout=None,
            stderr=None,
            subcommands=None):

        self.config = config
        self.name = name or self.name
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

        # nb. default entry point is like 'wutta_poser.subcommands'
        safe_name = self.name.replace('-', '_')
        self.subcommands = subcommands or load_entry_points(f'{safe_name}.subcommands')
        if not self.subcommands:

            # nb. legacy entry point is like 'wutta_poser.commands'
            self.subcommands = load_entry_points(f'{safe_name}.commands')
            if self.subcommands:
                msg = (f"entry point group '{safe_name}.commands' uses deprecated name; "
                       f"please define '{safe_name}.subcommands' instead")
                warnings.warn(msg, DeprecationWarning, stacklevel=2)
                log.warning(msg)

    def __str__(self):
        return self.name

    def sorted_subcommands(self):
        """
        Get the list of subcommand classes, sorted by name.
        """
        return [self.subcommands[name]
                for name in sorted(self.subcommands)]

    def print_help(self):
        """
        Print usage help text for the main command.
        """
        self.parser.print_help()

    def run(self, *args):
        """
        Parse command line arguments and execute appropriate
        subcommand.

        Or, if requested, or args are ambiguous, show help for either
        the top-level or subcommand.

        Usually of course this method is invoked by way of command
        line.  But if you need to run it programmatically, you must
        specify the full command line args *except* not the top-level
        command name.  So for example to run the equivalent of this
        command line:

        .. code-block:: sh

           wutta setup --help

        You could do this in Python::

           from wuttjamaican.cmd import Command

           cmd = Command()
           assert cmd.name == 'wutta'
           cmd.run('setup', '--help')
        """
        # build arg parser
        self.parser = self.make_arg_parser()
        self.add_args()

        # primary parser gets first pass at full args, and stores
        # everything not used within args.argv
        args = self.parser.parse_args(args)
        if not args or not args.argv:
            self.print_help()
            sys.exit(1)

        # then argv should include <subcommand> [subcommand-options]
        subcmd = args.argv[0]
        if subcmd in self.subcommands:
            if '-h' in args.argv or '--help' in args.argv:
                subcmd = self.subcommands[subcmd](self)
                subcmd.print_help()
                sys.exit(0)
        else:
            self.print_help()
            sys.exit(1)

        # we should be done needing to print help messages. now it's
        # safe to redirect STDOUT/STDERR, if necessary
        if args.stdout:
            self.stdout = args.stdout
        if args.stderr:
            self.stderr = args.stderr

        # make the config object
        if not self.config:
            self.config = self.make_config(args)

        # invoke subcommand
        log.debug("running command line: %s", sys.argv)
        subcmd = self.subcommands[subcmd](self)
        self.prep_subcommand(subcmd, args)
        subcmd._run(*args.argv[1:])

        # nb. must flush these in case they are file objects
        self.stdout.flush()
        self.stderr.flush()

    def make_arg_parser(self):
        """
        Must return a new :class:`argparse.ArgumentParser` instance
        for use by the main command.

        This will use :class:`CommandArgumentParser` by default.
        """
        subcommands = ""
        for subcmd in self.sorted_subcommands():
            subcommands += f"  {subcmd.name:<20s}  {subcmd.description}\n"

        epilog = f"""\
subcommands:
{subcommands}

also try: {self.name} <subcommand> -h
"""

        return CommandArgumentParser(
            prog=self.name,
            description=self.description,
            add_help=False,
            usage=f"{self.name} [options] <subcommand> [subcommand-options]",
            epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)

    def add_args(self):
        """
        Configure args for the main command arg parser.

        Anything you setup here will then be available when the
        command runs.  You can add arguments directly to
        ``self.parser``, e.g.::

           self.parser.add_argument('--foo', default='bar', help="Foo value")

        See also docs for :meth:`python:argparse.ArgumentParser.add_argument()`.
        """
        parser = self.parser

        parser.add_argument('-c', '--config', metavar='PATH',
                            action='append', dest='config_paths',
                            help="Config path (may be specified more than once)")

        parser.add_argument('--plus-config', metavar='PATH',
                            action='append', dest='plus_config_paths',
                            help="Extra configs to load in addition to normal config")

        parser.add_argument('-P', '--progress', action='store_true', default=False,
                            help="Report progress when relevant")

        parser.add_argument('-V', '--version', action='version',
                            version=f"%(prog)s {self.version}")

        parser.add_argument('--stdout', metavar='PATH', type=argparse.FileType('w'),
                            help="Optional path to which STDOUT should be written")
        parser.add_argument('--stderr', metavar='PATH', type=argparse.FileType('w'),
                            help="Optional path to which STDERR should be written")

    def make_config(self, args):
        """
        Make the config object in preparation for running a subcommand.

        By default this is a straightforward wrapper around
        :func:`wuttjamaican.conf.make_config()`.

        :returns: The new config object.
        """
        return make_config(args.config_paths,
                           plus_files=args.plus_config_paths)

    def prep_subcommand(self, subcommand, args):
        """
        Prepare the subcommand for running, as needed.
        """


class CommandArgumentParser(argparse.ArgumentParser):
    """
    Custom argument parser for use with :class:`Command`.

    This is based on standard :class:`python:argparse.ArgumentParser`
    but overrides some of the parsing logic which is specific to the
    primary command object, to separate command options from
    subcommand options.

    This is documented as FYI but you probably should not need to know
    about or try to use this yourself.  It will be used automatically
    by :class:`Command` or a subclass thereof.
    """

    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        args.argv = argv
        return args


class Subcommand:
    """
    Base class for application subcommands.

    Subcommands are where the real action happens.  Each must define
    the :meth:`run()` method with whatever logic is needed.  They can
    also define :meth:`add_args()` to expose options.

    Subcommands always belong to a top-level command - the association
    is made by way of :term:`entry point` registration, and the
    constructor for this class.

    :param command: Reference to top-level :class:`Command` object.

    Note that unlike :class:`Command`, the base ``Subcommand`` does
    not correspond to any real subcommand for WuttJamaican.  (It's
    *only* a base class.)  For a real example see
    :class:`~wuttjamaican.cmd.make_appdir.MakeAppDir`.

    For more info see :doc:`/narr/cli/subcommands`.

    .. attribute:: stdout

       Reference to file-like object which should be used for writing
       to STDOUT.  This is inherited from :attr:`Command.stdout`.

    .. attribute:: stderr

       Reference to file-like object which should be used for writing
       to STDERR.  This is inherited from :attr:`Command.stderr`.
    """
    name = 'UNDEFINED'
    description = "TODO: not defined"

    def __init__(
            self,
            command,
    ):
        self.command = command
        self.stdout = self.command.stdout
        self.stderr = self.command.stderr
        self.config = self.command.config
        if self.config:
            self.app = self.config.get_app()

        # build arg parser
        self.parser = self.make_arg_parser()
        self.add_args()

    def __repr__(self):
        return f"Subcommand(name={self.name})"

    def make_arg_parser(self):
        """
        Must return a new :class:`argparse.ArgumentParser` instance
        for use by the subcommand.
        """
        return argparse.ArgumentParser(
            prog=f'{self.command.name} {self.name}',
            description=self.description)

    def add_args(self):
        """
        Configure additional args for the subcommand arg parser.

        Anything you setup here will then be available within
        :meth:`run()`.  You can add arguments directly to
        ``self.parser``, e.g.::

           self.parser.add_argument('--foo', default='bar', help="Foo value")

        See also docs for :meth:`python:argparse.ArgumentParser.add_argument()`.
        """

    def print_help(self):
        """
        Print usage help text for the subcommand.
        """
        self.parser.print_help()

    def _run(self, *args):
        args = self.parser.parse_args(args)
        return self.run(args)

    def run(self, args):
        """
        Run the subcommand logic.  Subclass should override this.

        :param args: Reference to the
           :class:`python:argparse.Namespace` object, as returned by
           the subcommand arg parser.

        The ``args`` should have values for everything setup in
        :meth:`add_args()`.  For example if you added the ``--foo``
        arg then here in ``run()`` you can do::

           print("foo value is:", args.foo)

        Usually of course this method is invoked by way of command
        line. But if you need to run it programmatically, you should
        *not* try to invoke this method directly.  Instead create the
        ``Command`` object and invoke its :meth:`~Command.run()`
        method.

        For a command line like ``bin/poser hello --foo=baz`` then,
        you might do this::

           from poser.commands import PoserCommand

           cmd = PoserCommand()
           assert cmd.name == 'poser'
           cmd.run('hello', '--foo=baz')
        """
        self.stdout.write("TODO: command logic not yet implemented\n")


def main(*args):
    """
    Primary entry point for the ``wutta`` command.
    """
    args = list(args) or sys.argv[1:]

    cmd = Command()
    cmd.run(*args)
