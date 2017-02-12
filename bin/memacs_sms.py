#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Time-stamp: <2014-12-13 13:39:15 vk>

from memacs.sms import SmsMemacs

PROG_VERSION_NUMBER = u"0.2"
PROG_VERSION_DATE = u"2014-12-13"
PROG_SHORT_DESCRIPTION = u"Memacs for sms"
PROG_TAG = u"sms"
PROG_DESCRIPTION = u"""
This Memacs module will parse output of sms xml backup files

> A sample xml file you find in the documentation file memacs_sms.org.

Then an Org-mode file is generated.
"""
COPYRIGHT_YEAR = "2011-2014"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""

if __name__ == "__main__":
    memacs = SmsMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS
        )
    memacs.handle_main()
