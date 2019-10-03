#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-10-03 13:34:20 vk>

import os
from memacs.lib.memacs import Memacs
from memacs.lib.orgformat import OrgFormat, TimestampParseException
from memacs.lib.orgproperty import OrgProperties
import re
import logging
import time
import sys
import codecs

DATESTAMP_REGEX = re.compile("([12]\d{3})-([01]\d)(-([0123]\d))?")
TIMESTAMP_REGEX = re.compile("([12]\d{3})-([01]\d)-([0123]\d)T([012]\d)[.]([012345]\d)([.]([012345]\d))?")


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
                                  help="by default, if there is an ISO datestamp without time, the mtime " +
                                  "is used for time extraction, when the ISO days " +
                                  "are matching. If you set this option, this extraction of the file time " +
                                  "is omitted.")

        self._parser.add_argument("--force-file-date-extraction",
                                  dest="force_filedate_extraction",
                                  action="store_true", help="force extraction of the file date and time" +
                                  "even when there is an ISO datestamp in the filename.")

        self._parser.add_argument("--skip-files-with-no-or-wrong-timestamp",
                                  dest="skip_notimestamp_files",
                                  action="store_true",
                                  help="by default, files with a missing or a wrong time-stamp " +
                                  "(2019-12-33) will be linked without Org mode time-stamp. " +
                                  "If you set this option, these files will not be part of the " +
                                  "output at all.")

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

    def __check_timestamp_correctness(self, match):
        """
        Checks a date- or timestamp if its components are a valid date or time.
        """
        # I'll allow, e.g., 2019-00-00 here on purpose

        def check_day(year, month, day):
            if year < 1900 or \
               year > 2100 or \
               month < 0 or \
               month > 12 or \
               day < 0 or \
               day > 31:
                logging.debug('__check_timestamp_correctness(' + str(match.groups()) + ') D NEGATIVE')
                return False
            else:
                return True

        if len(match.groups()) == 4:
            # it's a datestamp, not a time-stamp
            # special case: no day is accepted as well (2019-12)
            # example: 2019-10 -> ('2019', '10', None, None)
            year = int(match.group(1))
            month = int(match.group(2))
            day = 1
            return check_day(year, month, day)

        if len(match.groups()) == 3:
            # it's a datestamp, not a time-stamp
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            return check_day(year, month, day)

        elif len(match.groups()) == 5 or len(match.groups()) == 7:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            hour = int(match.group(4))
            minute = int(match.group(5))

            if match.group(7):
                # for time-stamps with seconds
                second = int(match.group(7))
                if second < 0 or \
                   second > 59:
                    logging.debug('__check_timestamp_correctness(' + str(match.groups()) + ') seconds NEGATIVE')
                    return False

            if not check_day(year, month, day):
                return False
            else:
                if hour < 0 or \
                   hour > 23 or \
                   minute < 0 or \
                   minute > 59:
                    logging.debug('__check_timestamp_correctness(' + str(match.groups()) + ') 5 NEGATIVE')
                    return False
                else:
                    return True

        else:
            logging.error('__check_timestamp_correctness(' + str(match.groups()) + '): INTERNAL ERROR, this should never be reached. Maybe RegEx is not correct?')
            return False

    def __handle_file(self, file, rootdir):
        """
        handles a file (except ending with a tilde)
        """
        # don't handle emacs tmp files (file~)
        if file[-1:] == '~':
            return

        link = os.path.join(rootdir, file)
        logging.debug('__handle_file: ' + '#' * 50)
        logging.debug('__handle_file: ' + link)

        orgdate = False

        if self._args.force_filedate_extraction:
            # in this case, skip any clever
            # extraction mechanism to extract
            # date/time from file name and use
            # the mtime instead:
            logging.debug('__handle_file: force_filedate_extraction: using datetime from mtime of file')
            file_datetime = time.localtime(os.path.getmtime(link))
            orgdate = OrgFormat.datetime(file_datetime)
            self.__write_file(file, link, orgdate)
            return

        # very basic checks for correctness are part of these RegEx (and do not have to be checked below)
        filename_datestamp_match = DATESTAMP_REGEX.match(file)
        filename_timestamp_match = TIMESTAMP_REGEX.match(file)

        if filename_timestamp_match:
            if not self.__check_timestamp_correctness(filename_timestamp_match):
                logging.warn('File "' + file + '" has an invalid timestamp and will be handeld as with a missing time-stamp.')
                orgdate = False
            else:
                logging.debug('__handle_file: found correct timestamp')
                try:
                    orgdate = OrgFormat.strdatetimeiso8601(file[:16])  # ignoring seconds in Org mode time-stamp in any case
                except TimestampParseException:
                    # an incorrect time-stamp like 2019-10-00T23.59
                    # results in an exception here. Do not use it for
                    # the Org mode time-stamp.
                    orgdate = False

        elif filename_datestamp_match:
            if not self.__check_timestamp_correctness(filename_datestamp_match):
                logging.warn('File "' + file + '" has an invalid datestamp. File will be handeld as with a missing time-stamp.')
                orgdate = False
            else:
                logging.debug('__handle_file: found correct datestamp')
                if not filename_datestamp_match.group(3):
                    # special case: 2019-12 -> will be turned into 2019-12-01
                    orgdate = OrgFormat.strdate(file[:7] + '-01', False)
                else:
                    orgdate = OrgFormat.strdate(file[:10], False)

                if not self._args.skip_filetime_extraction:
                    # we've got only a day but we're able to determine
                    # time from file mtime, if same as ISO day in file
                    # name:
                    logging.debug('__handle_file: try to get file time from mtime if days match between mtime and filename ISO ...')
                    file_datetime = time.localtime(os.path.getmtime(link))
                    if self.__check_if_days_in_timestamps_are_same(file_datetime, filename_datestamp_match.groups()):
                        orgdate = OrgFormat.datetime(file_datetime)
                    else:
                        logging.debug('__handle_file: day of mtime and filename ISO differs, using filename ISO')

        else:
            logging.debug('__handle_file: no date- nor timestamp')
            orgdate = False

        if not orgdate and self._args.skip_notimestamp_files:
            logging.debug('__handle_file: file had no or wrong time-stamp and you decided to skip them.')
            return

        self.__write_file(file, link, orgdate)
        logging.debug('__handle_file: using orgdate: ' + str(orgdate))
        return

    def __check_if_days_in_timestamps_are_same(self, file_datetime, filename_datestamp):
        """handles timestamp differences for timestamps containing only day information (and not times)"""

        file_year = file_datetime.tm_year
        file_month = file_datetime.tm_mon
        file_day = file_datetime.tm_mday

        filename_year = int(filename_datestamp[0])
        filename_month = int(filename_datestamp[1])
        if not filename_datestamp[3]:
            # special case: day is not set as in "2019-12"
            return False
        filename_day = int(filename_datestamp[3])

        if file_year != filename_year or \
           file_month != filename_month or \
           file_day != filename_day:
            return False

        logging.debug('__check_if_days_in_timestamps_are_same: days match!')
        return True

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
