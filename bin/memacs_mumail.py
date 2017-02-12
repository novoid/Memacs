#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Time-stamp: <2015-04-30 17:12:02 vs>

from memacs.mu import MuMail

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2015-03-08"
PROG_SHORT_DESCRIPTION = u"Memacs for Mu Mails"
PROG_TAG = u"emails:mumail"
PROG_DESCRIPTION = u"""This memacs module will connect mu mail database,
fetch all mails and writes them to an orgfile.
"""
CONFIG_PARSER_NAME = ""
COPYRIGHT_YEAR = "2011-2015"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Stephanus Volke <post@stephanus-volke.de>"""

if __name__ == "__main__":
    
    memacs = MuMail(
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
