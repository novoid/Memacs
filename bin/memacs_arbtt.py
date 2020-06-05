#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2017-02-07 19:25 manu>

from memacs.arbtt import Arbtt

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2017-02-07"
PROG_SHORT_DESCRIPTION = "Memacs for arbtt"
PROG_TAG = "arbtt"
PROG_DESCRIPTION = """
This Memacs module will parse arbtt stats ....

"""

COPYRIGHT_YEAR = "2017"
COPYRIGHT_AUTHORS = """Manuel Koell <mankoell@gmail.com>"""


def main():
    global memacs
    memacs = Arbtt(
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
