#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-26 22:13:31 awieser>

import unittest
import os
from common import outputwriter
import codecs

class TestOutputWriter(unittest.TestCase):
    def setUp(self):
        # setting tmpfolder to "../tmp"
        self.TMPFOLDER = os.path.normpath(os.path.dirname(os.path.abspath(__file__))
                                           + os. path.sep + os.path.pardir)
        
    def test_tmpfolderexists(self):
        """
        Check if the tmp-folder exists, otherwise we cannot make tests
        """
        #print os.path.abspath(__file__)
        self.assertTrue(os.path.exists(self.TMPFOLDER), "please check if folder tests/tmp exists")
    
    def test_ouput_to_file(self):
        """
        Simple Test
        """
        test_filename = self.TMPFOLDER + "testfile.org"
        
        # writing test output
        writer = outputwriter.OutputWriter(test_filename)
        writer.write("## abc\n")
        writer.writeln("## abc")
        writer.write_comment("abc\n")
        writer.write_commentln("abc")
        writer.close()
        
        # read and check the file
        file = codecs.open(test_filename, "r", "utf-8")
        input = file.readlines()
        
        self.assertEqual(input[0], u"## -*- coding: utf-8 -*-\n", "incorrect header")
        self.assertEqual(input[1], u"## abc\n", "incorrect write()")
        self.assertEqual(input[2], u"## abc\n", "incorrect writeln()")
        self.assertEqual(input[3], u"## abc\n", "incorrect write_comment()")
        self.assertEqual(input[4], u"## abc\n", "incorrect write_commentln()")
        self.assertEqual(input[5][:24], u"* successfully parsed by", "incorrect footer()")

        #cleaning up
        os.remove(self.TMPFOLDER + "testfile.org")
        
if __name__ == '__main__':
    unittest.main()
