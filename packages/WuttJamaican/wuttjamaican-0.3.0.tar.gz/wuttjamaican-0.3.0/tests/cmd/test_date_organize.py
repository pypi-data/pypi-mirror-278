# -*- coding: utf-8; -*-

import datetime
import os

from wuttjamaican.conf import WuttaConfig
from wuttjamaican.cmd import Command, date_organize
from wuttjamaican.testing import FileConfigTestCase


class TestDateOrganize(FileConfigTestCase):

    def test_run(self):
        dates = [
            datetime.date(2023, 11, 21),
            datetime.date(2023, 11, 20),
            datetime.date(2023, 10, 15),
            datetime.date(2023, 9, 10),
        ]

        for date in dates:
            dt = datetime.datetime.combine(date, datetime.time(0))
            filename = date.strftime('%Y%m%d.txt')
            path = self.write_file(filename, '')
            os.utime(path, (dt.timestamp(), dt.timestamp()))

        cmd = Command(subcommands={
            'date-organize': date_organize.DateOrganize,
        })
        cmd.run('date-organize', self.tempdir)

        self.assertEqual(os.listdir(self.tempdir), ['2023'])
        self.assertEqual(sorted(os.listdir(os.path.join(self.tempdir, '2023'))),
                         ['09', '10', '11'])
