# -*- coding: utf-8 -*-
# Time-stamp: <2018-08-25 14:44:23 vk>

import unittest
import os
from memacs.rss import RssMemacs


class TestRss(unittest.TestCase):

    def setUp(self):
        self.test_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data', 'sample-rss.txt'
        )
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

        # omit the hour from the result because this depends on the current locals:
        self.assertTrue(data[0].startswith('** <2009-09-06 Sun '))
        self.assertTrue(data[0].endswith(':45> [[http://www.wikipedia.org/][Example entry]]'))

        self.assertEqual(
            data[2],
            "   :GUID:       unique string per item")
        self.assertEqual(
            data[3],
            '   :PUBLISHED:  Mon, 06 Sep 2009 16:45:00 +0000'
        )
        self.assertEqual(
            data[4],
            "   :ID:         a0df7d405a7e9822fdd86af04e162663f1dccf11"
        )
        self.assertEqual(
            data[6],
            "   Here is some text containing an interesting description."
        )

        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[5], "   :END:")
