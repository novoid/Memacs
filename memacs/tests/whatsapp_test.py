# -*- coding: utf-8 -*-
# Time-stamp: <2018-09-22 13:57:41 vk>

import os
import time
import unittest

from memacs.whatsapp import WhatsApp


class TestWhatsApp(unittest.TestCase):

    def setUp(self):
        msgstore = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data', 'msgstore.db'
        )

        self.argv = []
        self.argv.append('-f')
        self.argv.append(msgstore)

    def test_whatsapp(self):
        self.argv.append('--output-format')
        self.argv.append('{text}')

        memacs = WhatsApp(argv=self.argv)
        data = memacs.test_get_entries()

        # omit hours from check because of different TZ offset:
        self.assertTrue(data[0].startswith('** <2016-10-15 Sat '))
        self.assertTrue(data[0].endswith(':18> Hello World!'))
        self.assertEqual(data[1], '   :PROPERTIES:')
        self.assertEqual(data[2], '   :NUMBER:     00436604444333')
        self.assertEqual(data[3], '   :TYPE:       INCOMING')
        # Karl had to disable the ID check because with different TZ offsets, the ID hash changes:
        # self.assertEqual(data[4], '   :ID:         804c40b796f8d71f48c9cd0023d1059e56d54d61')
        self.assertEqual(data[5], '   :END:')
