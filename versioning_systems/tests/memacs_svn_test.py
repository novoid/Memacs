# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import unittest
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))
from versioning_systems.memacs_svn import SvnMemacs


class TestGitMemacs(unittest.TestCase):

    def setUp(self):
        test_file = os.path.dirname(os.path.abspath(__file__)) + \
            os.sep + "svn-log-xml.txt"
        argv = "-s -f " + test_file
        memacs = SvnMemacs(argv=argv.split(), append=True)
        self.data = memacs.test_get_entries()

    def test_from_file(self):
        data = self.data

        # generate assertEquals :)
        for d in range(len(data)):
            print "self.assertEqual(\n\tdata[%d],\n\t \"%s\")" % \
               (d, data[d])

        self.assertEqual(
            data[0],
             "** group-5 (r5): finished ?")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :REVISION: 5")
        self.assertEqual(
            data[3],
             "   :CREATED:  <2011-10-27 Thu 19:50:16>")
        self.assertEqual(
            data[4],
             "   :ID:       989b15f2695fbd240808fc8370a3364550a14f22")
        self.assertEqual(
            data[5],
             "   :END:")
        self.assertEqual(
            data[6],
             "** group-5 (r4): finished 5,")
        self.assertEqual(
            data[7],
             "   added package to assignment1.tex for landscaping (see 5.tex)")
        self.assertEqual(
            data[8],
             "   :PROPERTIES:")
        self.assertEqual(
            data[9],
             "   :REVISION: 4")
        self.assertEqual(
            data[10],
             "   :CREATED:  <2011-10-27 Thu 19:18:26>")
        self.assertEqual(
            data[11],
             "   :ID:       8c5472fdb0ba0d1398a64e60e3c3ea8abb915c04")
        self.assertEqual(
            data[12],
             "   :END:")
        self.assertEqual(
            data[13],
             "** group-5 (r3): 5b.")
        self.assertEqual(
            data[14],
             "   :PROPERTIES:")
        self.assertEqual(
            data[15],
             "   :REVISION: 3")
        self.assertEqual(
            data[16],
             "   :CREATED:  <2011-10-27 Thu 17:38:17>")
        self.assertEqual(
            data[17],
             "   :ID:       e584d18d63faee15e63022c8caaf12e84ab456fb")
        self.assertEqual(
            data[18],
             "   :END:")
        self.assertEqual(
            data[19],
             "** group-5 (r2): 5.tex")
        self.assertEqual(
            data[20],
             "   :PROPERTIES:")
        self.assertEqual(
            data[21],
             "   :REVISION: 2")
        self.assertEqual(
            data[22],
             "   :CREATED:  <2011-10-27 Thu 16:41:11>")
        self.assertEqual(
            data[23],
             "   :ID:       cc1be5e3314f3c078a69a5100f08b5d6e91087b5")
        self.assertEqual(
            data[24],
             "   :END:")
        self.assertEqual(
            data[25],
             "** group-5 (r1): initial files")
        self.assertEqual(
            data[26],
             "   :PROPERTIES:")
        self.assertEqual(
            data[27],
             "   :REVISION: 1")
        self.assertEqual(
            data[28],
             "   :CREATED:  <2011-10-27 Thu 10:44:55>")
        self.assertEqual(
            data[29],
             "   :ID:       c8ac88f77a645a7e7e1a78d772e89cd0ed731184")
        self.assertEqual(
            data[30],
             "   :END:")
