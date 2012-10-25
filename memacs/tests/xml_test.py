# -*- coding: utf-8 -*-
# Time-stamp: <2012-05-14 15:13:31 df>

import unittest
import os
from memacs.xmlsource import XmlMemacs


class TestXml(unittest.TestCase):

    def setUp(self):
        pass

    def test_from_file(self):
        test_file = os.path.dirname(
            os.path.abspath(__file__)) + os.sep + "tmp" \
            + os.sep + "samplexml.txt"

        test_ini = os.path.dirname(
            os.path.abspath(__file__)) + os.sep + "tmp" \
            + os.sep + "test.ini"

        argv = []
        argv.append("-f")
        argv.append(test_file)
        argv.append("-i")
        argv.append(test_ini)
        argv.append("-co")
        argv.append("0")
        memacs = XmlMemacs(argv=argv)
        data = memacs.test_get_entries()

        self.assertEqual(
            data[0],
            "** <2006-08-28 Mon 11:12:55> Example1: \t:tag1:tag2:tag3:")
        self.assertEqual(
            data[1],
            "   [[http://www.any.org/link.htm][link]]: http://www.any.org/link.htm")
        self.assertEqual(
            data[2],
            "   :PROPERTIES:")
        self.assertEqual(
            data[3],
            "   :ID:         9d0f38a71bdc3482efc4d33666082ff2b0b5ac02")
        self.assertEqual(
            data[4],
            "   :END:")

    def test_example2_delimiter(self):
        test_file = os.path.dirname(
            os.path.abspath(__file__)) + os.sep + "tmp" \
            + os.sep + "samplexml2.txt"

        test_ini = os.path.dirname(
            os.path.abspath(__file__)) + os.sep + "tmp" \
            + os.sep + "test.ini"

        argv = []
        argv.append("-f")
        argv.append(test_file)
        argv.append("-i")
        argv.append(test_ini)
        argv.append("-co")
        argv.append("1")
        argv.append("-de")
        argv.append(",")
        memacs = XmlMemacs(argv=argv)
        data = memacs.test_get_entries()

        self.assertEqual(
            data[0],
            "** <2011-01-01 Sat 00:00> Example1: \t:taga:tagb:tagc:")
        self.assertEqual(
            data[1],
            "   [[http://www.any.org/link.htm][link]]: http://www.any.org/link.htm")
        self.assertEqual(
            data[2],
            "   :PROPERTIES:")
        self.assertEqual(
            data[3],
            "   :ID:         e44364e7d7880a3d3315f1ba4adddd7f7201eb34")
        self.assertEqual(
            data[4],
            "   :END:")

        def tearDown(self):
            pass
