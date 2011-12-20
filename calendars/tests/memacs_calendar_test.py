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
        data = memacs.test_get_entries()
        #for d in range(len(data)):
        #    print "self.assertEqual(data[%d], \"%s\")" % \
        #        (d, data[d])

        self.assertEqual(data[0], "** Whit Monday")
        self.assertEqual(data[1], "  <2012-05-28 Mon>--<2012-05-29 Tue>")
        self.assertEqual(data[2], "  :PROPERTIES:")
        #self.assertEqual(data[3], "  :CREATED: [2011-12-20 Tue 23:09:15]")
        self.assertEqual(data[4], "  :END:")
        self.assertEqual(data[5], "** Valentine's day")
        self.assertEqual(data[6], "  <2011-02-14 Mon>--<2011-02-15 Tue>")
        self.assertEqual(data[7], "  :PROPERTIES:")
        #self.assertEqual(data[8], "  :CREATED: [2011-12-20 Tue 23:09:15]")
        self.assertEqual(data[9], "  :END:")
        self.assertEqual(data[10], "** Valentine's day")
        self.assertEqual(data[11], "  <2010-02-14 Sun>--<2010-02-15 Mon>")
        self.assertEqual(data[12], "  :PROPERTIES:")
        #self.assertEqual(data[13], "  :CREATED: [2011-12-20 Tue 23:09:15]")
        self.assertEqual(data[14], "  :END:")
        self.assertEqual(data[15], "** Valentine's day")
        self.assertEqual(data[16], "  <2012-02-14 Tue>--<2012-02-15 Wed>")
        self.assertEqual(data[17], "  :PROPERTIES:")
        #self.assertEqual(data[18], "  :CREATED: [2011-12-20 Tue 23:09:15]")
        self.assertEqual(data[19], "  :END:")
        self.assertEqual(data[20], "** St. Stephan's Day")
        self.assertEqual(data[21], "  <2012-12-26 Wed>--<2012-12-27 Thu>")
        self.assertEqual(data[22], "  :PROPERTIES:")
        #self.assertEqual(data[23], "  :CREATED: [2011-12-20 Tue 23:09:15]")
        self.assertEqual(data[24], "  :END:")
        self.assertEqual(data[25], "** St. Stephan's Day")
        self.assertEqual(data[26], "  <2010-12-26 Sun>--<2010-12-27 Mon>")
        self.assertEqual(data[27], "  :PROPERTIES:")
        #self.assertEqual(data[28], "  :CREATED: [2011-12-20 Tue 23:09:15]")
        self.assertEqual(data[29], "  :END:")
        self.assertEqual(data[30], "** St. Stephan's Day")
