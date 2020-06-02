#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-04 16:18:40 vk>

from memacs.git import GitMemacs

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2011-12-20"
PROG_SHORT_DESCRIPTION = "Memacs for git files "
PROG_TAG = "git"
PROG_DESCRIPTION = """
This class will parse files from git rev-parse output

use following command to generate input file
$ git rev-list --all --pretty=raw > /path/to/input file

Then an Org-mode file is generated that contains all commit message

If outputfile is specified, only non-existing commits are appended
"""
COPYRIGHT_YEAR = "2011-2013"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


def main():
    global memacs
    memacs = GitMemacs(
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
