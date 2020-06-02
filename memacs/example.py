#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-11-06 15:22:08 vk>

import logging
import time

from orgformat import OrgFormat

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties


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

        #self._parser.add_argument(
        #   "-i", "--int", dest="example_int",
        #   action="store_true",
        #   help="example2",
        #   type=int)

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

        # if you need something from config:
        # attention: foo will be unicode
        # foo = self._get_config_option("foo")

        logging.info("foo started")

        # how to handle config files ?
        # sample config file:
        # ---------8<-----------
        # [memacs-example]
        # foo = 0
        # bar = 1
        # --------->8-----------
        # to read it out, just do following:
        # foo = self._get_config_option("foo")
        # bar = self._get_config_option("bar")

        # use logging.debug() for debug messages
        # use logging.error() for error messages
        # use logging.info() instead of print for informing user
        #
        # on an fatal error:
        # use logging.error() and sys.exit(1)

        timestamp = OrgFormat.date(time.gmtime(0), show_time=True)
        # note: timestamp has to be a struct_time object

        # Orgproperties
        # Option 1: no properties given, specify argument for hashing data
        properties = OrgProperties("hashing data :ALKJ!@# should be unique")
        # Option 2: add properties which are all-together unique
        # properties.add("Category","fun")
        # properties.add("from","me@example.com")
        # properties.add("body","foo")

        self._writer.write_org_subitem(timestamp=timestamp,
                                       output="foo",
                                       properties=properties)

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
        #
        # if you *really*, *really* have already a unique id,
        # then you can call following method:
        # p.set_id("unique id here")

        p.add("DESCRIPTION", "foooo")
        p.add("foo-property", "asdf")

        tags = ["tag1", "tag2"]

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
        #   :FOO-PROPERTY:   asdf
        #   :ID:             97521347348df02dab8bf86fbb6817c0af333a3f
        #   :END:
