#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2019-11-06 15:29:12 vk>

import datetime
import json
import logging
import os
import re
import sqlite3

import emoji
from orgformat import OrgFormat

from memacs.lib.contactparser import parse_org_contact_file
from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties


class WhatsApp(Memacs):


    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
            "-f", "--file", dest="msgstore",
            action="store", type=open, required=True,
            help="path to decrypted msgstore.db file")

        self._parser.add_argument(
            "--ignore-incoming", dest="ignore_incoming",
            action="store_true", help="ignore received messages")

        self._parser.add_argument(
            "--ignore-outgoing", dest="ignore_outgoing",
            action="store_true", help="ignore sent messages")

        self._parser.add_argument(
            "--ignore-groups", dest="ignore_groups",
            action="store_true",help="ignore group messages")

        self._parser.add_argument(
            "--output-format", dest="output_format",
            action="store", default="{verb} [[{handler}:{name}][{name}]]: {text}",
            help="format string to use for the headline")

        self._parser.add_argument(
            "--set-handler", dest="handler",
            action="store", default="tel",
            help="set link handler")

        self._parser.add_argument(
            "--demojize", dest="demojize",
            action="store_true", help="replace emoji with the appropriate :shortcode:")

        self._parser.add_argument(
            "--skip-emoji", dest="skip_emoji",
            action="store_true", help="skip all emoji")

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
        if self._args.orgcontactsfile:
            if not (os.path.exists(self._args.orgcontactsfile) or \
                    os.access(self._args.orgcontactsfile, os.R_OK)):
                self._parser.error("Org-contacts file not found or not readable")
            self._numberdict = parse_org_contact_file(self._args.orgcontactsfile)
        else:
            self._numberdict = {}

    def _is_ignored(self, msg):
        """check for ignored message type"""

        if msg['type'] is 'INCOMING' and self._args.ignore_incoming:
            return True

        if msg['type'] is 'OUTGOING' and self._args.ignore_outgoing:
            return True

        group_message_regex = r'-[0-9]{10}'
        if self._args.ignore_groups and re.findall(group_message_regex, msg['number']):
            return True

    def _handle_message(self, msg):
        """parse a single message row"""

        msg['number'] = '00' + msg['number'].split('@')[0]
        msg['name'] = self._numberdict.get(msg['number'],msg['number'])
        msg['verb'] = 'to' if msg['type'] else 'from'
        msg['type'] = 'OUTGOING' if msg['type'] else 'INCOMING'
        msg['handler'] = self._args.handler

        if msg['text']:
            if self._args.demojize:
                msg['text'] = emoji.demojize(msg['text'])

            if self._args.skip_emoji:
                msg['text'] = re.sub(emoji.get_emoji_regexp(), '', msg['text'])

        timestamp = datetime.datetime.fromtimestamp(msg['timestamp'] / 1000)

        properties = OrgProperties(data_for_hashing=json.dumps(msg))
        properties.add('NUMBER', msg['number'])
        properties.add('TYPE', msg['type'])

        output = self._args.output_format.format(**msg)

        if msg['text'] and not self._is_ignored(msg):
            self._writer.write_org_subitem(timestamp=OrgFormat.date(timestamp, show_time=True),
                                           output=output, properties=properties)

    def _main(self):
        """
        get's automatically called from Memacs class
        """

        conn = sqlite3.connect(os.path.abspath(self._args.msgstore.name))
        query = conn.execute('SELECT * FROM messages')

        for row in query:
            self._handle_message({
                'timestamp': row[7],
                'number': row[1],
                'type': row[2],
                'text': row[6]
            })

            logging.debug(row)
