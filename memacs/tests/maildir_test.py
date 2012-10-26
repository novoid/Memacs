# -*- coding: utf-8 -*-
# Time-stamp: <2012-05-15 17:11:31 df>

import unittest
import os
from memacs.maildir import MaildirMemacs


class TestTagstore(unittest.TestCase):

    def setUp(self):
        pass

    def test_from_file(self):
        test_file = os.path.dirname(
            os.path.abspath(__file__)) + os.sep + "tmp" \
            + os.sep + "maildir"

        argv = []
        argv.append("-fp")
        argv.append(test_file)

        memacs = MaildirMemacs(argv=argv)
        data = memacs.test_get_entries()

        self.assertEqual(
            data[0],
            '** <2007-11-19 Mon 09:28:31> ' +
            '[[mailto:test.test@test.at]["test.test@test.at"]]: SomeSubject')
        self.assertEqual(
            data[1],
            "   :PROPERTIES:")
        self.assertEqual(
            data[3],
            '   :ID:         <200711190928.' +
            'lAJ9SVJr026663@fstgss22..at>')
        self.assertEqual(
            data[4],
            "   :END:")

        def tearDown(self):
            pass
