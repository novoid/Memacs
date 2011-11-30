#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-11-02 15:13:31 aw>

import unittest
import time
from common.orgformat import OrgFormat

class TestOrgFormat(unittest.TestCase):
    
    def test_link(self):
        """
        test Org links
        """
        self.assertEqual("[[/link/][description]]", OrgFormat.link("/link/", "description"), "format error link+description")
        self.assertEqual("[[/link/]]", OrgFormat.link("/link/"), "format error link")
        self.assertEqual("[[/link%20link/]]", OrgFormat.link("/link link/"), "quote error")

    def test_date(self):
        """
        test Org date
        """
        
        # testing tuples
        t = time.strptime("2011-11-02T20:38", "%Y-%m-%dT%H:%M")
        date = OrgFormat.date(t)
        datetime = OrgFormat.date(t, show_time=True)
        self.assertEqual("<2011-11-02 Wed>", date, "date error")
        self.assertEqual("<2011-11-02 Wed 20:38>", datetime, "datetime error")
        
        # testing strings
        self.assertEqual("<2011-11-03 Thu>",OrgFormat.strdate("2011-11-3"),"date string error")
        self.assertEqual("<2011-11-03 Thu 11:52>",OrgFormat.strdatetime("2011-11-3 11:52"),"datetime string error")
        
    


            
        
