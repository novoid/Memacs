# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-09 15:36:52 armin>

import unittest
import os
from memacs.sms import SmsMemacs


class TestSmsMemacs(unittest.TestCase):

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
            "   :ID:         9a7774b7a546119af169625366350ca6cf1675f8")
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
            "   :ID:         2163c59e66a84c391a1a00014801a2cb760b0125")
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
            "   :ID:         409d27ce4e9d08cce0acdea49b63b6d26b0b77c3")
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
            "   :ID:         4986730775a023fa0f268127f6ead9b8180337f0")
        self.assertEqual(
            data[15],
             "   :END:")
