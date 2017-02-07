# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31>

import os
import time
import unittest
from memacs.arbtt import Arbtt


class TestArbtt(unittest.TestCase):

    def setUp(self):
        self.memacs = Arbtt()

        self.sample = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data', 'sample-arbtt.csv'
        )

    def test_get_sec(self):
        self.assertEqual(self.memacs.get_sec('00:15:00'), 900)

    def test_get_timestamp(self):
        # assuming utc+1 w/o dst :)
        self.assertEqual(
            self.memacs.get_timestamp('02/05/17 19:00:00'),
            '<2017-02-05 Sun 20:00:00>'
        )

    def test_get_timerange(self):
        # assuming utc+1 w/o dst :)
        self.assertEqual(
            self.memacs.get_timerange('02/05/17 19:00:00', '02/05/17 19:15:00'),
            '<2017-02-05 Sun 20:00:00>--<2017-02-05 Sun 20:15:00>'
        )

    def test_functional(self):

        argv = []
        argv.append('-s')
        argv.append('--intervals=web')
        # argv.append('--logfile=%s' % self.log)
        # argv.append('--categorizefile=%s' % self.cfg)
        argv.append('--csv=%s' % self.sample)

        memacs = Arbtt(argv=argv)
        data = memacs.test_get_entries()

        entry = '** <2017-02-05 Sun 20:00:00>--<2017-02-05 Sun 20:15:00> Web\t:web:'

        self.assertEqual(data[0], entry)
        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[2], "   :DURATION:   900")
        self.assertEqual(data[4], "   :END:")

