#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-19 15:13:31 aw>

import unittest
import os
from memacs.filenametimestamps import FileNameTimeStamps


class TestFileNameTimeStamps(unittest.TestCase):

    def setUp(self):
        self.TMPFOLDER = os.path.normpath(
            os.path.dirname(os.path.abspath(__file__)) + os.path.sep + \
                "tmp") + os.path.sep
        if not os.path.exists(self.TMPFOLDER):
            os.makedirs(self.TMPFOLDER)

    def test_functional(self):
        tmpfile = self.TMPFOLDER + os.sep + '2011-12-19T23.59.12_test1.txt'
        entry = "** <2011-12-19 Mon 23:59:12> [[" + tmpfile + \
            "][2011-12-19T23.59.12_test1.txt]]"

        # touch file
        open(tmpfile, 'w').close()

        argv = "-s -f " + self.TMPFOLDER
        memacs = FileNameTimeStamps(argv=argv.split())
        data = memacs.test_get_entries()

        #for d in range(len(data)):
        #    print "self.assertEqual(\n\tdata[%d],\n\t\"%s\")" % \
        #        (d, data[d])

        self.assertEqual(
            data[0],
            entry)
        self.assertEqual(
            data[1],
            "   :PROPERTIES:")
        # id changes because data_for_hashing = link
        #self.assertEqual(
        #    data[2],
        #    "   :ID:             e3b38e22498caa8812c755ec20276714a1eb1919")
        self.assertEqual(
            data[3],
            "   :END:")

        os.remove(tmpfile)
        self.assertEqual(data[0], entry, "filenametimestamps - error")
