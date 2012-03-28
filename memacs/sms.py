#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-09 15:31:36 armin>

import sys
import os
import logging
import xml.sax
import time
from xml.sax._exceptions import SAXParseException
from lib.orgformat import OrgFormat
from lib.orgproperty import OrgProperties
from lib.memacs import Memacs
from lib.reader import CommonReader


class SmsSaxHandler(xml.sax.handler.ContentHandler):
    """
    Sax handler for sms backup xml files.
    See documentation memacs_sms.org for an example.
    """

    def __init__(self, writer, ignore_incoming, ignore_outgoing):
        """
        Ctor

        @param writer: orgwriter
        @param ignore_incoming: ignore incoming smses
        """
        self._writer = writer
        self._ignore_incoming = ignore_incoming
        self._ignore_outgoing = ignore_outgoing

    def startElement(self, name, attrs):
        """
        at every <sms> tag write to orgfile
        """
        logging.debug("Handler @startElement name=%s,attrs=%s", name, attrs)

        if name == "sms":
            sms_subject = attrs['subject']
            sms_date = int(attrs['date']) / 1000     # unix epoch
            sms_body = attrs['body']
            sms_address = attrs['address']
            sms_type_incoming = int(attrs['type']) == 1

            skip = False

            if sms_type_incoming == True:
                output = "SMS from "
                if self._ignore_incoming:
                    skip = True
            else:
                output = "SMS to "
                if self._ignore_outgoing:
                    skip = True

            if not skip:
                output += sms_address + ": "

                if sms_subject != "null":
                    # in case of MMS we have a subject
                    output += sms_subject
                    notes = sms_body
                else:
                    output += sms_body
                    notes = ""

                timestamp = OrgFormat.datetime(time.gmtime(sms_date))
                data_for_hashing = output + timestamp + notes
                properties = OrgProperties(data_for_hashing=data_for_hashing)

                self._writer.write_org_subitem(output=output,
                                               timestamp=timestamp,
                                               note=notes,
                                               properties=properties)


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

        self._parser.add_argument(
            "--ignore-incoming", dest="ignore_incoming",
            action="store_true",
            help="ignore incoming smses")

        self._parser.add_argument(
            "--ignore-outgoing", dest="ignore_outgoing",
            action="store_true",
            help="ignore outgoing smses")

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
        read the lines from sms backup xml file,
        parse and write them to org file
        """

        data = CommonReader.get_data_from_file(self._args.smsxmlfile)

        try:
            xml.sax.parseString(data.encode('utf-8'),
                                SmsSaxHandler(self._writer,
                                              self._args.ignore_incoming,
                                              self._args.ignore_outgoing))
        except SAXParseException:
            logging.error("No correct XML given")
            sys.exit(1)
