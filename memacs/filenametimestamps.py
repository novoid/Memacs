#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-10-02 18:59:27 vk>

import os
from memacs.lib.memacs import Memacs
from memacs.lib.orgformat import OrgFormat
from memacs.lib.orgformat import TimestampParseException
from memacs.lib.orgproperty import OrgProperties
import re
import logging
import time
import sys
import codecs

DATESTAMP_REGEX = re.compile("([12]\d{3})-([01]\d)-([0123]\d)")
TIMESTAMP_REGEX = re.compile("([12]\d{3})-([01]\d)-([0123]\d)T([012]\d)" +
                             "[.]([012345]\d)([.]([012345]\d))?")


class FileNameTimeStamps(Memacs):

    def _parser_add_arguments(self):
        Memacs._parser_add_arguments(self)

        self._parser.add_argument("-f", "--folder",
                                  dest="filenametimestamps_folder",
                                  action="append",
                                  help="path to a folder to search for " +
                                       "filenametimestamps, " +
                                       "multiple folders can be specified: " +
                                       "-f /path1 -f /path2")

        self._parser.add_argument("-x", "--exclude", dest="exclude_folder",
                                  help="path to excluding folder, for more excludes " +
                                  "use this: -x /path/exclude -x /path/exclude")

        self._parser.add_argument("--filelist", dest="filelist",
                                  help="file containing a list of files to process. " +
                                  "either use \"--folder\" or the \"--filelist\" argument, not both.")

        self._parser.add_argument("--ignore-non-existing-items",
                                  dest="ignore_nonexisting", action="store_true",
                                  help="ignores non-existing files or folders within filelist")

        self._parser.add_argument("-l", "--follow-links",
                                  dest="follow_links", action="store_true",
                                  help="follow symbolics links," +
                                  " default False")

        self._parser.add_argument("--skip-file-time-extraction",
                                  dest="skip_filetime_extraction",
                                  action="store_true",
                                  help="skip extraction of the file time " +
                                  "in files containing only the date in " +
                                  "the filename")

        self._parser.add_argument("--force-file-date-extraction",
                                  dest="force_filedate_extraction",
                                  action="store_true",
                                  help="force extraction of the file date" +
                                  " even if there is no ISO datestamp in " +
                                  "the filename")

        self._parser.add_argument("--omit-drawers",
                                  dest="omit_drawers", action="store_true",
                                  help="do not generate drawers that contain " +
                                  "ID properties. Can't be used with \"--append\".")

    def _parser_parse_args(self):
        Memacs._parser_parse_args(self)

        if self._args.filenametimestamps_folder and self._args.filelist:
            self._parser.error("You gave both \"--filelist\" and \"--folder\" argument. Please use either or.\n")

        if self._args.omit_drawers and self._args.append:
            self._parser.error("You gave both \"--append\" and \"--omit-drawers\" argument. Please use either or.\n")

        if not self._args.filelist and not self._args.filenametimestamps_folder:
            self._parser.error("no filenametimestamps_folder specified")

        if self._args.filelist:
            if not os.path.isfile(self._args.filelist):
                self._parser.error("Check the filelist argument: " +
                                   "[" + str(self._args.filelist) + "] is not an existing file")

        if self._args.filenametimestamps_folder:
            for f in self._args.filenametimestamps_folder:
                if not os.path.isdir(f):
                    self._parser.error("Check the folderlist argument: " +
                                       "[" + str(f) + "] and probably more aren't folders")

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

    def __parse_filename_iso_timestamp(self, file, link):
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

            if not self._args.skip_filetime_extraction:

                if os.path.exists(link):
                    file_datetime = time.localtime(os.path.getmtime(link))
                    # check if the file - time information matches year,month,day,
                    # then update time
                    if file_datetime.tm_year == orgdate_time_tupel.tm_year and \
                       file_datetime.tm_mon == orgdate_time_tupel.tm_mon and \
                       file_datetime.tm_mday == orgdate_time_tupel.tm_mday:

                        logging.debug("found a time in file.setting %s-->%s",
                                      orgdate, OrgFormat.date(file_datetime, True))
                        orgdate = OrgFormat.date(file_datetime, True)
                else:
                    logging.debug("item [%s] not found and thus could not determine mtime" % link)

        return orgdate

    def __write_file(self, file, link, timestamp):
        """
        write entry to org file (omit replacement of spaces in file names)
        """
        output = OrgFormat.link(link="file:" + link, description=file, replacespaces=False)
        properties = None
        if not self._args.omit_drawers:
            # we need optional data for hashing due it can be, that more
            # than one file have the same timestamp
            properties = OrgProperties(data_for_hashing=output)
        self._writer.write_org_subitem(timestamp=timestamp,
                                       output=output,
                                       properties=properties)

    def __handle_file(self, file, rootdir):
        """
        handles a file (except ending with a tilde)
        """
        # don't handle emacs tmp files (file~)
        if file[-1:] == '~':
            return

        link = os.path.join(rootdir, file)
        logging.debug(link)

        if self._args.force_filedate_extraction:
            file_datetime = time.localtime(os.path.getmtime(link))

            if self._args.skip_filetime_extraction:
                logging.debug('force_filedate_extraction and skip_filetime_extraction: using date')
                orgdate = OrgFormat.date(file_datetime)
            else:
                logging.debug('force_filedate_extraction and not skip_filetime_extraction: using datetime')
                orgdate = OrgFormat.datetime(file_datetime)

            self.__write_file(file, link, orgdate)

        elif DATESTAMP_REGEX.match(file):
            logging.debug('DATESTAMP_REGEX matches; trying __parse_filename_iso_timestamp() ...')
            try:
                # we put this in a try block because:
                # if a timestamp is false i.e. 2011-14-19 or false time
                # we can handle those not easy with REGEX, therefore we have
                # an Exception TimestampParseException, which is thrown,
                # when strptime (parse from string to time tupel) fails
                orgdate = self.__parse_filename_iso_timestamp(file, link)
                self.__write_file(file, link, orgdate)
            except TimestampParseException:
                logging.debug('__parse_filename_iso_timestamp() caused an TimestampParseException')
                logging.warning("False date(time) in file: %s", link)

    def _main(self):

        if self._args.filenametimestamps_folder:

            for folder in self._args.filenametimestamps_folder:
                self.__handle_folder(folder)

        elif self._args.filelist:

            for rawitem in codecs.open(self._args.filelist, "r", "utf-8"):

                item = rawitem.strip()

                if not os.path.exists(item):
                    if self._args.ignore_nonexisting:
                        logging.debug("File or folder does not exist: [%s] (add due to set ignore-nonexisting argument)", item)
                        self.__handle_file(os.path.basename(item), os.path.dirname(item))
                    else:
                        logging.warning("File or folder does not exist: [%s]", item)
                else:
                    self.__handle_file(os.path.basename(item), os.path.dirname(item))

        else:
            logging.error("\nERROR: You did not provide \"--filelist\" nor \"--folder\" argument. Please use one of them.\n")
            sys.exit(3)
