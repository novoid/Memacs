#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-10-09 15:12:44 vk>

import os
import shutil
import tempfile
import unittest
import datetime

from memacs.filenametimestamps import FileNameTimeStamps


class TestFileNameTimeStamps(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def touch_file(self, basename):
        """
        Creates a test file and returns the Org mode link to it
        """
        tmpfile = os.path.join(self._tmp_dir, basename)
        with open(tmpfile, 'w'):
            pass
        return '[[file:' + tmpfile + '][' + basename + ']]'

    #######################################################################

    # NOT tested so far:
    # --append
    # --columns-header STRING
    # --custom-header
    # --skip-files-with-no-or-wrong-timestamp
    # --add-to-time-stamps -> KNOWN BUG; see https://github.com/novoid/Memacs/issues/92 - disabled tests below!

    #######################################################################

    def call_omit_drawers(self):
        """
        Invokes the filenametimestamp module with basic parameters skipping the drawers
        """
        argv = "--suppress-messages --omit-drawers --folder " + self._tmp_dir
        memacs = FileNameTimeStamps(argv=argv.split())
        return memacs.test_get_entries()

    def test_good_case1(self):
        self.assertEqual('** <2019-10-03 Thu 09:55> ' + self.touch_file('2019-10-03T09.55.00 foo.txt'), self.call_omit_drawers()[0])

    def test_good_case2(self):
        self.assertEqual('** <2019-05-28 Tue>--<2019-07-24 Wed> ' + self.touch_file('2019-05-28--2019-07-24 Test -- scan notes.pdf'), self.call_omit_drawers()[0])

    def test_good_timestamp_with_no_second(self):
        self.assertEqual('** <2019-10-03 Thu 09:55> ' + self.touch_file('2019-10-03T09.55 foo.txt'), self.call_omit_drawers()[0])

    def test_good_datestamp(self):
        self.assertEqual('** <2019-10-02 Wed> ' + self.touch_file('2019-10-02 foo.txt'), self.call_omit_drawers()[0])

    def test_good_datestamp_with_determining_time_from_file(self):
        # FIXXME: caveat: this adds some tiny dependency: if the
        # minute changes between the file creation and the check, this
        # test fails
        today_weekday = datetime.datetime.now().strftime('<%Y-%m-%d %a %H:%M> ')  # FIXXME: dependency on current locale: works only with English weekdays
        today_day = datetime.datetime.now().strftime('%Y-%m-%d')
        self.assertEqual('** ' + today_weekday + self.touch_file(today_day + ' foo.txt'), self.call_omit_drawers()[0])

    def test_good_datestamp_without_month(self):
        self.assertEqual('** <2019-10-01 Tue> ' + self.touch_file('2019-10 foo.txt'), self.call_omit_drawers()[0])

    def test_good_case_with_seconds(self):
        self.assertEqual('** <2019-10-03 Thu 09:55> ' + self.touch_file('2019-10-03T09.55.00 foo.txt'), self.call_omit_drawers()[0])

    def test_good_case_without_datestamp(self):
        self.assertEqual('** ' + self.touch_file('foo.txt'), self.call_omit_drawers()[0])

    def test_wrong_timestamp_in_second(self):
        # this might be debatable: wrong seconds are wrong but the
        # seconds don't appear in the Org mode time stamp so I ignore
        # them so far.
        self.assertEqual('** <2019-10-01 Tue 09:55> ' + self.touch_file('2019-10-01T09.55.60 foo.txt'), self.call_omit_drawers()[0])

    def test_wrong_timestamp_in_minute(self):
        # an erroneous minute results in a correct date-stamp only
        self.assertEqual('** <2019-10-01 Tue> ' + self.touch_file('2019-10-01T09.60.01 foo.txt'), self.call_omit_drawers()[0])

    def test_wrong_timestamp_in_hour(self):
        self.assertEqual('** <2019-10-01 Tue> ' + self.touch_file('2019-10-01T24.59.01 foo.txt'), self.call_omit_drawers()[0])

    def test_wrong_timestamp_in_day1(self):
        self.assertEqual('** ' + self.touch_file('2019-10-00T23.59.59 foo.txt'), self.call_omit_drawers()[0])

    def test_wrong_timestamp_in_day2(self):
        self.assertEqual('** ' + self.touch_file('2019-10-32T23.59.59 foo.txt'), self.call_omit_drawers()[0])

    def test_wrong_timestamp_in_day3(self):
        self.assertEqual('** ' + self.touch_file('2019-04-31T23.59.59 foo.txt'), self.call_omit_drawers()[0])

    def test_wrong_timestamp_in_month1(self):
        self.assertEqual('** ' + self.touch_file('2019-00-30T23.59.59 foo.txt'), self.call_omit_drawers()[0])

    def test_wrong_timestamp_in_month2(self):
        self.assertEqual('** ' + self.touch_file('2019-13-30T23.59.59 foo.txt'), self.call_omit_drawers()[0])

    #######################################################################

#    def test_duration_case_dashdash(self):
#        self.assertEqual('** <2019-10-03 Thu 09:55>--<2019-10-05 Sat 17:59> ' + self.touch_file('2019-10-03T09.55.00--2019-10-05T17.59.59 foo.txt'), self.call_omit_drawers()[0])
#
#    def test_duration_case_dash(self):
#        self.assertEqual('** <2019-10-03 Thu 09:55>--<2019-10-05 Sat 17:59> ' + self.touch_file('2019-10-03T09.55.00-2019-10-05T17.59.59 foo.txt'), self.call_omit_drawers()[0])
#
#    def test_duration_timestamp_with_no_second_dashdash(self):
#        self.assertEqual('** <2019-10-03 Thu 09:55>--<2019-10-05 Sat 17:59> ' + self.touch_file('2019-10-03T09.55--2019-10-05T17.59 foo.txt'), self.call_omit_drawers()[0])
#
#    def test_duration_timestamp_with_no_second_dash(self):
#        self.assertEqual('** <2019-10-03 Thu 09:55>--<2019-10-05 Sat 17:59> ' + self.touch_file('2019-10-03T09.55-2019-10-05T17.59 foo.txt'), self.call_omit_drawers()[0])
#
#    def test_duration_datestamp_dashdash(self):
#        self.assertEqual('** <2019-10-02 Wed>--<2019-10-05 Sat> ' + self.touch_file('2019-10-02--2019-10-05 foo.txt'), self.call_omit_drawers()[0])
#
#    def test_duration_datestamp_dash(self):
#        self.assertEqual('** <2019-10-02 Wed>--<2019-10-05 Sat> ' + self.touch_file('2019-10-02-2019-10-05 foo.txt'), self.call_omit_drawers()[0])

    # FIXXME: tests with mixed time- and day-stamps + different order

    #######################################################################

    def call_force_file_date_extraction(self):
        argv = "--force-file-date-extraction --suppress-messages --omit-drawers --folder " + self._tmp_dir
        memacs = FileNameTimeStamps(argv=argv.split())
        return memacs.test_get_entries()

    def test_force_file_date_extraction(self):
        today_weekday = datetime.datetime.now().strftime('<%Y-%m-%d %a %H:%M> ')  # FIXXME: dependency on current locale: works only with English weekdays
        self.assertEqual('** ' + today_weekday + self.touch_file('2019-10-01T23.59.59 foo.txt'), self.call_force_file_date_extraction()[0])

    #######################################################################

    def call_skip_file_time_extraction(self):
        argv = "--skip-file-time-extraction --suppress-messages --omit-drawers --folder " + self._tmp_dir
        memacs = FileNameTimeStamps(argv=argv.split())
        return memacs.test_get_entries()

    def test_skip_file_time_extraction(self):
        today_weekday = datetime.datetime.now().strftime('<%Y-%m-%d %a> ')  # FIXXME: dependency on current locale: works only with English weekdays
        today_day = datetime.datetime.now().strftime('%Y-%m-%d')
        self.assertEqual('** ' + today_weekday + self.touch_file(today_day + ' foo.txt'), self.call_skip_file_time_extraction()[0])

    #######################################################################

    def call_inactive_time_stamps(self):
        argv = "--inactive-time-stamps --suppress-messages --omit-drawers --folder " + self._tmp_dir
        memacs = FileNameTimeStamps(argv=argv.split())
        return memacs.test_get_entries()

    def test_inactive_time_stamps_good_case(self):
        self.assertEqual('** [2019-10-03 Thu 09:55] ' + self.touch_file('2019-10-03T09.55.00 foo.txt'), self.call_inactive_time_stamps()[0])

    def test_inactive_time_stamps_good_timestamp_with_no_second(self):
        self.assertEqual('** [2019-10-03 Thu 09:55] ' + self.touch_file('2019-10-03T09.55 foo.txt'), self.call_inactive_time_stamps()[0])

    def test_inactive_time_stamps_good_datestamp(self):
        self.assertEqual('** [2019-10-02 Wed] ' + self.touch_file('2019-10-02 foo.txt'), self.call_inactive_time_stamps()[0])

    def test_inactive_time_stamps_good_datestamp_with_determining_time_from_file(self):
        # FIXXME: caveat: this adds some tiny dependency: if the
        # minute changes between the file creation and the check, this
        # test fails
        today_weekday = datetime.datetime.now().strftime('[%Y-%m-%d %a %H:%M] ')  # FIXXME: dependency on current locale: works only with English weekdays
        today_day = datetime.datetime.now().strftime('%Y-%m-%d')
        self.assertEqual('** ' + today_weekday + self.touch_file(today_day + ' foo.txt'), self.call_inactive_time_stamps()[0])

    def test_inactive_time_stamps_good_datestamp_without_month(self):
        self.assertEqual('** [2019-10-01 Tue] ' + self.touch_file('2019-10 foo.txt'), self.call_inactive_time_stamps()[0])

    def test_inactive_time_stamps_good_case_with_seconds(self):
        self.assertEqual('** [2019-10-03 Thu 09:55] ' + self.touch_file('2019-10-03T09.55.00 foo.txt'), self.call_inactive_time_stamps()[0])

    def test_inactive_time_stamps_good_case_without_datestamp(self):
        self.assertEqual('** ' + self.touch_file('foo.txt'), self.call_inactive_time_stamps()[0])

    #######################################################################

    def call_active_time_stamps(self):
        argv = "--suppress-messages --omit-drawers --folder " + self._tmp_dir
        memacs = FileNameTimeStamps(argv=argv.split())
        return memacs.test_get_entries()

    def test_active_time_stamps_good_case(self):
        self.assertEqual('** <2019-10-03 Thu 09:55> ' + self.touch_file('2019-10-03T09.55.00 foo.txt'), self.call_active_time_stamps()[0])

    def test_active_time_stamps_good_timestamp_with_no_second(self):
        self.assertEqual('** <2019-10-03 Thu 09:55> ' + self.touch_file('2019-10-03T09.55 foo.txt'), self.call_active_time_stamps()[0])

    def test_active_time_stamps_good_datestamp(self):
        self.assertEqual('** <2019-10-02 Wed> ' + self.touch_file('2019-10-02 foo.txt'), self.call_active_time_stamps()[0])

    def test_active_time_stamps_good_datestamp_with_determining_time_from_file(self):
        # FIXXME: caveat: this adds some tiny dependency: if the
        # minute changes between the file creation and the check, this
        # test fails
        today_weekday = datetime.datetime.now().strftime('<%Y-%m-%d %a %H:%M> ')  # FIXXME: dependency on current locale: works only with English weekdays
        today_day = datetime.datetime.now().strftime('%Y-%m-%d')
        self.assertEqual('** ' + today_weekday + self.touch_file(today_day + ' foo.txt'), self.call_active_time_stamps()[0])

    def test_active_time_stamps_good_datestamp_without_day(self):
        self.assertEqual('** <2019-10-01 Tue> ' + self.touch_file('2019-10 foo.txt'), self.call_active_time_stamps()[0])

    def test_active_time_stamps_good_case_with_seconds(self):
        self.assertEqual('** <2019-10-03 Thu 09:55> ' + self.touch_file('2019-10-03T09.55.00 foo.txt'), self.call_active_time_stamps()[0])

    def test_active_time_stamps_good_case_without_datestamp(self):
        self.assertEqual('** ' + self.touch_file('foo.txt'), self.call_active_time_stamps()[0])

    #######################################################################

    # Disabled for now due to a KNOWN BUG: see https://github.com/novoid/Memacs/issues/92 -> FIXXME

    # def call_add_to_time_stamps(self):
    #     argv = "--add-to-time-stamps \"+2\" --suppress-messages --omit-drawers --folder " + self._tmp_dir
    #     memacs = FileNameTimeStamps(argv=argv.split())
    #     return memacs.test_get_entries()
    #
    # def test_add_to_time_stamps_good_case(self):
    #     self.assertEqual('** <2019-10-03 Thu 11:55> ' + self.touch_file('2019-10-03T09.55.00 foo.txt'), self.call_add_to_time_stamps()[0])
    #
    # def test_add_to_time_stamps_good_timestamp_with_no_second(self):
    #     self.assertEqual('** <2019-10-03 Thu 11:55> ' + self.touch_file('2019-10-03T09.55 foo.txt'), self.call_add_to_time_stamps()[0])
    #
    # def test_add_to_time_stamps_good_datestamp(self):
    #     self.assertEqual('** <2019-10-02 Wed> ' + self.touch_file('2019-10-02 foo.txt'), self.call_add_to_time_stamps()[0])

    #######################################################################

    def call_basic(self):
        """
        Invokes the filenametimestamp module with basic parameters resulting in drawers with IDs
        """
        argv = "--suppress-messages --folder " + self._tmp_dir
        memacs = FileNameTimeStamps(argv=argv.split())
        return memacs.test_get_entries()

    def test_functional_with_drawer(self):
        link = self.touch_file('2011-12-19T23.59.12_test1.txt')
        entry = "** <2011-12-19 Mon 23:59> " + link
        data = self.call_basic()

        self.assertEqual(data[0], entry)
        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[2].strip()[:4], ":ID:")
        self.assertEqual(data[3], "   :END:")

    def test_functional_with_unusual_year_with_drawer(self):
        link = self.touch_file('1971-12-30T00.01.01_P1000286.jpg')
        entry = "** <1971-12-30 Thu 00:01> " + link
        data = self.call_basic()

        self.assertEqual(data[0], entry)
        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[2].strip()[:4], ":ID:")
        self.assertEqual(data[3], "   :END:")

    def test_year_out_of_range_with_drawer(self):
        link = self.touch_file('1899-12-30T00.00.00_P1000286.jpg')
        entry = "** " + link
        data = self.call_basic()

        self.assertEqual(data[0], entry)
        self.assertEqual(data[1], "   :PROPERTIES:")
        self.assertEqual(data[2].strip()[:4], ":ID:")
        self.assertEqual(data[3], "   :END:")

    #######################################################################

    # Testing private methods is considered a bad thing to do:
    # https://stackoverflow.com/questions/105007/should-i-test-private-methods-or-only-public-ones/47401015#47401015
    # Here, I deliberately decide to test private methods as well
    # since their failure would be complicated to test from the
    # public methods alone.
    # Still, their semantic is that way that they are not part of
    # the public method API of the class.

    def test__check_datestamp_correctness(self):
        argv = "--suppress-messages --omit-drawers --folder " + self._tmp_dir
        memacs = FileNameTimeStamps(argv=argv.split())
        self.assertTrue(memacs._FileNameTimeStamps__check_datestamp_correctness('2019-12-31'))
        self.assertTrue(memacs._FileNameTimeStamps__check_datestamp_correctness('2000-01-01'))
        self.assertFalse(memacs._FileNameTimeStamps__check_datestamp_correctness('1999-00-01'))
        self.assertFalse(memacs._FileNameTimeStamps__check_datestamp_correctness('1999-01-00'))
        self.assertFalse(memacs._FileNameTimeStamps__check_datestamp_correctness('1999-13-00'))
        self.assertFalse(memacs._FileNameTimeStamps__check_datestamp_correctness('1999-12-32'))
        self.assertFalse(memacs._FileNameTimeStamps__check_datestamp_correctness('abc'))
        self.assertFalse(memacs._FileNameTimeStamps__check_datestamp_correctness(''))
        self.assertFalse(memacs._FileNameTimeStamps__check_datestamp_correctness('1'))
        self.assertFalse(memacs._FileNameTimeStamps__check_datestamp_correctness('1-2-3'))
        self.assertFalse(memacs._FileNameTimeStamps__check_datestamp_correctness('2000-2-3'))

    def test__check_timestamp_correctness(self):
        argv = "--suppress-messages --omit-drawers --folder " + self._tmp_dir
        memacs = FileNameTimeStamps(argv=argv.split())
        self.assertTrue(memacs._FileNameTimeStamps__check_timestamp_correctness('00:00'))
        self.assertTrue(memacs._FileNameTimeStamps__check_timestamp_correctness('23:59'))
        self.assertFalse(memacs._FileNameTimeStamps__check_timestamp_correctness('1:2'))
        self.assertFalse(memacs._FileNameTimeStamps__check_timestamp_correctness('12:2'))
        self.assertFalse(memacs._FileNameTimeStamps__check_timestamp_correctness('1:23'))
        self.assertFalse(memacs._FileNameTimeStamps__check_timestamp_correctness(''))
        self.assertFalse(memacs._FileNameTimeStamps__check_timestamp_correctness('abcde'))
        self.assertFalse(memacs._FileNameTimeStamps__check_timestamp_correctness('ab:cd'))
        self.assertFalse(memacs._FileNameTimeStamps__check_timestamp_correctness('24:00'))
        self.assertFalse(memacs._FileNameTimeStamps__check_timestamp_correctness('23:61'))
        self.assertFalse(memacs._FileNameTimeStamps__check_timestamp_correctness('12.34'))
        self.assertFalse(memacs._FileNameTimeStamps__check_timestamp_correctness('a'))
