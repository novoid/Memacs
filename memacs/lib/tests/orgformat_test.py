#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2018-09-22 13:02:39 vk>

import unittest
import time
import datetime
import os
from memacs.lib.orgformat import OrgFormat


class TestOrgFormat(unittest.TestCase):

    def test_link(self):
        """
        test Org links
        """
        self.assertEqual("[[/link/][description]]",
                         OrgFormat.link("/link/", "description"),
                         "format error link+description")
        self.assertEqual("[[/link/]]",
                         OrgFormat.link("/link/"),
                         "format error link")
        self.assertEqual("[[/link%20link/]]",
                         OrgFormat.link("/link link/"),
                         "quote error")

    def test_date(self):
        """
        test Org date
        """
        # testing time.struct_time
        t = time.strptime("2011-11-02T20:38", "%Y-%m-%dT%H:%M")
        mydate = OrgFormat.date(t)
        mydatetime = OrgFormat.date(t, show_time=True)
        self.assertEqual("<2011-11-02 Wed>", mydate, "date error")
        self.assertEqual("<2011-11-02 Wed 20:38>", mydatetime, "datetime error")

        # testing datetime.datetime
        t = datetime.datetime(2018, 9, 22, hour=12, minute=55, second=59)
        mydate = OrgFormat.date(t)
        mydatetime = OrgFormat.date(t, show_time=True)
        self.assertEqual("<2018-09-22 Sat>", mydate, "date error")
        self.assertEqual("<2018-09-22 Sat 12:55>", mydatetime, "datetime error")

    def test_inactive_date(self):
        """
        test Org inactive_date
        """
        # testing time.struct_time
        t = time.strptime("2011-11-02T20:38", "%Y-%m-%dT%H:%M")
        mydate = OrgFormat.inactive_date(t)
        mydatetime = OrgFormat.inactive_datetime(t)
        self.assertEqual("[2011-11-02 Wed]", mydate, "mydate error")
        self.assertEqual("[2011-11-02 Wed 20:38]", mydatetime, "mydatetime error")

        # testing datetime.datetime
        t = datetime.datetime(2018, 9, 22, hour=12, minute=55, second=59)
        mydate = OrgFormat.inactive_date(t)
        mydatetime = OrgFormat.inactive_date(t, show_time=True)
        self.assertEqual("[2018-09-22 Sat]", mydate, "date error")
        self.assertEqual("[2018-09-22 Sat 12:55]", mydatetime, "datetime error")

    def test_strings(self):
        # testing strings
        self.assertEqual("<2011-11-03 Thu>",
                         OrgFormat.strdate("2011-11-3"),
                         "date string error")
        self.assertEqual("<2011-11-03 Thu 11:52>",
                         OrgFormat.strdatetime("2011-11-3 11:52"),
                         "datetime string error")

    def test_iso8601(self):
        # testing iso8601
        self.assertEqual(
            "<2011-11-30 Wed 21:06>", OrgFormat.strdatetimeiso8601("2011-11-30T21.06")
        )
        self.assertEqual(
            "<2011-11-30 Wed 21:06>",
            OrgFormat.strdatetimeiso8601("2011-11-30T21.06.00")
        )
        self.assertEqual(
            "<2011-11-30 Wed 21:06>",
            OrgFormat.strdatetimeiso8601("2011-11-30T21.06.02"),
        )

    def test_iso8601_datetimetupel(self):
        self.assertEqual(
            2011,
            OrgFormat.datetimetupeliso8601("2011-11-30T21.06.02").tm_year,
            "datetimeiso8601 error")
        self.assertEqual(
            11,
            OrgFormat.datetimetupeliso8601("2011-11-30T21.06.02").tm_mon,
            "datetimeiso8601 error")
        self.assertEqual(
            30,
            OrgFormat.datetimetupeliso8601("2011-11-30T21.06.02").tm_mday,
            "datetimeiso8601 error")
        self.assertEqual(
            21,
            OrgFormat.datetimetupeliso8601("2011-11-30T21.06.02").tm_hour,
            "datetimeiso8601 error")
        self.assertEqual(
            6,
            OrgFormat.datetimetupeliso8601("2011-11-30T21.06.02").tm_min,
            "datetimeiso8601 error")
        self.assertEqual(
            2,
            OrgFormat.datetimetupeliso8601("2011-11-30T21.06.02").tm_sec,
            "datetimeiso8601 error")

    def test_iso8601_datetupel(self):
        self.assertEqual(
            2011,
            OrgFormat.datetupeliso8601("2011-11-30").tm_year,
            "datetimeiso8601 error")
        self.assertEqual(
            11,
            OrgFormat.datetupeliso8601("2011-11-30").tm_mon,
            "datetimeiso8601 error")
        self.assertEqual(
            30,
            OrgFormat.datetupeliso8601("2011-11-30").tm_mday,
            "datetimeiso8601 error")

    def test_date_ranges(self):
        daterange = OrgFormat.daterange(
            OrgFormat.datetupeliso8601("2011-11-29"),
            OrgFormat.datetupeliso8601("2011-11-30"))
        self.assertEqual(
            daterange,
            "<2011-11-29 Tue>--<2011-11-30 Wed>")
        datetimerange = OrgFormat.datetimerange(
            OrgFormat.datetimetupeliso8601("2011-11-30T21.06.02"),
            OrgFormat.datetimetupeliso8601("2011-11-30T22.06.02"))
        self.assertEqual(
            datetimerange,
            "<2011-11-30 Wed 21:06>--<2011-11-30 Wed 22:06>")

    def test_utc_time(self):
        os.environ['TZ'] = "Europe/Vienna"
        time.tzset()

        self.assertEqual(
            OrgFormat.date(
                OrgFormat.datetupelutctimestamp("20111219T205510Z"), True
            ),
            "<2011-12-19 Mon 21:55>"
        )

        self.assertEqual(
            OrgFormat.date(
                OrgFormat.datetupelutctimestamp("20111219T205510"),
                True
            ),
            "<2011-12-19 Mon 20:55>")

        self.assertEqual(
            OrgFormat.date(OrgFormat.datetupelutctimestamp("20111219"), False),
            "<2011-12-19 Mon>"
        )

    def test_contact_mail_mailto_link(self):
        mail_link1 = OrgFormat.contact_mail_mailto_link(
                "Bob Bobby <bob.bobby@example.com>")
        mail_link2 = OrgFormat.contact_mail_mailto_link("<Bob@example.com>")
        self.assertEqual("[[mailto:bob.bobby@example.com][Bob Bobby]]",
                         mail_link1)
        self.assertEqual("[[mailto:Bob@example.com][Bob@example.com]]",
                         mail_link2)

    def test_n(self):
        self.assertEqual("[[news:foo][foo]]", OrgFormat.newsgroup_link("foo"))


    def test_get_hms_from_sec(self):

        self.assertEqual(OrgFormat.get_hms_from_sec(123), '0:02:03')
        self.assertEqual(OrgFormat.get_hms_from_sec(9999), '2:46:39')


    def test_get_dhms_from_sec(self):

        self.assertEqual(OrgFormat.get_dhms_from_sec(123), '0:02:03')
        self.assertEqual(OrgFormat.get_dhms_from_sec(9999), '2:46:39')
        self.assertEqual(OrgFormat.get_dhms_from_sec(99999), '1d 3:46:39')
        self.assertEqual(OrgFormat.get_dhms_from_sec(12345678), '142d 21:21:18')


# Local Variables:
# mode: flyspell
# eval: (ispell-change-dictionary "en_US")
# End:
