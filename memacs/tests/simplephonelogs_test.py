#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-05 15:10:14 vk>

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


    def test_generateOrgentry(self):

        test_timestamp = datetime.datetime(2013, 4, 5, 13, 39)
        test_timestamp_last_opposite = False

        self.assertEqual(
            self.logmodule._generateOrgentry(test_timestamp,
                                             u"boot", '42', '612',
                                             test_timestamp_last_opposite),
            u'** <2013-04-05 Fri 13:39> boot\n' + \
                u':PROPERTIES:\n' + \
                u':IN-BETWEEN: -\n' + \
                u':IN-BETWEEN-S: -\n' + \
                u':BATT-LEVEL: 42\n' + \
                u':UPTIME: 0:10:12\n' + \
                u':UPTIME-S: 612\n' + \
                u':END:\n')

        test_timestamp_last_opposite = datetime.datetime(2013, 4, 5, 13, 30)

        self.assertEqual(
            self.logmodule._generateOrgentry(test_timestamp,
                                             u"boot", '42', '612',
                                             test_timestamp_last_opposite),
            u'** <2013-04-05 Fri 13:39> boot (off for 0:09:00)\n' + \
                u':PROPERTIES:\n' + \
                u':IN-BETWEEN: 0:09:00\n' + \
                u':IN-BETWEEN-S: 540\n' + \
                u':BATT-LEVEL: 42\n' + \
                u':UPTIME: 0:10:12\n' + \
                u':UPTIME-S: 612\n' + \
                u':END:\n')



    def notest_parser(self):

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

        print "result[0]: " + self.logmodule.orgmode_result.split('\n')[0]  ## FIXXME print first line

    def tearDown(self):
        #print self.logmodule.orgmode_result
        pass


# Local Variables:
# mode: flyspell
# eval: (ispell-change-dictionary "en_US")
# End:
