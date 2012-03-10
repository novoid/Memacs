# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import unittest
import os
from memacs.rss import RssMemacs


class TestRss(unittest.TestCase):

    def setUp(self):
        self.test_file = os.path.dirname(
            os.path.abspath(__file__)) + os.sep + "tmp" \
            + os.path.sep + "sample-rss.txt"
        self.argv = "-s -f " + self.test_file

    def test_false_appending(self):
        try:
            memacs = RssMemacs(argv=self.argv.split())
            memacs.test_get_entries()
        except Exception:
            pass

    def test_all(self):
        memacs = RssMemacs(argv=self.argv.split())
        data = memacs.test_get_entries()

        # generate assertEquals :)
        #for d in range(len(data)):
        #    print "self.assertEqual(\n\tdata[%d],\n\t\"%s\")" % \
        #        (d, data[d])
        self.assertEqual(
            data[0],
            "** <2009-09-06 Sun 16:45> [[http://www.wikipedia.or" + \
            "g/][Example entry]]")
        self.assertEqual(
            data[1],
            "   Here is some text containing an interesting description.")
        self.assertEqual(
            data[2],
            "   :PROPERTIES:")
        self.assertEqual(
            data[3],
            "   :GUID:       unique string per item")
        self.assertEqual(
            data[4],
            "   :ID:         7ec7b2ec7d1ac5f18188352551b04f061af81e04")
        self.assertEqual(
            data[5],
            "   :END:")
