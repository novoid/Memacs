#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-10-02 21:51:07 vk>

import codecs
import shutil
import time
import tempfile
import unittest

from memacs.lib.orgformat import OrgFormat
from memacs.lib.orgwriter import OrgOutputWriter
from memacs.lib.orgproperty import OrgProperties


class TestOutputWriter(unittest.TestCase):
    def setUp(self):
        self.TMPFOLDER = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.TMPFOLDER)

    def test_output_to_file(self):
        """
        Simple Test
        """
        test_filename = self.TMPFOLDER + "testfile.org"

        properties = OrgProperties("data_for_hashing")

        # writing test output
        writer = OrgOutputWriter("short descript", "test-tag", test_filename)
        writer.write("## abc\n")
        writer.writeln("## abc")
        writer.write_comment("abc\n")
        writer.write_commentln("abc")
        writer.write_org_item("begin")

        timestamp = OrgFormat.datetime(time.gmtime(0))
        writer.write_org_subitem(timestamp=timestamp,
                                 output="sub",
                                 properties=properties)
        writer.write_org_subitem(timestamp=timestamp,
                                 output="sub",
                                 tags=["foo", "bar"],
                                 properties=properties)
        writer.write_org_subitem(timestamp=False,
                                 output="no timestamp",
                                 tags=["bar", "baz"],
                                 properties=properties)
        writer.close()

        # read and check the file_handler
        with codecs.open(test_filename, "r", "utf-8") as file_handler:
            data = file_handler.readlines()

        self.assertEqual(
            data[3],
            "* short descript          :Memacs:test-tag:\n")
        self.assertEqual(
            data[4],
            "## abc\n")
        self.assertEqual(
            data[5],
            "## abc\n")
        self.assertEqual(
            data[6],
            "## abc\n")
        self.assertEqual(
            data[7],
            "## abc\n")
        self.assertEqual(
            data[8],
            "* begin\n")
        self.assertEqual(
            data[9],
            "** <1970-01-01 Thu 00:00> sub\n")
        self.assertEqual(
            data[10],
            "   :PROPERTIES:\n")
        self.assertEqual(
            data[11],
            "   :ID:         9cc53a63e13e18437401513316185f6f3b7ed703\n")
        self.assertEqual(
            data[12],
            "   :END:\n")
        self.assertEqual(
            data[13],
            "\n")
        self.assertEqual(
            data[14],
            "** <1970-01-01 Thu 00:00> sub\t:foo:bar:\n")
        self.assertEqual(
            data[15],
            "   :PROPERTIES:\n")
        self.assertEqual(
            data[16],
            "   :ID:         9cc53a63e13e18437401513316185f6f3b7ed703\n")
        self.assertEqual(
            data[17],
            "   :END:\n")
        self.assertEqual(
            data[18],
            "\n")
        self.assertEqual(
            data[19],
            "** no timestamp\t:bar:baz:\n")
        self.assertEqual(
            data[20],
            "   :PROPERTIES:\n")
        self.assertEqual(
            data[21],
            "   :ID:         9cc53a63e13e18437401513316185f6f3b7ed703\n")
        self.assertEqual(
            data[22],
            "   :END:\n")

    def test_utf8(self):
        test_filename = self.TMPFOLDER + "testutf8.org"

        # writing test output
        writer = OrgOutputWriter("short-des", "tag", test_filename)
        writer.write("☁☂☃☄★☆☇☈☉☊☋☌☍☎☏☐☑☒☓☔☕☖☗♞♟♠♡♢♣♤♥♦♧♨♩♪♫♬♭♮♯♰♱♲♳♴♵\n")
        writer.close()

        # read and check the file_handler
        file_handler = codecs.open(test_filename, "r", "utf-8")
        input_handler = file_handler.readlines()
        file_handler.close()
        self.assertEqual(input_handler[4],
                         "☁☂☃☄★☆☇☈☉☊☋☌☍☎☏☐☑☒☓☔☕☖☗♞♟♠♡♢♣♤♥♦♧♨♩♪♫♬♭♮♯♰♱♲♳♴♵\n",
                         "utf-8 failure")

    def test_autotag(self):
        test_filename = self.TMPFOLDER + "testautotag.org"

        autotag_dict = {}
        autotag_dict["programming"] = ["programming", "python", "java"]
        autotag_dict["TUG"] = ["tugraz", "university"]

        output = "Programming for my bachelor thesis at University"

        # writing test output
        writer = OrgOutputWriter(short_description="short-des",
                                 tag="tag",
                                 file_name=test_filename,
                                 autotag_dict=autotag_dict)
        timestamp = OrgFormat.datetime(time.gmtime(0))

        properties = OrgProperties("data_for_hashing")

        writer.write_org_subitem(timestamp=timestamp,
                                 output=output,
                                 properties=properties)
        writer.close()

        # read and check the file_handler
        file_handler = codecs.open(test_filename, "r", "utf-8")
        input_handler = file_handler.readlines()
        file_handler.close()

        self.assertTrue(input_handler[4].startswith("** <1970-01-01 Thu 00:00> Programming for my " +
                         "bachelor thesis at University\t:"))
        self.assertTrue(input_handler[4].endswith("programming:TUG:\n") or
                        input_handler[4].endswith("TUG:programming:\n"))


if __name__ == '__main__':
    unittest.main()
