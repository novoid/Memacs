#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2018-08-25 15:07:37 vk>

import os
import shutil
import tempfile
import unittest

from memacs.simplephonelogs import SimplePhoneLogsMemacs
from memacs.lib.reader import CommonReader

## FIXXME: (Note) These test are *not* exhaustive unit tests. They only
##         show the usage of the methods. Please add "mean" test cases and
##         borderline cases!


class PhoneLogsTestCase(unittest.TestCase):
    """ Base class for PhoneLogs test cases. """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.result_file = os.path.join(self.temp_dir, 'result.org')
        self.input_file = os.path.join(self.temp_dir, 'input.csv')

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def get_result_from_file(self):
        """reads out the resulting file and returns its content
        without header lines, main heading, last finish message, and
        empty lines"""

        result_from_module = CommonReader.get_data_from_file(self.result_file)

        result_from_module_without_header_and_last_line = ''

        ## remove header and last line (which includes execution-specific timing)
        for line in result_from_module.split('\n'):
            if line.startswith('* successfully parsed ') or \
                    line.startswith('#') or \
                    line.startswith('* '):
                pass
            else:
                line = line.rstrip()
                result_from_module_without_header_and_last_line += line + '\n'

        return result_from_module_without_header_and_last_line.strip()


class TestSimplePhoneLogsBasic(PhoneLogsTestCase):

    argv = False
    logmodule = False
    input_file = False
    result_file = False
    maxDiff = None  ## show also large diff

    def setUp(self):
        super(TestSimplePhoneLogsBasic, self).setUp()
        self.argv = "--suppress-messages --file " + self.input_file + " --output " + self.result_file

    def test_boot_without_shutdown(self):

        with open(self.input_file, 'w') as inputfile:
            inputfile.write('2013-04-05 # 13.39 # boot # 42 # 612\n')

        self.logmodule = SimplePhoneLogsMemacs(argv = self.argv.split())
        self.logmodule.handle_main()

        result = self.get_result_from_file()

        self.assertEqual(result, """** <2013-04-05 Fri 13:39> boot
   :PROPERTIES:
   :IN-BETWEEN:
   :IN-BETWEEN-S:
   :BATT-LEVEL:   42
   :UPTIME:       0:10:12
   :UPTIME-S:     612
   :ID:           0d78f4b2834126ecfc3fcf9cd45e5a077d055f0c
   :END:""")

    def test_shutdown_with_boot(self):

        with open(self.input_file, 'w') as inputfile:
            inputfile.write('1970-01-01 # 00.01 # shutdown # 1 # 1\n' +
                            '2013-04-05 # 13.39 # boot # 42 # 612\n')

        self.logmodule = SimplePhoneLogsMemacs(argv = self.argv.split())
        self.logmodule.handle_main()

        result = self.get_result_from_file()

        self.assertEqual(result, """** <1970-01-01 Thu 00:01> shutdown
   :PROPERTIES:
   :IN-BETWEEN:
   :IN-BETWEEN-S:
   :BATT-LEVEL:   1
   :UPTIME:       0:00:01
   :UPTIME-S:     1
   :ID:           ef7327b6c8f6e9de6ae6271d601f96133cd5b524
   :END:

** <2013-04-05 Fri 13:39> boot (off for 15800d 13:38:00)
   :PROPERTIES:
   :IN-BETWEEN:   379213:38:00
   :IN-BETWEEN-S: 1365169080
   :BATT-LEVEL:   42
   :UPTIME:       0:10:12
   :UPTIME-S:     612
   :ID:           ff09a7043203c0d9eeb116779789dc19a992e299
   :END:""")


    def test_crashrecognition(self):


        with open(self.input_file, 'w') as inputfile:
            inputfile.write('2013-04-05 # 13.25 # shutdown # 1 # 10\n' +
                            '2013-04-05 # 13.30 # boot # 2 # 11\n' +
                            '2013-04-05 # 13.39 # boot # 3 # 12\n')

        self.logmodule = SimplePhoneLogsMemacs(argv = self.argv.split())
        self.logmodule.handle_main()

        result = self.get_result_from_file()

        self.assertEqual(result, """** <2013-04-05 Fri 13:25> shutdown
   :PROPERTIES:
   :IN-BETWEEN:
   :IN-BETWEEN-S:
   :BATT-LEVEL:   1
   :UPTIME:       0:00:10
   :UPTIME-S:     10
   :ID:           5a5fd30fcf0bb105d3fcbf3471d343adb8a1c57d
   :END:

** <2013-04-05 Fri 13:30> boot (off for 0:05:00)
   :PROPERTIES:
   :IN-BETWEEN:   0:05:00
   :IN-BETWEEN-S: 300
   :BATT-LEVEL:   2
   :UPTIME:       0:00:11
   :UPTIME-S:     11
   :ID:           e70436685735120f1e468e1ea155cc370b6d69ad
   :END:

** <2013-04-05 Fri 13:39> boot after crash
   :PROPERTIES:
   :IN-BETWEEN:
   :IN-BETWEEN-S:
   :BATT-LEVEL:   3
   :UPTIME:       0:00:12
   :UPTIME-S:     12
   :ID:           dc41b7d0b6b415ff3a3335c1a4ad0e5ce36f5152
   :END:""")




class TestSimplePhoneLogsFull(PhoneLogsTestCase):

    logmodule = False

    def setUp(self):
        super(TestSimplePhoneLogsFull, self).setUp()
        self.test_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data', 'sample-phonelog.csv'
        )
        self.argv = "-s -f " + self.test_file + " --output " + self.result_file
        self.logmodule = SimplePhoneLogsMemacs(argv = self.argv.split())
        self.logmodule.handle_main()

    def test_determine_opposite_eventname(self):

        self.assertEqual(self.logmodule._determine_opposite_eventname("boot"), 'shutdown')
        self.assertEqual(self.logmodule._determine_opposite_eventname('shutdown'), 'boot')
        self.assertEqual(self.logmodule._determine_opposite_eventname('foo'), 'foo-end')
        self.assertEqual(self.logmodule._determine_opposite_eventname('foo-end'), 'foo')


    def test_parser(self):

        argv = "-f " + self.test_file + \
            " --output " + self.result_file

        localmodule = SimplePhoneLogsMemacs(argv = argv.split())
        localmodule.handle_main()

        result = self.get_result_from_file()
        self.assertEqual(result, self.reference_result)

    maxDiff = None  ## show also large diff

    reference_result = """** <2012-11-20 Tue 11:56> boot
   :PROPERTIES:
   :IN-BETWEEN:
   :IN-BETWEEN-S:
   :BATT-LEVEL:   89
   :UPTIME:       1:51:32
   :UPTIME-S:     6692
   :ID:           b63fd30ff638d906ab9e28def69dae29e126ff80
   :END:

** <2012-11-20 Tue 11:56> boot
   :PROPERTIES:
   :IN-BETWEEN:
   :IN-BETWEEN-S:
   :BATT-LEVEL:   89
   :UPTIME:       1:51:34
   :UPTIME-S:     6694
   :ID:           f2bc17a65a66f3b63623751cbfd772e75027be6f
   :END:

** <2012-11-20 Tue 19:59> shutdown (on for 8:03:00)
   :PROPERTIES:
   :IN-BETWEEN:   8:03:00
   :IN-BETWEEN-S: 28980
   :BATT-LEVEL:   72
   :UPTIME:       9:54:42
   :UPTIME-S:     35682
   :ID:           0c462b507e45a07e6cdb5b7339f2ab9d3c29d267
   :END:

** <2012-11-20 Tue 21:32> boot (off for 1:33:00)
   :PROPERTIES:
   :IN-BETWEEN:   1:33:00
   :IN-BETWEEN-S: 5580
   :BATT-LEVEL:   71
   :UPTIME:       0:01:57
   :UPTIME-S:     117
   :ID:           69733c4f4d9676c6dec41010afd0b55880ff6055
   :END:

** <2012-11-20 Tue 23:52> shutdown (on for 2:20:00)
   :PROPERTIES:
   :IN-BETWEEN:   2:20:00
   :IN-BETWEEN-S: 8400
   :BATT-LEVEL:   63
   :UPTIME:       2:22:04
   :UPTIME-S:     8524
   :ID:           193f1e38681a8b559ad21c52a7d883cd375c18e6
   :END:

** <2012-11-21 Wed 07:23> boot (off for 7:31:00)
   :PROPERTIES:
   :IN-BETWEEN:   7:31:00
   :IN-BETWEEN-S: 27060
   :BATT-LEVEL:   100
   :UPTIME:       0:01:55
   :UPTIME-S:     115
   :ID:           e869e7cc49d7aca1128ae0d6fc9651c69c5acb28
   :END:

** <2012-11-21 Wed 07:52> wifi-home
   :PROPERTIES:
   :IN-BETWEEN:
   :IN-BETWEEN-S:
   :BATT-LEVEL:   95
   :UPTIME:       0:31:19
   :UPTIME-S:     1879
   :ID:           4ff44273f4c79ea2d36d1eb637b1a1f6087f9a4a
   :END:

** <2012-11-21 Wed 08:17> wifi-home-end (home for 0:25:00)
   :PROPERTIES:
   :IN-BETWEEN:   0:25:00
   :IN-BETWEEN-S: 1500
   :BATT-LEVEL:   92
   :UPTIME:       0:56:18
   :UPTIME-S:     3378
   :ID:           7c10c6104b0de033661b6e7835d2006b730e624b
   :END:

** <2012-11-21 Wed 13:06> boot after crash
   :PROPERTIES:
   :IN-BETWEEN:
   :IN-BETWEEN-S:
   :BATT-LEVEL:   77
   :UPTIME:       0:02:04
   :UPTIME-S:     124
   :ID:           96e31802e4b176e060e008c0d934ff2e83f1d179
   :END:

** <2012-11-21 Wed 21:08> wifi-home (not home for 12:51:00)
   :PROPERTIES:
   :IN-BETWEEN:   12:51:00
   :IN-BETWEEN-S: 46260
   :BATT-LEVEL:   50
   :UPTIME:       8:03:53
   :UPTIME-S:     29033
   :ID:           7dacfb9e8480cd19a60e2e3a7c850ec9a73fc2d6
   :END:

** <2012-11-22 Thu 00:12> shutdown (on for 16:49:00)
   :PROPERTIES:
   :IN-BETWEEN:                  16:49:00
   :IN-BETWEEN-S:                60540
   :BATT-LEVEL:                  39
   :UPTIME:                      11:08:09
   :UPTIME-S:                    40089
   :HOURS_RUNTIME_EXTRAPOLATION: 29
   :ID:                          2d60fb40bfd9fe2da0b819c37246c4ecf6cf6f56
   :END:

** <2012-11-29 Thu 08:47> boot (off for 7d 8:35:00)
   :PROPERTIES:
   :IN-BETWEEN:   176:35:00
   :IN-BETWEEN-S: 635700
   :BATT-LEVEL:   100
   :UPTIME:       0:01:54
   :UPTIME-S:     114
   :ID:           010ec58776415894e6de09bdea6f179f1c740a15
   :END:

** <2012-11-29 Thu 08:48> wifi-home (not home for 8d 0:31:00)
   :PROPERTIES:
   :IN-BETWEEN:   192:31:00
   :IN-BETWEEN-S: 693060
   :BATT-LEVEL:   100
   :UPTIME:       0:01:58
   :UPTIME-S:     118
   :ID:           e5c44c0116f8a7497389a9e357aa16b5b7a84654
   :END:

** <2012-11-29 Thu 09:41> wifi-home-end (home for 0:53:00)
   :PROPERTIES:
   :IN-BETWEEN:   0:53:00
   :IN-BETWEEN-S: 3180
   :BATT-LEVEL:   98
   :UPTIME:       0:55:17
   :UPTIME-S:     3317
   :ID:           fc97dc08aa615ce3e7761ac98e7764d0bb800484
   :END:

** <2012-11-29 Thu 14:46> wifi-office
   :PROPERTIES:
   :IN-BETWEEN:
   :IN-BETWEEN-S:
   :BATT-LEVEL:   81
   :UPTIME:       6:00:33
   :UPTIME-S:     21633
   :ID:           a49fde06e577f5be565360fb78a11bd46ce9a4bb
   :END:

** <2012-11-29 Thu 16:15> wifi-home (not home for 6:34:00)
   :PROPERTIES:
   :IN-BETWEEN:   6:34:00
   :IN-BETWEEN-S: 23640
   :BATT-LEVEL:   76
   :UPTIME:       7:29:15
   :UPTIME-S:     26955
   :ID:           a14540f83262d71ce1e897f1bb201c59a327dbe4
   :END:

** <2012-11-29 Thu 17:04> wifi-home-end (home for 0:49:00)
   :PROPERTIES:
   :IN-BETWEEN:   0:49:00
   :IN-BETWEEN-S: 2940
   :BATT-LEVEL:   74
   :UPTIME:       8:18:32
   :UPTIME-S:     29912
   :ID:           59ccab7e44acc68645431eb404d9ee7ba105391f
   :END:

** <2012-11-29 Thu 23:31> shutdown (on for 14:44:00)
   :PROPERTIES:
   :IN-BETWEEN:                  14:44:00
   :IN-BETWEEN-S:                53040
   :BATT-LEVEL:                  48
   :UPTIME:                      14:45:46
   :UPTIME-S:                    53146
   :HOURS_RUNTIME_EXTRAPOLATION: 28
   :ID:                          5ce419edfe8f0268ce29369bd28160b7345e1c1d
   :END:

** <2013-09-10 Tue 07:00> boot (off for 284d 7:29:00)
   :PROPERTIES:
   :IN-BETWEEN:   6823:29:00
   :IN-BETWEEN-S: 24564540
   :BATT-LEVEL:   100
   :UPTIME:       0:02:10
   :UPTIME-S:     130
   :ID:           061afa34eb7edb532ea672f68b6f69ce4f7f967c
   :END:

** <2013-09-10 Tue 08:23> wifi-office
   :PROPERTIES:
   :IN-BETWEEN:   6833:37:00
   :IN-BETWEEN-S: 24601020
   :BATT-LEVEL:   95
   :UPTIME:       1:23:16
   :UPTIME-S:     4996
   :ID:           8e2999bcdd72126460a44ce827d95d004c6083a9
   :END:

** <2013-09-10 Tue 12:13> wifi-office-end (office for 3:50:00; today 3:50:00; today total 3:50:00)
   :PROPERTIES:
   :IN-BETWEEN:     3:50:00
   :IN-BETWEEN-S:   13800
   :BATT-LEVEL:     87
   :UPTIME:         5:13:46
   :UPTIME-S:       18826
   :OFFICE-SUMMARY: | 2013-09-10 | Tue | 08:23 | 11:30 | 12:00 | 12:13 | | |
   :ID:             80fb255f140f0956cde1f82af93e37d6c3206445
   :END:

** <2013-09-10 Tue 12:59> wifi-office (not office for 0:46:00)
   :PROPERTIES:
   :IN-BETWEEN:   0:46:00
   :IN-BETWEEN-S: 2760
   :BATT-LEVEL:   85
   :UPTIME:       6:00:00
   :UPTIME-S:     21600
   :ID:           d9a446d1acd443bd2b3d10df95f77e2805ead615
   :END:

** <2013-09-10 Tue 17:46> wifi-office-end (office for 4:47:00; today 8:37:00; today total 9:23:00)
   :PROPERTIES:
   :IN-BETWEEN:     4:47:00
   :IN-BETWEEN-S:   17220
   :BATT-LEVEL:     73
   :UPTIME:         10:47:06
   :UPTIME-S:       38826
   :OFFICE-SUMMARY: | 2013-09-10 | Tue | 08:23 | 12:13 | 12:59 | 17:46 | | |
   :ID:             b88052de1aaa8646fad9de6aa2f01c3e62cc14fe
   :END:

** <2013-09-10 Tue 22:10> shutdown (on for 15:10:00)
   :PROPERTIES:
   :IN-BETWEEN:                  15:10:00
   :IN-BETWEEN-S:                54600
   :BATT-LEVEL:                  58
   :UPTIME:                      15:10:38
   :UPTIME-S:                    54638
   :HOURS_RUNTIME_EXTRAPOLATION: 36
   :ID:                          8c71c9c8471972b05941d913c74fefc5613576fe
   :END:

** <2013-09-11 Wed 12:15> boot (off for 14:05:00)
   :PROPERTIES:
   :IN-BETWEEN:   14:05:00
   :IN-BETWEEN-S: 50700
   :BATT-LEVEL:   87
   :UPTIME:       5:15:05
   :UPTIME-S:     18905
   :ID:           8cc417754401bbd143036ad7ff58cef186232e53
   :END:

** <2013-09-11 Wed 13:19> wifi-office (not office for 19:33:00)
   :PROPERTIES:
   :IN-BETWEEN:   19:33:00
   :IN-BETWEEN-S: 70380
   :BATT-LEVEL:   82
   :UPTIME:       6:19:29
   :UPTIME-S:     22769
   :ID:           e0b62e92f6e75a70d3cfdfb1b8ef0964933a7f8d
   :END:

** <2013-09-11 Wed 18:55> wifi-office-end (office for 5:36:00; today 5:36:00; today total 5:36:00)
   :PROPERTIES:
   :IN-BETWEEN:     5:36:00
   :IN-BETWEEN-S:   20160
   :BATT-LEVEL:     69
   :UPTIME:         11:56:01
   :UPTIME-S:       42961
   :OFFICE-SUMMARY: | 2013-09-11 | Wed | 13:19 | 11:30 | 12:00 | 18:55 | | |
   :ID:             10f0f6606f3a92a5b7c599906db39e57cd4719bb
   :END:

** <2013-09-11 Wed 19:10> wifi-home (not home for 286d 2:06:00)
   :PROPERTIES:
   :IN-BETWEEN:   6866:06:00
   :IN-BETWEEN-S: 24717960
   :BATT-LEVEL:   68
   :UPTIME:       12:10:46
   :UPTIME-S:     43846
   :ID:           694280a75f124200e0faab9537c63a32f35f5838
   :END:

** <2013-09-11 Wed 22:55> shutdown (on for 10:40:00)
   :PROPERTIES:
   :IN-BETWEEN:                  10:40:00
   :IN-BETWEEN-S:                38400
   :BATT-LEVEL:                  53
   :UPTIME:                      15:55:23
   :UPTIME-S:                    57323
   :HOURS_RUNTIME_EXTRAPOLATION: 46
   :ID:                          2794e95db63f1752156fecb276b8b4fb20877dbb
   :END:"""

# Local Variables:
# mode: flyspell
# eval: (ispell-change-dictionary "en_US")
# End:
