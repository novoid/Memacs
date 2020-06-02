#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-04 16:20:01 vk>

from memacs.svn import SvnMemacs

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2011-12-27"
PROG_SHORT_DESCRIPTION = "Memacs for svn"
PROG_TAG = "svn"
PROG_DESCRIPTION = """
This Memacs module will parse output of svn log --xml

sample xml:
 <?xml version="1.0"?>
    <log>
    <logentry
       revision="13">
    <author>bob</author>
    <date>2011-11-05T18:18:22.936127Z</date>
    <msg>Bugfix.</msg>
    </logentry>
    </log>

Then an Org-mode file is generated that contains information
about the log messages, author, and revision
"""
COPYRIGHT_YEAR = "2011-2013"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


def main():
    global memacs
    memacs = SvnMemacs(
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
