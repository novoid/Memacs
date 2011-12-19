#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-19 15:13:31 aw>

import unittest
import time
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.orgformat import OrgFormat
from filenametimestamps.filenametimestamps import FileNameTimeStamps

class TestFileNameTimeStamps(unittest.TestCase):
    
    def setUp(self):
        self.TMPFOLDER = os.path.normpath(os.path.dirname(os.path.abspath(__file__))
                                           + os.path.sep + "tmp" ) + os.path.sep 
        if not os.path.exists(self.TMPFOLDER):
            os.makedirs(self.TMPFOLDER)
        
    def test_functional(self):
        file = self.TMPFOLDER + os.sep +  '2011-12-19T23.59.12_test1.txt'
        entry = "** <2011-12-19 Mon 23:59:12> [["+file+"][2011-12-19T23.59.12_test1.txt]]"
        
        # touch file
        open(file , 'w').close()
        
        argv = "-s -f " +self.TMPFOLDER
        memacs = FileNameTimeStamps(argv=argv.split())
        data = memacs.test_get_entries()
        
        os.remove(file)
        self.assertEqual(data[0], entry, "filenametimestamps - error")