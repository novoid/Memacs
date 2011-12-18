#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import logging
import sys
import os

def handle_logging(verbose=False,org_file=""):
    """
    Handle/format logging regarding boolean parameter verbose  
    
    @param verbose: options from OptionParser 
    """
   
    if verbose:
        FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    else:
        FORMAT = "%(message)s"
        logging.basicConfig(level=logging.INFO, format=FORMAT)
    
    if org_file:
        if not os.path.exists(os.path.dirname(org_file)):
            org_file = None
        else:
            org_error_file = os.path.dirname(org_file) + os.sep +  "error.org_archive"
            memacs_module_filname = os.path.basename(sys.argv[0])
            # add file logger
            console = logging.FileHandler(org_error_file, 'a', 'utf-8', 0)
            console.setLevel(logging.ERROR)
            formatter = logging.Formatter('** %(asctime)s '+memacs_module_filname+' had an %(levelname)s \n   %(message)s',datefmt="<%Y-%m-%d %a %H:%M:%S +1d>")
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
    


    
