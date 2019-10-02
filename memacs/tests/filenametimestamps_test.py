#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-10-03 00:33:36 vk>

import os
import shutil
import tempfile
import unittest

from memacs.filenametimestamps import FileNameTimeStamps


class TestFileNameTimeStamps(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def touch_file(self, basename):
        """
        Creates a test file and returns the Org mode link to it
        """
        tmpfile = os.path.join(self._tmp_dir, basename)
        with open(tmpfile, 'w'):
            pass
        return '[[file:' + tmpfile + '][' + basename + ']]'

    def call_basic(self):
        """
        Invokes the filenametimestamp module with basic parameters
        """
        argv = "--suppress-messages --folder " + self._tmp_dir
        memacs = FileNameTimeStamps(argv=argv.split())
        return memacs.test_get_entries()

    def test_functional(self):
        link = self.touch_file('2011-12-19T23.59.12_test1.txt')
        entry = "** <2011-12-19 Mon 23:59> " + link
        data = self.call_basic()

        self.assertEqual(data[0], entry)
        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[3], "   :END:")

    def test_functional_with_unusual_year(self):
        link = self.touch_file('1971-12-30T00.01.01_P1000286.jpg')
        entry = "** <1971-12-30 Thu 00:01> " + link
        data = self.call_basic()

        self.assertEqual(data[0], entry)
        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[3], "   :END:")

    def test_year_out_of_range(self):
        link = self.touch_file('1899-12-30T00.00.00_P1000286.jpg')
        entry = "** " + link
        data = self.call_basic()

        self.assertEqual(data[0], entry)
        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[3], "   :END:")
