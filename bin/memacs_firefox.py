#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-04 16:18:07 vk>

from memacs.firefox import Firefox

PROG_VERSION_NUMBER = "0.0"
PROG_VERSION_DATE = "2018-07-14"
PROG_SHORT_DESCRIPTION = "Memacs for firefox url history "
PROG_TAG = "firefox"
PROG_DESCRIPTION = """
This class will parse firefox history file (places.sqlite) and
produce an org file with all your visited sites
"""
# set CONFIG_PARSER_NAME only, when you want to have a config file
# otherwise you can comment it out
# CONFIG_PARSER_NAME="memacs-example"
COPYRIGHT_YEAR = "2018"
COPYRIGHT_AUTHORS = """Raimon Grau <raimonster@gmail.com>"""


def main():
    global memacs
    memacs = Firefox(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS
        # use_config_parser_name=CONFIG_PARSER_NAME
    )
    memacs.handle_main()


if __name__ == "__main__":
    main()
