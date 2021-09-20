#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-11-05 16:01:05 vk>

import datetime
import logging
import os
import pytz
import sys
import time

from orgformat import OrgFormat

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties
from memacs.lib.reader import CommonReader

try:
    from icalendar import Calendar
except ImportError as e:
    print("please install python package \"icalendar\"")
    print(e)
    sys.exit(3)


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

        Sets fallback timezone for parsing of "floating events"
        (events which don't specify a timezone), if a `X-WR-TIMEZONE`
        line is provided in the calendar.

        @param component: icalendar component

        """
        # Set timezone
        timezone = component.get('x-wr-timezone')

        if timezone:
            self.fallback_tz = pytz.timezone(timezone)

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
            return str(vtext)
        else:
            return nonetype

    def __parse_ical_dt(self, component):
        """
        Parse an iCalendar DATE or DATE-TIME component.

        @return datetime.date (possibly datetime.datetime)
        @param component: the iCalendar component to parse
        """

        # Lean on `icalendar` to handle timezones, especially around
        # `VTIMEZONE` specifications, which can be complex.
        if isinstance(component.dt, datetime.date) and not isinstance(component.dt, datetime.datetime):
            # DATE
            return component.dt
        elif isinstance(component.dt, datetime.datetime) and component.dt.tzinfo is not None:
            # DATE-TIME w/ TZ - could be UTC, VTIMEZONE, or inline IANA-style
            return component.dt.astimezone()
        elif self.fallback_tz:
            # Floating DATE-TIME w/ fallback TZ
            dt_str = component.to_ical().decode('utf-8')

            if len(dt_str) == 15: # YYYYMMDDTHHMMSS
                return self.fallback_tz.localize(datetime.datetime.strptime(dt_str, '%Y%m%dT%H%M%S')).astimezone()
            else:
                raise ValueError("Invalid date format: " + dt_str)
        else:
            # Floating DATE-TIME
            return component.dt

    def __get_org_datetime_range(self, dtstart, dtend):
        """
        @return string (range in Org format)
        """
        assert isinstance(dtstart, datetime.date)
        assert isinstance(dtend,   datetime.date)

        dates_only = not isinstance(dtend, datetime.datetime)

        # Per the author of RFC5545, a one-day event should have the
        # same start and end date, but the general practice in the
        # wild (including Google Calendar) is to have a one-day event
        # end the following day.
        if dates_only:
            dtend -= datetime.timedelta(days=1)

        dtstart = dtstart.timetuple()
        dtend   = dtend.timetuple()

        if dates_only and dtstart == dtend:
            return OrgFormat.date(dtstart)
        else:
            return OrgFormat.daterange_autodetect_time(dtstart, dtend)

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

        dtstart = self.__parse_ical_dt(component.get('DTSTART'))

        ## notice: end date/time is optional; no end date results in end date 9999-12-31
        if component.has_key('DTEND'):
            dtend = self.__parse_ical_dt(component.get('DTEND'))
            orgdate = self.__get_org_datetime_range(dtstart, dtend)
        else:
            have_time = isinstance(dtstart, datetime.datetime)
            orgdate = OrgFormat.date(dtstart.timetuple(), show_time=have_time) + "--<9999-12-31 Fri>"

        logging.debug(orgdate + " " + summary)

        # format: 20091207T180000Z
        # not used: Datestamp created
        # dtstamp = self.__vtext_to_unicode(component.get('dtstamp'))

        # handle repeating events
        # not implemented due to org-mode datestime-range cannot be repeated
        # component.get('rrule')

        org_properties = OrgProperties(data_for_hashing=component.get('UID'))

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
            data = CommonReader.get_data_from_file(self._args.calendar_file,
            encoding=None)
        elif self._args.calendar_url:
            data = CommonReader.get_data_from_url(self._args.calendar_url)

        self.fallback_tz = None

        # read and go through calendar
        cal = Calendar.from_ical(data)
        for component in cal.walk():
            if component.name == "VCALENDAR":
                self.__handle_vcalendar(component)
            elif component.name == "VEVENT":
                self.__handle_vevent(component)
            else:
                logging.debug("Not handling component: " + component.name)
