#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-11 14:11:25 daniel>

from memacs.maildir import MaildirMemacs

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2012-03-011"
PROG_SHORT_DESCRIPTION = u"Memacs for mbox"
PROG_TAG = u"emails:maildir"
PROG_DESCRIPTION = u"""Todo


"""
COPYRIGHT_YEAR = "2011-2012"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>, 
Daniel Fussenegger <daniel.pandapaps@gmail.com>"""


if __name__ == "__main__":
    memacs = MaildirMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS,
        )
    memacs.handle_main()
