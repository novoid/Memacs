#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-10-03 15:18:07 br>

from memacs.chrome import Chrome

PROG_VERSION_NUMBER = "0.0"
PROG_VERSION_DATE = "2018-10-02"
PROG_SHORT_DESCRIPTION = "Memacs for chrome url history "
PROG_TAG = "chrome"
PROG_DESCRIPTION = """
This class will parse chrome history file (History) and
produce an org file with all your visited sites
"""
# set CONFIG_PARSER_NAME only, when you want to have a config file
# otherwise you can comment it out
# CONFIG_PARSER_NAME="memacs-example"
COPYRIGHT_YEAR = "2018"
COPYRIGHT_AUTHORS = """Bala Ramadurai <bala@balaramadurai.net>"""


def main():
    global memacs
    memacs = Chrome(
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
