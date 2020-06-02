#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-04 16:18:15 vk>

from memacs.csv import Csv

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2012-02-24"
PROG_SHORT_DESCRIPTION = "Memacs for csv files"
PROG_TAG = "csv"
PROG_DESCRIPTION = """
This Memacs module will parse csv files

"""
# set CONFIG_PARSER_NAME only, when you want to have a config file
# otherwise you can comment it out
# CONFIG_PARSER_NAME="memacs-example"
COPYRIGHT_YEAR = "2012-2013"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


def main():
    global memacs
    memacs = Csv(
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
