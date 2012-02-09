#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-01-07 19:55:25 armin>

from memacs.imap import ImapMemacs

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2011-12-30"
PROG_SHORT_DESCRIPTION = u"Memacs for imap emails"
PROG_TAG = u"emails:imap"
PROG_DESCRIPTION = u"""The memacs module will connect to an IMAP Server,
fetch all mails of given folder (-f or --folder-name <folder>),
parses the mails and writes them to an orgfile.

This module uses configfiles (-c, --config-file <path>)

sample-config:

[memacs-imap]
host = imap.gmail.com
port = 993
user = foo@gmail.com
password = bar
"""
CONFIG_PARSER_NAME = "memacs-imap"
COPYRIGHT_YEAR = "2011-2012"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


if __name__ == "__main__":
    memacs = ImapMemacs(
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
