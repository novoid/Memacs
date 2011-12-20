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
from common.orgproperty import OrgProperty


class TestOrgProperties(unittest.TestCase):

    def test_properties_default_ctor(self):
        p = OrgProperties()
        properties = unicode(p).splitlines()
        self.assertEqual(properties[0], u"  :PROPERTIES:")
        self.assertEqual(properties[1][:-24], u"  :CREATED: [")
        self.assertEqual(properties[2], u"  :END:")

    def test_properties_with_own_created(self):
        p = OrgProperties()
        p.add(OrgProperty(u"CREATED",
                          OrgFormat.datetime(time.gmtime(0))))
        properties = unicode(p).splitlines()

        self.assertEqual(properties[0], u"  :PROPERTIES:")
        self.assertEqual(properties[1], u"  :CREATED: <1970-01-01 Thu 00:00>")
        self.assertEqual(properties[2], u"  :END:")
