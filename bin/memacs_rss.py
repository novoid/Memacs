#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-04 16:19:47 vk>

from memacs.rss import RssMemacs

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2011-12-27"
PROG_SHORT_DESCRIPTION = "Memacs for rss feeds"
PROG_TAG = "rss"
PROG_DESCRIPTION = """
This Memacs module will parse rss files.

rss can be read from file (-f FILE) or url (-u URL)

The items are automatically be appended to the org file.


Attention: RSS2.0 is required

Sample Org-entries
: ** <2009-09-06 Sun 18:45> [[http://www.wikipedia.org/][link]]: Example entry
:   Here is some text containing an interesting description.
:   :PROPERTIES:
:   :LINK:    [[http://www.wikipedia.org/]]
:   :GUID:    rss guid
:   :SUMMARY: Here is some text containing an interesting description.
:   :ID:      unique string per item
:   :END:
"""
COPYRIGHT_YEAR = "2011-2013"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


def main():
    global memacs
    memacs = RssMemacs(
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
