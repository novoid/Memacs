# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-09 15:39:33 armin>

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
            "   :ID:         5d4b551b7804f763ab2a62d287628aedee3e17a4")
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
            "   :ID:         8a377f25d80b1c137fcf6f28835d234141dfe179")
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
            "   :ID:         556373e703194e9919489f3497b485b63b9e6978")
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
            "   :ID:         6cc7b095acf4b4ac7d647821541ad4b3c611d56e")
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
            "   :ID:         8865ef73de0bb1dc9d9de0b362f885defda9ada1")
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
            "   :ID:         8561807f509b66f3a8dd639b19776a2a06e0463e")
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
            "   :ID:         1f1ebb7853e28d66d6908f72a454cec378011605")
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
            "   :ID:         9558d013e3522e5bcbb02cb6599182ca0802547d")
        self.assertEqual(
            data[31],
             "   :END:")
