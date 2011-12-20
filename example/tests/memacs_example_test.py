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
from example.memacs_example import Foo


class TestFoo(unittest.TestCase):

    def setUp(self):
        pass

    def test_all(self):
        argv = "-s"
        memacs = Foo(argv=argv.split())
        data = memacs.test_get_entries()

        self.assertEqual(data[0], "** foo", "first entry did not match")
        self.assertEqual(data[1], "** bar", "first entry did not match")

    def tearDown(self):
        pass
