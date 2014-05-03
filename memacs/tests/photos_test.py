# -*- coding: utf-8 -*-
# Time-stamp: <2014-05-03 17:46:44 vk>

import unittest
import os
from memacs.photos import PhotosMemacs


class TestPhotoMemacs(unittest.TestCase):

    def test_from_file(self):
        test_path = os.path.dirname(os.path.abspath(__file__)) + \
            os.sep + "tmp"
        argv = "-s -f " + test_path
        memacs = PhotosMemacs(argv=argv.split())
        data = memacs.test_get_entries()

        # generate assertEquals :)
#        for d in range(len(data)):
#            print "self.assertEqual(\n\tdata[%d],\n\t \"%s\")" % \
#               (d, data[d])

        self.assertEqual(
            data[0],
             u"** <2000-08-04 Fri 18:22> [[/home/vk/src/memacs/mema" + \
             "cs/tests/tmp/fujifilm-finepix40i.jpg][fujifilm-finepix40i.jpg]]")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             u"   :ID:         c2833ac1c683dea5b600ac4f303a572d2148e1e7")
        self.assertEqual(
            data[3],
             "   :END:")
