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
WuttJamaican - subcommand ``make-appdir``
"""

import os
import sys

from .base import Subcommand


class MakeAppDir(Subcommand):
    """
    Make or refresh the "app dir" for virtual environment
    """
    name = 'make-appdir'
    description = __doc__.strip()

    def add_args(self):
        """ """
        self.parser.add_argument('--path', metavar='APPDIR',
                                 help="Optional path to desired app dir.  If not specified "
                                 "it will be named ``app`` and  placed in the root of the "
                                 "virtual environment.")

    def run(self, args):
        """
        This may be used during setup to establish the :term:`app dir`
        for a virtual environment.  This folder will contain config
        files, log files etc. used by the app.
        """
        if args.path:
            appdir = os.path.abspath(args.path)
        else:
            appdir = os.path.join(sys.prefix, 'app')

        self.make_appdir(appdir, args)
        self.stdout.write(f"established appdir: {appdir}\n")

    def make_appdir(self, appdir, args):
        """
        Make the :term:`app dir` for the given path.

        Calls :meth:`~wuttjamaican.app.AppHandler.make_appdir()` to do
        the heavy lifting.
        """
        self.app.make_appdir(appdir)
