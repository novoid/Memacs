# -*- coding: utf-8 -*-
# Time-stamp: <2012-09-06 22:02:48 armin>

import os
import re
import time
import unittest
import xml.etree.ElementTree as ET

from memacs.phonecalls import PhonecallsMemacs


class TestPhonecallsMemacs(unittest.TestCase):

    def setUp(self):
        self._test_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'data', 'calls.xml'
        )
        argv = "-s -f " + self._test_file
        memacs = PhonecallsMemacs(argv=argv.split())
        self.data = memacs.test_get_entries()
        self._calls = ET.parse(self._test_file)

    def test_from_file(self):
        data = self.data
        for i in range(8):
            self._assertPhoneLog(i, data[i*7:(i+1)*7])

    def _assertPhoneLog(self, index, call_data):
        call = self._calls.findall('call')[index]

        duration = call_data[3].split()[-1]
        number = call_data[4].split()[-1]
        start, _ = re.findall('<(.*?)>', call_data[0])
        date = time.gmtime(int(call.get('date'))/1000.)

        self.assertEqual(time.strftime('%Y-%m-%d %a %H:%M', date), start)
        self.assertEqual(duration, call.get('duration'))
        self.assertEqual(number, call.get('number'))
