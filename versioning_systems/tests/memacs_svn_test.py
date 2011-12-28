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
             "   :REVISION:       5")
        self.assertEqual(
            data[3],
             "   :CREATED:        <2011-10-27 Thu 19:50:16>")
#        self.assertEqual(
#            data[4],
#             "   :MEMACS_CREATED: [2011-12-28 Wed 18:48:46]")
        self.assertEqual(
            data[5],
             "   :ID:             989b15f2695fbd240808fc8370a3364550a14f22")
        self.assertEqual(
            data[6],
             "   :END:")
        self.assertEqual(
            data[7],
             "** group-5 (r4): finished 5,")
        self.assertEqual(
            data[8],
             "   added package to assignment1.tex for landscaping (see 5.tex)")
        self.assertEqual(
            data[9],
             "   :PROPERTIES:")
        self.assertEqual(
            data[10],
             "   :REVISION:       4")
        self.assertEqual(
            data[11],
             "   :CREATED:        <2011-10-27 Thu 19:18:26>")
#        self.assertEqual(
#            data[12],
#             "   :MEMACS_CREATED: [2011-12-28 Wed 18:48:46]")
        self.assertEqual(
            data[13],
             "   :ID:             8c5472fdb0ba0d1398a64e60e3c3ea8abb915c04")
        self.assertEqual(
            data[14],
             "   :END:")
        self.assertEqual(
            data[15],
             "** group-5 (r3): 5b.")
        self.assertEqual(
            data[16],
             "   :PROPERTIES:")
        self.assertEqual(
            data[17],
             "   :REVISION:       3")
        self.assertEqual(
            data[18],
             "   :CREATED:        <2011-10-27 Thu 17:38:17>")
#        self.assertEqual(
#            data[19],
#             "   :MEMACS_CREATED: [2011-12-28 Wed 18:48:46]")
        self.assertEqual(
            data[20],
             "   :ID:             e584d18d63faee15e63022c8caaf12e84ab456fb")
        self.assertEqual(
            data[21],
             "   :END:")
        self.assertEqual(
            data[22],
             "** group-5 (r2): 5.tex")
        self.assertEqual(
            data[23],
             "   :PROPERTIES:")
        self.assertEqual(
            data[24],
             "   :REVISION:       2")
        self.assertEqual(
            data[25],
             "   :CREATED:        <2011-10-27 Thu 16:41:11>")
#        self.assertEqual(
#            data[26],
#             "   :MEMACS_CREATED: [2011-12-28 Wed 18:48:46]")
        self.assertEqual(
            data[27],
             "   :ID:             cc1be5e3314f3c078a69a5100f08b5d6e91087b5")
        self.assertEqual(
            data[28],
             "   :END:")
        self.assertEqual(
            data[29],
             "** group-5 (r1): initial files")
        self.assertEqual(
            data[30],
             "   :PROPERTIES:")
        self.assertEqual(
            data[31],
             "   :REVISION:       1")
        self.assertEqual(
            data[32],
             "   :CREATED:        <2011-10-27 Thu 10:44:55>")
#        self.assertEqual(
#            data[33],
#             "   :MEMACS_CREATED: [2011-12-28 Wed 18:48:46]")
        self.assertEqual(
            data[34],
             "   :ID:             c8ac88f77a645a7e7e1a78d772e89cd0ed731184")
        self.assertEqual(
            data[35],
             "   :END:")       