#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-19 15:13:31 aw>

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

    def test_functional(self):
        # touch file
        tmpfile = os.path.join(self._tmp_dir, '2011-12-19T23.59.12_test1.txt')
        with open(tmpfile, 'w'):
            pass

        entry = "** <2011-12-19 Mon 23:59> [[" + tmpfile + \
            "][2011-12-19T23.59.12_test1.txt]]"

        argv = "-s -f " + self._tmp_dir
        memacs = FileNameTimeStamps(argv=argv.split())
        data = memacs.test_get_entries()

        self.assertEqual(data[0], entry)
        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[3], "   :END:")
