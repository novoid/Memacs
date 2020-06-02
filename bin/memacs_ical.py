#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-04 16:18:50 vk>

from memacs.ical import CalendarMemacs

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2011-12-28"
PROG_SHORT_DESCRIPTION = "Memacs for ical Calendars"
PROG_TAG = "calendar"
PROG_DESCRIPTION = """This script parses a *.ics file and generates
Entries for VEVENTS
* other's like VALARM are not implemented by now
"""
COPYRIGHT_YEAR = "2011-2013"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


def main():
    global memacs
    memacs = CalendarMemacs(prog_version=PROG_VERSION_NUMBER,
                            prog_version_date=PROG_VERSION_DATE,
                            prog_description=PROG_DESCRIPTION,
                            prog_short_description=PROG_SHORT_DESCRIPTION,
                            prog_tag=PROG_TAG,
                            copyright_year=COPYRIGHT_YEAR,
                            copyright_authors=COPYRIGHT_AUTHORS
                            )
    memacs.handle_main()


if __name__ == "__main__":
    main()
