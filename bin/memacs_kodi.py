#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from memacs.kodi import Kodi

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2018-10-22"
PROG_SHORT_DESCRIPTION = "Memacs for Kodi "
PROG_TAG = "kodi"
PROG_DESCRIPTION = """
this class will parse logs from the Kodi Mediacenter

"""
COPYRIGHT_YEAR = "2018"
COPYRIGHT_AUTHORS = """Max Beutelspacher <max.beutelspacher@mailbox.org>"""


def main():
    global memacs
    memacs = Kodi(
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


if __name__ == "__main__":
    main()
