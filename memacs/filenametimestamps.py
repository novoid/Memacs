#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2022-05-15 16:18:39 vk>

import codecs
import logging
import os
import re
import sys
import time

from orgformat import OrgFormat, TimestampParseException

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties

# Note: here, the day of the month is optional to allow "2019-10
# foo.txt" as valid ISO datestamp which will be changed to
# "<2019-10-01..." later on.
DATETIME_PATTERN = '([12]\d{3})-([01]\d)(-([0123]\d))?([- _T]([012]\d)[-_.]([012345]\d)([-_.]([012345]\d))?)?'
DATETIME_REGEX = re.compile('^' + DATETIME_PATTERN + '(--?' + DATETIME_PATTERN + ')?')


class FileNameTimeStamps(Memacs):

    def _parser_add_arguments(self):
        Memacs._parser_add_arguments(self)

        self._parser.add_argument("-f", "--folder",
                                  dest="filenametimestamps_folder",
                                  action="append", nargs='*',
                                  help="path to a folder to search for " +
                                       "filenametimestamps, " +
                                       "multiple folders can be specified: " +
                                       "-f /path1 -f /path2")

        self._parser.add_argument("-x", "--exclude", dest="exclude_folder", action="append", nargs='*',
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
            for f in self._args.filenametimestamps_folder[0]:
                if not os.path.isdir(f):
                    self._parser.error("Check the folderlist argument: " +
                                       "[" + str(f) + "] and probably more aren't folders")

    def __ignore_dir(self, ignore_dir):
        """
        @param ignore_dir: should this ignore_dir be ignored?
        @param return: true  - if ignore_dir should be ignored
                       false - otherwise
        """
        ## [item for ... ] -> flatten out list of lists to a single list
        if self._args.exclude_folder and \
           ignore_dir in [item for sublist in self._args.exclude_folder for item in sublist]:
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

    def __check_datestamp_correctness(self, datestamp):
        """
        Checks a datestamp 'YYYY.MM.DD' if its components are a valid date.
        """

        if len(datestamp) != 10:
            return False
        try:
            year = int(datestamp[:4])
            month = int(datestamp[5:7])
            day = int(datestamp[8:10])
        except ValueError:
            logging.debug('__check_datestamp_correctness(' + str(datestamp) + ') does not follow YYYY-MM-DD with integers as components for year, month, day.')
            return False

        if year < 1900 or \
           year > 2100 or \
           month < 1 or \
           month > 12 or \
           day < 1 or \
           day > 31:
            logging.debug('__check_datestamp_correctness(' + str(datestamp) + ') NEGATIVE')
            return False
        else:
            try:
                orgdate = OrgFormat.strdate(datestamp)
            except ValueError:
                return False
            return True

    def __check_timestamp_correctness(self, timestamp):
        """
        Checks a timestamp 'HH.MM' (no seconds) if its components are a valid time.
        """
        if len(timestamp) != 5 or timestamp[2:3] != ':':
            return False
        try:
            hour = int(timestamp[:2])
            minute = int(timestamp[-2:])
        except ValueError:
            logging.debug('__check_timestamp_correctness(' + str(timestamp) + ') does not follow HH.MM with integers as components for hour and minute (and leading zeros).')
            return False

        if hour < 0 or \
           hour > 23 or \
           minute < 0 or \
           minute > 59:
            logging.debug('__check_timestamp_correctness(' + str(timestamp) + ') NEGATIVE')
            return False
        else:
            return True

    def __extract_days_and_times(self, match):
        """Takes a RegEx match group of corresponding DATETIME_REGEX and
        derives booleans that indicate the existance of months,
        days, hours and minutes. Further more, it extracts ISO
        days ('YYYY-MM-DD') for one and an optional a second day
        and their corresponding time-stamps lacking their optional
        seconds ('HH:MM').

        """

        # DATETIME_REGEX.match('2019-10-03T01.02.03--2019-10-04T23.59.59') results in:
        #   1    ('2019',
        #   2    '10',
        #  (3)  '-03',
        #   4    '03',
        #  (5)   'T01.02.03',
        #   6    '01',
        #   7    '02',
        #  (8)   '.03',
        #   9    '03',
        # (10)   '--2019-10-04T23.59.59',
        #  11    '2019',
        #  12    '10',
        # (13)   '-04',
        #  14    '04',
        # (15)   'T23.59.59',
        #  16    '23',
        #  17    '59',
        # (18)   '.59',
        #  19    '59')
        has_1ym = match.group(1) and match.group(2)
        has_1ymd = has_1ym and match.group(4)
        has_1ymdhm = has_1ymd and match.group(6) and match.group(7)
        has_1ymdhms = has_1ymdhm and match.group(9)
        has_2ym = match.group(11) and match.group(12)
        has_2ymd = has_2ym and match.group(14)
        has_2ymdhm = has_2ymd and match.group(15) and match.group(17)
        has_2ymdhms = has_2ymdhm and match.group(19)

        # initialize return values with None - their default if not found
        day1 = None
        day2 = None
        time1 = None
        time2 = None

        # this method does not make any sense when the first day
        # is not found. Please check for a positive match before.
        assert(has_1ym)

        # Note: assumption is that the match.group entries do
        # contain leading zeros already.

        if has_1ymd:
            day1 = match.group(1) + '-' + match.group(2) + '-' + match.group(4)
        elif has_1ym:
            # assume if day of month is missing, set it to 1; allowing
            # '2019-10' as date-stamp and change to '2019-10-01'
            day1 = match.group(1) + '-' + match.group(2) + '-01'
            has_1ymd = True  # overwrite value from data with value including the added day
        if has_1ymdhms or has_1ymdhm:
            time1 = match.group(6) + ':' + match.group(7)

        if has_2ymd:
            day2 = match.group(11) + '-' + match.group(12) + '-' + match.group(14)
        elif has_2ym:
            # see comment above about missing day of month
            day2 = match.group(11) + '-' + match.group(12) + '-01'
        if has_2ymdhms or has_2ymdhm:
            time2 = match.group(16) + ':' + match.group(17)

        return has_1ymd, has_1ymdhm, has_2ymd, has_2ymdhm, day1, time1, day2, time2

    def __check_if_days_in_timestamps_are_same(self, file_datetime, filename_datestamp):
        """handles timestamp differences for timestamps containing only day
        information (and not times). filename_datestamp is like
        'YYYY-MM-DD'."""

        file_year = file_datetime.tm_year
        file_month = file_datetime.tm_mon
        file_day = file_datetime.tm_mday

        try:
            filename_year = int(filename_datestamp[:4])
            filename_month = int(filename_datestamp[5:7])
            filename_day = int(filename_datestamp[8:10])
        except ValueError:
            logging.debug('__check_if_days_in_timestamps_are_same(..., ' + str(filename_datestamp) + ') does not follow YYYY-MM-DD with integers as components for year, month, day.')
            return False

        if file_year != filename_year or \
           file_month != filename_month or \
           file_day != filename_day:
            return False

        logging.debug('__check_if_days_in_timestamps_are_same: days match!')
        return True

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

        orgdate = False  # set to default value

        if self._args.force_filedate_extraction:
            # in this case, skip any clever
            # extraction mechanism to extract
            # date/time from file name and use
            # the mtime instead:
            logging.debug('__handle_file: force_filedate_extraction: using datetime from mtime of file')
            file_datetime = time.localtime(os.path.getmtime(link))
            orgdate = OrgFormat.date(file_datetime, show_time=True)
            self.__write_file(file, link, orgdate)
            return

        # very basic checks for correctness (e.g., month=20, hour=70)
        # are part of these RegEx (and do not have to be checked
        # below)
        filename_timestamp_match = DATETIME_REGEX.match(file)
        logging.debug('__handle_file: filename_timestamp_match? ' + str(filename_timestamp_match is True))

        if filename_timestamp_match:
            # day1/2 are like 'YYYY-MM-DD' time1/2 like 'HH:MM':
            has_1ymd, has_1ymdhm, has_2ymd, has_2ymdhm, \
                day1, time1, day2, time2 = self.__extract_days_and_times(filename_timestamp_match)

            # Note: following things are available for formatting:
            # self._args.inactive_timestamps -> Bool
            # OrgFormat.strdate('YYYY-MM-DD', inactive=False) -> <YYYY-MM-DD Sun>
            # OrgFormat.strdate('YYYY-MM-DD HH:MM', inactive=False, show_time=True) -> <YYYY-MM-DD Sun HH:MM>

            assert(has_1ymd)
            try:
                if has_1ymdhm:
                    if self.__check_datestamp_correctness(day1):
                        if self.__check_timestamp_correctness(time1):
                            orgdate = OrgFormat.strdate(day1 + ' ' + time1, inactive=self._args.inactive_timestamps, show_time=True)
                        else:
                            logging.warning('File "' + file + '" has an invalid timestamp (' + str(time1) + '). Skipping this faulty time-stamp.')
                            orgdate = OrgFormat.strdate(day1, inactive=self._args.inactive_timestamps)
                    else:
                        logging.warning('File "' + file + '" has an invalid datestamp (' + str(day1) + ').')
                        # omit optional second day if first has an issue:
                        has_2ymd = False
                        has_2ymdhm = False
                        orgdate = False
                elif has_1ymd:  # missing time-stamp for day1
                    if self.__check_datestamp_correctness(day1):
                        if not self._args.skip_filetime_extraction:
                            # we've got only a day but we're able to determine
                            # time from file mtime, if same as ISO day in file
                            # name:
                            logging.debug('__handle_file: try to get file time from mtime if days match between mtime and filename ISO ...')
                            file_datetime = time.localtime(os.path.getmtime(link))
                            if self.__check_if_days_in_timestamps_are_same(file_datetime, day1):
                                orgdate = OrgFormat.date(file_datetime, inactive=self._args.inactive_timestamps, show_time=True)
                            else:
                                logging.debug('__handle_file: day of mtime and filename ISO differs, using filename ISO day')
                                orgdate = OrgFormat.strdate(day1, inactive=self._args.inactive_timestamps)
                        else:
                            # we've got only a day and determining mtime
                            # is not planned, so use the day as date-stamp
                            orgdate = OrgFormat.strdate(day1, inactive=self._args.inactive_timestamps)
                    else:
                        logging.warning('File "' + file + '" has an invalid datestamp (' + str(day1) + ').')
                        orgdate = False
                else:
                    logging.warning('File "' + file + '" has an invalid datestamp (' + str(day1) + '). Skipping this faulty date.')
                    # omit optional second day if first has an issue:
                    has_2ymd = False
                    has_2ymdhm = False

                # there is a time range:
                if has_2ymdhm:
                    assert(day2)
                    if self.__check_datestamp_correctness(day2):
                        if self.__check_timestamp_correctness(time2):
                            orgdate += '--' + OrgFormat.strdate(day2 + ' ' + time2, inactive=self._args.inactive_timestamps, show_time=True)
                        else:
                            logging.warning('File "' + file + '" has an invalid timestamp (' + str(time2) + '). Skipping this faulty time-stamp.')
                            orgdate += '--' + OrgFormat.strdate(day2, inactive=self._args.inactive_timestamps)
                    else:
                        logging.warning('File "' + file + '" has an invalid datestamp (' + str(day2) + '). Skipping this faulty date.')
                elif has_2ymd:
                    assert(day2)
                    if self.__check_datestamp_correctness(day2):
                        orgdate += '--' + OrgFormat.strdate(day2, inactive=self._args.inactive_timestamps)
                    else:
                        logging.warning('File "' + file + '" has an invalid datestamp (' + str(day2) + '). Skipping this faulty date.')
            except TimestampParseException:
                logging.error('File "' + str(file) + '" has in invalid date- or timestamp. OrgFormat of one of day1: "' +
                              str(day1) + '" time1: "' + str(time1) + '" day2: "' +
                              str(day2) + '" time2: "' + str(time2) + '" ' +
                              'failed with TimestampParseException. Skipping this faulty date.')
                orgdate = False

        else:
            logging.debug('__handle_file: no date- nor timestamp')
            orgdate = False

        if not orgdate and self._args.skip_notimestamp_files:
            logging.debug('__handle_file: file had no or wrong time-stamp and you decided to skip them.')
            return

        self.__write_file(file, link, orgdate)
        logging.debug('__handle_file: using orgdate: ' + str(orgdate))
        return

    def _main(self):

        if self._args.filenametimestamps_folder:

            for folder in [item for sublist in self._args.filenametimestamps_folder for item in sublist]:
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
