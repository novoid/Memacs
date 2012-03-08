#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

from memacs.sms import SmsMemacs

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2012-03-07"
PROG_SHORT_DESCRIPTION = u"Memacs for sms"
PROG_TAG = u"sms"
PROG_DESCRIPTION = u"""
This Memacs module will parse output of sms xml backup files

sample xml file:
<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<smses count="4">
  <sms protocol="0" address="+436812314123" date="1312452353000" type="1" subject="null" body="did you see the new sms memacs module?" toa="145" sc_toa="0" service_center="+436990008999" read="1" status="-1" locked="0" />
  <sms protocol="0" address="+43612341234" date="1312473895759" type="2" subject="null" body="Memacs FTW!" toa="0" sc_toa="0" service_center="null" read="1" status="-1" locked="0" />
  <sms protocol="0" address="+43612341238" date="1312489550928" type="2" subject="null" body="i like memacs" toa="0" sc_toa="0" service_center="null" read="1" status="-1" locked="0" />
  <sms protocol="0" address="+4312341234" date="1312569121554" type="2" subject="null" body="http://google.at" toa="0" sc_toa="0" service_center="null" read="1" status="-1" locked="0" />
</smses>


Then an Org-mode file is generated.
"""
COPYRIGHT_YEAR = "2011-2012"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""

if __name__ == "__main__":
    memacs = SmsMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS
        )
    memacs.handle_main()
