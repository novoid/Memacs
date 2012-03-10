#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-06 16:51:25 daniel>

import sys
import os
import logging
from lib.memacs import Memacs
from lib.mailparser import MailParser
from lib.reader import CommonReader


class MboxMemacs(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
           "-mf", "--mbox-file", dest="mbox_file",
           action="store",
           help="path to mbox file")

        self._parser.add_argument(
           "-nf", "--news-file", dest="news_file",
           action="store",
           help="path to newsgroup file")


    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)

        if not self._args.mbox_file and not self._args.news_file:
            self._parser.error("please specify a file")
            
        if self._args.mbox_file and self._args.news_file:
            self._parser.error("please specify an mbox file OR an newsgroup file - not both")    


    def __read_mails_and_write(self, data):
        timestamp, output, note, properties = MailParser.parse_message(data)

        self._writer.write_org_subitem(timestamp,
                                           output,
                                           note,
                                           properties)
            


    def _main(self):
        
        if self._args.mbox_file:            
            data = CommonReader.get_data_from_file(self._args.mbox_file) 
            self.__read_mails_and_write(data)
            
            
            
#        elif self._args.news_file:
#            data = CommonReader.get_data_from_url(self._args.news_file)
#
#            self.__read_news_and_write(data)
        
        
        