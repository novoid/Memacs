#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-04 16:18:07 vk>

from memacs.twitter import Twitter

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2013-09-01"
PROG_SHORT_DESCRIPTION = "Memacs for Twitter "
PROG_TAG = "mytag"
PROG_DESCRIPTION = """
This Memacs module will process your Twitter timeline ....


sample config:
[memacs-twitter]           <-- "memacs-example" has to be CONFIG_PARSER_NAME
APP_KEY =
APP_SECRET =
OAUTH_TOKEN =
OAUTH_TOKEN_SECRET =
screen_name =
count =


"""
# set CONFIG_PARSER_NAME only, when you want to have a config file
# otherwise you can comment it out
CONFIG_PARSER_NAME="memacs-twitter"
COPYRIGHT_YEAR = "2013"
COPYRIGHT_AUTHORS = """Ian Barton <ian@manor-farm.org>"""


def main():
    global memacs
    memacs = Twitter(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS,
        use_config_parser_name=CONFIG_PARSER_NAME
    )
    memacs.handle_main()


if __name__ == "__main__":
    main()
