#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

from memacs.phonecalls import PhonecallsMemacs

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2012-03-08"
PROG_SHORT_DESCRIPTION = u"Memacs for phonecalls"
PROG_TAG = u"phonecalls"
PROG_DESCRIPTION = u"""
This Memacs module will parse output of phonecalls xml backup files

sample xml file:
<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<calls count="8">
  <call number="+43691234123" duration="59" date="1312563906092" type="1" />
  <call number="06612341234" duration="22" date="1312541215834" type="2" />
  <call number="-1" duration="382" date="1312530691081" type="1" />
  <call number="+4312341234" duration="289" date="1312482327195" type="1" />
  <call number="+4366412341234" duration="70" date="1312476334059" type="1" />
  <call number="+4366234123" duration="0" date="1312473751975" type="2" />
  <call number="+436612341234" duration="0" date="1312471300072" type="3" />
  <call number="+433123412" duration="60" date="1312468562489" type="2" />
</calls>

Then an Org-mode file is generated.
"""
COPYRIGHT_YEAR = "2011-2012"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""

if __name__ == "__main__":
    memacs = PhonecallsMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS
        )
    memacs.handle_main()
