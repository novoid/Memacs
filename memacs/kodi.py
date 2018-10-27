#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import argparse
import json
import logging
import time
import csv
import datetime
from .lib.orgproperty import OrgProperties
from .lib.orgformat import OrgFormat
from .lib.memacs import Memacs
from .lib.reader import UnicodeDictReader
from .csv import Csv

from itertools import tee, islice, chain


# stolen from https://stackoverflow.com/questions/1011938/python-previous-and-next-values-inside-a-loop/1012089#1012089
def previous_and_current(some_iterable):
    prevs, items = tee(some_iterable, 2)
    prevs = chain([None], prevs)
    return zip(prevs, items)


class Kodi(Csv):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        super()._parser_add_arguments()

        self._parser.add_argument(
            '--action-field',
            dest="action_field",
            required=True,
            action='store',
            help='field name of the action (start/paused,stopped)',
            type=str.lower)


    def read_timestamp(self, row):
        if not self._args.timestamp_format:
            timestamp = datetime.datetime.fromtimestamp(
                int(row[self._args.timestamp_field]))
        else:
            timestamp = time.strptime(row[self._args.timestamp_field],
                                      self._args.timestamp_format)

        # show time with the timestamp format, but only
        # if it contains at least hours and minutes
        if not self._args.timestamp_format or \
            any(x in self._args.timestamp_format for x in ['%H', '%M']):
            timestamp = OrgFormat.datetime(timestamp)
        else:
            timestamp = OrgFormat.date(timestamp)
        return timestamp

    def read_properties(self, row):
        properties = OrgProperties(data_for_hashing=json.dumps(row))
        output = self._args.output_format.format(**row)

        if self._args.properties:
            for prop in self._args.properties.split(','):
                properties.add(prop.upper().strip(), row[prop])
        return properties

    def write_one_track(self, row, start_time, stop_time):
        properties = self.read_properties(row)
        output = self._args.output_format.format(**row)
        self._writer.write_org_subitem(
            timestamp=start_time + '--' + stop_time,
            output=output,
            properties=properties)

    def read_log(self, reader):
        """goes through rows and searches for start/stop actions"""
        start_actions = ['started', 'resumed']
        stop_actions = ['paused', 'stopped']
        start_time, stop_time = None, None
        for prev_row, row in previous_and_current(reader):
            timestamp = self.read_timestamp(row)
            action = row[self._args.action_field]
            if action in start_actions:
                if not start_time:
                    start_time = timestamp
                else:
                    if prev_row:
                        self.write_one_track(prev_row, start_time, timestamp)
                    start_time = timestamp
            elif action in stop_actions and start_time:
                stop_time = timestamp
            if start_time and stop_time:
                self.write_one_track(row, start_time, stop_time)
                start_time, stop_time = None, None

    def _main(self):
        """
        get's automatically called from Memacs class
        """

        with self._args.csvfile as f:

            try:
                reader = UnicodeDictReader(f, self._args.delimiter,
                                           self._args.encoding,
                                           self._args.fieldnames)

                if self._args.skip_header:
                    next(reader)

                self.read_log(reader)

            except TypeError as e:
                logging.error("not enough fieldnames or wrong delimiter given")
                logging.debug("Error: %s" % e)
                sys.exit(1)

            except UnicodeDecodeError as e:
                logging.error(
                    "could not decode file in utf-8, please specify input encoding"
                )
                sys.exit(1)
