#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2017-04-13 22:23:42 vk>

from memacs.simplephonelogs import SimplePhoneLogsMemacs

PROG_VERSION_NUMBER = "0.2"
PROG_VERSION_DATE = "2017-04-13"
PROG_SHORT_DESCRIPTION = "Memacs for simple phone logs"
PROG_TAG = "phonelog"
PROG_DESCRIPTION = """
This Memacs module will parse simple log files which were written
for example by Tasker.

sample log file: (DATE # TIME # WHAT # BATTERYSTATE # UPTIMESECONDS)
2012-11-20 # 11.56 # boot     #   89 # 6692
2012-11-20 # 11.56 # boot     #   89 # 6694
2012-11-20 # 19.59 # shutdown #   72 # 35682
2012-11-20 # 21.32 # boot     #   71 # 117
2012-11-20 # 23.52 # shutdown #  63 # 8524
2012-11-21 # 07.23 # boot # 100 # 115
2012-11-21 # 07.52 # wifi-home # 95 # 1879
2012-11-21 # 08.17 # wifi-home-end # 92 # 3378
2012-11-21 # 13.06 # boot # 77 # 124
2012-11-21 # 21.08 # wifi-home # 50 # 29033
2012-11-21 # 21.15 # charging-start # 49 # 29253
2012-11-21 # 21.45 # charging-end # 95 # 32758
2012-11-22 # 00.12 # shutdown #  83 # 40089
2012-11-29 # 08.47 # boot # 100 # 114
2012-11-29 # 08.48 # wifi-home # 100 # 118
2012-11-29 # 09.41 # wifi-home-end # 98 # 3317
2012-11-29 # 14.46 # wifi-office # 81 # 21633
2012-11-29 # 16.15 # wifi-home # 76 # 26955
2012-11-29 # 17.04 # wifi-home-end # 74 # 29912
2012-11-29 # 23.31 # shutdown #  48 # 53146

Then an Org-mode file is generated accordingly.
"""
COPYRIGHT_YEAR = "2013"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>"""


def main():
    global memacs
    memacs = SimplePhoneLogsMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS
    )
    memacs.handle_main()


if __name__ == "__main__":
    main()
