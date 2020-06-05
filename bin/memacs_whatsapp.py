#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from memacs.whatsapp import WhatsApp

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2017-02-28"
PROG_SHORT_DESCRIPTION = "Memacs for whatsapp"
PROG_TAG = "whatsapp"

COPYRIGHT_YEAR = "2017"
COPYRIGHT_AUTHORS = """Manuel Koell <mankoell@gmail.com>"""


def main():
    memacs = WhatsApp(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS
        )
    memacs.handle_main()


if __name__ == "__main__":
    main()
