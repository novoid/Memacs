#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

from memacs.rss import RssMemacs

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2011-12-27"
PROG_SHORT_DESCRIPTION = u"Memacs for rss feeds"
PROG_TAG = u"rss"
PROG_DESCRIPTION = u"""
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
COPYRIGHT_YEAR = "2011-2012"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


if __name__ == "__main__":
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
