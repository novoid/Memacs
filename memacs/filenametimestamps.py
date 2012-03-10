#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import os
from lib.memacs import Memacs
from lib.orgformat import OrgFormat
from lib.orgformat import TimestampParseException
from lib.orgproperty import OrgProperties
import re
import logging
import time

DATESTAMP_REGEX = re.compile("([12]\d{3})-([01]\d)-([0123]\d)")
TIMESTAMP_REGEX = re.compile("([12]\d{3})-([01]\d)-([0123]\d)T([012]\d)" + \
                             "[.]([012345]\d)([.]([012345]\d))?")


class FileNameTimeStamps(Memacs):

    def _parser_add_arguments(self):
        Memacs._parser_add_arguments(self)

        self._parser.add_argument("-f", "--folder",
                                  dest="filenametimestamps_folder",
                                  action="append",
                                  help="path to a folder to search for " + \
                                      "filenametimestamps, " + \
                                  "multiple folders can be specified: " + \
                                      "-f /path1 -f /path2")

        self._parser.add_argument("-x", "--exclude", dest="exclude_folder",
                        help="path to excluding folder, for more excludes " + \
                             "use this: -x /path/exclude -x /path/exclude")

        self._parser.add_argument("-l", "--follow-links",
                                  dest="follow_links", action="store_true",
                                  help="follow symbolics links," + \
                                      " default False")

    def _parser_parse_args(self):
        Memacs._parser_parse_args(self)
        if not self._args.filenametimestamps_folder:
            self._parser.error("no filenametimestamps_folder specified")

        for f in self._args.filenametimestamps_folder:
            if not os.path.isdir(f):
                self._parser.error("Check the folderlist - " + \
                                       "one or more aren't folders")

    def __ignore_dir(self, ignore_dir):
        """
        @param ignore_dir: should this ignore_dir be ignored?
        @param return: true  - if ignore_dir should be ignored
                       false - otherwise
        """
        if self._args.exclude_folder and \
        ignore_dir in self._args.exclude_folder:
            logging.info("ignoring ignore_dir: " + ignore_dir)
            return True
        else:
            return False

    def __handle_folder(self, folder):
        """
        walks through a folder
        """
        for rootdir, dirs, files in os.walk(folder,
                                        followlinks=self._args.follow_links):
            if not self.__ignore_dir(rootdir):
                for file in files:
                    self.__handle_file(file, rootdir)

    def __parse_and_write_file(self, file, link):
        """
        Parses the date+time and writes entry to outputfile

        @param file: filename
        @param link: path
        """
        if TIMESTAMP_REGEX.match(file):
            # if we found a timestamp too,take hours,min
            # and optionally seconds from this timestamp
            timestamp = TIMESTAMP_REGEX.match(file).group()
            orgdate = OrgFormat.strdatetimeiso8601(timestamp)
            logging.debug("found timestamp: " + orgdate)
        else:
            datestamp = DATESTAMP_REGEX.match(file).group()
            orgdate = OrgFormat.strdate(datestamp)
            orgdate_time_tupel = OrgFormat.datetupeliso8601(datestamp)
            file_datetime = time.localtime(os.path.getmtime(link))
            # check if the file - time information matches year,month,day,
            # then update time
            if file_datetime.tm_year == orgdate_time_tupel.tm_year and \
                    file_datetime.tm_mon == orgdate_time_tupel.tm_mon and \
                    file_datetime.tm_mday == orgdate_time_tupel.tm_mday:
                logging.debug("found a time in file.setting %s-->%s",
                              orgdate, OrgFormat.date(file_datetime, True))
                orgdate = OrgFormat.date(file_datetime, True)

        # write entry to org file
        output = OrgFormat.link(link=link, description=file)
        # we need optional data for hashing due it can be, that more
        # than one file have the same timestamp
        properties = OrgProperties(data_for_hashing=output)
        self._writer.write_org_subitem(timestamp=orgdate,
                                       output=output,
                                       properties=properties)

    def __handle_file(self, file, rootdir):
        """
        handles a file
        """
        # don't handle emacs tmp files (file~)
        if DATESTAMP_REGEX.match(file) and file[-1:] != '~':
            link = rootdir + os.sep + file
            logging.debug(link)
            try:
                # we put this in a try block because:
                # if a timestamp is false i.e. 2011-14-19 or false time
                # we can handle those not easy with REGEX, therefore we have
                # an Exception TimestampParseException, which is thrown,
                # wen strptime (parse from string to time tupel) fails
                self.__parse_and_write_file(file, link)
            except TimestampParseException, e:
                logging.warning("False date(time) in file: %s", link)

    def _main(self):
        for folder in self._args.filenametimestamps_folder:
            self.__handle_folder(folder)
