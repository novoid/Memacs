#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-10-03 11:44:44 vk>

from memacs.filenametimestamps import FileNameTimeStamps

PROG_VERSION_NUMBER = "1.0"
PROG_VERSION_DATE = "2019-10-03"
PROG_SHORT_DESCRIPTION = "Memacs for file name time stamp"
PROG_TAG = "filedatestamps"
PROG_DESCRIPTION = """This script parses a text file containing absolute paths
to files with ISO datestamps and timestamps in their file names:

Examples:  "2010-03-29T20.12 Divegraph.tiff"
           "2010-12-31T23.59_Cookie_recipies.pdf"
           "2011-08-29T08.23.59_test.pdf"

Emacs tmp-files like file~ are automatically ignored

Then an Org-mode file is generated that contains links to the files.

At files, containing only the date information i.e. "2013-03-08_foo.txt", the
time will be extracted from the filesystem, when both dates are matching. To
Turn off this feature see argument "--skip-file-time-extraction"
"""
COPYRIGHT_YEAR = "2011 and higher"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


def main():
    global memacs
    memacs = FileNameTimeStamps(prog_version=PROG_VERSION_NUMBER,
                                prog_version_date=PROG_VERSION_DATE,
                                prog_description=PROG_DESCRIPTION,
                                prog_short_description=PROG_SHORT_DESCRIPTION,
                                prog_tag=PROG_TAG,
                                copyright_year=COPYRIGHT_YEAR,
                                copyright_authors=COPYRIGHT_AUTHORS)
    memacs.handle_main()


if __name__ == "__main__":
    main()
