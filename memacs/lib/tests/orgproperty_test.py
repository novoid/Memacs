# -*- coding: utf-8 -*-
# Time-stamp: <2019-11-06 15:24:56 vk>

import time
import unittest

from orgformat import OrgFormat

from memacs.lib.orgproperty import OrgProperties


class TestOrgProperties(unittest.TestCase):

    def test_properties_default_ctor(self):
        p = OrgProperties("hashing data 1235")
        properties = str(p).splitlines()
        self.assertEqual(properties[0], "   :PROPERTIES:")
        self.assertEqual(properties[1],
            "   :ID:         063fad7f77461ed6a818b6b79306d641e9c90a83")
        self.assertEqual(properties[2], "   :END:")

    def test_properties_with_own_created(self):
        p = OrgProperties()
        p.add("CREATED",
              OrgFormat.date(time.gmtime(0), show_time=True))
        properties = str(p).splitlines()

        self.assertEqual(properties[0], "   :PROPERTIES:")
        self.assertEqual(properties[1], "   :CREATED:    <1970-01-0" + \
                         "1 Thu 00:00>")
        self.assertEqual(properties[2], "   :ID:         fede47e9" + \
                         "f49e1b7f5c6599a6d607e9719ca98625")
        self.assertEqual(properties[3], "   :END:")
