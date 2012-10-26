#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-04-30 20:55:31>

from memacs.xmlsource import XmlMemacs

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2011-12-27"
PROG_SHORT_DESCRIPTION = u"Memacs for xml"
PROG_TAG = u"xml"
PROG_DESCRIPTION = u"""
This Memacs module will parse XML files.
"""


COPYRIGHT_YEAR = "2011-2012"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>,
Daniel Fussenegger <daniel.pandapaps@gmail.com> """

if __name__ == "__main__":
    memacs = XmlMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS)
    memacs.handle_main()
