# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31>

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

        self.assertEqual(data[0], '** <2016-10-15 Sat 20:18> Hello World!')
        self.assertEqual(data[1], '   :PROPERTIES:')
        self.assertEqual(data[2], '   :TYPE:       INCOMING')
        self.assertEqual(data[3], '   :NUMBER:     00436604444333')
        self.assertEqual(data[4], '   :ID:         d8fa64a86286432a42a13f129cad0d7ebd56873e')
        self.assertEqual(data[5], '   :END:')
