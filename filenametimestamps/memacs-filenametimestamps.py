#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import os
import logging
from common.loggingsettings import *  
from common.orgwriter import OrgOutputWriter
from common.optparser import MemacsOptionParser

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2011-10-28"
SHORT_DESCRIPTION=u"Memacs for file name time stamp"
TAG=u"filedatestamps"
DESCRIPTION = u"""This script parses a text file containing absolute paths to files
with ISO datestamps and timestamps in their file names:x

Examples:  "2010-03-29T20.12 Divegraph.tiff"
           "2010-12-31T23.59_Cookie_recipies.pdf"
           "2011-08-29T08.23.59_test.pdf"

Then an Org-mode file is generated that contains links to the files.
"""

def main():
    ###########################################################################
    parser = MemacsOptionParser(prog_version=PROG_VERSION_NUMBER,
                                prog_version_date=PROG_VERSION_DATE,
                                description=DESCRIPTION,
                                )
    # adding additional options
    parser.add_option("-f", "--folderlist", dest="folderlist",
                      help="path to one or more folders seperated with \"|\","+\
                      "i.e.:\"/path/to/folder1|/path/to/folder2|..\"")
    # do parsing  
    (options, args) = parser.parse_args()
    handle_logging(options.verbose)
    logging.debug("options specified:") 
    logging.debug(options)
    
    ### outputfile        
    if not options.folderlist:
        parser.error("Please provide a folder or a " +\
                     "folderlist(\"/path/to/folder1|/path/to/folder2|..\")!")
    
    folders = options.folderlist.split("|")
    for f in folders:
        if not os.path.isdir(f):
            parser.error("Check the folderlist - one or more aren't folders")
    logging.debug("folders:")
    logging.debug(folders)
    
    
    if os.path.exists(options.outputfile) and not os.access(options.outputfile, os.W_OK):
        parser.error("Output file is not writeable!")
    output_file = None
    if options.outputfile:
        logging.debug("Output file specified: " + options.outputfile)
        output_file = options.outputfile
    
    writer = OrgOutputWriter(file_name=output_file,short_description=SHORT_DESCRIPTION,tag=TAG);
    # do stuff
    for folder in folders:
        for root,dirs,files in os.walk(folder):
            for file in files:
                print root + file
    # end do stuff 
    writer.close();
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Received KeyboardInterrupt")
