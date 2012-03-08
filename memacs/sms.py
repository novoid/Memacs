#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import sys
import os
import logging
import xml.sax
import time
from xml.sax._exceptions import SAXParseException
from lib.orgformat import OrgFormat
from lib.memacs import Memacs
from lib.reader import CommonReader


class SmsSaxHandler(xml.sax.handler.ContentHandler):
    """
    Sax handler for following xml's:

    <?xml version="1.0"?>
    <log>
    <logentry
       revision="13">
    <author>bob</author>
    <date>2011-11-05T18:18:22.936127Z</date>
    <msg>Bugfix.</msg>
    </logentry>
    </log>
    """

    def __init__(self, writer):
        """
        Ctor

        @param writer: orgwriter
        """
        self._writer = writer


    def startElement(self, name, attrs):
        """
        at every <tag> remember the tagname
        * sets the revision when in tag "logentry"
        """
        logging.debug("Handler @startElement name=%s,attrs=%s", name, attrs)
        
        if name == "sms":
            sms_subject = attrs['subject']
            sms_date = int(attrs['date']) / 1000     # unix epoch
            sms_body = attrs['body']
            sms_address  = attrs['address']
            sms_type_incoming = int(attrs['type']) == 1
            
            if sms_type_incoming == True: 
                output = "SMS from "
            else:
                output = "SMS to " 
            
            output += sms_address + ": "
            
            if sms_subject != "null":
                # in case of MMS we have a subject
                output += sms_subject
                notes = sms_body
            else:
                output += sms_body
                notes = ""

            timestamp = OrgFormat.datetime(time.gmtime(sms_date))
            
            #properties = OrgProperties()
            
            self._writer.write_org_subitem(output=output,
                                           timestamp=timestamp,
                                           note=notes)

class SmsMemacs(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
            "-f", "--file", dest="smsxmlfile",
            action="store", required=True,
            help="path to sms xml backup file")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if not (os.path.exists(self._args.smsxmlfile) or \
                     os.access(self._args.smsxmlfile, os.R_OK)):
            self._parser.error("input file not found or not readable")

    def _main(self):
        """
        get's automatically called from Memacs class
        read the lines from svn xml file, parse and write them to org file
        """

        data = CommonReader.get_data_from_file(self._args.smsxmlfile)

        try:
            xml.sax.parseString(data.encode('utf-8'),
                                SmsSaxHandler(self._writer))
        except SAXParseException:
            logging.error("No correct XML given")
            sys.exit(1)
