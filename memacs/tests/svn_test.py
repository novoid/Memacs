# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import unittest
import os
from memacs.svn import SvnMemacs


class TestGitMemacs(unittest.TestCase):

    def setUp(self):
        test_file = os.path.dirname(os.path.abspath(__file__)) + \
            os.sep + "tmp" + os.sep + "svn-log-xml.txt"
        argv = "-s -f " + test_file
        memacs = SvnMemacs(argv=argv.split())
        self.data = memacs.test_get_entries()

    def test_from_file(self):
        data = self.data

        # generate assertEquals :)
        #for d in range(len(data)):
        #    print "self.assertEqual(\n\tdata[%d],\n\t \"%s\")" % \
        #       (d, data[d])

        self.assertEqual(
            data[0],
             "** <2011-10-27 Thu 17:50:16> group-5 (r5): finished ?")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :REVISION:   5")
        self.assertEqual(
            data[3],
             "   :ID:         819908c0cedb0098bf5dd96aa0d213598da45614")
        self.assertEqual(
            data[4],
             "   :END:")
        self.assertEqual(
            data[5],
             "** <2011-10-27 Thu 17:18:26> group-5 (r4): finished 5,")
        self.assertEqual(
            data[6],
             "   added package to assignment1.tex for landscaping (see 5.tex)")
        self.assertEqual(
            data[7],
             "   :PROPERTIES:")
        self.assertEqual(
            data[8],
             "   :REVISION:   4")
        self.assertEqual(
            data[9],
             "   :ID:         629716ff44b206745fdc34c910fe8b0f3d877f85")
        self.assertEqual(
            data[10],
             "   :END:")
        self.assertEqual(
            data[11],
             "** <2011-10-27 Thu 15:38:17> group-5 (r3): 5b.")
        self.assertEqual(
            data[12],
             "   :PROPERTIES:")
        self.assertEqual(
            data[13],
             "   :REVISION:   3")
        self.assertEqual(
            data[14],
             "   :ID:         cf204bc9b36ba085275e03b7316ac34a496daf78")
        self.assertEqual(
            data[15],
             "   :END:")
        self.assertEqual(
            data[16],
             "** <2011-10-27 Thu 14:41:11> group-5 (r2): 5.tex")
        self.assertEqual(
            data[17],
             "   :PROPERTIES:")
        self.assertEqual(
            data[18],
             "   :REVISION:   2")
        self.assertEqual(
            data[19],
             "   :ID:         f45be418de175ccf56e960a6941c9973094ab9e3")
        self.assertEqual(
            data[20],
             "   :END:")
        self.assertEqual(
            data[21],
             "** <2011-10-27 Thu 08:44:55> group-5 (r1): initial files")
        self.assertEqual(
            data[22],
             "   :PROPERTIES:")
        self.assertEqual(
            data[23],
             "   :REVISION:   1")
        self.assertEqual(
            data[24],
             "   :ID:         9b7d570e2dc4fb3a009461714358c35cbe24a8fd")
        self.assertEqual(
            data[25],
             "   :END:")
