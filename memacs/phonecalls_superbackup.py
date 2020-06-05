#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-11-06 15:26:30 vk>

import datetime
import logging
import os
import sys
import time
import xml.sax

from orgformat import OrgFormat
from xml.sax._exceptions import SAXParseException

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties
from memacs.lib.reader import CommonReader

#import pdb

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

class PhonecallsSaxHandler(xml.sax.handler.ContentHandler):
    """
    Sax handler for following xml's:

    <?xml version="1.0" encoding="UTF-8"?>
    <alllogs count="500">
            <log number="01270811333" time="3 Sep 2013 10:03:26" date="1378199006383" type="1" name="" new="1" dur="30" />
            <log number="01270588896" time="1 Sep 2013 19:41:05" date="1378060865117" type="2" name="Nick Powell" new="1" dur="143" />
            <log number="07989385391" time="1 Sep 2013 13:41:23" date="1378039283149" type="1" name="Anne Barton" new="1" dur="19" />
            <log number="+447943549963" time="1 Sep 2013 13:26:31" date="1378038391562" type="2" name="John M Barton" new="1" dur="0" />
            <log number="+447943549963" time="1 Sep 2013 13:11:46" date="1378037506896" type="2" name="John M Barton" new="1" dur="0" />

    </alllogs>"""


    def __init__(self,
                 writer,
                 ignore_incoming,
                 ignore_outgoing,
                 ignore_missed,
                 ignore_voicemail,
                 ignore_rejected,
                 ignore_refused,
                 minimum_duration
                 ):
        """
        Ctor

        @param writer: orgwriter
        @param ignore_incoming:  ignore incoming phonecalls
        @param ignore_outgoing:  ignore outgoing phonecalls
        @param ignore_missed:    ignore missed   phonecalls
        @param ignore_voicemail: ignore voicemail phonecalls
        @param ignore_rejected:  ignore rejected phonecalls
        @param ignore_refused:   ignore refused  phonecalls
        @param minimum_duration:    ignore phonecalls less than that time
        """
        self._writer = writer
        self._ignore_incoming = ignore_incoming
        self._ignore_outgoing = ignore_outgoing
        self._ignore_missed = ignore_missed
        self._ignore_voicemail = ignore_voicemail
        self._ignore_rejected = ignore_rejected
        self._ignore_refused = ignore_refused
        self._minimum_duration = minimum_duration

    def startElement(self, name, attrs):
        """
        at every <log> write to orgfile
        """
        logging.debug("Handler @startElement name=%s,attrs=%s", name, attrs)

        if name == "log":
            call_number = attrs['number']
            call_duration = int(attrs['dur'])

            call_date = int(attrs['date']) / 1000     # unix epoch

            call_type = int(attrs['type'])
            call_incoming = call_type == 1
            call_outgoing = call_type == 2
            call_missed = call_type == 3
            call_voicemail = call_type == 4
            call_rejected = call_type == 5
            call_refused = call_type == 6

            call_name = attrs['name']

            output = "Phonecall "

            skip = False

            if call_incoming:
                output += "from "
                if self._ignore_incoming:
                    skip = True
            elif call_outgoing:
                output += "to "
                if self._ignore_outgoing:
                    skip = True
            elif call_missed:
                output += "missed "
                if self._ignore_missed:
                    skip = True
            elif call_voicemail:
                output += "voicemail "
                if self._ignore_voicemail:
                    skip = True
            elif call_rejected:
                output += "rejected "
                if self._ignore_rejected:
                    skip = True
            elif call_refused:
                output += "refused "
                if self._ignore_refused:
                    skip = True
            else:
                raise Exception("Invalid Phonecall Type: %d", call_type)

            call_number_string = ""
            if call_number != "-1":
                call_number_string = call_number
            else:
                call_number_string = "Unknown Number"

            name_string = ""
            if call_name != "(Unknown)":
                name_string = '[[contact:' + call_name + '][' + call_name + ']]'
            else:
                name_string = "Unknown"
            output += name_string

            if call_duration < self._minimum_duration:
                skip = True

            timestamp = OrgFormat.date(time.gmtime(call_date), show_time=True)

            end_datetimestamp = datetime.datetime.utcfromtimestamp(call_date + call_duration)
            logging.debug("timestamp[%s] duration[%s] end[%s]" %
                          (str(timestamp), str(call_duration), str(end_datetimestamp)))

            end_timestamp_string = OrgFormat.date(end_datetimestamp, show_time=True)
            logging.debug("end_time [%s]" % end_timestamp_string)

            data_for_hashing = output + timestamp
            properties = OrgProperties(data_for_hashing=data_for_hashing)
            properties.add("NUMBER", call_number_string)
            properties.add("DURATION", call_duration)
            properties.add("NAME", call_name)

            if not skip:
                self._writer.write_org_subitem(output=output,
                                               timestamp=timestamp + '-' + end_timestamp_string,
                                               properties=properties
                                               )


class PhonecallsSuperBackupMemacs(Memacs):
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
            help="ignore incoming phonecalls")

        self._parser.add_argument(
            "--ignore-outgoing", dest="ignore_outgoing",
            action="store_true",
            help="ignore outgoing phonecalls")

        self._parser.add_argument(
            "--ignore-missed", dest="ignore_missed",
            action="store_true",
            help="ignore outgoing phonecalls")

        self._parser.add_argument(
            "--ignore-voicemail", dest="ignore_voicemail",
            action="store_true",
            help="ignore voicemail phonecalls")

        self._parser.add_argument(
            "--ignore-rejected", dest="ignore_rejected",
            action="store_true",
            help="ignore rejected phonecalls")

        self._parser.add_argument(
            "--ignore-refused", dest="ignore_refused",
            action="store_true",
            help="ignore refused phonecalls")

        self._parser.add_argument(
            "--minimum-duration", dest="minimum_duration",
            action="store", type=int,
            help="[sec] show only calls with duration >= this argument")


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
        gets called automatically from Memacs class.
        read the lines from phonecalls backup xml file,
        parse and write them to org file
        """

        data = CommonReader.get_data_from_file(self._args.smsxmlfile)

        try:
            xml.sax.parseString(data.encode('utf-8'),
                                PhonecallsSaxHandler(self._writer,
                                              self._args.ignore_incoming,
                                              self._args.ignore_outgoing,
                                              self._args.ignore_missed,
                                              self._args.ignore_voicemail,
                                              self._args.ignore_rejected,
                                              self._args.ignore_refused,
                                              self._args.minimum_duration or 0,
                                              ))
        except SAXParseException:
            logging.error("No correct XML given")
            sys.exit(1)
