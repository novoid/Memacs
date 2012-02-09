#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

from memacs.filenametimestamps import FileNameTimeStamps

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2011-12-28"
PROG_SHORT_DESCRIPTION = u"Memacs for file name time stamp"
PROG_TAG = u"filedatestamps"
PROG_DESCRIPTION = u"""This script parses a text file containing absolute paths
to files with ISO datestamps and timestamps in their file names:

Examples:  "2010-03-29T20.12 Divegraph.tiff"
           "2010-12-31T23.59_Cookie_recipies.pdf"
           "2011-08-29T08.23.59_test.pdf"

Emacs tmp-files like file~ are automatically ignored

Then an Org-mode file is generated that contains links to the files.
"""
COPYRIGHT_YEAR = "2011-2012"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""

if __name__ == "__main__":

    memacs = FileNameTimeStamps(prog_version=PROG_VERSION_NUMBER,
                                prog_version_date=PROG_VERSION_DATE,
                                prog_description=PROG_DESCRIPTION,
                                prog_short_description=PROG_SHORT_DESCRIPTION,
                                prog_tag=PROG_TAG,
                                copyright_year=COPYRIGHT_YEAR,
                                copyright_authors=COPYRIGHT_AUTHORS)
    memacs.handle_main()
