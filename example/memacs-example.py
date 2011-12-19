#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import sys, os
from example.foo import Foo
# needed to import common.*
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


PROG_VERSION_NUMBER = u"0.0"
PROG_VERSION_DATE = u"2011-12-18"
PROG_SHORT_DESCRIPTION = u"Memacs for ... "
PROG_TAG = u"mytag"
PROG_DESCRIPTION = u"""
this class will do ....

Then an Org-mode file is generated that contains links to the files.
"""

if __name__ == "__main__":
    memacs = Foo(prog_version=PROG_VERSION_NUMBER
                           , prog_version_date=PROG_VERSION_DATE
                           , prog_description=PROG_DESCRIPTION
                           , prog_short_description=PROG_SHORT_DESCRIPTION
                           , prog_tag=PROG_TAG)
    memacs.handle_main()
