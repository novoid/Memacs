#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-09-12 09:11 igb>

from memacs.sms_superbackup import SmsSuperBackupMemacs

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2012-03-07"
PROG_SHORT_DESCRIPTION = "Memacs for sms"
PROG_TAG = "sms"
PROG_DESCRIPTION = """
This Memacs module will parse output of sms xml backup files

> A sample xml file you find in the documentation file memacs_sms.org.

Then an Org-mode file is generated.
"""
COPYRIGHT_YEAR = "2011-2013"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>
Ian Barton <ian@manor-farm.org>"""


def main():
    global memacs
    memacs = SmsSuperBackupMemacs(
        prog_version=PROG_VERSION_NUMBER,
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
