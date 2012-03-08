# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import unittest
import os
from memacs.sms import SmsMemacs


class TestGitMemacs(unittest.TestCase):

    def setUp(self):
        test_file = os.path.dirname(os.path.abspath(__file__)) + \
            os.sep + "tmp" + os.sep + "smsxml.txt"
        argv = "-s -f " + test_file
        memacs = SmsMemacs(argv=argv.split())
        self.data = memacs.test_get_entries()

    def test_from_file(self):
        data = self.data

        # generate assertEquals :)
#        for d in range(len(data)):
#            print "self.assertEqual(\n\tdata[%d],\n\t \"%s\")" % \
#               (d, data[d])

        self.assertEqual(
            data[0],
             "** <2011-08-04 Thu 10:05:53> SMS from +436812314" + \
             "123: did you see the new sms memacs module?")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :ID:         da39a3ee5e6b4b0d3255bfef95601890afd80709")
        self.assertEqual(
            data[3],
             "   :END:")
        self.assertEqual(
            data[4],
             "** <2011-08-04 Thu 16:04:55> SMS to +43612341234: Memacs FTW!")
        self.assertEqual(
            data[5],
             "   :PROPERTIES:")
        self.assertEqual(
            data[6],
             "   :ID:         da39a3ee5e6b4b0d3255bfef95601890afd80709")
        self.assertEqual(
            data[7],
             "   :END:")
        self.assertEqual(
            data[8],
             "** <2011-08-04 Thu 20:25:50> SMS to +43612341238: i like memacs")
        self.assertEqual(
            data[9],
             "   :PROPERTIES:")
        self.assertEqual(
            data[10],
             "   :ID:         da39a3ee5e6b4b0d3255bfef95601890afd80709")
        self.assertEqual(
            data[11],
             "   :END:")
        self.assertEqual(
            data[12],
             "** <2011-08-05 Fri 18:32:01> SMS to +4312341" + \
             "234: http://google.at")
        self.assertEqual(
            data[13],
             "   :PROPERTIES:")
        self.assertEqual(
            data[14],
             "   :ID:         da39a3ee5e6b4b0d3255bfef95601890afd80709")
        self.assertEqual(
            data[15],
             "   :END:")
