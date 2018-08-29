# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import unittest
import os
from memacs.csv import Csv

class TestCsv(unittest.TestCase):

    def test_example1(self):
        example1 = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data', 'example1.csv'
        )

        argv = []
        argv.append("-f")
        argv.append(example1)
        argv.append("--fieldnames")
        argv.append("date,text,value,currency,")
        argv.append("--timestamp-field")
        argv.append("date")
        argv.append("--timestamp-format")
        argv.append("%d.%m.%Y")
        argv.append("--output-format")
        argv.append("{text}")
        argv.append("--properties")
        argv.append("currency,value")

        memacs = Csv(argv=argv)
        data = memacs.test_get_entries()

        self.assertEqual(data[0], "** <2012-02-23 Thu> Amazon")
        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[2], "   :CURRENCY:   EUR")
        self.assertEqual(data[3], "   :VALUE:      100,00")
        self.assertEqual(data[4], "   :ID:         a9cfa86bd9d89b72f35bfca0bb75131be0ca86b1")
        self.assertEqual(data[5], "   :END:")

    def test_example2(self):
        example1 = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data', 'example2.csv'
        )

        argv = []
        argv.append("--delimiter")
        argv.append("|")
        argv.append("-f")
        argv.append(example1)
        argv.append("--timestamp-field")
        argv.append("date")
        argv.append("--output-format")
        argv.append("{text}")

        memacs = Csv(argv=argv)
        data = memacs.test_get_entries()

        self.assertEqual(data[0], "** <2012-02-23 Thu 14:40> Alibaba")
        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[2], "   :ID:         b1a598a360d4766cf94822cdcd96629f0b3936ef")
        self.assertEqual(data[3], "   :END:")
