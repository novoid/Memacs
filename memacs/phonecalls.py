#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-11-06 15:26:05 vk>

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

class PhonecallsSaxHandler(xml.sax.handler.ContentHandler):
    """
    Sax handler for following xml's:
    2013-04-10: update: contact_name is also recognized

    <?xml version='1.0' encoding='UTF-8' standalone='yes' ?>

    <calls count="8">
      <call number="+43691234123" duration="59" date="13193906092" type="1" />
      <call number="06612341234" duration="22" date="131254215834" type="2" />
      <call number="-1" duration="382" date="1312530691081" type="1" />
      <call number="+4312341234" duration="289" date="13124327195" type="1" />
      <call number="+4366412341234" duration="70" date="136334059" type="1" />
      <call number="+4366234123" duration="0" date="1312473751975" type="2" />
      <call number="+436612341234" duration="0" date="12471300072" type="3" />
      <call number="+433123412" duration="60" date="1312468562489" type="2" />
    </calls>"""

    def __init__(self,
                 writer,
                 ignore_incoming,
                 ignore_outgoing,
                 ignore_missed,
                 ignore_cancelled,
                 minimum_duration
                 ):
        """
        Ctor

        @param writer: orgwriter
        @param ignore_incoming:  ignore incoming  phonecalls
        @param ignore_outgoing:  ignore outgoing  phonecalls
        @param ignore_missed:    ignore missed    phonecalls
        @param ignore_cancelled: ignore cancelled phonecalls
        @param minimum_duration: ignore phonecalls less than that time
        """
        self._writer = writer
        self._ignore_incoming = ignore_incoming
        self._ignore_outgoing = ignore_outgoing
        self._ignore_missed = ignore_missed
        self._ignore_cancelled = ignore_cancelled
        self._minimum_duration = minimum_duration

    def startElement(self, name, attrs):
        """
        at every <call> write to orgfile
        """
        logging.debug("Handler @startElement name=%s,attrs=%s", name, attrs)

        if name == "call":
            call_number = attrs['number']
            call_duration = int(attrs['duration'])
            call_date = int(attrs['date']) / 1000     # unix epoch

            call_type = int(attrs['type'])
            call_incoming = call_type == 1
            call_outgoing = call_type == 2
            call_missed = call_type == 3
            call_cancelled = call_type == 5

            call_name = call_number
            if 'contact_name' in attrs:
                ## NOTE: older version of backup app did not insert contact_name into XML
                call_name = attrs['contact_name']

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
            elif call_cancelled:
                output += "cancelled "
                if self._ignore_cancelled:
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


class PhonecallsMemacs(Memacs):
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
            "--ignore-cancelled", dest="ignore_cancelled",
            action="store_true",
            help="ignore cancelled phonecalls")

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
                                              self._args.ignore_cancelled,
                                              self._args.minimum_duration or 0,
                                              ))
        except SAXParseException:
            logging.error("No correct XML given")
            sys.exit(1)
