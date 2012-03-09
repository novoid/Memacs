# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import unittest
import os
from memacs.phonecalls import PhonecallsMemacs


class TestPhonecallsMemacs(unittest.TestCase):

    def setUp(self):
        test_file = os.path.dirname(os.path.abspath(__file__)) + \
            os.sep + "tmp" + os.sep + "phonecallsxml.txt"
        argv = "-s -f " + test_file
        memacs = PhonecallsMemacs(argv=argv.split())
        self.data = memacs.test_get_entries()

    def test_from_file(self):
        data = self.data

        # generate assertEquals :)
#        for d in range(len(data)):
#            print "self.assertEqual(\n\tdata[%d],\n\t \"%s\")" % \
#               (d, data[d])

        self.assertEqual(
            data[0],
             "** <2011-08-05 Fri 17:05:06> Phonecall from +43691234123" + \
             " Duration: 59 sec")
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
             "** <2011-08-05 Fri 10:46:55> Phonecall to 06612341234 " + \
             "Duration: 22 sec")
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
             "** <2011-08-05 Fri 07:51:31> Phonecall from Unknown Number " + \
             "Duration: 382 sec")
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
             "** <2011-08-04 Thu 18:25:27> Phonecall from +4312341234 " + \
             "Duration: 289 sec")
        self.assertEqual(
            data[13],
             "   :PROPERTIES:")
        self.assertEqual(
            data[14],
             "   :ID:         da39a3ee5e6b4b0d3255bfef95601890afd80709")
        self.assertEqual(
            data[15],
             "   :END:")
        self.assertEqual(
            data[16],
             "** <2011-08-04 Thu 16:45:34> Phonecall from +4366412341234" + \
             " Duration: 70 sec")
        self.assertEqual(
            data[17],
             "   :PROPERTIES:")
        self.assertEqual(
            data[18],
             "   :ID:         da39a3ee5e6b4b0d3255bfef95601890afd80709")
        self.assertEqual(
            data[19],
             "   :END:")
        self.assertEqual(
            data[20],
             "** <2011-08-04 Thu 16:02:31> Phonecall to +4366234123" + \
             " Duration: 0 sec")
        self.assertEqual(
            data[21],
             "   :PROPERTIES:")
        self.assertEqual(
            data[22],
             "   :ID:         da39a3ee5e6b4b0d3255bfef95601890afd80709")
        self.assertEqual(
            data[23],
             "   :END:")
        self.assertEqual(
            data[24],
             "** <2011-08-04 Thu 15:21:40> Phonecall missed +436612341234" + \
             " Duration: 0 sec")
        self.assertEqual(
            data[25],
             "   :PROPERTIES:")
        self.assertEqual(
            data[26],
             "   :ID:         da39a3ee5e6b4b0d3255bfef95601890afd80709")
        self.assertEqual(
            data[27],
             "   :END:")
        self.assertEqual(
            data[28],
             "** <2011-08-04 Thu 14:36:02> Phonecall to +433123412" + \
             " Duration: 60 sec")
        self.assertEqual(
            data[29],
             "   :PROPERTIES:")
        self.assertEqual(
            data[30],
             "   :ID:         da39a3ee5e6b4b0d3255bfef95601890afd80709")
        self.assertEqual(
            data[31],
             "   :END:")
