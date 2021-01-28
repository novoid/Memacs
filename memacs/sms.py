#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-11-06 15:27:28 vk>

import codecs  ## Unicode conversion
import html.parser  ## un-escaping HTML entities like emojis
import logging
import os
import sys
import tempfile  ## create temporary files
import time
import xml.sax

from orgformat import OrgFormat
from xml.sax._exceptions import SAXParseException

from memacs.lib.contactparser import parse_org_contact_file
from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties
from memacs.lib.reader import CommonReader


class SmsSaxHandler(xml.sax.handler.ContentHandler):
    """
    Sax handler for sms backup xml files.
    See documentation memacs_sms.org for an example.
    """

    ## from https://github.com/wooorm/emoji-emotion/blob/master/Support.md
    EMOJIS = {
        '\ud83d\udc7f':'imp',
        '\ud83d\ude3e':'pouting_cat',
        '\ud83d\ude21':'rage',
        '\ud83d\ude20':'angry',
        '\ud83d\ude27':'anguished',
        '\ud83d\ude2d':'sob',
        '\ud83d\ude31':'scream',
        '\ud83d\ude40':'scream_cat',
        '\ud83d\ude08':'smiling_imp',
        '\ud83d\ude1f':'worried',
        '\ud83d\ude3f':'crying_cat_face',
        '\ud83d\ude15':'confused',
        '\ud83d\ude16':'confounded',
        '\ud83d\ude30':'cold_sweat',
        '\ud83d\ude22':'cry',
        '\ud83d\ude1e':'disappointed',
        '\ud83d\ude33':'flushed',
        '\ud83d\ude28':'fearful',
        '\ud83d\ude2c':'grimacing',
        '\ud83d\ude2e':'open_mouth',
        '\ud83d\ude23':'persevere',
        '\ud83d\ude2b':'tired_face',
        '\ud83d\ude12':'unamused',
        '\ud83d\ude29':'weary',
        '\ud83d\ude35':'dizzy_face',
        '\ud83d\ude25':'disappointed_relieved',
        '\ud83d\ude26':'frowning',
        '\ud83d\ude01':'grin',
        '\ud83d\ude2f':'hushed',
        '\ud83d\ude37':'mask',
        '\ud83d\ude14':'pensive',
        '\ud83d\ude13':'sweat',
        '\ud83d\ude1c':'stuck_out_tongue_winking_eye',
        '\ud83d\ude11':'expressionless',
        '\ud83d\ude36':'no_mouth',
        '\ud83d\ude10':'neutral_face',
        '\ud83d\ude34':'sleeping',
        '\ud83d\ude1d':'stuck_out_tongue_closed_eyes',
        '\ud83d\ude2a':'sleepy',
        '\ud83d\ude06':'laughing; satisfied',
        '\ud83d\ude0e':'sunglasses',
        '\ud83d\ude1b':'stuck_out_tongue',
        '\ud83d\ude32':'astonished',
        '\ud83d\ude0a':'blush',
        '\ud83d\ude00':'grinning',
        '\ud83d\ude3d':'kissing_cat',
        '\ud83d\ude19':'kissing_smiling_eyes',
        '\ud83d\ude17':'kissing',
        '\ud83d\ude1a':'kissing_closed_eyes',
        '\u263a\ufe0f':'relaxed',
        '\ud83d\ude0c':'relieved',
        '\ud83d\ude04':'smile',
        '\ud83d\ude3c':'smirk_cat',
        '\ud83d\ude38':'smile_cat',
        '\ud83d\ude03':'smiley',
        '\ud83d\ude3a':'smiley_cat',
        '\ud83d\ude05':'sweat_smile',
        '\ud83d\ude0f':'smirk',
        '\ud83d\ude3b':'heart_eyes_cat',
        '\ud83d\ude0d':'heart_eyes',
        '\ud83d\ude07':'innocent',
        '\ud83d\ude02':'joy',
        '\ud83d\ude39':'joy_cat',
        '\ud83d\ude18':'kissing_heart',
        '\ud83d\ude09':'wink',
        '\ud83d\ude0b':'yum',
        '\ud83d\ude24':'triumph'}

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
        htmlparser = html.parser.HTMLParser()

        if name == "sms":
            sms_subject = attrs.get('subject','')
            sms_date = int(attrs['date']) / 1000     # unix epoch
            sms_body = attrs['body']
            sms_address = attrs['address'].strip().replace('-','').replace('/','').replace(' ','').replace('+','00')
            sms_type_incoming = int(attrs['type']) == 1
            contact_name = False
            if 'contact_name' in attrs:
                ## NOTE: older version of backup app did not insert contact_name into XML
                contact_name = attrs['contact_name']
            else:
                if self._numberdict:
                    if sms_address in list(self._numberdict.keys()):
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
                sms_body = html.unescape(sms_body.replace('EnCoDiNgHaCk42', '&#'))
                for emoji in list(self.EMOJIS.keys()):
                    ## FIXXME: this is a horrible dumb brute-force algorithm.
                    ##         In case of bad performance, this can be optimized dramtically
                    sms_body = sms_body.replace(emoji, self.EMOJI_ENCLOSING_CHARACTER + \
                                                self.EMOJIS[emoji] + self.EMOJI_ENCLOSING_CHARACTER).replace('\n', '⏎')

                if sms_subject != "null":
                    # in case of MMS we have a subject
                    output += sms_subject
                    notes = sms_body
                else:
                    output += sms_body
                    notes = ""

                timestamp = OrgFormat.date(time.gmtime(sms_date), show_time=True)
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
            self._numberdict = parse_org_contact_file(self._args.orgcontactsfile)


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
                    outputhandle.write(line.replace('&#', 'EnCoDiNgHaCk42') + '\n')
                except IOError as e:
                    print("tempfile line " + str(line_number) +  " [" + str(temp_xml_file) + "]")
                    print("I/O error({0}): {1}".format(e.errno, e.strerror))
                except ValueError as e:
                    print("tempfile line " + str(line_number) +  " [" + str(temp_xml_file) + "]")
                    print("Value error: {0}".format(e))
                    #print "line [%s]" % str(line)
                except:
                    print("tempfile line " + str(line_number) +  " [" + str(temp_xml_file) + "]")
                    print("Unexpected error:", sys.exc_info()[0])
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
