#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2022-07-14 16:04:14 vk>

import argparse
import datetime
import json
import logging
import sys
import time

from orgformat import OrgFormat

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties
from memacs.lib.reader import UnicodeDictReader


class Csv(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
           "-f", "--file", dest="csvfile", required=True,
           action="store", help="input csv file", type=argparse.FileType('rb'))

        self._parser.add_argument(
           "-d", "--delimiter", dest="delimiter", default=";",
           action="store", help='delimiter, default ";"')

        self._parser.add_argument(
           "-e", "--encoding", dest="encoding",
           action="store", default="utf-8", help="default encoding utf-8, " +
           "see http://docs.python.org/library/codecs.html#standard-encodings" +
           "for possible encodings")

        self._parser.add_argument(
            "-n", "--fieldnames", dest="fieldnames", default=None,
            action="store", help="header field names of the columns",
            type=str.lower)

        self._parser.add_argument(
            "-p", "--properties", dest="properties", default='',
            action="store", help="fields to use for properties",
            type=str.lower)

        self._parser.add_argument(
            "--timestamp-field", dest="timestamp_field", required=True,
            action="store", help="field name of the timestamp",
            type=str.lower)

        self._parser.add_argument(
            "--timestamp-format", dest="timestamp_format",
            action="store", help='format of the timestamp, i.e. ' +
            '"%%d.%%m.%%Y %%H:%%M:%%S" for "14.02.2012 10:22:37" ' +
            'see http://docs.python.org/library/time.html#time.strftime' +
            'for possible formats. Default is the current local format, ' +
            'so please do specify format in order to be unambiguous.')

        self._parser.add_argument(
            "--output-format", dest="output_format", required=True,
            action="store", help="format string to use for the output")

        self._parser.add_argument(
            "--skip-header", dest="skip_header",
            action="store_true", help="skip first line of the csv file")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)

        if self._args.fieldnames:
            self._args.fieldnames = [name.strip() for name in self._args.fieldnames.split(',')]

    def _handle_row(self, row):
        """
        handle a single row
        """

        try:
            # assume unix timestamp
            if not self._args.timestamp_format:
                timestamp = datetime.datetime.fromtimestamp(int(row[self._args.timestamp_field]))
            else:
                timestamp = time.strptime(row[self._args.timestamp_field], self._args.timestamp_format)

            # show time with the timestamp format, but only
            # if it contains at least hours and minutes
            if not self._args.timestamp_format or \
             any(x in self._args.timestamp_format for x in ['%H', '%M']):
                timestamp = OrgFormat.date(timestamp, show_time=True)
            else:
                timestamp = OrgFormat.date(timestamp)

        except ValueError as e:
            logging.error("timestamp-format does not match: %s", e)
            sys.exit(1)

        except IndexError as e:
            logging.error("did you specify the right delimiter?", e)
            sys.exit(1)

        properties = OrgProperties(data_for_hashing=json.dumps(row))
        output = self._args.output_format.format(**row)

        if self._args.properties:
            for prop in self._args.properties.split(','):
                properties.add(prop.upper().strip(), row[prop])

        self._writer.write_org_subitem(timestamp=timestamp,
                                       output=output,
                                       properties=properties)

    def _main(self):
        """
        get's automatically called from Memacs class
        """

        with self._args.csvfile as f:

            try:
                reader = UnicodeDictReader(f,
                                           self._args.delimiter,
                                           self._args.encoding,
                                           self._args.fieldnames)

                if self._args.skip_header:
                    next(reader)

                for row in reader:
                    self._handle_row(row)
                    logging.debug(row)

            except TypeError as e:
                logging.error("not enough fieldnames or wrong delimiter given")
                logging.debug("Error: %s" % e)
                sys.exit(1)

            except UnicodeDecodeError as e:
                logging.error("could not decode file in utf-8, please specify input encoding")
                sys.exit(1)
