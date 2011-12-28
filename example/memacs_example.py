#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-28 20:25:37 armin>

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
COPYRIGHT_YEAR = "2011-2012" 
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>, 
Armin Wieser <armin.wieser@gmail.com>"""


class Foo(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        #self._parser.add_argument(
        #   "-e", "--example", dest="example",
        #   action="store_true",
        #   help="path to a folder to search for filenametimestamps, " +
        #   "multiple folders can be specified: -f /path1 -f /path2")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        # if self._args.example == ...:
        #     self._parser.error("could not parse foo")

    def _main(self):
        """
        get's automatically called from Memacs class
        """
        # do all the stuff
        
        logging.info("foo started")

        # use logging.debug() for debug messages
        # use logging.error() for error messages
        # use logging.info() instead of print for informing user
        #
        # on an fatal error:
        # use logging.error() and sys.exit(1) 

        timestamp = time.gmtime(0)
        # note: timestamp has to be a struct_time object
        self._writer.write_org_subitem(timestamp=timestamp,
                                       output="foo")
       
        # writes following:        
        #** <1970-01-01 Thu 00:00> foo
        #   :PROPERTIES:
        #   :ID:             da39a3ee5e6b4b0d3255bfef95601890afd80709
        #   :END:
        
        notes = "bar notes\nfoo notes"
        
        p = OrgProperties(data_for_hashing="read comment below")
        # if a hash is not unique only with its :PROPERTIES: , then
        # set data_for_hasing string additional information i.e. the output
        # , which then makes the hash really unique
        p.add("DESCRIPTION", "foooo")
        p.add("CREATED", OrgFormat.datetime(time.gmtime(0)))

        tags = [u"tag1", u"tag2"]
        
        timestamp = time.gmtime(0)
        
        self._writer.write_org_subitem(timestamp=timestamp,
                                       output="bar",
                                       note=notes,
                                       properties=p,
                                       tags=tags)
        # writes following:
        #** <1970-01-01 Thu 00:00> bar    :tag1:tag2:
        #   bar notes
        #   foo notes
        #   :PROPERTIES:
        #   :DESCRIPTION:    foooo
        #   :CREATED:        <1970-01-01 Thu 00:00>
        #   :ID:             47341f0e0fa6e13768a69bc302dfa9f834747827
        #   :END:


if __name__ == "__main__":
    memacs = Foo(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS
        )
    memacs.handle_main()
