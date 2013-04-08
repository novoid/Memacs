#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-08 19:08:31 vk>

import unittest
import time
import datetime
import os
from memacs.simplephonelogs import SimplePhoneLogsMemacs
from memacs.lib.reader import CommonReader


class TestSimplePhoneLogs(unittest.TestCase):

    ## FIXXME: (Note) These test are *not* exhaustive unit tests. They only 
    ##         show the usage of the methods. Please add "mean" test cases and
    ##         borderline cases!

    logmodule = False

    def setUp(self):

        result_file = os.path.dirname(
            os.path.abspath(__file__)) + os.path.sep + "sample-phonelog-result-TEMP.org"

        self.test_file = os.path.dirname(
            os.path.abspath(__file__)) + os.sep + "tmp" \
            + os.path.sep + "sample-phonelog.csv"

        self.argv = "-s -f " + self.test_file + " --output " + result_file

        self.logmodule = SimplePhoneLogsMemacs(argv = self.argv.split())
        self.logmodule.handle_main()


    def test_all(self):

        pass


    def test_determine_opposite_eventname(self):

        self.assertEqual(self.logmodule._determine_opposite_eventname(u"boot"), u'shutdown')
        self.assertEqual(self.logmodule._determine_opposite_eventname(u'shutdown'), u'boot')
        self.assertEqual(self.logmodule._determine_opposite_eventname(u'foo'), u'foo-end')
        self.assertEqual(self.logmodule._determine_opposite_eventname(u'foo-end'), u'foo')


    def NOtest_generateOrgentry_basics(self):

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



    def NOtest_generateOrgentry_crashrecognition(self):

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

        result_file = os.path.dirname(
            os.path.abspath(__file__)) + os.path.sep + "sample-phonelog-result-TEMP.org"

        argv = "-f " + self.test_file + \
            " --output " + result_file

        localmodule = SimplePhoneLogsMemacs(argv = argv.split())
        localmodule.handle_main()

        result_from_module = CommonReader.get_data_from_file(result_file)

        result_from_module_without_header_and_last_line = u''
        for line in result_from_module.split('\n'):
            if line.startswith(u'* successfully parsed ') or \
                    line.startswith(u'#') or \
                    line.startswith(u'* '):
                pass
            else:
                result_from_module_without_header_and_last_line += line + '\n'

        ## self.reference_result is defined below!
        self.assertEqual(result_from_module_without_header_and_last_line, self.reference_result)
        
        os.remove(result_file)



    def tearDown(self):
        #print self.logmodule.orgmode_result
        pass

    maxDiff = None  ## show also large diff

    reference_result = u"""** <2012-11-20 Tue 11:56> boot
   :PROPERTIES:
   :IN-BETWEEN:   
   :BATT-LEVEL:   89
   :UPTIME:       1:51:32
   :UPTIME-S:     6692
   :IN-BETWEEN-S: 
   :ID:           746417eaaf657df53a744aa10bc925fef8b7901b
   :END:

** <2012-11-20 Tue 11:56> boot
   :PROPERTIES:
   :IN-BETWEEN:   
   :BATT-LEVEL:   89
   :UPTIME:       1:51:34
   :UPTIME-S:     6694
   :IN-BETWEEN-S: 
   :ID:           2da1bc746cdb4ca6f1a4d5c77673212d8a9ff762
   :END:

** <2012-11-20 Tue 19:59> shutdown (on for 8:03:00)
   :PROPERTIES:
   :IN-BETWEEN:   8:03:00
   :BATT-LEVEL:   72
   :UPTIME:       9:54:42
   :UPTIME-S:     35682
   :IN-BETWEEN-S: 28980
   :ID:           49ac414c512872a3d29465f41fd65a9e31f70ab2
   :END:

** <2012-11-20 Tue 21:32> boot (off for 1:33:00)
   :PROPERTIES:
   :IN-BETWEEN:   1:33:00
   :BATT-LEVEL:   71
   :UPTIME:       0:01:57
   :UPTIME-S:     117
   :IN-BETWEEN-S: 5580
   :ID:           3220003537db597474a361e023f2e610fd8437fc
   :END:

** <2012-11-20 Tue 23:52> shutdown (on for 2:20:00)
   :PROPERTIES:
   :IN-BETWEEN:   2:20:00
   :BATT-LEVEL:   63
   :UPTIME:       2:22:04
   :UPTIME-S:     8524
   :IN-BETWEEN-S: 8400
   :ID:           9b2addfa63569cddd56d8c725177948568368834
   :END:

** <2012-11-21 Wed 07:23> boot (off for 7:31:00)
   :PROPERTIES:
   :IN-BETWEEN:   7:31:00
   :BATT-LEVEL:   100
   :UPTIME:       0:01:55
   :UPTIME-S:     115
   :IN-BETWEEN-S: 27060
   :ID:           03547e5c9ea339b2a4350021a1c180161ba0324e
   :END:

** <2012-11-21 Wed 07:52> wifi-home
   :PROPERTIES:
   :IN-BETWEEN:   
   :BATT-LEVEL:   95
   :UPTIME:       0:31:19
   :UPTIME-S:     1879
   :IN-BETWEEN-S: 
   :ID:           9a65cf95dcf23a2a5add2238888cc7158e8615b6
   :END:

** <2012-11-21 Wed 08:17> wifi-home-end (home for 0:25:00)
   :PROPERTIES:
   :IN-BETWEEN:   0:25:00
   :BATT-LEVEL:   92
   :UPTIME:       0:56:18
   :UPTIME-S:     3378
   :IN-BETWEEN-S: 1500
   :ID:           d600d9aeddde8a0a8109c5b2def1091b46ecb2ab
   :END:

** <2012-11-21 Wed 13:06> boot after crash
   :PROPERTIES:
   :IN-BETWEEN:   
   :BATT-LEVEL:   77
   :UPTIME:       0:02:04
   :UPTIME-S:     124
   :IN-BETWEEN-S: 
   :ID:           70ccb21b1c0e75e93fcdc70d1eed5c24c5657074
   :END:

** <2012-11-21 Wed 21:08> wifi-home (not home for 12:51:00)
   :PROPERTIES:
   :IN-BETWEEN:   12:51:00
   :BATT-LEVEL:   50
   :UPTIME:       8:03:53
   :UPTIME-S:     29033
   :IN-BETWEEN-S: 46260
   :ID:           300798be8d2f9182995f823667122622e71298b4
   :END:

** <2012-11-22 Thu 00:12> shutdown (on for 16:49:00)
   :PROPERTIES:
   :IN-BETWEEN:   16:49:00
   :BATT-LEVEL:   39
   :UPTIME:       11:08:09
   :UPTIME-S:     40089
   :IN-BETWEEN-S: 60540
   :ID:           050e9723a23cd063e869ae7464a2a6a9e878055a
   :END:

** <2012-11-29 Thu 08:47> boot (off for 7d 8:35:00)
   :PROPERTIES:
   :IN-BETWEEN:   176:35:00
   :BATT-LEVEL:   100
   :UPTIME:       0:01:54
   :UPTIME-S:     114
   :IN-BETWEEN-S: 635700
   :ID:           b3ae1a136db220c283607a9e16c9828aa246f6be
   :END:

** <2012-11-29 Thu 08:48> wifi-home (not home for 8d 0:31:00)
   :PROPERTIES:
   :IN-BETWEEN:   192:31:00
   :BATT-LEVEL:   100
   :UPTIME:       0:01:58
   :UPTIME-S:     118
   :IN-BETWEEN-S: 693060
   :ID:           ab3e1a1af54520f76470ec6a26ca6879eafb67dc
   :END:

** <2012-11-29 Thu 09:41> wifi-home-end (home for 0:53:00)
   :PROPERTIES:
   :IN-BETWEEN:   0:53:00
   :BATT-LEVEL:   98
   :UPTIME:       0:55:17
   :UPTIME-S:     3317
   :IN-BETWEEN-S: 3180
   :ID:           0b105cc35f0df367357e25c5c87061e61c132321
   :END:

** <2012-11-29 Thu 14:46> wifi-office
   :PROPERTIES:
   :IN-BETWEEN:   
   :BATT-LEVEL:   81
   :UPTIME:       6:00:33
   :UPTIME-S:     21633
   :IN-BETWEEN-S: 
   :ID:           7e9e6f886f4b6445cb7bb2046dfe8bfc1fc787ff
   :END:

** <2012-11-29 Thu 16:15> wifi-home (not home for 6:34:00)
   :PROPERTIES:
   :IN-BETWEEN:   6:34:00
   :BATT-LEVEL:   76
   :UPTIME:       7:29:15
   :UPTIME-S:     26955
   :IN-BETWEEN-S: 23640
   :ID:           3118600d6f3c8e14cad6ae718b1e37303f19b95a
   :END:

** <2012-11-29 Thu 17:04> wifi-home-end (home for 0:49:00)
   :PROPERTIES:
   :IN-BETWEEN:   0:49:00
   :BATT-LEVEL:   74
   :UPTIME:       8:18:32
   :UPTIME-S:     29912
   :IN-BETWEEN-S: 2940
   :ID:           05a37ed12bb8968ea200b966d8d50568221d180d
   :END:

** <2012-11-29 Thu 23:31> shutdown (on for 14:44:00)
   :PROPERTIES:
   :IN-BETWEEN:   14:44:00
   :BATT-LEVEL:   48
   :UPTIME:       14:45:46
   :UPTIME-S:     53146
   :IN-BETWEEN-S: 53040
   :ID:           1388ccd5e0c9a54e166b41be1431eae18b6c5031
   :END:


"""


# Local Variables:
# mode: flyspell
# eval: (ispell-change-dictionary "en_US")
# End:
