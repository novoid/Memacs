# -*- coding: utf-8 -*-
# Time-stamp: <2014-05-03 17:46:44 vk>

import unittest
import os
from memacs.photos import PhotosMemacs


class TestPhotoMemacs(unittest.TestCase):

    def test_from_file(self):
        test_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data'
        )
        argv = "-s -f " + test_path
        memacs = PhotosMemacs(argv=argv.split())
        data = memacs.test_get_entries()

        filename = 'fujifilm-finepix40i.jpg'
        path = os.path.join(test_path, filename)

        self.assertEqual(
            data[0],
            "** <2000-08-04 Fri 18:22> [[%s][%s]]" % (path, filename)
        )
        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(
            data[2],
            "   :ID:         c2833ac1c683dea5b600ac4f303a572d2148e1e7"
        )
        self.assertEqual(data[3], "   :END:")
