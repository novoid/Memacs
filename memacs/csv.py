#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-30 03:38:09 armin>

import logging
import time
import os
import sys
from lib.orgformat import OrgFormat
from lib.memacs import Memacs
from lib.reader import UnicodeCsvReader
from lib.orgproperty import OrgProperties


class Csv(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
           "-f", "--file", dest="csvfile",
           action="store",
           help="input csv file")

        self._parser.add_argument(
           "-d", "--delimiter", dest="delimiter",
           action="store",
           help="delimiter, default \";\"")

        self._parser.add_argument(
           "-e", "--encoding", dest="encoding",
           action="store",
           help="default encoding utf-8, see " + \
           "http://docs.python.org/library/codecs.html#standard-encodings" + \
           "for possible encodings")

        self._parser.add_argument(
           "-ti", "--timestamp-index", dest="timestamp_index",
           action="store",
           help="on which column is timestamp?")

        self._parser.add_argument(
           "-tf", "--timestamp-format", dest="timestamp_format",
           action="store",
           #help="format of the timestamp, i.e. \"%d.%m.%Y %H:%M:%S:%f\" " + \
           help="format of the timestamp, i.e. " + \
           "\"%%d.%%m.%%Y %%H:%%M:%%S:%%f\" " + \
           "for  \"14.02.2012 10:22:37:958\" see " + \
           "http://docs.python.org/library/time.html#time.strftime" + \
           "for possible formats")

        self._parser.add_argument(
           "-oi", "--output-indices", dest="output_indices",
           action="store",
           help="indices to use for output i.e. \"1 2 3\"")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if not self._args.csvfile:
            self._parser.error("please specify input csv file")
        if not (os.path.exists(self._args.csvfile) or \
            os.access(self._args.csvfile, os.R_OK)):
            self._parser.error("input file not found or not readable")

        if self._args.delimiter:
            self._args.delimiter = self._args.delimiter
        else:
            self._args.delimiter = ";"

        if not self._args.encoding:
            self._args.encoding = "utf-8"

        if not self._args.timestamp_index:
            self._parser.error("need to know timestamp index")
        else:
            try:
                self._args.timestamp_index = int(self._args.timestamp_index)
            except ValueError:
                self._parser.error("timestamp index not an int")

        if not self._args.timestamp_format:
            self._parser.error("need to know timestamp format")

        if not self._args.output_indices:
            self._parser.error("need to know output indices")
        else:
            try:
                self._args.output_indices = map(
                    int, self._args.output_indices.split())
            except ValueError:
                self._parser.error("output-indices must have " + \
                                   "following format i.e: \"1 2 3\"")

    def _main(self):
        """
        get's automatically called from Memacs class
        """

        with open(self._args.csvfile, 'rb') as f:
            try:
                for row in UnicodeCsvReader(f, encoding=self._args.encoding,
                                         delimiter=self._args.delimiter):
                    logging.debug(row)
                    try:
                        tstamp = time.strptime(row[self._args.timestamp_index],
                                               self._args.timestamp_format)
                    except ValueError, e:
                        logging.error("timestamp-format does not match: %s",
                                      e)
                        sys.exit(1)
                    except IndexError, e:
                        logging.error("did you specify the right delimiter?",
                                      e)
                        sys.exit(1)

                    timestamp = OrgFormat.datetime(tstamp)

                    output = []
                    for i in self._args.output_indices:
                        output.append(row[i])
                    output = " ".join(output)

                    data_for_hashing = "".join(row)

                    properties = OrgProperties(
                            data_for_hashing=data_for_hashing)

                    self._writer.write_org_subitem(timestamp=timestamp,
                                                   output=output,
                                                   properties=properties,
                                                   )
            except UnicodeDecodeError, e:
                logging.error("could not decode file in utf-8," + \
                              "please specify input encoding")
                sys.exit(1)
