#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-19 15:13:31 aw>

import unittest
import time
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.orgformat import OrgFormat
from filenametimestamps import __init__

class TestFileNameTimeStamps(unittest.TestCase):
    
    def test_x(self):
        self.assertEqual(True, False, "implement here a lot of stuff!")
        
    # test:
    # -f 
    # -x 
    # -l 
    
    def test(self):
        pass