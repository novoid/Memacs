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
from rss.memacs_rss import RssMemacs


class TestRss(unittest.TestCase):

    def setUp(self):
        self.test_file = test_file = os.path.dirname(
            os.path.abspath(__file__)) + os.path.sep + "sample-rss.txt"
        self.argv = "-s -f " + self.test_file

    def test_false_appending(self):
        try:
            memacs = RssMemacs(argv=self.argv.split())
            data = memacs.test_get_entries()
        except Exception, e:
            pass

    def test_all(self):
        memacs = RssMemacs(argv=self.argv.split(), append=True)
        data = memacs.test_get_entries()

        # generate assertEquals :)
        #for d in range(len(data)):
        #    print "self.assertEqual(\n\tdata[%d],\n\t\"%s\")" % \
        #        (d, data[d])
        self.assertEqual(
            data[0],
            "** [[http://www.wikipedia.org/][Example entry]]")
        self.assertEqual(
            data[1],
            "   Here is some text containing an interesting description.")
        self.assertEqual(
            data[2],
            "   :PROPERTIES:")
        self.assertEqual(
            data[3],
            "   :GUID:           unique string per item")
        self.assertEqual(
            data[4],
            "   :CREATED:        <2009-09-06 Sun 18:45>")
#        self.assertEqual(
#            data[5],
#            "   :MEMACS_CREATED: [2011-12-28 Wed 18:50:42]")
        self.assertEqual(
            data[6],
            "   :ID:             af9b90163e9e4727b21e8a6b452c9529a438f314")
        self.assertEqual(
            data[7],
            "   :END:")