# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import unittest
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))
from calendars.memacs_calendar import CalendarMemacs


class TestCalendar(unittest.TestCase):

    def setUp(self):
        pass

    def test_all(self):
        test_file = os.path.dirname(os.path.abspath(__file__)) + \
            os.sep + "austrian_holidays_from_google.ics"
        argv = "-s -cf " + test_file
        memacs = CalendarMemacs(argv=argv.split())
        print test_file
        data = memacs.test_get_entries()
        self.assertEqual(data[0], "** Whit Monday",
                         "calendar line 0 failed")
        self.assertEqual(data[1], "   <2012-05-28 Mon>--<2012-05-29 Tue>",
                         "calendar line 1 failed")
        self.assertEqual(data[2], "** Valentine's day",
                         "calendar line 2 failed")
        self.assertEqual(data[3], "   <2011-02-14 Mon>--<2011-02-15 Tue>",
                         "calendar line 3 failed")
        self.assertEqual(data[4], "** Valentine's day",
                         "calendar line 4 failed")
        self.assertEqual(data[5], "   <2010-02-14 Sun>--<2010-02-15 Mon>",
                         "calendar line 5 failed")
        self.assertEqual(data[6], "** Valentine's day",
                         "calendar line 6 failed")
        self.assertEqual(data[7], "   <2012-02-14 Tue>--<2012-02-15 Wed>",
                         "calendar line 7 failed")
        self.assertEqual(data[8], "** St. Stephan's Day",
                         "calendar line 8 failed")
        self.assertEqual(data[9], "   <2012-12-26 Wed>--<2012-12-27 Thu>",
                         "calendar line 9 failed")
        self.assertEqual(data[10], "** St. Stephan's Day",
                         "calendar line 10 failed")
        self.assertEqual(data[11], "   <2010-12-26 Sun>--<2010-12-27 Mon>",
                         "calendar line 11 failed")
        self.assertEqual(data[12], "** St. Stephan's Day",
                         "calendar line 12 failed")
        self.assertEqual(data[13], "   <2011-12-26 Mon>--<2011-12-27 Tue>",
                         "calendar line 13 failed")
        self.assertEqual(data[14], "** St. Nicholas",
                         "calendar line 14 failed")
        self.assertEqual(data[15], "   <2011-12-06 Tue>--<2011-12-07 Wed>",
                         "calendar line 15 failed")
        self.assertEqual(data[16], "** St. Nicholas",
                         "calendar line 16 failed")
        self.assertEqual(data[17], "   <2010-12-06 Mon>--<2010-12-07 Tue>",
                         "calendar line 17 failed")
        self.assertEqual(data[18], "** St. Nicholas",
                         "calendar line 18 failed")
        self.assertEqual(data[19], "   <2012-12-06 Thu>--<2012-12-07 Fri>",
                         "calendar line 19 failed")
        self.assertEqual(data[20], "** New Year's Eve",
                         "calendar line 20 failed")
        self.assertEqual(data[21], "   <2011-12-31 Sat>--<2012-01-01 Sun>",
                         "calendar line 21 failed")
        self.assertEqual(data[22], "** New Year's Eve",
                         "calendar line 22 failed")
        self.assertEqual(data[23], "   <2010-12-31 Fri>--<2011-01-01 Sat>",
                         "calendar line 23 failed")
        self.assertEqual(data[24], "** New Year",
                         "calendar line 24 failed")
        self.assertEqual(data[25], "   <2012-01-01 Sun>--<2012-01-02 Mon>",
                         "calendar line 25 failed")
        self.assertEqual(data[26], "** New Year",
                         "calendar line 26 failed")
        self.assertEqual(data[27], "   <2010-01-01 Fri>--<2010-01-02 Sat>",
                         "calendar line 27 failed")
        self.assertEqual(data[28], "** New Year",
                         "calendar line 28 failed")
        self.assertEqual(data[29], "   <2011-01-01 Sat>--<2011-01-02 Sun>",
                         "calendar line 29 failed")
        self.assertEqual(data[30], "** National Holiday",
                         "calendar line 30 failed")
        self.assertEqual(data[31], "   <2010-10-26 Tue>--<2010-10-27 Wed>",
                         "calendar line 31 failed")
        self.assertEqual(data[32], "** National Holiday",
                         "calendar line 32 failed")
        self.assertEqual(data[33], "   <2012-10-26 Fri>--<2012-10-27 Sat>",
                         "calendar line 33 failed")
        self.assertEqual(data[34], "** National Holiday",
                         "calendar line 34 failed")
        self.assertEqual(data[35], "   <2011-10-26 Wed>--<2011-10-27 Thu>",
                         "calendar line 35 failed")
        self.assertEqual(data[36], "** Labour Day",
                         "calendar line 36 failed")
        self.assertEqual(data[37], "   <2011-05-01 Sun>--<2011-05-02 Mon>",
                         "calendar line 37 failed")
        self.assertEqual(data[38], "** Labour Day",
                         "calendar line 38 failed")
        self.assertEqual(data[39], "   <2010-05-01 Sat>--<2010-05-02 Sun>",
                         "calendar line 39 failed")
        self.assertEqual(data[40], "** Labour Day",
                         "calendar line 40 failed")
        self.assertEqual(data[41], "   <2012-05-01 Tue>--<2012-05-02 Wed>",
                         "calendar line 41 failed")
        self.assertEqual(data[42], "** Immaculate Conception",
                         "calendar line 42 failed")
        self.assertEqual(data[43], "   <2012-12-08 Sat>--<2012-12-09 Sun>",
                         "calendar line 43 failed")
        self.assertEqual(data[44], "** Immaculate Conception",
                         "calendar line 44 failed")
        self.assertEqual(data[45], "   <2010-12-08 Wed>--<2010-12-09 Thu>",
                         "calendar line 45 failed")
        self.assertEqual(data[46], "** Immaculate Conception",
                         "calendar line 46 failed")
        self.assertEqual(data[47], "   <2011-12-08 Thu>--<2011-12-09 Fri>",
                         "calendar line 47 failed")
        self.assertEqual(data[48], "** Good Friday",
                         "calendar line 48 failed")
        self.assertEqual(data[49], "   <2012-04-06 Fri>--<2012-04-07 Sat>",
                         "calendar line 49 failed")
        self.assertEqual(data[50], "** Epiphany",
                         "calendar line 50 failed")
        self.assertEqual(data[51], "   <2010-01-06 Wed>--<2010-01-07 Thu>",
                         "calendar line 51 failed")
        self.assertEqual(data[52], "** Epiphany",
                         "calendar line 52 failed")
        self.assertEqual(data[53], "   <2012-01-06 Fri>--<2012-01-07 Sat>",
                         "calendar line 53 failed")
        self.assertEqual(data[54], "** Epiphany",
                         "calendar line 54 failed")
        self.assertEqual(data[55], "   <2011-01-06 Thu>--<2011-01-07 Fri>",
                         "calendar line 55 failed")
        self.assertEqual(data[56], "** Easter Monday",
                         "calendar line 56 failed")
        self.assertEqual(data[57], "   <2012-04-09 Mon>--<2012-04-10 Tue>",
                         "calendar line 57 failed")
        self.assertEqual(data[58], "** Easter",
                         "calendar line 58 failed")
        self.assertEqual(data[59], "   <2012-04-08 Sun>--<2012-04-09 Mon>",
                         "calendar line 59 failed")
        self.assertEqual(data[60], "** Corpus Christi",
                         "calendar line 60 failed")
        self.assertEqual(data[61], "   <2012-06-07 Thu>--<2012-06-08 Fri>",
                         "calendar line 61 failed")
        self.assertEqual(data[62], "** Christmas Eve",
                         "calendar line 62 failed")
        self.assertEqual(data[63], "   <2011-12-24 Sat>--<2011-12-25 Sun>",
                         "calendar line 63 failed")
        self.assertEqual(data[64], "** Christmas Eve",
                         "calendar line 64 failed")
        self.assertEqual(data[65], "   <2010-12-24 Fri>--<2010-12-25 Sat>",
                         "calendar line 65 failed")
        self.assertEqual(data[66], "** Christmas Eve",
                         "calendar line 66 failed")
        self.assertEqual(data[67], "   <2012-12-24 Mon>--<2012-12-25 Tue>",
                         "calendar line 67 failed")
        self.assertEqual(data[68], "** Christmas",
                         "calendar line 68 failed")
        self.assertEqual(data[69], "   <2010-12-25 Sat>--<2010-12-26 Sun>",
                         "calendar line 69 failed")
        self.assertEqual(data[70], "** Christmas",
                         "calendar line 70 failed")
        self.assertEqual(data[71], "   <2011-12-25 Sun>--<2011-12-26 Mon>",
                         "calendar line 71 failed")
        self.assertEqual(data[72], "** Christmas",
                         "calendar line 72 failed")
        self.assertEqual(data[73], "   <2012-12-25 Tue>--<2012-12-26 Wed>",
                         "calendar line 73 failed")
        self.assertEqual(data[74], "** Assumption",
                         "calendar line 74 failed")
        self.assertEqual(data[75], "   <2010-08-15 Sun>--<2010-08-16 Mon>",
                         "calendar line 75 failed")
        self.assertEqual(data[76], "** Assumption",
                         "calendar line 76 failed")
        self.assertEqual(data[77], "   <2012-08-15 Wed>--<2012-08-16 Thu>",
                         "calendar line 77 failed")
        self.assertEqual(data[78], "** Assumption",
                         "calendar line 78 failed")
        self.assertEqual(data[79], "   <2011-08-15 Mon>--<2011-08-16 Tue>",
                         "calendar line 79 failed")
        self.assertEqual(data[80], "** Ascension Day",
                         "calendar line 80 failed")
        self.assertEqual(data[81], "   <2012-05-17 Thu>--<2012-05-18 Fri>",
                         "calendar line 81 failed")
        self.assertEqual(data[82], "** All Souls' Day",
                         "calendar line 82 failed")
        self.assertEqual(data[83], "   <2011-11-02 Wed>--<2011-11-03 Thu>",
                         "calendar line 83 failed")
        self.assertEqual(data[84], "** All Souls' Day",
                         "calendar line 84 failed")
        self.assertEqual(data[85], "   <2010-11-02 Tue>--<2010-11-03 Wed>",
                         "calendar line 85 failed")
        self.assertEqual(data[86], "** All Souls' Day",
                         "calendar line 86 failed")
        self.assertEqual(data[87], "   <2012-11-02 Fri>--<2012-11-03 Sat>",
                         "calendar line 87 failed")
        self.assertEqual(data[88], "** All Saints' Day",
                         "calendar line 88 failed")
        self.assertEqual(data[89], "   <2010-11-01 Mon>--<2010-11-02 Tue>",
                         "calendar line 89 failed")
        self.assertEqual(data[90], "** All Saints' Day",
                         "calendar line 90 failed")
        self.assertEqual(data[91], "   <2012-11-01 Thu>--<2012-11-02 Fri>",
                         "calendar line 91 failed")
        self.assertEqual(data[92], "** All Saints' Day",
                         "calendar line 92 failed")
        self.assertEqual(data[93], "   <2011-11-01 Tue>--<2011-11-02 Wed>",
                         "calendar line 93 failed")

    def tearDown(self):
        pass
