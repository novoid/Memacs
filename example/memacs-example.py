#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import logging
import os
from common.loggingsettings import *  
from common.orgwriter import OrgOutputWriter
from common.optparser import MemacsOptionParser

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2011-10-28"
DESCRIPTION = """This script ....

Then an Org-mode file is generated that contains links to the files.
"""

def main():
    ###########################################################################
    parser = MemacsOptionParser(prog_version=PROG_VERSION_NUMBER,
                                prog_version_date=PROG_VERSION_DATE,
                                description=DESCRIPTION)
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
    
    if not os.access(options.outputfile, os.W_OK):
        parser.error("Output file is not writeable!")
    output_file = None
    if options.outputfile:
        logging.debug("Output file specified: " + options.outputfile)
        output_file = options.outputfile
    
    writer = OrgOutputWriter(output_file);
    # do stuff
    
    # end do stuff 
    writer.close();
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Received KeyboardInterrupt")
