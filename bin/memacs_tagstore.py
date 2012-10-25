#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-14 09:34:25 daniel>

from memacs.tagstore import TagstoreMemacs

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2012-03-14"
PROG_SHORT_DESCRIPTION = u"Memacs for tagstore"
PROG_TAG = u"tagstore"
PROG_DESCRIPTION = u"""The memacs module will fetch all infos
of given file (-f or --store_file <path to Tagstore store.tgs file>),
parses the file and writes the output to an orgfile.
"""
COPYRIGHT_YEAR = "2011-2012"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>,
Daniel Fussenegger <daniel.pandapaps@gmail.com>"""


if __name__ == "__main__":
    memacs = TagstoreMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS,
        )
    memacs.handle_main()
