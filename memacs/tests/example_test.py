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
from memacs.example import Foo


class TestFoo(unittest.TestCase):

    def setUp(self):
        pass

    def test_all(self):
        argv = "-s"
        memacs = Foo(argv=argv.split())
        # or when in append mode:
        # memacs = Foo(argv=argv.split(), append=True)
        data = memacs.test_get_entries()

        # generate assertEquals :)
        #for d in range(len(data)):
        #   print "self.assertEqual(\n\tdata[%d],\n\t\"%s\")" % \
        #        (d, data[d])

        self.assertEqual(
            data[0],
            "** <1970-01-01 Thu 00:00> foo")
        self.assertEqual(
            data[1],
            "   :PROPERTIES:")
        self.assertEqual(
            data[2],
            "   :ID:         da39a3ee5e6b4b0d3255bfef95601890afd80709")
        self.assertEqual(
            data[3],
            "   :END:")
        self.assertEqual(
            data[4],
            "** <1970-01-01 Thu 00:00> bar\t:tag1:tag2:")
        self.assertEqual(
            data[5],
            "   bar notes")
        self.assertEqual(
            data[6],
            "   foo notes")
        self.assertEqual(
            data[7],
            "   :PROPERTIES:")
        self.assertEqual(
            data[8],
            "   :DESCRIPTION:  foooo")
        self.assertEqual(
            data[9],
            "   :FOO-PROPERTY: asdf")
        self.assertEqual(
            data[10],
            "   :ID:           97521347348df02dab8bf86fbb6817c0af333a3f")
        self.assertEqual(
            data[11],
            "   :END:")

    def tearDown(self):
        pass
