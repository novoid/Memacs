# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-20 15:13:31 awieser>
import unittest
import time
import os
import sys
from common.orgformat import OrgFormat
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))
from common.orgproperty import OrgProperties


class TestOrgProperties(unittest.TestCase):

    def test_properties_default_ctor(self):
        p = OrgProperties()
        properties = unicode(p).splitlines()
        self.assertEqual(properties[0], u"   :PROPERTIES:")
        self.assertEqual(properties[1][:-24], u"   :MEMACS_CREATED: [")
        # this changes every time
        #self.assertEqual(properties[2],
        # u"   :ID:      849079e99d237b31b6a2184743cf9e33929dc749")
        self.assertEqual(properties[3], u"   :END:")

    def test_properties_with_own_created(self):
        p = OrgProperties()
        p.add(u"CREATED",
              OrgFormat.datetime(time.gmtime(0)))
        properties = unicode(p).splitlines()
        
        self.assertEqual(properties[0], u"   :PROPERTIES:")
        self.assertEqual(properties[1], u"   :CREATED:        <1970-01-01 Thu 00:00>")
        self.assertEqual(properties[2][:-24],u"   :MEMACS_CREATED: [")
        self.assertEqual(properties[3], u"   :ID:             fede47e9f49e1b7f5c6599a6d607e9719ca98625")
        self.assertEqual(properties[4], u"   :END:")


