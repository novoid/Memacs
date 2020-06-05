# -*- coding: utf-8 -*-
# Time-stamp: <2012-05-30 18:19:27 armin>

import logging
import os
import sys


def handle_logging(args,
                   verbose=False,
                   suppressmessages=False,
                   org_file=""):
    """
    Handle/format logging regarding boolean parameter verbose
    @param verbose: options from OptionParser
    """
    if suppressmessages == True:
        logging.basicConfig(level=logging.ERROR)
    elif verbose:
        FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    else:
        FORMAT = "%(message)s"
        logging.basicConfig(level=logging.INFO, format=FORMAT)

    if org_file:
        if not os.path.exists(os.path.dirname(org_file)):
            org_file = None
        else:
            org_error_file = os.path.dirname(org_file) + os.sep + \
                "error.org"
            memacs_module_filename = os.path.basename(sys.argv[0])
            # add file logger
            console = logging.FileHandler(org_error_file, 'a', 'utf-8', 0)
            console.setLevel(logging.ERROR)
            formatter = logging.Formatter(
                '** %(asctime)s ' + memacs_module_filename + \
                    ' had an %(levelname)s \n   %(message)s \n' + \
                '   Arguments: ' + str(args) + '\n',
                datefmt="<%Y-%m-%d %a %H:%M:%S +1d>")
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
