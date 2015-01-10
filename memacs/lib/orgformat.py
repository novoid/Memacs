# -*- coding: utf-8 -*-
# Time-stamp: <2014-03-13 17:13:23 karl.voit>

## This file is originally from Memacs
## https://github.com/novoid/Memacs
## and was written mainly by https://github.com/awieser
## see: https://github.com/novoid/Memacs/blob/master/memacs/lib/orgformat.py
## for unit tests, see: https://github.com/novoid/Memacs/blob/master/memacs/lib/tests/orgformat_test.py

import time
import datetime
import calendar
import logging
import re

#import pdb  ## pdb.set_trace()  ## FIXXME


class TimestampParseException(Exception):
    """
    Own excption should be raised when
    strptime fails
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class OrgFormat(object):
    """
    Class for handle special Org Formats linke link, time
    """

    SINGLE_ORGMODE_TIMESTAMP = "([<\[]([12]\d\d\d)-([012345]\d)-([012345]\d) " + \
        "(Mon|Tue|Wed|Thu|Fri|Sat|Sun) " + \
        "(([01]\d)|(20|21|22|23)):([012345]\d)[>\]])"

    ORGMODE_TIMESTAMP_REGEX = re.compile(SINGLE_ORGMODE_TIMESTAMP + "$")

    ORGMODE_TIMESTAMP_RANGE_REGEX = re.compile(SINGLE_ORGMODE_TIMESTAMP + "-(-)?" + SINGLE_ORGMODE_TIMESTAMP + "$")

    @staticmethod
    def struct_time_to_datetime(tuple_date):
        """
        returns a datetime object which was generated from the struct_time parameter
        @param struct_time with possible false day of week
        """

        assert tuple_date.__class__ == time.struct_time

        return datetime.datetime(tuple_date.tm_year,
                                 tuple_date.tm_mon,
                                 tuple_date.tm_mday,
                                 tuple_date.tm_hour,
                                 tuple_date.tm_min,
                                 tuple_date.tm_sec)

    @staticmethod
    def datetime_to_struct_time(tuple_date):
        """
        returns time.struct_time which was generated from the datetime.datetime parameter
        @param datetime object
        """

        assert tuple_date.__class__ == datetime.datetime

        return tuple_date.timetuple()

    @staticmethod
    def fix_struct_time_wday(tuple_date):
        """
        returns struct_time timestamp with correct day of week
        @param struct_time with possible false day of week
        """

        assert tuple_date.__class__ == time.struct_time

        datetimestamp = OrgFormat.struct_time_to_datetime(tuple_date)

        return time.struct_time([datetimestamp.year,
                                 datetimestamp.month,
                                 datetimestamp.day,
                                 datetimestamp.hour,
                                 datetimestamp.minute,
                                 datetimestamp.second,
                                 datetimestamp.weekday(),
                                 0, 0])

    ## timestamp = time.struct_time([2013,4,3,10,54,0,0,0,0])  ## wday == 0
    ## OrgFormat.date(timestamp)  ## '<2013-04-03 Mon>' -> Mon is wrong for April 3rd 2013
    ## OrgFormat.date( OrgFormat.fix_struct_time_wday(timestamp) ) ## '<2013-04-03 Wed>'

    @staticmethod
    def link(link, description=None, replacespaces=True):
        """
        returns string of a link in org-format
        @param link link to i.e. file
        @param description optional
        @param replacespaces: if True (default), spaces within link are being sanitized
        """

        if replacespaces:
            link = link.replace(" ", "%20")

        if description:
            return u"[[" + link + u"][" + description + u"]]"
        else:
            return u"[[" + link + u"]]"

    @staticmethod
    def date(tuple_date, show_time=False):
        """
        returns a date string in org format
        i.e.: * <YYYY-MM-DD Sun>
              * <YYYY-MM-DD Sun HH:MM>
        @param tuple_date: has to be of type time.struct_time or datetime
        @param show_time: optional show time also
        """
        # <YYYY-MM-DD hh:mm>
        assert (tuple_date.__class__ == time.struct_time or tuple_date.__class__ == datetime.datetime)

        local_structtime = False

        if tuple_date.__class__ == time.struct_time:
            ## fix day of week in struct_time
            local_structtime = OrgFormat.fix_struct_time_wday(tuple_date)
        else:
            ## convert datetime to struc_time
            local_structtime = OrgFormat.datetime_to_struct_time(tuple_date)

        if show_time:
            return time.strftime("<%Y-%m-%d %a %H:%M>", local_structtime)
        else:
            return time.strftime("<%Y-%m-%d %a>", local_structtime)

    @staticmethod
    def inactive_date(tuple_date, show_time=False):
        """
        returns a date string in org format
        i.e.: * [YYYY-MM-DD Sun]
              * [YYYY-MM-DD Sun HH:MM]
        @param tuple_date: has to be a time.struct_time
        @param show_time: optional show time also
        """
        # <YYYY-MM-DD hh:mm>
        assert tuple_date.__class__ == time.struct_time

        if show_time:
            return time.strftime("[%Y-%m-%d %a %H:%M]", OrgFormat.fix_struct_time_wday(tuple_date))
        else:
            return time.strftime("[%Y-%m-%d %a]", OrgFormat.fix_struct_time_wday(tuple_date))

    @staticmethod
    def datetime(tuple_datetime):
        """
        returns a date+time string in org format
        wrapper for OrgFormat.date(show_time=True)

        @param tuple_datetime has to be a time.struct_time
        """
        return OrgFormat.date(tuple_datetime, show_time=True)

    @staticmethod
    def inactive_datetime(tuple_datetime):
        """
        returns a date+time string in org format
        wrapper for OrgFormat.inactive_date(show_time=True)

        @param tuple_datetime has to be a time.struct_time
        """
        return OrgFormat.inactive_date(tuple_datetime, show_time=True)

    @staticmethod
    def daterange(begin, end):
        """
        returns a date range string in org format

        @param begin,end: has to be a time.struct_time
        """
        assert type(begin) == time.struct_time
        assert type(end) == time.struct_time
        return "%s--%s" % (OrgFormat.date(begin, False),
                           OrgFormat.date(end, False))

    @staticmethod
    def datetimerange(begin, end):
        """
        returns a date range string in org format

        @param begin,end: has to be a time.struct_time
        """
        assert type(begin) == time.struct_time
        assert type(end) == time.struct_time
        return "%s--%s" % (OrgFormat.date(begin, True),
                           OrgFormat.date(end, True))

    @staticmethod
    def utcrange(begin_tupel, end_tupel):
        """
        returns a date(time) range string in org format
        if both parameters do not contain time information,
        utcrange is same as daterange, else it is same as datetimerange.

        @param begin,end: has to be a a time.struct_time
        """

        if begin_tupel.tm_sec == 0 and \
                begin_tupel.tm_min == 0 and \
                begin_tupel.tm_hour == 0 and \
                end_tupel.tm_sec == 0 and \
                end_tupel.tm_min == 0 and \
                end_tupel.tm_hour == 0:

            return OrgFormat.daterange(begin_tupel, end_tupel)
        else:
            return OrgFormat.datetimerange(begin_tupel, end_tupel)

    @staticmethod
    def strdate(date_string, inactive=False):
        """
        returns a date string in org format
        i.e.: * <YYYY-MM-DD Sun>
        @param date-string: has to be a str in following format:  YYYY-MM-DD
        @param inactive: (boolean) True: use inactive time-stamp; else use active
        """
        assert date_string.__class__ == str or date_string.__class__ == unicode
        tuple_date = OrgFormat.datetupeliso8601(date_string)
        if inactive:
            return OrgFormat.inactive_date(tuple_date, show_time=False)
        else:
            return OrgFormat.date(tuple_date, show_time=False)

    @staticmethod
    def strdatetime(datetime_string):
        """
        returns a date string in org format
        i.e.: * <YYYY-MM-DD Sun HH:MM>
        @param date-string: has to be a str in
                           following format: YYYY-MM-DD HH:MM
        """
        assert datetime_string.__class__ == str or \
            datetime_string.__class__ == unicode
        try:
            tuple_date = time.strptime(datetime_string, "%Y-%m-%d %H:%M")
        except ValueError, e:
            raise TimestampParseException(e)
        return OrgFormat.date(tuple_date, show_time=True)

    @staticmethod
    def strdatetimeiso8601(datetime_string):
        """
        returns a date string in org format
        i.e.: * <YYYY-MM-DD Sun HH:MM>
        @param date-string: has to be a str
                            in following format: YYYY-MM-DDTHH.MM.SS or
                                                 YYYY-MM-DDTHH.MM
        """
        assert datetime_string.__class__ == str or \
            datetime_string.__class__ == unicode
        tuple_date = OrgFormat.datetimetupeliso8601(datetime_string)
        return OrgFormat.date(tuple_date, show_time=True)

    @staticmethod
    def datetimetupeliso8601(datetime_string):
        """
        returns a time_tupel
        @param datetime_string: YYYY-MM-DDTHH.MM.SS or
                                YYYY-MM-DDTHH.MM
        """
        assert datetime_string.__class__ == str or \
            datetime_string.__class__ == unicode
        try:
            if len(datetime_string) == 16:  # YYYY-MM-DDTHH.MM
                return time.strptime(datetime_string, "%Y-%m-%dT%H.%M")
            elif len(datetime_string) == 19:  # YYYY-MM-DDTHH.MM.SS
                return time.strptime(datetime_string, "%Y-%m-%dT%H.%M.%S")
        except ValueError, e:
            raise TimestampParseException(e)

    @staticmethod
    def datetupeliso8601(datetime_string):
        """
        returns a time_tupel
        @param datetime_string: YYYY-MM-DD
        """
        assert datetime_string.__class__ == str or \
            datetime_string.__class__ == unicode
        try:
            return time.strptime(datetime_string, "%Y-%m-%d")
        except ValueError, e:
            raise TimestampParseException(e)

    @staticmethod
    def datetupelutctimestamp(datetime_string):
        """
        returns a time_tupel
        @param datetime_string: YYYYMMDDTHHMMSSZ or
                                YYYYMMDDTHHMMSS or
                                YYYYMMDD
        """
        assert datetime_string.__class__ == str or \
            datetime_string.__class__ == unicode
        string_length = len(datetime_string)

        try:
            if string_length == 16:
                #YYYYMMDDTHHMMSSZ
                return time.localtime(
                    calendar.timegm(
                        time.strptime(datetime_string, "%Y%m%dT%H%M%SZ")))
            elif string_length == 15:
                #YYYYMMDDTHHMMSS
                return time.strptime(datetime_string, "%Y%m%dT%H%M%S")
            elif string_length == 8:
                #YYYYMMDD
                return time.strptime(datetime_string, "%Y%m%d")
            elif string_length == 27:
                #2011-11-02T14:48:54.908371Z
                datetime_string = datetime_string.split(".")[0] + "Z"
                return time.localtime(
                    calendar.timegm(
                        time.strptime(datetime_string,
                                      "%Y-%m-%dT%H:%M:%SZ")))
            else:
                logging.error("string has no correct format: %s",
                              datetime_string)
        except ValueError, e:
            raise TimestampParseException(e)

    # @staticmethod
    # def date_tupel_mail_date(mail_date_string):
    #     """
    #     @param mail_date_string: following format:
    #         "Mon, 26 Dec 2011 17:16:28 +0100"
    #     @return: time_struct
    #     """
    #
    #     return None

    @staticmethod
    def contact_mail_mailto_link(contact_mail_string):
        """
        @param contact_mailto_string: possibilities:
        - "Bob Bobby <bob.bobby@example.com>" or
        - <Bob@example.com>"

        @return:
        - [[mailto:bob.bobby@example.com][Bob Bobby]]
        - [[mailto:bob.bobby@example.com][bob.bobby@excample.com]]
        """
        delimiter = contact_mail_string.find("<")
        name = contact_mail_string[:delimiter].strip()
        mail = contact_mail_string[delimiter + 1:][:-1].strip()
        if name != "":
            return u"[[mailto:" + mail + u"][" + name + u"]]"
        else:
            return u"[[mailto:" + mail + u"][" + mail + u"]]"

    @staticmethod
    def newsgroup_link(newsgroup_string):
        """
        @param newsgroup_string: Usenet name
            i.e: news:comp.emacs
        @param return: [[news:comp.emacs][comp.emacs]]
        """
        return "[[news:" + newsgroup_string + "][" + newsgroup_string + "]]"

    @staticmethod
    def get_hms_from_sec(sec):
        """
        Returns a string of hours:minutes:seconds from the seconds given.

        @param sec: seconds
        @param return: h:mm:ss as string
        """

        assert sec.__class__ == int

        seconds = sec % 60
        minutes = (sec / 60) % 60
        hours = (sec / (60 * 60))

        return str(hours) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

    @staticmethod
    def get_dhms_from_sec(sec):
        """
        Returns a string of days hours:minutes:seconds (like
        "9d 13:59:59") from the seconds given. If days is zero, omit
        the part of the days (like "13:59:59").

        @param sec: seconds
        @param return: xd h:mm:ss as string
        """

        assert sec.__class__ == int

        seconds = sec % 60
        minutes = (sec / 60) % 60
        hours = (sec / (60 * 60)) % 24
        days = (sec / (60 * 60 * 24))

        if days > 0:
            daystring = str(days) + "d "
        else:
            daystring = ''

        return daystring + str(hours) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

    @staticmethod
    def orgmode_timestamp_to_datetime(orgtime):
        """
        Returns a datetime object containing the time-stamp of an Org-mode time-stamp.

        @param orgtime: <YYYY-MM-DD Sun HH:MM>
        @param return: date time object
        """

        assert orgtime.__class__ == str or \
            orgtime.__class__ == unicode

        components = re.match(OrgFormat.ORGMODE_TIMESTAMP_REGEX, orgtime)

        assert components

        ## components: <1980-12-31 Wed 23:59>
        ## components.groups(1) -> ('1980', '12', '31', 'Wed', '23', 1, '23', '59')

        year = int(components.group(2))
        month = int(components.group(3))
        day = int(components.group(4))
        hour = int(components.group(6))
        minute = int(components.group(9))

        return datetime.datetime(year, month, day, hour, minute, 0)

    @staticmethod
    def apply_timedelta_to_Orgmode_timestamp(orgtime, deltahours):
        """
        Returns a string containing an Org-mode time-stamp which has
        delta added in hours. It works also for a time-stamp range
        which uses two strings <YYYY-MM-DD Sun HH:MM> concatenated
        with one or two dashes.

        @param orgtime: <YYYY-MM-DD Sun HH:MM>
        @param deltahours: integer like, e.g., "3" or "-2" (in hours)
        @param return: <YYYY-MM-DD Sun HH:MM>
        """

        assert deltahours.__class__ in (int, float)
        assert orgtime.__class__ == str or \
            orgtime.__class__ == unicode

        ## first time-stamp: range_components.groups(0)[0]
        ## second time-stamp: range_components.groups(0)[10]
        range_components = re.match(OrgFormat.ORGMODE_TIMESTAMP_RANGE_REGEX, orgtime)

        if range_components:
            return OrgFormat.datetime(
                OrgFormat.orgmode_timestamp_to_datetime(
                    range_components.groups(0)[0]) +
                datetime.timedelta(0, 0, 0, 0, 0, deltahours)) + \
                "-" + \
                OrgFormat.datetime(
                    OrgFormat.orgmode_timestamp_to_datetime(
                        range_components.groups(0)[10]) +
                    datetime.timedelta(0, 0, 0, 0, 0, deltahours))
        else:
            return OrgFormat.datetime(OrgFormat.orgmode_timestamp_to_datetime(orgtime) +
                                      datetime.timedelta(0, 0, 0, 0, 0, deltahours))


# Local Variables:
# mode: flyspell
# eval: (ispell-change-dictionary "en_US")
# End:
