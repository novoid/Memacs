#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Time-stamp: <2015-01-30 18:30:03 vk>

import sys
import os
import logging
import xml.sax
import time
import re          ## RegEx for detecting patterns
import codecs      ## Unicode conversion
import HTMLParser  ## un-escaping HTML entities like emojis
import tempfile    ## create temporary files
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

    ## from https://github.com/wooorm/emoji-emotion/blob/master/Support.md
    EMOJIS = {
        u'\ud83d\udc7f':'imp',
        u'\ud83d\ude3e':'pouting_cat',
        u'\ud83d\ude21':'rage',
        u'\ud83d\ude20':'angry',
        u'\ud83d\ude27':'anguished',
        u'\ud83d\ude2d':'sob',
        u'\ud83d\ude31':'scream',
        u'\ud83d\ude40':'scream_cat',
        u'\ud83d\ude08':'smiling_imp',
        u'\ud83d\ude1f':'worried',
        u'\ud83d\ude3f':'crying_cat_face',
        u'\ud83d\ude15':'confused',
        u'\ud83d\ude16':'confounded',
        u'\ud83d\ude30':'cold_sweat',
        u'\ud83d\ude22':'cry',
        u'\ud83d\ude1e':'disappointed',
        u'\ud83d\ude33':'flushed',
        u'\ud83d\ude28':'fearful',
        u'\ud83d\ude2c':'grimacing',
        u'\ud83d\ude2e':'open_mouth',
        u'\ud83d\ude23':'persevere',
        u'\ud83d\ude2b':'tired_face',
        u'\ud83d\ude12':'unamused',
        u'\ud83d\ude29':'weary',
        u'\ud83d\ude35':'dizzy_face',
        u'\ud83d\ude25':'disappointed_relieved',
        u'\ud83d\ude26':'frowning',
        u'\ud83d\ude01':'grin',
        u'\ud83d\ude2f':'hushed',
        u'\ud83d\ude37':'mask',
        u'\ud83d\ude14':'pensive',
        u'\ud83d\ude13':'sweat',
        u'\ud83d\ude1c':'stuck_out_tongue_winking_eye',
        u'\ud83d\ude11':'expressionless',
        u'\ud83d\ude36':'no_mouth',
        u'\ud83d\ude10':'neutral_face',
        u'\ud83d\ude34':'sleeping',
        u'\ud83d\ude1d':'stuck_out_tongue_closed_eyes',
        u'\ud83d\ude2a':'sleepy',
        u'\ud83d\ude06':'laughing; satisfied',
        u'\ud83d\ude0e':'sunglasses',
        u'\ud83d\ude1b':'stuck_out_tongue',
        u'\ud83d\ude32':'astonished',
        u'\ud83d\ude0a':'blush',
        u'\ud83d\ude00':'grinning',
        u'\ud83d\ude3d':'kissing_cat',
        u'\ud83d\ude19':'kissing_smiling_eyes',
        u'\ud83d\ude17':'kissing',
        u'\ud83d\ude1a':'kissing_closed_eyes',
        u'\u263a\ufe0f':'relaxed',
        u'\ud83d\ude0c':'relieved',
        u'\ud83d\ude04':'smile',
        u'\ud83d\ude3c':'smirk_cat',
        u'\ud83d\ude38':'smile_cat',
        u'\ud83d\ude03':'smiley',
        u'\ud83d\ude3a':'smiley_cat',
        u'\ud83d\ude05':'sweat_smile',
        u'\ud83d\ude0f':'smirk',
        u'\ud83d\ude3b':'heart_eyes_cat',
        u'\ud83d\ude0d':'heart_eyes',
        u'\ud83d\ude07':'innocent',
        u'\ud83d\ude02':'joy',
        u'\ud83d\ude39':'joy_cat',
        u'\ud83d\ude18':'kissing_heart',
        u'\ud83d\ude09':'wink',
        u'\ud83d\ude0b':'yum',
        u'\ud83d\ude24':'triumph'}

    EMOJI_ENCLOSING_CHARACTER = "~" ## character which encloses emojis found ~wink~


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
        htmlparser = HTMLParser.HTMLParser()

        if name == "sms":
            sms_subject = attrs['subject']
            sms_date = int(attrs['date']) / 1000     # unix epoch
            sms_body = attrs['body']
            sms_address = attrs['address'].strip().replace('-',u'').replace('/',u'').replace(' ',u'').replace('+',u'00')
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

                ## reverse encoding hack from just before:
                sms_body = htmlparser.unescape(sms_body.replace(u'EnCoDiNgHaCk42', u'&#'))
                for emoji in self.EMOJIS.keys():
                    ## FIXXME: this is a horrible dumb brute-force algorithm.
                    ##         In case of bad performance, this can be optimized dramtically
                    sms_body = sms_body.replace(emoji, self.EMOJI_ENCLOSING_CHARACTER + \
                                                self.EMOJIS[emoji] + self.EMOJI_ENCLOSING_CHARACTER).replace(u'\n', u'⏎')

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
        PHONE_REGEX = re.compile(':(PHONE|oldPHONE|MOBILE|oldMOBILE|HOMEPHONE|oldHOMEPHONE|WORKPHONE|oldWORKPHONE):' + PHONE)

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
                    phonenumber = phone_components.group(2).strip().replace('-',u'').replace('/',u'').replace(' ',u'').replace('+',u'00')
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

        ## replace HTML entities "&#" in original file to prevent XML parser from worrying:
        temp_xml_file = tempfile.mkstemp()[1]
        line_number = 0
        logging.debug("tempfile [%s]", str(temp_xml_file))
        with codecs.open(temp_xml_file, 'w', encoding='utf-8') as outputhandle:
            for line in codecs.open(self._args.smsxmlfile, 'r', encoding='utf-8'):
                try:
                    ## NOTE: this is a dirty hack to prevent te XML parser from complainaing about
                    ##       encoding issues of UTF-8 encoded emojis. Will be reverted when parsing sms_body
                    outputhandle.write(line.replace(u'&#', u'EnCoDiNgHaCk42') + u'\n')
                except IOError as e:
                    print "tempfile line " + str(line_number) +  " [" + str(temp_xml_file) + "]"
                    print "I/O error({0}): {1}".format(e.errno, e.strerror)
                except ValueError as e:
                    print "tempfile line " + str(line_number) +  " [" + str(temp_xml_file) + "]"
                    print "Value error: {0}".format(e)
                    #print "line [%s]" % str(line)
                except:
                    print "tempfile line " + str(line_number) +  " [" + str(temp_xml_file) + "]"
                    print "Unexpected error:", sys.exc_info()[0]
                    raise

        data = CommonReader.get_data_from_file(temp_xml_file)

        try:
            xml.sax.parseString(data.encode('utf-8'),
                                SmsSaxHandler(self._writer,
                                              self._args.ignore_incoming,
                                              self._args.ignore_outgoing,
                                              self._numberdict))
        except SAXParseException:
            logging.error("No correct XML given")
            sys.exit(1)
        else:
            os.remove(temp_xml_file)
