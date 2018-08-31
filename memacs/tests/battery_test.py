# -*- coding: utf-8 -*-

import unittest
import os

from memacs.battery import Battery


class TestCsv(unittest.TestCase):

    def test_battery(self):

        path = os.path.dirname(os.path.abspath(__file__))

        argv = []
        argv.append("-p")
        argv.append(os.path.join(path, "data"))

        memacs = Battery(argv=argv)
        data = memacs.test_get_entries()

        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[2], "   :CYCLE_COUNT: 866")
        self.assertEqual(data[3], "   :CAPACITY:    97%")
        self.assertEqual(data[4], "   :STATUS:      discharging")
        self.assertEqual(data[5], "   :CONSUMPTION: 11.9 W")
        self.assertEqual(data[7], "   :END:")
