#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import sys
import os
import logging
import time
# needed to import common.*
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.orgproperty import OrgProperties
from common.orgformat import OrgFormat
from common.memacs import Memacs


PROG_VERSION_NUMBER = u"0.0"
PROG_VERSION_DATE = u"2011-12-18"
PROG_SHORT_DESCRIPTION = u"Memacs for ... "
PROG_TAG = u"mytag"
PROG_DESCRIPTION = u"""
this class will do ....

Then an Org-mode file is generated that contains ....
"""


class Foo(Memacs):
    def _parser_add_arguments(self):
        Memacs._parser_add_arguments(self)
        # add additional arguments

        #self._parser.add_argument(
        #   "-e", "--example", dest="example",
        #   action="store_true",
        #   help="path to a folder to search for filenametimestamps, " +
        #   "multiple folders can be specified: -f /path1 -f /path2")

    def _parser_parse_args(self):
        Memacs._parser_parse_args(self)
        # parse additional arguments:
        # if self._args.example == ...:
        #     self._parser.error("could not parse foo")

    def _main(self):
        # do all the stuff
        # this function is automatically called to start

        self._writer.write_org_subitem("foo")
        #** foo
        #  :PROPERTIES:
        #  :CREATED: <current timestamp>
        #  :END:

        notes = "bar notes\nfoo notes"
        p = OrgProperties()
        p.add_property("DESCRIPTION", "foooo")
        p.add_property("CREATED", OrgFormat.datetime(time.gmtime(0)))
        self._writer.write_org_subitem("bar", note=notes, properties=p)
        #** bar
        #  bar notes
        #  foo notes
        #  :PROPERTIES:
        #  :DESCRIPTION: foooo
        #  :CREATED: <1970-01-01 Thu 00:00>
        #  :END:

if __name__ == "__main__":
    memacs = Foo(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG)
    memacs.handle_main()
