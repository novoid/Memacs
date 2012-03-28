#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-11-02 15:13:31 aw>

import unittest
import time
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
        # testing tuples
        t = time.strptime("2011-11-02T20:38", "%Y-%m-%dT%H:%M")
        date = OrgFormat.date(t)
        datetime = OrgFormat.date(t, show_time=True)
        self.assertEqual("<2011-11-02 Wed>", date, "date error")
        self.assertEqual("<2011-11-02 Wed 20:38>", datetime, "datetime error")

    def test_inactive_date(self):
        """
        test Org inactive_date
        """
        # testing tuples
        t = time.strptime("2011-11-02T20:38", "%Y-%m-%dT%H:%M")
        date = OrgFormat.inactive_date(t)
        datetime = OrgFormat.inactive_datetime(t)
        self.assertEqual("[2011-11-02 Wed]", date, "date error")
        self.assertEqual("[2011-11-02 Wed 20:38]", datetime, "datetime error")

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
        self.assertEqual("<2011-11-30 Wed 21:06>",
                         OrgFormat.strdatetimeiso8601("2011-11-30T21.06"),
                         "datetimeiso8601 error")
        self.assertEqual("<2011-11-30 Wed 21:06>",
                         OrgFormat.strdatetimeiso8601("2011-11-30T21.06.00"),
                         "datetimeiso8601 error")
        self.assertEqual("<2011-11-30 Wed 21:06:02>",
                         OrgFormat.strdatetimeiso8601("2011-11-30T21.06.02"),
                         "datetimeiso8601 error")

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
            "<2011-11-30 Wed 21:06:02>--<2011-11-30 Wed 22:06:02>")

    def test_utc_time(self):
        os.environ['TZ'] = "Europe/Vienna"
        time.tzset()
        self.assertEqual(
            OrgFormat.date(
                OrgFormat.datetupelutctimestamp("20111219T205510Z"), True),
            "<2011-12-19 Mon 21:55:10>")
        self.assertEqual(
            OrgFormat.date(OrgFormat.datetupelutctimestamp("20111219T205510"),
                           True),
            "<2011-12-19 Mon 20:55:10>")
        self.assertEqual(
            OrgFormat.date(OrgFormat.datetupelutctimestamp("20111219"), False),
            "<2011-12-19 Mon>")

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
