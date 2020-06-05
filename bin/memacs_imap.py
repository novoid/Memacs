#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-04 16:19:02 vk>

from memacs.imap import ImapMemacs

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2011-12-30"
PROG_SHORT_DESCRIPTION = "Memacs for imap emails"
PROG_TAG = "emails:imap"
PROG_DESCRIPTION = """The memacs module will connect to an IMAP Server,
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
COPYRIGHT_YEAR = "2011-2013"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


def main():
    global memacs
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


if __name__ == "__main__":
    main()
