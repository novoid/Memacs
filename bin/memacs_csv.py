#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-02-22 17:12:59 armin>

from memacs.csv import Csv

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2012-02-24"
PROG_SHORT_DESCRIPTION = u"Memacs for csv files"
PROG_TAG = u"csv"
PROG_DESCRIPTION = u"""
This Memacs module will parse csv files

Then an Org-mode file is generated that contains ....

if youre module needs a config file please give information about usage:

sample config:
[memacs-example]           <-- "memacs-example" has to be CONFIG_PARSER_NAME
foo = 0
bar = 1

"""
# set CONFIG_PARSER_NAME only, when you want to have a config file 
# otherwise you can comment it out
# CONFIG_PARSER_NAME="memacs-example" 
COPYRIGHT_YEAR = "2012"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


if __name__ == "__main__":
    memacs = Csv(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS
#       use_config_parser_name=CONFIG_PARSER_NAME
        )
    memacs.handle_main()