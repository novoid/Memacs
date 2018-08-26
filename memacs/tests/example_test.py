# -*- coding: utf-8 -*-
# Time-stamp: <2018-08-25 14:16:04 vk>

import unittest
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
            "   :ID:         e7663db158b7ba301fb23e3dc40347970c7f8a0f")
        self.assertEqual(
            data[3],
            "   :END:")
        self.assertEqual(
            data[4],
            "** <1970-01-01 Thu 00:00> bar\t:tag1:tag2:")
        self.assertEqual(
            data[5],
            "   :PROPERTIES:")
        self.assertEqual(
            data[6],
            "   :DESCRIPTION:  foooo")
        self.assertEqual(
            data[7],
            "   :FOO-PROPERTY: asdf")
        self.assertEqual(
            data[8],
            "   :ID:           97521347348df02dab8bf86fbb6817c0af333a3f")
        self.assertEqual(
            data[9],
            "   :END:")
        self.assertEqual(
            data[10],
            "   bar notes")
        self.assertEqual(
            data[11],
            "   foo notes")

    def tearDown(self):
        pass
