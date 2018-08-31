# -*- coding: utf-8 -*-

import unittest
import os

from memacs.gpx import GPX


class TestGPX(unittest.TestCase):

    def test_google(self):
        sample = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data', 'sample.gpx'
        )

        argv = []
        argv.append('-f')
        argv.append(sample)

        memacs = GPX(argv=argv)
        try:
            data = memacs.test_get_entries()

            # both addresses are reasonable for the given coordinates and
            # OSM seems to return the second one at 2018-08-25 while the
            # first one was true when the original author developed this
            # test:
            self.assertTrue(
                data[0] in ['** <2017-04-01 Sat 10:50> Eggenberger Allee 9, 8020 Graz, Austria	:network:',
                            '** <2017-04-01 Sat 10:50> Alte Poststraße 150, 8020 Graz, Austria	:network:'])
            self.assertEqual(
                data[1],
                "   :PROPERTIES:")
            self.assertEqual(
                data[2],
                "   :LATITUDE:   47.0693")
            self.assertEqual(
                data[3],
                "   :LONGITUDE:  15.4076001")
            self.assertEqual(
                data[4],
                "   :ID:         c2dc4f2289d79cff4cf27faa95863f8cb5b8cb21")
            self.assertEqual(
                data[5],
                "   :END:")
        except RuntimeError as e:
            print('skipped test_google because of {}'.format(e))

    def test_osm(self):
        sample = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data', 'sample.gpx'
        )

        argv = []
        argv.append('-f')
        argv.append(sample)
        argv.append('-p osm')

        memacs = GPX(argv=argv)
        data = memacs.test_get_entries()

        # both addresses are reasonable for the given coordinates and
        # OSM seems to return the second one at 2018-08-25 while the
        # first one was true when the original author developed this
        # test:
        self.assertTrue(
            data[0] in ['** <2017-04-01 Sat 10:50> FH Joanneum - Prüffeld, 150, Alte Poststraße, Gries, Graz, Steiermark, 8020, Österreich	:network:',
                        '** <2017-04-01 Sat 10:50> FH Joanneum, 13, Eggenberger Allee, Eggenberg, Graz, Steiermark, 8020, Österreich	:network:'])
        self.assertEqual(
            data[1],
            "   :PROPERTIES:")
        self.assertEqual(
            data[2],
            "   :LATITUDE:   47.0693")
        self.assertEqual(
            data[3],
            "   :LONGITUDE:  15.4076001")
        self.assertEqual(
            data[4],
            "   :ID:         c2dc4f2289d79cff4cf27faa95863f8cb5b8cb21")
        self.assertEqual(
            data[5],
            "   :END:")
