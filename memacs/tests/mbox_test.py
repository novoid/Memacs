# -*- coding: utf-8 -*-
# Time-stamp: <2012-05-15 17:11:31 df>

import unittest
import os
from memacs.mbox import MboxMemacs


class TestTagstore(unittest.TestCase):

    def setUp(self):
        pass

    def test_from_file(self):
        test_file = os.path.dirname(
            os.path.abspath(__file__)) + os.sep + "tmp" \
            + os.sep + "mboxexample"

        argv = []
        argv.append("-nf")
        argv.append(test_file)

        memacs = MboxMemacs(argv=argv)
        data = memacs.test_get_entries()

        self.assertEqual(
            data[0],
            "** <2012-02-20 Mon 12:27:50> [[mailto:foo.bob@gmail.com]" +
            "[Foo Bob]]@[[news:tu-graz.flames][tu-graz.flames]]:" +
            " Re: Thats a Test")
        self.assertEqual(
            data[1],
            "   :PROPERTIES:")
        self.assertEqual(
            data[3],
            "   :ID:         <foo.bob@gmail.com>")
        self.assertEqual(
            data[4],
            "   :END:")

        def tearDown(self):
            pass
