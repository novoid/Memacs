#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import sys
import os
import logging
import feedparser
import calendar
import time
# needed to import common.*
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.reader import CommonReader
from common.orgproperty import OrgProperties
from common.orgformat import OrgFormat
from common.memacs import Memacs


PROG_VERSION_NUMBER = u"0.0"
PROG_VERSION_DATE = u"2011-12-18"
PROG_SHORT_DESCRIPTION = u"Memacs for rss feeds"
PROG_TAG = u"rss"
PROG_DESCRIPTION = u"""
This Memacs module will parse rss files.

rss can be read from file (-f FILE) or url (-u URL)

The items are automatically be appended to the org file.


Attention: RSS2.0 is required

Sample Org-entries
: ** [[http://www.wikipedia.org/][link]]: Example entry
:   Here is some text containing an interesting description.
:   :PROPERTIES:
:   :LINK:    [[http://www.wikipedia.org/]]
:   :CREATED: <2009-09-06 Sun 18:45>
:   :ID:      unique string per item
:   :SUMMARY: Here is some text containing an interesting description.
:   :ID:      unique string per item
:   :END:
"""


class RssMemacs(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
           "-u", "--url", dest="url",
           action="store",
           help="url to a rss file")

        self._parser.add_argument(
           "-f", "--file", dest="file",
           action="store",
           help="path to rss file")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if self._args.url and self._args.file:
            self._parser.error("you cannot set both url and file")

        if not self._args.url and not self._args.file:
            self._parser.error("please specify a file or url")

        if self._args.file:
            if not os.path.exists(self._args.file):
                self._parser.error("file %s not readable", self._args.file)
            if not os.access(self._args.file, os.R_OK):
                self._parser.error("file %s not readable", self._args.file)

    def __get_item_data(self, item):
        """
        gets information out of <item>..</item>

        @return:  output, note, properties, tags
                  variables for orgwriter.append_org_subitem
        """
        try:
            #logging.debug(item)
            properties = OrgProperties()
            id = item['id']
            if not id:
                logging.error("got no id")

            unformatted_link = item['link']
            link = OrgFormat.link(unformatted_link)
            short_link = OrgFormat.link(unformatted_link, "link")

            properties.add("link", link)

            output = short_link + ": "
            output += item['title']

            #note = link + "\n"
            note = item['description']
            # was: just take the time (but this is not localtime)
            # updated_time_struct = OrgFormat.datetime(item['updated_parsed'])
            # is: converting updated_parsed UTC --> LOCALTIME
            updated_time_struct = OrgFormat.datetime(
                time.localtime(calendar.timegm(item['updated_parsed'])))
            properties.add("created", updated_time_struct)
            properties.add("id", id)

        except KeyError:
            logging.error("input is not a RSS 2.0")
            sys.exit(1)

        tags = []
        dont_parse = ['title', 'description', 'updated',
                          'updated_parsed', 'link', 'links']
        for i in  item:
            logging.debug(i)
            if i not in dont_parse:
                if (type(i) == unicode or type(i) == str) and \
                type(item[i]) == unicode and  item[i] != "":
                    properties.add(i, item[i])
                else:
                    if i == "tags":
                        for tag in item[i]:
                            logging.debug("found tag: %s", tag['term'])
                            tags.append(tag['term'])

        return output, note, properties, tags

    def _main(self):
        """
        get's automatically called from Memacs class
        """
        # getting data
        if self._args.file:
            data = CommonReader.get_data_from_file(self._args.file)
        elif self._args.url:
            data = CommonReader.get_data_from_url(self._args.url)

        rss = feedparser.parse(data)
        logging.info("title: %s", rss['feed']['title'])
        logging.info("there are: %d entries", len(rss.entries))

        for item in rss.entries:
            logging.debug(item)
            output, note, properties, tags = self.__get_item_data(item)
            self._writer.append_org_subitem(output,
                                            note=note,
                                            properties=properties,
                                            tags=tags)

if __name__ == "__main__":
    memacs = RssMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        append_orgfile=True)
    memacs.handle_main()
