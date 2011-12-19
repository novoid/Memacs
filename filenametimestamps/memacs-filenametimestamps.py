#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import sys, os
# needed to import common.*
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.memacs import Memacs
from common.orgformat import OrgFormat
import re
import logging
import time

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2011-12-18"
PROG_SHORT_DESCRIPTION = u"Memacs for file name time stamp"
PROG_TAG = u"filedatestamps"
PROG_DESCRIPTION = u"""This script parses a text file containing absolute paths to files
with ISO datestamps and timestamps in their file names:

Examples:  "2010-03-29T20.12 Divegraph.tiff"
           "2010-12-31T23.59_Cookie_recipies.pdf"
           "2011-08-29T08.23.59_test.pdf"

Emacs tmp-files like file~ are automatically ignored

Then an Org-mode file is generated that contains links to the files.
"""


DATESTAMP_REGEX = re.compile("([12]\d{3})-([01]\d)-([0123]\d)")
TIMESTAMP_REGEX = re.compile("([12]\d{3})-([01]\d)-([0123]\d)T([012]\d)[.]([012345]\d)([.]([012345]\d))?")
class FileNameTimeStamps(Memacs):
        
    def _parser_add_arguments(self):
        Memacs._parser_add_arguments(self)
        
        self._parser.add_argument("-f", "--folder", dest="filenametimestamps_folder", action="append", \
                        help="path to a folder to search for filenametimestamps, " + 
                        "multiple folders can be specified: -f /path1 -f /path2")
    
        self._parser.add_argument("-x", "--exclude", dest="exclude_folder",
                        help="path to excluding folder, for more excludes use this: -x /path/exclude -x /path/exclude")
    
        self._parser.add_argument("-l", "--follow-links", dest="follow_links", action="store_true",
                        help="follow symbolics links, default False")
    
    def _parser_parse_args(self):
        Memacs._parser_parse_args(self)
        if not self._args.filenametimestamps_folder:
            self._parser.error("no filenametimestamps_folder specified")
    
        for f in self._args.filenametimestamps_folder:
            if not os.path.isdir(f):
                self._parser.error("Check the folderlist - one or more aren't folders")
    
    def _main(self):
        for folder in self._args.filenametimestamps_folder:
            for rootdir, dirs, files in os.walk(folder, followlinks=self._args.follow_links):
                if self._args.exclude_folder and rootdir in self._args.exclude_folder:
                    logging.info("ignoring dir: " + rootdir)
                else:
                    for file in files: 
                        if DATESTAMP_REGEX.match(file) and file[-1:] != '~': #  don't handle emacs tmp files (file~)
                            link = rootdir + os.sep + file
                            logging.debug(link)
                            if TIMESTAMP_REGEX.match(file):
                                # if we found a timestamp too,take hours,minutes and optionally seconds from this timestamp
                                orgdate = OrgFormat.strdatetimeiso8601(TIMESTAMP_REGEX.match(file).group())
                                logging.debug("found timestamp: " + orgdate)
                            else:
                                orgdate = OrgFormat.strdate(DATESTAMP_REGEX.match(file).group())
                                orgdate_time_tupel = OrgFormat.datetupeliso8601(DATESTAMP_REGEX.match(file).group())
                                file_datetime = time.localtime(os.path.getmtime(link))
                                # check if the file - time information matches year,month,day , then update time
                                if  file_datetime.tm_year == orgdate_time_tupel.tm_year and \
                                    file_datetime.tm_mon == orgdate_time_tupel.tm_mon  and \
                                    file_datetime.tm_mday == orgdate_time_tupel.tm_mday:
                                    logging.debug("found a time in file. setting time from %s to %s", orgdate, OrgFormat.date(file_datetime, True))
                                    orgdate = OrgFormat.date(file_datetime, True)
                            # write entry to org file
                            self._writer.write_org_subitem(orgdate + " " + OrgFormat.link(link=link, description=file))
                            
if __name__ == "__main__":
    
    memacs = FileNameTimeStamps(prog_version=PROG_VERSION_NUMBER
                           , prog_version_date=PROG_VERSION_DATE
                           , prog_description=PROG_DESCRIPTION
                           , prog_short_description=PROG_SHORT_DESCRIPTION
                           , prog_tag=PROG_TAG
                           , write_footer=True)
    memacs.handle_main()
