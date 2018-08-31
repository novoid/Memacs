# -*- coding: utf-8 -*-
# Time-stamp: <2018-08-26 21:40:32 vk>

import unittest
import os
from memacs.svn import SvnMemacs


class TestSvnMemacs(unittest.TestCase):

    def setUp(self):
        test_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data', 'svn-log-xml.txt'
        )

        argv = "-s -f " + test_file
        memacs = SvnMemacs(argv=argv.split())
        self.data = memacs.test_get_entries()

    def test_from_file(self):
        data = self.data

        # omit the hours when comparing the results since this is depending on the locales:
        self.assertTrue(
            data[0].startswith('** <2011-10-27 Thu ')
            )
        self.assertTrue(
            data[0].endswith(':50> group-5 (r5): finished ?')
            )
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :REVISION:   5")
        self.assertEqual(
            data[3],
             "   :ID:         819908c0cedb0098bf5dd96aa0d213598da45614")
        self.assertEqual(
            data[4],
             "   :END:")
        # omit the hours when comparing the results since this is depending on the locales:
        self.assertTrue(
            data[5].startswith('** <2011-10-27 Thu ')
            )
        self.assertTrue(
            data[5].endswith(':18> group-5 (r4): finished 5,')
            )
        self.assertEqual(
            data[6],
             "   :PROPERTIES:")
        self.assertEqual(
            data[7],
             "   :REVISION:   4")
        self.assertEqual(
            data[8],
             "   :ID:         629716ff44b206745fdc34c910fe8b0f3d877f85")
        self.assertEqual(
            data[9],
             "   :END:")
        self.assertEqual(
            data[10],
             "   added package to assignment1.tex for landscaping (see 5.tex)")
        # omit the hours when comparing the results since this is depending on the locales:
        self.assertTrue(
            data[11].startswith('** <2011-10-27 Thu ')
            )
        self.assertTrue(
            data[11].endswith(':38> group-5 (r3): 5b.')
            )
        self.assertEqual(
            data[12],
             "   :PROPERTIES:")
        self.assertEqual(
            data[13],
             "   :REVISION:   3")
        self.assertEqual(
            data[14],
             "   :ID:         cf204bc9b36ba085275e03b7316ac34a496daf78")
        self.assertEqual(
            data[15],
             "   :END:")
        # omit the hours when comparing the results since this is depending on the locales:
        self.assertTrue(
            data[16].startswith('** <2011-10-27 Thu ')
            )
        self.assertTrue(
            data[16].endswith(':41> group-5 (r2): 5.tex')
            )
        self.assertEqual(
            data[17],
             "   :PROPERTIES:")
        self.assertEqual(
            data[18],
             "   :REVISION:   2")
        self.assertEqual(
            data[19],
             "   :ID:         f45be418de175ccf56e960a6941c9973094ab9e3")
        self.assertEqual(
            data[20],
             "   :END:")
        # omit the hours when comparing the results since this is depending on the locales:
        self.assertTrue(
            data[21].startswith('** <2011-10-27 Thu ')
            )
        self.assertTrue(
            data[21].endswith(':44> group-5 (r1): initial files')
            )
        self.assertEqual(
            data[22],
             "   :PROPERTIES:")
        self.assertEqual(
            data[23],
             "   :REVISION:   1")
        self.assertEqual(
            data[24],
             "   :ID:         9b7d570e2dc4fb3a009461714358c35cbe24a8fd")
        self.assertEqual(
            data[25],
             "   :END:")
