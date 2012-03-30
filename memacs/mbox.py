#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-06 16:51:25 daniel>

import os
from lib.memacs import Memacs
from lib.reader import CommonReader
from lib.mailparser import MailParser



class MboxMemacs(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)
        self._parser.add_argument(
           "-mf", "--mbox-mail-file", dest="mail_file",
           action="store",
           help="path to maildir file")

        self._parser.add_argument(
           "-nf", "--mbox-news-file", dest="news_file",
           action="store",
           help="path to mbox newsgroup file")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if not self._args.mail_file and not self._args.news_file:
            self._parser.error("please specify a file")       
        if self._args.mail_file and self._args.news_file:
            self._parser.error("please specify an mbox mail file "
                               "OR an mbox newsgroup file - not both")
        if self._args.mail_file and not (os.path.exists
                                        (self._args.mail_file) or \
            os.access(self._args.mail_file, os.R_OK)):
            self._parser.error("input file not found or not readable")
        if self._args.news_file and not (os.path.exists
                                        (self._args.news_file) or \
            os.access(self._args.news_file, os.R_OK)):
            self._parser.error("input file not found or not readable")

    def __read_mails_and_write(self, data):
        """
        Read All mails, let Mailparser parse each mail,
        write to outputfile

        @param data: string containing all mails of mbox-file
        """
        message = data.split("Message-ID:")
       
        for mail in message:
            if not (mail == message[0]):
                timestamp, output, note, properties = \
                    MailParser.parse_message(mail)
                self._writer.write_org_subitem(timestamp,
                                               output,
                                               note,
                                               properties)
           
    def __read_news_and_write(self, data):
        """
        Read All newsgroup entries, let Mailparser parse each 
        newsgroup entry, write to outputfile

        @param data: string containing all mails of mbox-file
        """
        message = data.split("X-Mozilla-Status: 0001"+"\n"+"X-Mozilla-Status2:"
                             " 00000000"+"\n"+"Path:")
        
        for news in message:
            if not (news == message[0]):           
                timestamp, output, note, properties = \
                    MailParser.parse_message(news)
                self._writer.write_org_subitem(timestamp,
                                               output,
                                               note,
                                               properties)

    def _main(self):
        """
        get's automatically called from Memacs class
        """
        if self._args.mail_file:
            data = CommonReader.get_data_from_file(self._args.mail_file)
            data = data.decode("utf-8","replace")
            data = data.encode("utf-8")
            self.__read_mails_and_write(data)
            
        elif self._args.news_file:
            data = CommonReader.get_data_from_file(self._args.news_file)
            data = data.decode("utf-8","replace")
            data = data.encode("utf-8")
            self.__read_news_and_write(data)
            