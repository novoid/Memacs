#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import sys
import os
import logging
import feedparser
import re
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
This Memacs module will parse rss files
RSS2.0 is required
TODO
Then to an Org-mode file is generated that contains ...
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
        
        @return
        """
        try:
            #logging.debug(item)
            properties = OrgProperties()
            id = item['id']
            if not id:
                logging.error("got no id")
            output = item['title']
            link = OrgFormat.link(item['link'])
            note = link + "\n"
            note += item['description']
            # old
            # updated_time_struct = OrgFormat.datetime(item['updated_parsed'])
            # new one:
            # converting updated_parsed UTC --> LOCALTIME
            updated_time_struct = OrgFormat.datetime(
                time.localtime(calendar.timegm(item['updated_parsed'])))
            properties.add_property("created", updated_time_struct)
            properties.add_property("id", id)
            
        except KeyError:
            logging.error("input is not a RSS 2.0")
            sys.exit(1)
        
        dont_parse = ['title', 'description', 'link', 'updated',
                          'updated_parsed', 'links']
        for i in  item:
            if i not in dont_parse:
                if type(i) == unicode and type(item[i]) == unicode:
                    properties.add_property(i, item[i])

        return output, note, properties, id

    def __get_existing_ids(self):
        
        # if we have no outputfile, then we cannot have existing ids
        if not self._args.outputfile:
            return []
        
        existing_ids = []
        
        data = CommonReader.get_data_from_file(self._args.outputfile)
        for found_id in re.findall(":ID:(.*)", data):
            found_id = found_id.strip()
            if found_id != "":
                existing_ids.append(found_id)
        
        logging.debug("there are already %d entries", len(existing_ids))
        return existing_ids

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
        
        existing_ids = self.__get_existing_ids()
        
        for item in rss.entries:
            output, note, properties, id = self.__get_item_data(item)
            if id not in existing_ids:
                logging.debug("appending item to file")
                self._writer.write_org_subitem(output, note=note, properties=properties)
            else:
                logging.debug("not appending item to file")

if __name__ == "__main__":
    memacs = RssMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        append_orgfile=True)
    memacs.handle_main()
