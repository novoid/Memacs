# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import unittest
import os
from memacs.csv import Csv


class TestCsv(unittest.TestCase):

    def test_example1(self):
        example1 = os.path.dirname(os.path.abspath(__file__)) + \
        os.sep + "tmp" + os.sep + "example1.csv"

        argv = []
        argv.append("-f")
        argv.append(example1)
        argv.append("-ti")
        argv.append("5")
        argv.append("-tf")
        argv.append("%d.%m.%Y %H:%M:%S:%f")
        argv.append("-oi")
        argv.append("4 3 1")
        memacs = Csv(argv=argv)
        data = memacs.test_get_entries()

        self.assertEqual(
            data[0],
            "** <2012-02-23 Thu 14:40> EUR 100,00 Amazon")
        self.assertEqual(
            data[1],
            "   :PROPERTIES:")
        self.assertEqual(
            data[2],
            "   :ID:         5526fcec678ca1dea255b60177e5daaa737d3805")
        self.assertEqual(
            data[3],
            "   :END:")

    def test_example2_delimiter(self):
        example1 = os.path.dirname(os.path.abspath(__file__)) + \
        os.sep + "tmp" + os.sep + "example2.csv"

        argv = []
        argv.append("--delimiter")
        argv.append("|")
        argv.append("-f")
        argv.append(example1)
        argv.append("-ti")
        argv.append("5")
        argv.append("-tf")
        argv.append("%d.%m.%Y %H:%M:%S:%f")
        argv.append("-oi")
        argv.append("4 3 1")
        memacs = Csv(argv=argv)
        data = memacs.test_get_entries()

        self.assertEqual(
            data[0],
            "** <2012-02-23 Thu 14:40> EUR 100,00 Amazon")
        self.assertEqual(
            data[1],
            "   :PROPERTIES:")
        self.assertEqual(
            data[2],
            "   :ID:         5526fcec678ca1dea255b60177e5daaa737d3805")
        self.assertEqual(
            data[3],
            "   :END:")
