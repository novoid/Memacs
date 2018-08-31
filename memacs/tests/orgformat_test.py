#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-09-28 13:02:55 vk>

import unittest
import time
import datetime
from memacs.lib.orgformat import OrgFormat
from memacs.lib.orgformat import TimestampParseException

class TestOrgFormat(unittest.TestCase):

    ## FIXXME: (Note) These test are *not* exhaustive unit tests. They only 
    ##         show the usage of the methods. Please add "mean" test cases and
    ##         borderline cases!

    def setUp(self):
        pass

    def test_all(self):

        self.assertEqual(
            "foo",
            "foo")

    def test_link(self):

        self.assertEqual(
            OrgFormat.link("http://github.org/novoid/memacs"),
            '[[http://github.org/novoid/memacs]]')

        self.assertEqual(
            OrgFormat.link("http://github.org/novoid/memacs with space"),
            '[[http://github.org/novoid/memacs%20with%20space]]')

        self.assertEqual(
            OrgFormat.link("http://github.org/novoid/memacs", "Memacs Repository"),
            '[[http://github.org/novoid/memacs][Memacs Repository]]')


    def test_date(self):

        ## fixed day:
        self.assertEqual(
            OrgFormat.date(time.struct_time([1980,12,31,0,0,0,0,0,0])),
            '<1980-12-31 Wed>' )
        
        ## fixed time with seconds:
        self.assertEqual(
            OrgFormat.date(time.struct_time([1980,12,31,23,59,58,0,0,0]), 'foo'),
            '<1980-12-31 Wed 23:59>' )  ## seconds are not (yet) defined in Org-mode

        ## fixed time without seconds:
        self.assertEqual(
            OrgFormat.date(time.struct_time([1980,12,31,23,59,0,0,0,0]), 'foo'),
            '<1980-12-31 Wed 23:59>' )

        YYYYMMDDwday = time.strftime('%Y-%m-%d %a', time.localtime())
        hhmmss = time.strftime('%H:%M', time.localtime())  ## seconds are not (yet) defined in Org-mode

        ## simple form with current day:
        self.assertEqual(
            OrgFormat.date(time.localtime()),
            '<' + YYYYMMDDwday + '>' )
        
        ## show_time parameter not named:
        self.assertEqual(
            OrgFormat.date(time.localtime(), True),
            '<' + YYYYMMDDwday + ' ' + hhmmss + '>' )
        
        ## show_time parameter named:
        self.assertEqual(
            OrgFormat.date(time.localtime(), show_time=True),
            '<' + YYYYMMDDwday + ' ' + hhmmss + '>' )
        

    def test_inactive_date(self):

        ## fixed day:
        self.assertEqual(
            OrgFormat.inactive_date(time.struct_time([1980,12,31,0,0,0,0,0,0])),
            '[1980-12-31 Wed]' )
        
        ## fixed time with seconds:
        self.assertEqual(
            OrgFormat.inactive_date(time.struct_time([1980,12,31,23,59,58,0,0,0]), 'foo'),
            '[1980-12-31 Wed 23:59]' )  ## seconds are not (yet) defined in Org-mode

        ## fixed time without seconds:
        self.assertEqual(
            OrgFormat.inactive_date(time.struct_time([1980,12,31,23,59,0,0,0,0]), 'foo'),
            '[1980-12-31 Wed 23:59]' )

        YYYYMMDDwday = time.strftime('%Y-%m-%d %a', time.localtime())
        hhmmss = time.strftime('%H:%M', time.localtime())  ## seconds are not (yet) defined in Org-mode

        ## simple form with current day:
        self.assertEqual(
            OrgFormat.inactive_date(time.localtime()),
            '[' + YYYYMMDDwday + ']' )
        
        ## show_time parameter not named:
        self.assertEqual(
            OrgFormat.inactive_date(time.localtime(), True),
            '[' + YYYYMMDDwday + ' ' + hhmmss + ']' )
        
        ## show_time parameter named:
        self.assertEqual(
            OrgFormat.inactive_date(time.localtime(), show_time=True),
            '[' + YYYYMMDDwday + ' ' + hhmmss + ']' )
        

    def test_datetime(self):

        ## fixed time with seconds:
        self.assertEqual(
            OrgFormat.datetime(time.struct_time([1980,12,31,23,59,58,0,0,0])),
            '<1980-12-31 Wed 23:59>' )  ## seconds are not (yet) defined in Org-mode

        ## fixed time without seconds:
        self.assertEqual(
            OrgFormat.datetime(time.struct_time([1980,12,31,23,59,0,0,0,0])),
            '<1980-12-31 Wed 23:59>' )

        YYYYMMDDwday = time.strftime('%Y-%m-%d %a', time.localtime())
        hhmmss = time.strftime('%H:%M', time.localtime())  ## seconds are not (yet) defined in Org-mode

        ## show_time parameter not named:
        self.assertEqual(
            OrgFormat.datetime(time.localtime()),
            '<' + YYYYMMDDwday + ' ' + hhmmss + '>' )
        
        ## show_time parameter named:
        self.assertEqual(
            OrgFormat.datetime(time.localtime()),
            '<' + YYYYMMDDwday + ' ' + hhmmss + '>' )
        

    def test_inactive_datetime(self):

        ## fixed time with seconds:
        self.assertEqual(
            OrgFormat.inactive_datetime(time.struct_time([1980,12,31,23,59,58,0,0,0])),
            '[1980-12-31 Wed 23:59]' )  ## seconds are not (yet) defined in Org-mode

        ## fixed time without seconds:
        self.assertEqual(
            OrgFormat.inactive_datetime(time.struct_time([1980,12,31,23,59,0,0,0,0])),
            '[1980-12-31 Wed 23:59]' )

        YYYYMMDDwday = time.strftime('%Y-%m-%d %a', time.localtime())
        hhmmss = time.strftime('%H:%M', time.localtime())  ## seconds are not (yet) defined in Org-mode

        ## show_time parameter not named:
        self.assertEqual(
            OrgFormat.inactive_datetime(time.localtime()),
            '[' + YYYYMMDDwday + ' ' + hhmmss + ']' )
        
        ## show_time parameter named:
        self.assertEqual(
            OrgFormat.inactive_datetime(time.localtime()),
            '[' + YYYYMMDDwday + ' ' + hhmmss + ']' )

        
    def test_daterange(self):

        ## fixed time with seconds:
        self.assertEqual(
            OrgFormat.daterange(
                time.struct_time([1980,12,31,23,59,58,0,0,0]),
                time.struct_time([1981,1,15,15,30,0o2,0,0,0]),
                ),
            '<1980-12-31 Wed>--<1981-01-15 Thu>' )

        ## provoke error:
        with self.assertRaises(AssertionError):
            OrgFormat.daterange('foo', 42)


    def test_datetimerange(self):

        self.assertEqual(
            OrgFormat.datetimerange(
                time.struct_time([1980,12,31,23,59,58,0,0,0]),
                time.struct_time([1981,1,15,15,30,0o2,0,0,0]),
                ),
            '<1980-12-31 Wed 23:59>--<1981-01-15 Thu 15:30>' )  ## seconds are not (yet) defined in Org-mode

        self.assertEqual(
            OrgFormat.datetimerange(
                time.struct_time([1980,12,31,23,59,0,0,0,0]),
                time.struct_time([1981,1,15,15,30,0o2,0,0,0]),
                ),
            '<1980-12-31 Wed 23:59>--<1981-01-15 Thu 15:30>' )


        self.assertEqual(
            OrgFormat.datetimerange(
                time.struct_time([1980,12,31,23,59,0,0,0,0]),
                time.struct_time([1981,1,15,15,30,0,0,0,0]),
                ),
            '<1980-12-31 Wed 23:59>--<1981-01-15 Thu 15:30>' )


    def test_utcrange(self):

        self.assertEqual(
            OrgFormat.utcrange(
                time.struct_time([1980,12,31,23,59,58,0,0,0]),
                time.struct_time([1981,1,15,15,30,0o2,0,0,0]),
                ),
            OrgFormat.datetimerange(
                time.struct_time([1980,12,31,23,59,58,0,0,0]),
                time.struct_time([1981,1,15,15,30,0o2,0,0,0]),
                )
             )

        self.assertEqual(
            OrgFormat.utcrange(
                time.struct_time([1980,12,31,23,59,0,0,0,0]),
                time.struct_time([1981,1,15,15,30,0o2,0,0,0]),
                ),
            OrgFormat.datetimerange(
                time.struct_time([1980,12,31,23,59,0,0,0,0]),
                time.struct_time([1981,1,15,15,30,0o2,0,0,0]),
                )
            )

        self.assertEqual(
            OrgFormat.utcrange(
                time.struct_time([1980,12,31,0,0,0,0,0,0]),
                time.struct_time([1981,1,15,0,0,0,0,0,0]),
                ),
            OrgFormat.daterange(
                time.struct_time([1980,12,31,23,59,0,0,0,0]),
                time.struct_time([1981,1,15,15,30,0o2,0,0,0]),
                )
            )


    def test_strdate(self):

        self.assertEqual(
            OrgFormat.strdate('1980-12-31'),
            '<1980-12-31 Wed>' )
        
        self.assertEqual(
            OrgFormat.strdate('1981-01-15'),
            '<1981-01-15 Thu>' )

        self.assertEqual(
            OrgFormat.strdate('1980-12-31', False),
            '<1980-12-31 Wed>' )
        
        self.assertEqual(
            OrgFormat.strdate('1981-01-15', False),
            '<1981-01-15 Thu>' )

        self.assertEqual(
            OrgFormat.strdate('1980-12-31', True),
            '[1980-12-31 Wed]' )
        
        self.assertEqual(
            OrgFormat.strdate('1981-01-15', True),
            '[1981-01-15 Thu]' )

        with self.assertRaises(TimestampParseException):
            OrgFormat.strdate('1981-01-15foo'),
        

    def test_strdatetime(self):

        self.assertEqual(
            OrgFormat.strdatetime('1980-12-31 23:59'),
            '<1980-12-31 Wed 23:59>' )
        
        self.assertEqual(
            OrgFormat.strdatetime('1981-01-15 15:10'),
            '<1981-01-15 Thu 15:10>' )

        with self.assertRaises(TimestampParseException):
            OrgFormat.strdatetime('1981-01-15 15.10')

        with self.assertRaises(TimestampParseException):
            OrgFormat.strdatetime('1981-01-15T15:10')
        

    def test_strdatetimeiso8601(self):

        self.assertEqual(
            OrgFormat.strdatetimeiso8601('1980-12-31T23.59'),
            '<1980-12-31 Wed 23:59>' )
        
        self.assertEqual(
            OrgFormat.strdatetimeiso8601('1981-01-15T15.10.23'),
            '<1981-01-15 Thu 15:10>' )  ## seconds are not (yet) defined in Org-mode
        
        with self.assertRaises(TimestampParseException):
            OrgFormat.strdatetimeiso8601('1981-01-15T15:10')
        

    def test_datetimetupeliso8601(self):
        
        self.assertEqual(
            OrgFormat.datetimetupeliso8601('1980-12-31T23.59'),
            time.struct_time([1980, 12, 31, 
                             23, 59, 0, 
                             2, 366, -1]) )

        self.assertEqual(
            OrgFormat.datetimetupeliso8601('1980-12-31T23.59.58'),
            time.struct_time([1980, 12, 31, 
                             23, 59, 58, 
                             2, 366, -1]) )
    
        
    def test_datetupleiso8601(self):

        self.assertEqual(
            OrgFormat.datetupeliso8601('1980-12-31'),
            time.struct_time([1980, 12, 31, 
                             0, 0, 0, 
                             2, 366, -1]) )

        with self.assertRaises(TimestampParseException):
            OrgFormat.datetupeliso8601('1980-12-31T23.59'),
        
        
    def test_datetupelutctimestamp(self):

        self.assertEqual(
            OrgFormat.datetupelutctimestamp('19801231'),
            time.struct_time([1980, 12, 31, 
                             0, 0, 0, 
                             2, 366, -1]) )

        self.assertEqual(
            OrgFormat.datetupelutctimestamp('19801231T235958'),
            time.struct_time([1980, 12, 31, 
                             23, 59, 58, 
                             2, 366, -1]) )

        ## FIXXME: this is most likely time zone depending:
        # self.assertEqual(
        #     OrgFormat.datetupelutctimestamp('19801231T120000Z'),
        #     time.struct_time([1980, 12, 31, 
        #                      13, 00, 00, 
        #                      2, 366, 0]) )



    def test_contact_mail_mailto_link(self):

        self.assertEqual(
            OrgFormat.contact_mail_mailto_link("<bob.bobby@example.com>"),
            "[[mailto:bob.bobby@example.com][bob.bobby@example.com]]" )

        self.assertEqual(
            OrgFormat.contact_mail_mailto_link("Bob Bobby <bob.bobby@example.com>"),
            "[[mailto:bob.bobby@example.com][Bob Bobby]]" )


    def test_newsgroup_link(self):

        self.assertEqual(
            OrgFormat.newsgroup_link("foo"),
            "[[news:foo][foo]]" )

        self.assertEqual(
            OrgFormat.newsgroup_link("foo.bar.baz"),
            "[[news:foo.bar.baz][foo.bar.baz]]" )


    def test_orgmode_timestamp_to_datetime(self):

        self.assertEqual(
            OrgFormat.orgmode_timestamp_to_datetime("<1980-12-31 Wed 23:59>"),
            datetime.datetime(1980, 12, 31, 23, 59, 0))
        

    def test_apply_timedelta_to_Orgmode_timestamp(self):

        self.assertEqual(
            OrgFormat.apply_timedelta_to_Orgmode_timestamp("<1980-12-31 Wed 23:59>", +2),
            "<1981-01-01 Thu 01:59>" )

        self.assertEqual(
            OrgFormat.apply_timedelta_to_Orgmode_timestamp("<1981-01-01 Thu 01:59>", -2),
            "<1980-12-31 Wed 23:59>" )

        self.assertEqual(
            OrgFormat.apply_timedelta_to_Orgmode_timestamp("<2009-12-07 Mon 12:25>-<2009-12-07 Mon 12:26>", -2),
            "<2009-12-07 Mon 10:25>-<2009-12-07 Mon 10:26>" )


    def tearDown(self):
        pass
