#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-04 16:18:07 vk>

from memacs.example import Foo

PROG_VERSION_NUMBER = "0.0"
PROG_VERSION_DATE = "2011-12-18"
PROG_SHORT_DESCRIPTION = "Memacs for ... "
PROG_TAG = "mytag"
PROG_DESCRIPTION = """
this class will do ....

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
COPYRIGHT_YEAR = "2011-2013"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


def main():
    global memacs
    memacs = Foo(
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
