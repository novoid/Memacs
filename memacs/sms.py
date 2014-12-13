#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2014-12-13 13:39:42 vk>

import sys
import os
import logging
import xml.sax
import time
import re
import codecs
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

    def __init__(self, writer, ignore_incoming, ignore_outgoing, numberdict):
        """
        Ctor

        @param writer: orgwriter
        @param ignore_incoming: ignore incoming smses
        """
        self._writer = writer
        self._ignore_incoming = ignore_incoming
        self._ignore_outgoing = ignore_outgoing
        self._numberdict = numberdict


    def startElement(self, name, attrs):
        """
        at every <sms> tag write to orgfile
        """
        logging.debug("Handler @startElement name=%s,attrs=%s", name, attrs)

        if name == "sms":
            sms_subject = attrs['subject']
            sms_date = int(attrs['date']) / 1000     # unix epoch
            sms_body = attrs['body']
            sms_address = attrs['address'].replace('-', '')
            sms_type_incoming = int(attrs['type']) == 1
            contact_name = False
            if 'contact_name' in attrs:
                ## NOTE: older version of backup app did not insert contact_name into XML
                contact_name = attrs['contact_name']
            else:
                if self._numberdict:
                    if sms_address in self._numberdict.keys():
                        contact_name = self._numberdict[sms_address]

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

                name_string = ""
                if contact_name:
                    name_string = '[[contact:' + contact_name + '][' + contact_name + ']]'
                else:
                    name_string = "Unknown"
                output += name_string + ": "

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

                properties.add("NUMBER", sms_address)
                properties.add("NAME", contact_name)

                self._writer.write_org_subitem(output=output,
                                               timestamp=timestamp,
                                               note=notes,
                                               properties=properties)


class SmsMemacs(Memacs):

    _numberdict = False

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

        self._parser.add_argument(
            "--orgcontactsfile", dest="orgcontactsfile",
            action="store", required=False,
            help="path to Org-contacts file for phone number lookup. Phone numbers have to match.")


    def parse_org_contact_file(self, orgfile):
        """
        Parses the given Org-mode file for contact entries.

        The return format is a follows:
        numbers = {'004369912345678':'First2 Last1', '0316987654':'First2 Last2', ...}

        @param orgfile: file name of a Org-mode file to parse
        @param return: list of dict-entries containing the numbers to name dict
        """

        linenr = 0

        ## defining distinct parsing status states:
        headersearch = 21
        propertysearch = 42
        inproperty = 73
        status = headersearch

        contacts = {}
        current_name = u''

        HEADER_REGEX = re.compile('^(\*+)\s+(.*?)(\s+(:\S+:)+)?$')
        PHONE = '\s+([\+\d\-/ ]{7,})$'
        PHONE_REGEX = re.compile(':(PHONE|MOBILE|HOMEPHONE|WORKPHONE):' + PHONE)

        for rawline in codecs.open(orgfile, 'r', encoding='utf-8'):
            line = rawline.strip()   ## trailing and leading spaces are stupid
            linenr += 1

            header_components = re.match(HEADER_REGEX, line)
            if header_components:
                ## in case of new header, make new currententry because previous one was not a contact header with a property
                current_name = header_components.group(2)
                status = propertysearch
                continue

            if status == headersearch:
                ## if there is something to do, it was done above when a new heading is found
                continue

            if status == propertysearch:
                if line == u':PROPERTIES:':
                    status = inproperty
                continue

            elif status == inproperty:

                phone_components = re.match(PHONE_REGEX, line)
                if phone_components:
                    phonenumber = phone_components.group(2).strip().replace('-',u'').replace('/',u'').replace(' ',u'')
                    contacts[phonenumber] = current_name
                elif line == u':END:':
                    status = headersearch

                continue

            else:
                ## I must have mixed up status numbers or similar - should never be reached.
                logging.error("Oops. Internal parser error: status \"%s\" unknown. The programmer is an idiot. Current contact entry might get lost due to recovering from that shock. (line number %s)" % (str(status), str(linenr)))
                status = headersearch
                continue

        logging.info("found %s suitable contacts while parsing \"%s\"" % (str(len(contacts)), orgfile))
        return contacts


    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if not (os.path.exists(self._args.smsxmlfile) or \
                     os.access(self._args.smsxmlfile, os.R_OK)):
            self._parser.error("input file not found or not readable")

        if self._args.orgcontactsfile:
            if not (os.path.exists(self._args.orgcontactsfile) or \
                    os.access(self._args.orgcontactsfile, os.R_OK)):
                self._parser.error("Org-contacts file not found or not readable")
            self._numberdict = self.parse_org_contact_file(self._args.orgcontactsfile)


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
                                              self._args.ignore_outgoing,
                                              self._numberdict))
        except SAXParseException:
            logging.error("No correct XML given")
            sys.exit(1)
