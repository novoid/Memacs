# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-09 15:39:33 armin>

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
             "** <2000-08-04 Fri 18:22:57> [[/home/armin/repos/Memacs/mema" + \
             "cs/tests/tmp/fujifilm-finepix40i.jpg][fujifilm-finepix40i.jpg]]")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :ID:         c593ea66ff52d070902d0a8e0952875fa6a53bf9")
        self.assertEqual(
            data[3],
             "   :END:")
