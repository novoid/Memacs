#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

from memacs.ical import CalendarMemacs

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
