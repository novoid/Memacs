# -*- coding: utf-8 -*-

import unittest
from memacs.kodi import Kodi
import os


class TestKodi(unittest.TestCase):
    def test_audio_log(self):

        log_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data',
            'kodi_audio.log')
        argv = []
        argv.append("-f")
        argv.append(log_file)
        argv.append("--fieldnames")
        argv.append(
            'timestamp,action,position,length,path,album,artist,title,')
        argv.append("--timestamp-field")
        argv.append("timestamp")
        argv.append("--action-field")
        argv.append("action")
        argv.append("--output-format")
        argv.append("{artist} - {title}")
        argv.append("--properties")
        argv.append("album,artist,title")

        memacs = Kodi(argv=argv)
        data = memacs.test_get_entries()

        # Test Simple Play and Paused
        self.assertEqual(
            data[0],
            "** <2018-10-01 Mon 21:58>--<2018-10-01 Mon 21:59> Clueso - So sehr dabei"
        )
        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[2], "   :ALBUM:      Barfuss")
        self.assertEqual(data[3], "   :ARTIST:     Clueso")
        self.assertEqual(data[4], "   :TITLE:      So sehr dabei")
        self.assertEqual(
            data[5],
            "   :ID:         332b5cd71e335d2cf55f681a3a1fc26161465069")
        self.assertEqual(data[6], "   :END:")

        #Test started one track and switched to another
        self.assertEqual(
            data[7],
            "** <2018-10-01 Mon 22:03>--<2018-10-01 Mon 22:08> Clueso - Chicago"
        )
        self.assertEqual(data[8], "   :PROPERTIES:")
        self.assertEqual(data[9], "   :ALBUM:      Barfuss")
        self.assertEqual(data[10], "   :ARTIST:     Clueso")
        self.assertEqual(data[11], "   :TITLE:      Chicago")
        self.assertEqual(
            data[12],
            "   :ID:         13b38e428bb4d8c9e55183877096c921bee871e5")
        self.assertEqual(data[13], "   :END:")
        self.assertEqual(
            data[14],
            "** <2018-10-01 Mon 22:08>--<2018-10-01 Mon 22:15> Clueso - So sehr dabei"
        )
        self.assertEqual(data[15], "   :PROPERTIES:")
        self.assertEqual(data[16], "   :ALBUM:      Barfuss")
        self.assertEqual(data[17], "   :ARTIST:     Clueso")
        self.assertEqual(data[18], "   :TITLE:      So sehr dabei")
        self.assertEqual(
            data[19],
            "   :ID:         4ed907d4337faaca7b2fd059072fc5046e80dc11")
        self.assertEqual(data[20], "   :END:")
