#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-04 16:19:39 vk>

from memacs.photos import PhotosMemacs

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2012-03-10"
PROG_SHORT_DESCRIPTION = "Memacs for photos (exif)"
PROG_TAG = "photos"
PROG_DESCRIPTION = """

This memacs module will walk through a given folder looking for photos.
If a photo is found, it will get a timestamp from the  exif information.

Then an Org-mode file is generated.
"""
COPYRIGHT_YEAR = "2012-2013"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


def main():
    global memacs
    memacs = PhotosMemacs(
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
