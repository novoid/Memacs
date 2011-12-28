#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import sys
import os
import logging
import time
# needed to import common.*
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.memacs import Memacs
from common.orgformat import OrgFormat
from common.orgproperty import OrgProperties
from common.reader import CommonReader


try:
    from icalendar import Calendar
except ImportError:
    print "please install python package \"icalendar\""
    sys.exit(3)

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2011-12-28"
PROG_SHORT_DESCRIPTION = u"Memacs for ical Calendars"
PROG_TAG = u"calendar"
PROG_DESCRIPTION = u"""This script parses a *.ics file and generates
Entries for VEVENTS
* other's like VALARM are not implemented by now
"""
COPYRIGHT_YEAR = "2011-2012" 
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>, 
Armin Wieser <armin.wieser@gmail.com>"""


class CalendarMemacs(Memacs):
    def _parser_add_arguments(self):
        self._parser.add_argument("-c", "--calendar-url", dest="calendar_url",
                        help="url to calendar")

        self._parser.add_argument("-cf", "--calendar-file",
                                  dest="calendar_file",
                                  help="path to calendar")

        self._parser.add_argument(
            "-x", "--exclude", dest="excludelist",
            help="path to one or more folders seperated with \"|\"," + \
                "i.e.:\"/path/to/folder1|/path/to/folder2|..\"")

    def _parser_parse_args(self):
        Memacs._parser_parse_args(self)

        if not self._args.calendar_url and not self._args.calendar_file:
            self._parser.error("specify a calendar url or calendar file")

        if self._args.calendar_url and self._args.calendar_file:
            self._parser.error(
                "only set a url or path to a calendar not both.")

        if self._args.calendar_file  \
        and not os.path.exists(self._args.calendar_file):
            self._parser.error("calendar path not exists")

    def __handle_vcalendar(self, component):
        """
        handles a VCALENDAR Component

        sets timezone to calendar's timezone

        @param component: icalendar component
        """
        # Set timezone
        timezone = component.get('x-wr-timezone')
        logging.debug("Setting timezone to: " + timezone)
        os.environ['TZ'] = timezone
        time.tzset()

    def __handle_rrule(self, component):
        """
        Handles calendars rrule (used for reoccuring events)

        returns org string for reoccuring date
        """
        freq = self.__vtext_to_unicode(component.get('freq'))

        if freq == "MINUTELY":
            raise NotImplemented
        elif freq == "HOURLY":
            raise NotImplemented
        elif freq == "DAILY":
            return "+1d"
        elif freq == "WEEKLY":
            return "+1w"
        elif freq == "YEARLY":
            return "+1y"
        else:
            return ""

    def __vtext_to_unicode(self, vtext, nonetype=None):
        """
        @return unicode-string
                None: otherwise
        """
        if vtext:
            return unicode(vtext)
        else:
            return nonetype

    def __get_datetime_range(self, dtstart, dtend):
        """
        @return string: Datetime - Range in Org Format
        """
        begin_tupel = OrgFormat.datetupelutctimestamp(dtstart)
        end_tupel = OrgFormat.datetupelutctimestamp(dtend)

        # handle "all-day" - events
        if begin_tupel.tm_sec == 0 and \
                begin_tupel.tm_min == 0 and \
                begin_tupel.tm_hour == 0 and \
                end_tupel.tm_sec == 0 and \
                end_tupel.tm_min == 0 and \
                end_tupel.tm_hour == 0:
            # we have to subtract 1 day to get the correct dates
            end_tupel = time.localtime(time.mktime(end_tupel) - 24 * 60 * 60)
        
        return OrgFormat.utcrange(begin_tupel, end_tupel)

    def __handle_vevent(self, component):
        """
        handles a VCALENDAR Component

        sets timezone to calendar's timezone

        @param component: icalendar component
        """

        logging.debug(component)
        summary = self.__vtext_to_unicode(component.get('summary'),
                                          nonetype="")
        location = self.__vtext_to_unicode(component.get('location'))
        description = self.__vtext_to_unicode(component.get('description'))
        # format: 20091207T180000Z or 20100122
        dtstart = self.__vtext_to_unicode(component.get('dtstart'))
        # format: 20091207T180000Z or 20100122
        dtend = self.__vtext_to_unicode(component.get('dtend'))
        # format: 20091207T180000Z
        # not used: Datestamp created
        #dtstamp = self.__vtext_to_unicode(component.get('dtstamp'))

        # handle repeating events
        # not implemented due to org-mode datestime-range cannot be repeated
        # component.get('rrule')

        orgdate = self.__get_datetime_range(dtstart, dtend)

        logging.debug(orgdate + " " + summary)

        # we need to set data_for_hashing=summary to really get a other sha1
        org_properties = OrgProperties(data_for_hashing=summary)

        if location != None:
            org_properties.add("LOCATION", location)
        if description != None:
            org_properties.add("DESCRIPTION", description)

        
        self._writer.write_org_subitem(output=summary,
                                       properties=org_properties,
                                       timestamp=orgdate)

    def _main(self):
        # getting data
        if self._args.calendar_file:
            data = CommonReader.get_data_from_file(self._args.calendar_file)
        elif self._args.calendar_url:
            data = CommonReader.get_data_from_url(self._args.calendar_url)

        # read and go through calendar
        cal = Calendar.from_string(data)
        for component in cal.walk():
            if component.name == "VCALENDAR":
                self.__handle_vcalendar(component)
            elif component.name == "VEVENT":
                self.__handle_vevent(component)
            else:
                logging.info("Not handling component: " + component.name)


if __name__ == "__main__":
    memacs = CalendarMemacs(prog_version=PROG_VERSION_NUMBER,
                            prog_version_date=PROG_VERSION_DATE,
                            prog_description=PROG_DESCRIPTION,
                            prog_short_description=PROG_SHORT_DESCRIPTION,
                            prog_tag=PROG_TAG,
                            copyright_year=COPYRIGHT_YEAR,
                            copyright_authors=COPYRIGHT_AUTHORS
        )
    memacs.handle_main()
