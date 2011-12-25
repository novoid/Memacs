import unittest
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))))
from common.reader import CommonReader


class TestArgParser(unittest.TestCase):

    def test_file_no_path(self):
        try:
            CommonReader.get_data_from_file("")
            self.assertTrue(False, "false path failed")
        except SystemExit:
            pass
