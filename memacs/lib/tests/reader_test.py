# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-30 12:16:47 armin>

import unittest
from memacs.lib.reader import CommonReader


class TestReader(unittest.TestCase):

    def test_file_no_path(self):
        try:
            CommonReader.get_data_from_file("")
            self.assertTrue(False, "false path failed")
        except SystemExit:
            pass
