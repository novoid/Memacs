#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2013-09-16 19:13:46 vk>

import unittest
import time
import datetime
import os
from memacs.simplephonelogs import SimplePhoneLogsMemacs
from memacs.lib.reader import CommonReader

## FIXXME: (Note) These test are *not* exhaustive unit tests. They only 
##         show the usage of the methods. Please add "mean" test cases and
##         borderline cases!


class TestSimplePhoneLogs_Basics(unittest.TestCase):

    argv = False
    logmodule = False
    input_file = False
    result_file = False
    maxDiff = None  ## show also large diff

    def setUp(self):

        self.result_file = os.path.dirname(
            os.path.abspath(__file__)) + os.path.sep + "phonelog-result-TEMP-DELETEME.org"

        self.input_file = os.path.dirname(
            os.path.abspath(__file__)) + os.path.sep + "phonelog-input-TEMP-DELETEME.csv"

        self.argv = "--suppress-messages --file " + self.input_file + " --output " + self.result_file



    def tearDown(self):

        os.remove(self.result_file)
        os.remove(self.input_file)


    def get_result_from_file(self):
        """reads out the resulting file and returns its content
        without header lines, main heading, last finish message, and
        empty lines"""

        result_from_module = CommonReader.get_data_from_file(self.result_file)

        result_from_module_without_header_and_last_line = u''

        ## remove header and last line (which includes execution-specific timing)
        for line in result_from_module.split('\n'):
            if line.startswith(u'* successfully parsed ') or \
                    line.startswith(u'#') or \
                    line.startswith(u'* ') or \
                    line == u'':
                pass
            else:
                result_from_module_without_header_and_last_line += line + '\n'

        return result_from_module_without_header_and_last_line


    def test_boot_without_shutdown(self):

        with open(self.input_file, 'w') as inputfile:
            inputfile.write('2013-04-05 # 13.39 # boot # 42 # 612\n')

        self.logmodule = SimplePhoneLogsMemacs(argv = self.argv.split())
        self.logmodule.handle_main()

        result = self.get_result_from_file()

        self.assertEqual(result, u"""** <2013-04-05 Fri 13:39> boot
   :PROPERTIES:
   :IN-BETWEEN:   
   :BATT-LEVEL:   42
   :UPTIME:       0:10:12
   :UPTIME-S:     612
   :IN-BETWEEN-S: 
   :ID:           50f3642555b86335789cc0850ee02652765b30a8
   :END:
""")


    def test_shutdown_with_boot(self):

        with open(self.input_file, 'w') as inputfile:
            inputfile.write('1970-01-01 # 00.01 # shutdown # 1 # 1\n' +
                            '2013-04-05 # 13.39 # boot # 42 # 612\n')

        self.logmodule = SimplePhoneLogsMemacs(argv = self.argv.split())
        self.logmodule.handle_main()

        result = self.get_result_from_file()

        self.assertEqual(result, u"""** <1970-01-01 Thu 00:01> shutdown
   :PROPERTIES:
   :IN-BETWEEN:   
   :BATT-LEVEL:   1
   :UPTIME:       0:00:01
   :UPTIME-S:     1
   :IN-BETWEEN-S: 
   :ID:           908b94cc00a0981c811f8392b85d4b5603476907
   :END:
** <2013-04-05 Fri 13:39> boot (off for 15800d 13:38:00)
   :PROPERTIES:
   :IN-BETWEEN:   379213:38:00
   :BATT-LEVEL:   42
   :UPTIME:       0:10:12
   :UPTIME-S:     612
   :IN-BETWEEN-S: 1365169080
   :ID:           0602b98ba31416e5ae7e2964455de121c7492a70
   :END:
""")
        

    def test_crashrecognition(self):


        with open(self.input_file, 'w') as inputfile:
            inputfile.write('2013-04-05 # 13.25 # shutdown # 1 # 10\n' +
                            '2013-04-05 # 13.30 # boot # 2 # 11\n' +
                            '2013-04-05 # 13.39 # boot # 3 # 12\n')

        self.logmodule = SimplePhoneLogsMemacs(argv = self.argv.split())
        self.logmodule.handle_main()

        result = self.get_result_from_file()

        self.assertEqual(result, u"""** <2013-04-05 Fri 13:25> shutdown
   :PROPERTIES:
   :IN-BETWEEN:   
   :BATT-LEVEL:   1
   :UPTIME:       0:00:10
   :UPTIME-S:     10
   :IN-BETWEEN-S: 
   :ID:           0ec0d92a33e4476756659fe6ca0ab78fc470747c
   :END:
** <2013-04-05 Fri 13:30> boot (off for 0:05:00)
   :PROPERTIES:
   :IN-BETWEEN:   0:05:00
   :BATT-LEVEL:   2
   :UPTIME:       0:00:11
   :UPTIME-S:     11
   :IN-BETWEEN-S: 300
   :ID:           5af2d989502a85deefc296936e9bf59087ecec2b
   :END:
** <2013-04-05 Fri 13:39> boot after crash
   :PROPERTIES:
   :IN-BETWEEN:   
   :BATT-LEVEL:   3
   :UPTIME:       0:00:12
   :UPTIME-S:     12
   :IN-BETWEEN-S: 
   :ID:           00903218ae1c5d02f79f9d527c5767dce580f10f
   :END:
""")







class TestSimplePhoneLogs_full_example_file(unittest.TestCase):

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


    def test_determine_opposite_eventname(self):

        self.assertEqual(self.logmodule._determine_opposite_eventname(u"boot"), u'shutdown')
        self.assertEqual(self.logmodule._determine_opposite_eventname(u'shutdown'), u'boot')
        self.assertEqual(self.logmodule._determine_opposite_eventname(u'foo'), u'foo-end')
        self.assertEqual(self.logmodule._determine_opposite_eventname(u'foo-end'), u'foo')


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

** <2013-09-10 Tue 07:00> boot (off for 284d 7:29:00)
   :PROPERTIES:
   :IN-BETWEEN:   6823:29:00
   :BATT-LEVEL:   100
   :UPTIME:       0:02:10
   :UPTIME-S:     130
   :IN-BETWEEN-S: 24564540
   :ID:           1ab501758e7c68e6ce9455dc0262cc66947b52a5
   :END:

** <2013-09-10 Tue 08:23> wifi-office
   :PROPERTIES:
   :IN-BETWEEN:   
   :BATT-LEVEL:   95
   :UPTIME:       1:23:16
   :UPTIME-S:     4996
   :IN-BETWEEN-S: 
   :ID:           721bed72de6ba9295e7e0c5ca26414b1cbc819b5
   :END:

** <2013-09-10 Tue 12:13> wifi-office-end (office for 3:50:00; today 3:50:00; today total 3:50:00)
   :PROPERTIES:
   :IN-BETWEEN:   3:50:00
   :BATT-LEVEL:   87
   :UPTIME:       5:13:46
   :UPTIME-S:     18826
   :IN-BETWEEN-S: 13800
   :ID:           c668c3a34c5b6e8260c8b512af4697079d48cdc0
   :END:

** <2013-09-10 Tue 12:59> wifi-office (not office for 0:46:00)
   :PROPERTIES:
   :IN-BETWEEN:   0:46:00
   :BATT-LEVEL:   85
   :UPTIME:       6:00:00
   :UPTIME-S:     21600
   :IN-BETWEEN-S: 2760
   :ID:           4b681ff00c7ce3a8475319c10488b5d623dfb451
   :END:

** <2013-09-10 Tue 17:46> wifi-office-end (office for 4:47:00; today 8:37:00; today total 9:23:00)
   :PROPERTIES:
   :IN-BETWEEN:   4:47:00
   :BATT-LEVEL:   73
   :UPTIME:       10:47:06
   :UPTIME-S:     38826
   :IN-BETWEEN-S: 17220
   :ID:           754e6caaa22dc067440d4e0336dc3fd9b58faf22
   :END:

** <2013-09-10 Tue 22:10> shutdown (on for 15:10:00)
   :PROPERTIES:
   :IN-BETWEEN:   15:10:00
   :BATT-LEVEL:   58
   :UPTIME:       15:10:38
   :UPTIME-S:     54638
   :IN-BETWEEN-S: 54600
   :ID:           e1fe490c7090ba02640e9f01bb6f29d7973fbb1d
   :END:

** <2013-09-11 Wed 12:15> boot (off for 14:05:00)
   :PROPERTIES:
   :IN-BETWEEN:   14:05:00
   :BATT-LEVEL:   87
   :UPTIME:       5:15:05
   :UPTIME-S:     18905
   :IN-BETWEEN-S: 50700
   :ID:           c135298c813b09d23150777f7fa82cd6070db427
   :END:

** <2013-09-11 Wed 13:19> wifi-office (not office for 19:33:00)
   :PROPERTIES:
   :IN-BETWEEN:   19:33:00
   :BATT-LEVEL:   82
   :UPTIME:       6:19:29
   :UPTIME-S:     22769
   :IN-BETWEEN-S: 70380
   :ID:           35b64d133eb69ff2527769b3f836a352a9918bea
   :END:

** <2013-09-11 Wed 18:55> wifi-office-end (office for 5:36:00; today 5:36:00; today total 5:36:00)
   :PROPERTIES:
   :IN-BETWEEN:   5:36:00
   :BATT-LEVEL:   69
   :UPTIME:       11:56:01
   :UPTIME-S:     42961
   :IN-BETWEEN-S: 20160
   :ID:           d67377260ad01ee8794224392c858b171ddfbf11
   :END:

** <2013-09-11 Wed 19:10> wifi-home (not home for 286d 2:06:00)
   :PROPERTIES:
   :IN-BETWEEN:   6866:06:00
   :BATT-LEVEL:   68
   :UPTIME:       12:10:46
   :UPTIME-S:     43846
   :IN-BETWEEN-S: 24717960
   :ID:           d3a6e6cc276d43ce021f391c2a7443f4cf2957b9
   :END:

** <2013-09-11 Wed 22:55> shutdown (on for 10:40:00)
   :PROPERTIES:
   :IN-BETWEEN:   10:40:00
   :BATT-LEVEL:   53
   :UPTIME:       15:55:23
   :UPTIME-S:     57323
   :IN-BETWEEN-S: 38400
   :ID:           740eab692eb65559a005511d8926546bd780d787
   :END:


"""


# Local Variables:
# mode: flyspell
# eval: (ispell-change-dictionary "en_US")
# End:
