#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2013-04-05 10:28:55 vk>

import sys
import os
import re
import logging
import time
from lib.orgformat import OrgFormat
from lib.memacs import Memacs
from lib.reader import CommonReader
from lib.orgproperty import OrgProperties
import pdb





class SimplePhoneLogsMemacs(Memacs):

    ## match for example: "2012-11-20 # 19.59 # shutdown #   72 # 35682"
    LOGFILEENTRY_REGEX = re.compile("([12]\d\d\d-[012345]\d-[012345]\d)" +
                                    " *# *" +
                                    "([ 012]\d)[:.]([012345])\d" +
                                    " *# *" +
                                    ".+" +
                                    " *# *" +
                                    "(\d+)" +
                                    " *# *" +
                                    "(\d+)$")

    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
            "-f", "--file", dest="phonelogfile",
            action="store", required=True,
            help="path to sms xml backup file")


    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if not (os.path.exists(self._args.phonelogfile) or \
                     os.access(self._args.phonelogfile, os.R_OK)):
            self._parser.error("input file not found or not readable")


    def _parse_data(self, data):
        """parses the phone log data"""

        last = { } # holds the last occurrences of each event

        for rawline in data.split('\n'):

            if not rawline:
                continue

            line = rawline.encode('utf-8')
            logging.debug("line: %s", line)

            components = re.match(self.LOGFILEENTRY_REGEX, line)

            if components:
                logging.debug("line matches")
            else:
                logging.debug("line does not match!")

            #pdb.set_trace()
        
## - algorithm sketch
##   - while read line
##     - if 3rd argument not in last_ocurrences_dict key-list:
##       - add to it with its last occurence
##     - case
##       - boot
##         - if last shutdown
##           - add "(off for $diff)"
##         - remember timestamp > last_ocurrences_dict
##       - shutdown
##         - if last boot
##           - add "(on for $diff)"
##         - remember timestamp > last_ocurrences_dict
##       - FOO
##         - if last FOO-end is found
##           - add "(away/not FOO for $diff)"
##         - remember timestamp > last_ocurrences_dict FOO
##       - FOO-end
##         - if last FOO is found
##           - add "(FOO for $diff)"
##         - remember timestamp > last_ocurrences_dict FOO-end

##  ** <2012-11-20 Tue 11:56> boot (off for ?)
##  :PROPERTIES:
##  :IN-BETWEEN: 
##  :IN-BETWEEN-S: 
##  :BATT-LEVEL: 89
##  :UPTIME: 1:51:39
##  :UPTIME-S: 6692
##  :END:
## 
## - timestamp
## - eventname
## - previous-event-timestamp
## - batt-level
## - uptime
## 
##  ** <2012-11-20 Tue 11:56> boot after crash
##  :PROPERTIES:
##  :IN-BETWEEN: 
##  :IN-BETWEEN-S: 
##  :BATT-LEVEL: 89
##  :UPTIME: 1:51:34
##  :UPTIME-S: 6694
##  :END:
## 
##  ** <2012-11-20 Tue 19:59> shutdown (on for 9:54:42)
##  :PROPERTIES:
##  :IN-BETWEEN: 9:54:42
##  :IN-BETWEEN-S: 35682
##  :BATT-LEVEL: 72
##  :UPTIME: 9:54:42
##  :UPTIME-S: 35682
##  :END:
## 

    def _main(self):
        """
        gets called automatically from Memacs class.
        read the lines from phonecalls backup xml file,
        parse and write them to org file
        """

        data = CommonReader.get_data_from_file(self._args.phonelogfile)

        self._parse_data(data)


# Local Variables:
# mode: flyspell
# eval: (ispell-change-dictionary "en_US")
# End:
