#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import os
import logging
from common.loggingsettings import *  
from common.orgwriter import OrgOutputWriter
from common.argparser import MemacsArgumentParser
import re
from common.orgformat import OrgFormat
import time

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2011-10-28"
SHORT_DESCRIPTION = u"Memacs for file name time stamp"
TAG = u"filedatestamps"
DESCRIPTION = u"""This script parses a text file containing absolute paths to files
with ISO datestamps and timestamps in their file names:

Examples:  "2010-03-29T20.12 Divegraph.tiff"
           "2010-12-31T23.59_Cookie_recipies.pdf"
           "2011-08-29T08.23.59_test.pdf"

Emacs tmp-files like file~ are automatically ignored

Then an Org-mode file is generated that contains links to the files.
"""

DATESTAMP_REGEX = re.compile("([12]\d{3})-([01]\d)-([0123]\d)")
TIMESTAMP_REGEX = re.compile("([12]\d{3})-([01]\d)-([0123]\d)T([012]\d)[.]([012345]\d)([.]([012345]\d))?")

def main():
    ###########################################################################
    parser = MemacsArgumentParser(prog_version=PROG_VERSION_NUMBER,
                                  prog_version_date=PROG_VERSION_DATE,
                                  description=DESCRIPTION,
                                  )
    # adding additional arguments
    parser.add_argument("-f", "--folderlist", dest="folderlist",
                        help="path to one or more folders seperated with \"|\"," + \
                        "i.e.:\"/path/to/folder1|/path/to/folder2|..\"")
    
    parser.add_argument("-x", "--exclude", dest="excludelist",
                        help="path to one or more folders seperated with \"|\"," + \
                        "i.e.:\"/path/to/folder1|/path/to/folder2|..\"")
    
    parser.add_argument("-l", "--follow-links", dest="follow_links", action="store_true",
                        help="follow symbolics links, default False")
    # do parsing  
    args = parser.parse_args()
    
    handle_logging(args.verbose)
    logging.debug("args specified:") 
    logging.debug(args)
    
    ### outputfile        
    if not args.folderlist:
        parser.error("Please provide a folder or a " + \
                     "folderlist(\"/link/to/folder1|/link/to/folder2|..\")!")
    
    folders = args.folderlist.split("|")
    for f in folders:
        if not os.path.isdir(f):
            parser.error("Check the folderlist - one or more aren't folders")
    logging.debug("folders:")
    logging.debug(folders)
    
    if not args.outputfile:
        parser.error("Please provide a output file")
    if os.path.exists(args.outputfile) and not os.access(args.outputfile, os.W_OK):
        parser.error("Output file is not writeable!")
        
    output_file = None
    if args.outputfile:
        logging.debug("Output file specified: " + args.outputfile)
        output_file = args.outputfile
    
    if args.excludelist:
        exclude_folders = agrs.excludelist.split("|")
    else:
        exclude_folders = []
    
    # follow symbolic links ?
    if args.follow_links: 
        followlinks = True
    else:
        followlinks = False
    
    writer = OrgOutputWriter(file_name=output_file, short_description=SHORT_DESCRIPTION, tag=TAG);
    # do stuff
    for folder in folders:
        for rootdir, dirs, files in os.walk(folder, followlinks=followlinks):
            if rootdir in exclude_folders:
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
                            if  file_datetime.tm_year is orgdate_time_tupel.tm_year and \
                                file_datetime.tm_mon  is orgdate_time_tupel.tm_mon  and \
                                file_datetime.tm_mday is orgdate_time_tupel.tm_mday:
                                logger.debug("found a time in file. setting time from %s to %s", orgdate, file_datetime)
                                orgdate = file_datetime    
                        writer.write_org_subitem(orgdate + " " + OrgFormat.link(link=link, description=file))    
    # end do stuff 
    writer.close();
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Received KeyboardInterrupt")
