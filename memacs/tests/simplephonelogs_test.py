#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-08 16:25:48 vk>

import unittest
import time
import datetime
import os
from memacs.simplephonelogs import SimplePhoneLogsMemacs
from memacs.lib.reader import CommonReader
#from memacs.lib.orgformat import OrgFormat
#from memacs.lib.orgformat import TimestampParseException

class TestSimplePhoneLogs(unittest.TestCase):

    ## FIXXME: (Note) These test are *not* exhaustive unit tests. They only 
    ##         show the usage of the methods. Please add "mean" test cases and
    ##         borderline cases!

    logmodule = False

    def setUp(self):

        self.test_file = os.path.dirname(
            os.path.abspath(__file__)) + os.sep + "tmp" \
            + os.path.sep + "sample-phonelog.csv"

        self.argv = "-s -f " + self.test_file

        self.logmodule = SimplePhoneLogsMemacs(argv = self.argv.split())


    def test_all(self):

        self.assertEqual(
            "foo",
            "foo")


    def test_determine_opposite_eventname(self):

        self.assertEqual(self.logmodule._determine_opposite_eventname(u"boot"), u'shutdown')
        self.assertEqual(self.logmodule._determine_opposite_eventname(u'shutdown'), u'boot')
        self.assertEqual(self.logmodule._determine_opposite_eventname(u'foo'), u'foo-end')
        self.assertEqual(self.logmodule._determine_opposite_eventname(u'foo-end'), u'foo')


    def test_generateOrgentry_basics(self):

        foobar_timestamp = datetime.datetime(1970, 1, 1, 0, 0)
        test_timestamp = datetime.datetime(2013, 4, 5, 13, 39)
        test_timestamp_last_opposite = False

        self.assertEqual(
            self.logmodule._generateOrgentry(test_timestamp,
                                             u"boot", '42', '612',
                                             test_timestamp_last_opposite,
                                             foobar_timestamp),
            (u'** <2013-04-05 Fri 13:39> boot\n' + \
                u':PROPERTIES:\n' + \
                u':IN-BETWEEN: \n' + \
                u':IN-BETWEEN-S: \n' + \
                u':BATT-LEVEL: 42\n' + \
                u':UPTIME: 0:10:12\n' + \
                u':UPTIME-S: 612\n' + \
                u':END:\n', False))

        test_timestamp_last_opposite = datetime.datetime(2013, 4, 5, 13, 30)

        self.assertEqual(
            self.logmodule._generateOrgentry(test_timestamp,
                                             u"boot", '42', '612',
                                             test_timestamp_last_opposite,
                                             foobar_timestamp),
            (u'** <2013-04-05 Fri 13:39> boot (off for 0:09:00)\n' + \
                u':PROPERTIES:\n' + \
                u':IN-BETWEEN: 0:09:00\n' + \
                u':IN-BETWEEN-S: 540\n' + \
                u':BATT-LEVEL: 42\n' + \
                u':UPTIME: 0:10:12\n' + \
                u':UPTIME-S: 612\n' + \
                u':END:\n', False))



    def test_generateOrgentry_crashrecognition(self):

        test_timestamp_last_opposite = datetime.datetime(2013, 4, 5, 13, 25)  ## shutdown
        test_timestamp_last = datetime.datetime(2013, 4, 5, 13, 30)  ## boot
        test_timestamp = datetime.datetime(2013, 4, 5, 13, 39)  ## boot

        self.assertEqual(
            self.logmodule._generateOrgentry(test_timestamp,
                                             u"boot", '42', '612',
                                             test_timestamp_last_opposite,
                                             test_timestamp_last),
            (u'** <2013-04-05 Fri 13:39> boot after crash\n' + \
                u':PROPERTIES:\n' + \
                u':IN-BETWEEN: \n' + \
                u':IN-BETWEEN-S: \n' + \
                u':BATT-LEVEL: 42\n' + \
                u':UPTIME: 0:10:12\n' + \
                u':UPTIME-S: 612\n' + \
                u':END:\n', True))




    def test_parser(self):

        ## at the beginning, internal object variables ought to be empty
        self.assertEqual(self.logmodule.phonelogfile_content, u'')
        self.assertEqual(self.logmodule.orgmode_result, u'')

        self.logmodule.phonelogfile_content = CommonReader.get_data_from_file(self.test_file)

        ## after reading in, content should be in object var:
        self.assertNotEqual(self.logmodule.phonelogfile_content, u'')
        self.assertEqual(self.logmodule.orgmode_result, u'')

        self.logmodule._parse_data()

        ## after parsing, org-mode results should be not empty
        self.assertNotEqual(self.logmodule.phonelogfile_content, u'')
        self.assertNotEqual(self.logmodule.orgmode_result, u'')

        ## self.test_file_result is defined below!
        self.assertEqual(self.logmodule.orgmode_result, self.test_file_result)

    def tearDown(self):
        #print self.logmodule.orgmode_result
        pass

    maxDiff = None  ## show also large diff

    test_file_result = u"""** <2012-11-20 Tue 11:56> boot
:PROPERTIES:
:IN-BETWEEN: 
:IN-BETWEEN-S: 
:BATT-LEVEL: 89
:UPTIME: 1:51:32
:UPTIME-S: 6692
:END:
** <2012-11-20 Tue 11:56> boot
:PROPERTIES:
:IN-BETWEEN: 
:IN-BETWEEN-S: 
:BATT-LEVEL: 89
:UPTIME: 1:51:34
:UPTIME-S: 6694
:END:
** <2012-11-20 Tue 19:59> shutdown (on for 8:03:00)
:PROPERTIES:
:IN-BETWEEN: 8:03:00
:IN-BETWEEN-S: 28980
:BATT-LEVEL: 72
:UPTIME: 9:54:42
:UPTIME-S: 35682
:END:
** <2012-11-20 Tue 21:32> boot (off for 1:33:00)
:PROPERTIES:
:IN-BETWEEN: 1:33:00
:IN-BETWEEN-S: 5580
:BATT-LEVEL: 71
:UPTIME: 0:01:57
:UPTIME-S: 117
:END:
** <2012-11-20 Tue 23:52> shutdown (on for 2:20:00)
:PROPERTIES:
:IN-BETWEEN: 2:20:00
:IN-BETWEEN-S: 8400
:BATT-LEVEL: 63
:UPTIME: 2:22:04
:UPTIME-S: 8524
:END:
** <2012-11-21 Wed 07:23> boot (off for 7:31:00)
:PROPERTIES:
:IN-BETWEEN: 7:31:00
:IN-BETWEEN-S: 27060
:BATT-LEVEL: 100
:UPTIME: 0:01:55
:UPTIME-S: 115
:END:
** <2012-11-21 Wed 07:52> wifi-home
:PROPERTIES:
:IN-BETWEEN: 
:IN-BETWEEN-S: 
:BATT-LEVEL: 95
:UPTIME: 0:31:19
:UPTIME-S: 1879
:END:
** <2012-11-21 Wed 08:17> wifi-home-end (home for 0:25:00)
:PROPERTIES:
:IN-BETWEEN: 0:25:00
:IN-BETWEEN-S: 1500
:BATT-LEVEL: 92
:UPTIME: 0:56:18
:UPTIME-S: 3378
:END:
** <2012-11-21 Wed 13:06> boot after crash
:PROPERTIES:
:IN-BETWEEN: 
:IN-BETWEEN-S: 
:BATT-LEVEL: 77
:UPTIME: 0:02:04
:UPTIME-S: 124
:END:
** <2012-11-21 Wed 21:08> wifi-home (not home for 12:51:00)
:PROPERTIES:
:IN-BETWEEN: 12:51:00
:IN-BETWEEN-S: 46260
:BATT-LEVEL: 50
:UPTIME: 8:03:53
:UPTIME-S: 29033
:END:
** <2012-11-22 Thu 00:12> shutdown (on for 16:49:00)
:PROPERTIES:
:IN-BETWEEN: 16:49:00
:IN-BETWEEN-S: 60540
:BATT-LEVEL: 39
:UPTIME: 11:08:09
:UPTIME-S: 40089
:END:
** <2012-11-29 Thu 08:47> boot (off for 176:35:00)
:PROPERTIES:
:IN-BETWEEN: 176:35:00
:IN-BETWEEN-S: 635700
:BATT-LEVEL: 100
:UPTIME: 0:01:54
:UPTIME-S: 114
:END:
** <2012-11-29 Thu 08:48> wifi-home (not home for 192:31:00)
:PROPERTIES:
:IN-BETWEEN: 192:31:00
:IN-BETWEEN-S: 693060
:BATT-LEVEL: 100
:UPTIME: 0:01:58
:UPTIME-S: 118
:END:
** <2012-11-29 Thu 09:41> wifi-home-end (home for 0:53:00)
:PROPERTIES:
:IN-BETWEEN: 0:53:00
:IN-BETWEEN-S: 3180
:BATT-LEVEL: 98
:UPTIME: 0:55:17
:UPTIME-S: 3317
:END:
** <2012-11-29 Thu 14:46> wifi-office
:PROPERTIES:
:IN-BETWEEN: 
:IN-BETWEEN-S: 
:BATT-LEVEL: 81
:UPTIME: 6:00:33
:UPTIME-S: 21633
:END:
** <2012-11-29 Thu 16:15> wifi-home (not home for 6:34:00)
:PROPERTIES:
:IN-BETWEEN: 6:34:00
:IN-BETWEEN-S: 23640
:BATT-LEVEL: 76
:UPTIME: 7:29:15
:UPTIME-S: 26955
:END:
** <2012-11-29 Thu 17:04> wifi-home-end (home for 0:49:00)
:PROPERTIES:
:IN-BETWEEN: 0:49:00
:IN-BETWEEN-S: 2940
:BATT-LEVEL: 74
:UPTIME: 8:18:32
:UPTIME-S: 29912
:END:
** <2012-11-29 Thu 23:31> shutdown (on for 14:44:00)
:PROPERTIES:
:IN-BETWEEN: 14:44:00
:IN-BETWEEN-S: 53040
:BATT-LEVEL: 48
:UPTIME: 14:45:46
:UPTIME-S: 53146
:END:
"""

# Local Variables:
# mode: flyspell
# eval: (ispell-change-dictionary "en_US")
# End:
