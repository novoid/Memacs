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
             "** group-5 (r5): finished ?")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :CREATED: <2011-10-27 Thu 19:50:16>")
        self.assertEqual(
            data[3],
             "   :END:")
        self.assertEqual(
            data[4],
             "** group-5 (r4): finished 5,")
        self.assertEqual(
            data[5],
             "   added package to assignment1.tex for landscaping (see 5.tex)")
        self.assertEqual(
            data[6],
             "   :PROPERTIES:")
        self.assertEqual(
            data[7],
             "   :CREATED: <2011-10-27 Thu 19:18:26>")
        self.assertEqual(
            data[8],
             "   :END:")
        self.assertEqual(
            data[9],
             "** group-5 (r3): 5b.")
        self.assertEqual(
            data[10],
             "   :PROPERTIES:")
        self.assertEqual(
            data[11],
             "   :CREATED: <2011-10-27 Thu 17:38:17>")
        self.assertEqual(
            data[12],
             "   :END:")
        self.assertEqual(
            data[13],
             "** group-5 (r2): 5.tex")
        self.assertEqual(
            data[14],
             "   :PROPERTIES:")
        self.assertEqual(
            data[15],
             "   :CREATED: <2011-10-27 Thu 16:41:11>")
        self.assertEqual(
            data[16],
             "   :END:")
        self.assertEqual(
            data[17],
             "** group-5 (r1): initial files")
        self.assertEqual(
            data[18],
             "   :PROPERTIES:")
        self.assertEqual(
            data[19],
             "   :CREATED: <2011-10-27 Thu 10:44:55>")
        self.assertEqual(
            data[20],
             "   :END:")
