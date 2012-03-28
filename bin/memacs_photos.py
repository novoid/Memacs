#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-10 18:04:01 armin>

from memacs.photos import PhotosMemacs

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2012-03-10"
PROG_SHORT_DESCRIPTION = u"Memacs for photos (exif)"
PROG_TAG = u"photos"
PROG_DESCRIPTION = u"""

This memacs module will walk through a given folder looking for photos.
If a photo is found, it will get a timestamp from the  exif information.

Then an Org-mode file is generated.
"""
COPYRIGHT_YEAR = "2012"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""

if __name__ == "__main__":
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
