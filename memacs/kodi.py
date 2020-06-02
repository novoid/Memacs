#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json
import logging
import sys
import time
from itertools import tee, islice, chain

from orgformat import OrgFormat

from memacs.lib.orgproperty import OrgProperties
from memacs.lib.reader import UnicodeDictReader
from .csv import Csv


# stolen from https://stackoverflow.com/questions/1011938/python-previous-and-next-values-inside-a-loop/1012089#1012089
def previous_current_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)


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

        self._parser.add_argument(
            '--identification-fields',
            dest="identification_fields",
            required=True,
            action='store',
            help='field names to uniquely identify one track e.g. title,artist',
            type=str.lower)

        self._parser.add_argument(
            '--minimal-pause-duration',
            dest='minimal_pause_duration',
            required=False,
            action='store',
            default=0,
            help=
            'minimal duration in seconds of a pause to be logged as a pause instead of being ignored',
            type=int,
        )
        self._parser.add_argument(
            '--start-actions',
            dest='start_actions',
            required=False,
            action='store',
            default='started,resumed',
            help=
            'comma seperated action commands when track is started (default started,resumed)'
        )

        self._parser.add_argument(
            '--stop-actions',
            dest='stop_actions',
            required=False,
            action='store',
            default='stopped,paused',
            help=
            'comma seperated action commands when track is stopped/paused (default stopped,paused)'
        )

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        super()._parser_parse_args()

        self._args.stop_actions = [
            name.strip() for name in self._args.stop_actions.split(',')
        ]
        self._args.start_actions = [
            name.strip() for name in self._args.start_actions.split(',')
        ]

        if self._args.identification_fields:
            self._args.identification_fields = [
                name.strip()
                for name in self._args.identification_fields.split(',')
            ]

    def read_timestamp(self, row):
        if not self._args.timestamp_format:
            timestamp = datetime.datetime.fromtimestamp(
                int(row[self._args.timestamp_field]))
        else:
            timestamp = time.strptime(row[self._args.timestamp_field],
                                      self._args.timestamp_format)

        return timestamp

    def format_timestamp(self, timestamp):
        # show time with the timestamp format, but only
        # if it contains at least hours and minutes
        show_time =  not self._args.timestamp_format or \
            any(x in self._args.timestamp_format for x in ['%H', '%M'])
        timestamp = OrgFormat.date(timestamp,show_time=show_time)
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
            timestamp=self.format_timestamp(start_time) + '--' +
            self.format_timestamp(stop_time),
            output=output,
            properties=properties)

    def tracks_are_identical(self, row1, row2):
        for field in self._args.identification_fields:
            if row1[field] != row2[field]:
                return False
        return True

    def track_is_paused(self, row, next_row):
        return next_row and self.tracks_are_identical(row, next_row) and (
            self.read_timestamp(next_row) - self.read_timestamp(row)
        ).total_seconds() < self._args.minimal_pause_duration

    def read_log(self, reader):
        """goes through rows and searches for start/stop actions"""
        start_time, stop_time = None, None
        for prev_row, row, next_row in previous_current_next(reader):
            timestamp = self.read_timestamp(row)
            action = row[self._args.action_field]
            if action in self._args.start_actions:
                if not start_time:
                    start_time = timestamp
                elif prev_row and not self.track_is_paused(prev_row, row):
                    self.write_one_track(prev_row, start_time, timestamp)
                    start_time = timestamp
            elif action in self._args.stop_actions and start_time:
                if not self.track_is_paused(row, next_row):
                    stop_time = timestamp
                else:
                    stop_time = None
            if start_time and stop_time:
                if self.tracks_are_identical(row, prev_row):
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
