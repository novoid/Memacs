#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import sys, os
# needed to import common.*
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.memacs import Memacs
from common.orgformat import OrgFormat
import codecs
from urllib2 import urlopen, HTTPError, URLError
import logging
import time

try:
    from icalendar import Calendar
except ImportError:
    print "please install python package \"icalendar\""
    sys.exit(3)

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2011-12-18"
PROG_SHORT_DESCRIPTION = u"Memacs for ical Calendars"
PROG_TAG = u"calendar"
PROG_DESCRIPTION = u"""This script parses a *.ics file and generates 
Entries for VEVENTS

Emacs tmp-files like file~ are automatically ignored
"""

class CalendarMemacs(Memacs):
    def _parser_add_arguments(self):
        self._parser.add_argument("-c", "--calendar-url", dest="calendar_url",
                        help="url to calendar")
    
        self._parser.add_argument("-cf", "--calendar-file", dest="calendar_file",
                        help="path to calendar")
    
        self._parser.add_argument("-x", "--exclude", dest="excludelist",
                        help="path to one or more folders seperated with \"|\"," + \
                        "i.e.:\"/path/to/folder1|/path/to/folder2|..\"")
 
    def _parser_parse_args(self):
        Memacs._parser_parse_args(self)
        
        if not self._args.calendar_url and not self._args.calendar_file:
            self._parser.error("specify a calendar url or calendar file")
            
        if self._args.calendar_url and self._args.calendar_file:
            self._parser.error("only set a url or path to a calendar not both.")
    
        if self._args.calendar_file and not os.path.exists(self._args.calendar_file):
            self._parser.error("calendar path not exists")
        
    def _main(self):
        # getting data
        if self._args.calendar_file:
            try:
                file = codecs.open(self._args.calendar_file, 'rb')
                data = file.read()
                file.close()
            except IOError:
                logging.error("Error at opening file: %s" % self._args.calendar_file)
                sys.exit(1)
                
        elif self._args.calendar_url:
            try:
                req = urlopen(self._args.calendar_url, None, 10)
                data = req.read()
            except HTTPError:
                logging.error("Error at opening url: %s" % self._args.calendar_url)
                sys.exit(1)
            except URLError:
                logging.error("Error at opening url: %s" % self._args.calendar_url)
                sys.exit(1)
            except ValueError:
                logging.error("Error - no valid url: %s" % self._args.calendar_url)
                sys.exit(1)
        
        # read and go through calendar
        cal = Calendar.from_string(data);
        for component in cal.walk():
            if component.name == "VCALENDAR":
                # Set timezone
                timezone = component.get('x-wr-timezone')
                logging.debug("Setting timezone to: " + timezone)
                os.environ['TZ'] = timezone;
                time.tzset()
            elif component.name == "VEVENT":
                summary  = unicode(component.get('summary'))
                location = unicode(component.get('location'))
                description = unicode(component.get('description'))
                dtstart  = unicode(component.get('dtstart')) # format: 20091207T180000Z or 20100122
                dtend    = unicode(component.get('dtend'))   # format: 20091207T180000Z or 20100122
                dtstamp  = unicode(component.get('dtstamp')) # format: 20091207T180000Z
                orgdatecreated = OrgFormat.date(OrgFormat.datetupelutctimestamp(dtstamp))
                orgdate = OrgFormat.utcrange(dtstart, dtend)
                logging.debug(orgdate + " " + summary)
                self._writer.write_org_subitem(summary)
                self._writer.writeln("   " +orgdate)
                self._writer.writeln("   :PROPERTIES:")
                if location:
                    self._writer.writeln("   :LOCATION:" +location)
                if description:
                    self._writer.writeln("   :DESCRIPTION:" +description)
                self._writer.writeln("   :END:")
            else:
                logging.info("Not handling component: "+component.name)


if __name__ == "__main__":
    memacs = CalendarMemacs(prog_version=PROG_VERSION_NUMBER
                           , prog_version_date=PROG_VERSION_DATE
                           , prog_description=PROG_DESCRIPTION
                           , prog_short_description=PROG_SHORT_DESCRIPTION
                           , prog_tag=PROG_TAG)
    memacs.handle_main()



