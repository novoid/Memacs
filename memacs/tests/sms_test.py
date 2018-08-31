# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-09 15:36:52 armin>

import os
import re
import time
import unittest
import xml.etree.ElementTree as ET

from memacs.sms import SmsMemacs


class TestSmsMemacs(unittest.TestCase):

    def setUp(self):
        self._test_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data', 'smsxml.txt'
        )
        argv = "-s -f " + self._test_file
        memacs = SmsMemacs(argv=argv.split())
        self.data = memacs.test_get_entries()
        self._smses = ET.parse(self._test_file)

    def test_from_file(self):
        data = self.data

        for i in range(4):
            self._assertSMSLog(i, data[i*6:(i+1)*6])

    def _assertSMSLog(self, index, sms_data):
        sms = self._smses.findall('sms')[index]

        name = sms_data[3].split()[-1]
        name = 'Unknown' if name == 'False' else name
        to_from = 'SMS to' if sms.get('type') == '2' else 'SMS from'
        number = sms_data[2].split()[-1]
        timestamp, = re.findall('<(.*?)>', sms_data[0])
        date = time.gmtime(int(sms.get('date'))/1000.)

        self.assertIn(name, sms_data[0])
        self.assertIn(to_from, sms_data[0])
        self.assertEqual(time.strftime('%Y-%m-%d %a %H:%M', date), timestamp)
        self.assertEqual(number, sms.get('address').replace('+','00'))
