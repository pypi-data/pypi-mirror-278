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
WuttJamaican - subcommand ``date-organize``
"""

import os
import shutil
import datetime

from .base import Subcommand


class DateOrganize(Subcommand):
    """
    Organize files into subfolders according to date
    """
    name = 'date-organize'
    description = __doc__.strip()

    def add_args(self):
        """ """
        self.parser.add_argument('folder', metavar='PATH',
                                 help="Path to directory containing files which are "
                                 "to be organized by date.")

    def run(self, args):
        """ """
        today = datetime.date.today()
        for filename in sorted(os.listdir(args.folder)):
            path = os.path.join(args.folder, filename)
            if os.path.isfile(path):
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
                if mtime.date() < today:
                    datedir = mtime.strftime(os.sep.join(('%Y', '%m', '%d')))
                    datedir = os.path.join(args.folder, datedir)
                    if not os.path.exists(datedir):
                        os.makedirs(datedir)
                    shutil.move(path, datedir)
