#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import os
import logging
from common.loggingsettings import *  
from common.orgwriter import OrgOutputWriter
from common.argparser import MemacsArgumentParser
import re
import codecs
from common.orgformat import OrgFormat
import urllib2
from urllib2 import HTTPError, URLError
from symbol import xor_expr


PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2011-10-28"
# TODO set real description and so on
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

REGEX_VEVENT               = re.compile("BEGIN:VEVENT(.*?)END:VEVENT", re.DOTALL)
REGEX_VEVENT_DTSTART       = re.compile("DTSTART:(.*)")
REGEX_VEVENT_DTSTARTALLDAY = re.compile("DTSTART;VALUE=DATE(.*)")
REGEX_VEVENT_DTEND         = re.compile("DTEND:(.*)")
REGEX_VEVENT_SUMMARY       = re.compile("SUMMARY:(.*)")
REGEX_VEVENT_DESCRIPTION   = re.compile("DESCRIPTION:(.*)")
REGEX_VEVENT_LOCATION      = re.compile("LOCATION:(.*)")

def main():
    ###########################################################################
    parser = MemacsArgumentParser(prog_version=PROG_VERSION_NUMBER,
                                  prog_version_date=PROG_VERSION_DATE,
                                  description=DESCRIPTION,
                                  )
    # adding additional arguments
    parser.add_argument("-c", "--calendar-url", dest="calendar_url",
                        help="url to calendar")
    
    parser.add_argument("-cf", "--calendar-file", dest="calendar_file",
                        help="path to calendar")
    
    parser.add_argument("-x", "--exclude", dest="excludelist",
                        help="path to one or more folders seperated with \"|\"," + \
                        "i.e.:\"/path/to/folder1|/path/to/folder2|..\"")
    
    # do parsing  
    args = parser.parse_args()
    
    handle_logging(args.verbose)
    logging.debug("args specified:") 
    logging.debug(args)
    
    ### outputfile
    
    if not args.calendar_url and not args.calendar_file:
        parser.error("specify a calendar url or calendar file")
            
    if args.calendar_url and args.calendar_file:
        parser.error("only set a url or path to a calendar not both.")
    
    if args.calendar_file and not os.path.exists(args.calendar_file):
        parser.error("calendar path not exists")
    
    if not args.outputfile:
        parser.error("Please provide a output file")
    if os.path.exists(args.outputfile) and not os.access(args.outputfile, os.W_OK):
        parser.error("Output file is not writeable!")
        
    output_file = None
    if args.outputfile:
        logging.debug("Output file specified: " + args.outputfile)
        output_file = args.outputfile
    
    writer = OrgOutputWriter(file_name=output_file, short_description=SHORT_DESCRIPTION, tag=TAG);
    # do stuff
    if args.calendar_file:
        try:
            file = codecs.open(args.calendar_file, 'rb', "utf_8")
            data = file.read()
            file.close()
        except IOError:
            logging.error("Error at opening file: %s" % args.calendar_file)
            
    elif args.calendar_url:
        try:
            req = urllib2.urlopen(args.calendar_url, None, 10)
            data = req.read()
        except HTTPError:
            logging.error("Error at opening url: %s" % args.calendar_url)
        except URLError:
            logging.error("Error at opening url: %s" % args.calendar_url)
    
    #print VEVENT_REGEX.findall(data)
    for vevent in  REGEX_VEVENT.findall(data):
        print vevent
        # dstart 
        dtstart_search = REGEX_VEVENT_DTSTART.search(vevent)
        if dtstart_search:
            dtstart = dtstart_search.group(1)
        else:
            dtstart = REGEX_VEVENT_DTSTARTALLDAY.search(vevent).group(1)
        #dtend       =  REGEX_VEVENT_DTEND.search(vevent).group(1)
        #description =  REGEX_VEVENT_DESCRIPTION.search(vevent).group(1)
        summary     =  REGEX_VEVENT_SUMMARY.search(vevent).group(1)
        #location    =  REGEX_VEVENT_LOCATION.search(vevent).group(1)
        
        print dtstart
        #print dtend
        #print description
        #print summary
    
    
    #writer.write_org_subitem(orgdate + " " + OrgFormat.link(link=link, description=file))    
    # end do stuff 
    writer.close();
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Received KeyboardInterrupt")
