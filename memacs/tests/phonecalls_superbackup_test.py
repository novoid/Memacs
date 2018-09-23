# -*- coding: utf-8 -*-

import unittest
import os
from memacs.phonecalls_superbackup import PhonecallsSuperBackupMemacs


class TestPhonecallsSuperBackup(unittest.TestCase):
    def setUp(self):
        self._test_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data',
            'calls_superbackup.xml')
        argv = "-s -f " + self._test_file
        memacs = PhonecallsSuperBackupMemacs(argv=argv.split())
        self.data = memacs.test_get_entries()

    def test_all(self):
        self.assertEqual(
            self.data[0],
            "** <2018-09-17 Mon 19:58>-<2018-09-17 Mon 20:02> Phonecall from [[contact:TestPerson1][TestPerson1]]"
        )
        self.assertEqual(self.data[1], "   :PROPERTIES:")
        self.assertEqual(self.data[2], "   :NUMBER:     +49123456789")
        self.assertEqual(self.data[3], "   :DURATION:   264")
        self.assertEqual(self.data[4], "   :NAME:       TestPerson1")
        self.assertEqual(
            self.data[5],
            "   :ID:         4a6f6cb848be3870cd1540afb50185e12fa7a02c")
        self.assertEqual(self.data[6], "   :END:")
        self.assertEqual(
            self.data[7],
            "** <2018-09-17 Mon 17:24>-<2018-09-17 Mon 17:25> Phonecall from [[contact:TestPerson2][TestPerson2]]"
        )
        self.assertEqual(self.data[8], "   :PROPERTIES:")
        self.assertEqual(self.data[9], "   :NUMBER:     +4912345678910")
        self.assertEqual(self.data[10], "   :DURATION:   73")
        self.assertEqual(self.data[11], "   :NAME:       TestPerson2")
        self.assertEqual(
            self.data[12],
            "   :ID:         09df2166236a87f343523257fbd8f2b5537ea882")
        self.assertEqual(self.data[13], "   :END:")
