# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-29 22:21:46 armin>

import time
import calendar
import logging


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
    @staticmethod
    def link(link, description=None):
        """
        returns string of a link in org-format
        @param link link to i.e. file
        @param description optional
        """

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
        @param tuple_date: has to be a time.struct_time
        @param show_time: optional show time also
        """
        # <YYYY-MM-DD hh:mm>
        assert tuple_date.__class__ == time.struct_time

        if show_time:
            if tuple_date.tm_sec == 0:
                return time.strftime("<%Y-%m-%d %a %H:%M>", tuple_date)
            else:
                return time.strftime("<%Y-%m-%d %a %H:%M:%S>", tuple_date)
        else:
            return time.strftime("<%Y-%m-%d %a>", tuple_date)

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
            if tuple_date.tm_sec == 0:
                return time.strftime("[%Y-%m-%d %a %H:%M]", tuple_date)
            else:
                return time.strftime("[%Y-%m-%d %a %H:%M:%S]", tuple_date)
        else:
            return time.strftime("[%Y-%m-%d %a]", tuple_date)

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

        @param begin,end: has to be a String:  YYYYMMDDTHHMMSSZ or
                                               YYYYMMDDTHHMMSST or
                                               YYYYMMDD
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
    def strdate(date_string):
        """
        returns a date string in org format
        i.e.: * <YYYY-MM-DD Sun>
        @param date-string: has to be a str in following format:  YYYY-MM-DD
        """
        assert date_string.__class__ == str or date_string.__class__ == unicode
        tuple_date = OrgFormat.datetupeliso8601(date_string)
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
                                YYYYMMDDTHHMMSST or
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
                #YYYYMMDDTHHMMSST
                return time.strptime(datetime_string, "%Y%m%dT%H%M%S")
            elif string_length == 8:
                #YYYYMMDD
                return time.strptime(datetime_string, "%Y%m%d")
            elif string_length == 27:
                #2011-11-02T14:48:54.908371Z
                datetime_string = datetime_string.split(".")[0] + "Z"
                return time.localtime(
                    calendar.timegm(
                        time.strptime(
                                      datetime_string,
                                      "%Y-%m-%dT%H:%M:%SZ")))
            else:
                logging.error("string has no correct format: %s",
                              datetime_string)
        except ValueError, e:
            raise TimestampParseException(e)

    @staticmethod
    def date_tupel_mail_date(mail_date_string):
        """
        @param mail_date_string: following format:
            "Mon, 26 Dec 2011 17:16:28 +0100"
        @return: time_struct
        """

        return None

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
