#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2017-02-07 19:25 manu>

import calendar
import distutils.spawn
import io
import logging
import os.path
import subprocess
import sys
import time

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties
from memacs.lib.reader import UnicodeCsvReader

ARBTT_STATS = 'arbtt-stats'
ARBTT_FORMAT = '%m/%d/%y %H:%M:%S'


class Arbtt(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
            "--logfile",
            dest="log",
            action="store",
            help="use this file instead of ~/.arbtt/capture.log")

        self._parser.add_argument(
            "--categorizefile",
            dest="cfg",
            action="store",
            help="use this file instead of ~/.arbtt/categorize.cfg")

        self._parser.add_argument(
            "--also-inactive",
            dest="inactive",
            action="store_true",
            help="include inactive samples")

        self._parser.add_argument(
            "--intervals",
            dest="intervals",
            action="append", required=True,
            help="list intervals of tag or category " + \
                 "(the latter has to end with a colon)"
        )

        self._parser.add_argument(
            "--csv",
            dest="csv",
            action="store",
            help="csv file"
        )

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)

        if self._args.log:
            if not os.path.isfile(self._args.log):
                self._parser.error("logfile does not exist")

        if self._args.cfg:
            if not os.path.isfile(self._args.cfg):
                self._parser.error("config file does not exist")

        if self._args.csv:
            if not os.path.isfile(self._args.csv):
                self._parser.error("csv file does not exist")

        if self._args.csv and self._args.log or self._args.inactive:
            self._parser.error("You gave both \"--csv\" and \"--logfile\" or \"--also-inactive\" argument." + \
                               "Please use either or.")

        if not self._args.intervals:
            self._parser.error("No intervals tag or category specified")

    def get_sec(self, t):
        """
        get H:M:S as seconds

        @param t: hms string
        @return: seconds
        """
        h, m, s = [int(i) for i in t.split(':')]
        return h*3600 + m*60 + s

    def get_timestamp(self, dt):
        """
        1. parse datetime string
        2. utc to local time

        @param dt: datetime string
        @return: datetime in org format
        """
        dt_tuple = time.strptime(dt, ARBTT_FORMAT)
        dt_local = time.localtime(calendar.timegm(dt_tuple))

        return time.strftime('<%Y-%m-%d %a %H:%M:%S>', dt_local)

    def get_timerange(self, begin, end):
        """
        return a date+time range (including seconds)

        @param begin: start date (string)
        @param end: end date (string)
        @return: datetime range in org format
        """
        return "%s--%s" % (self.get_timestamp(begin),
                           self.get_timestamp(end))

    def __parse_sample(self, target, row):
        """
        parse a row of csv and write entry

        @param target: tag or category
        @param row: list of columns
        """
        tag, begin, end, duration = row

        timestamp = self.get_timerange(begin, end)
        duration = self.get_sec(duration)

        properties = OrgProperties(data_for_hashing=timestamp)
        properties.add('DURATION', duration)

        tags = []

        # remove colon from output
        if target.endswith(':'):
            target = target[:-1]
            tags.append(target)
        elif ':' in target:
            target = target.split(':')[0]

        output = target.capitalize()
        tags.append(tag)

        self._writer.write_org_subitem(
            timestamp=timestamp,
            output=output,
            tags=tags,
            properties=properties
        )

    def __handle_intervals(self, target):
        """
        handles an interval of data records

        @param target: tag or category
        """
        command = [
            ARBTT_STATS,
            '--output-format=csv',
            '--intervals=%s' % target
        ]

        if self._args.log:
            command.append('--logfile=%s' % self._args.log)

        if self._args.cfg:
            command.append('--categorizefile=%s' % self._args.cfg)

        if self._args.inactive:
            command.append('--also-inactive')

        if not self._args.csv:
            stats = subprocess.check_output(command)
            f = io.StringIO(str(stats))
        else:
            # skip dump of stats data
            f = open(self._args.csv)

        # skip header columns
        reader = UnicodeCsvReader(f, delimiter=',')
        next(reader)

        for row in reader:
            self.__parse_sample(target, row)

    def _main(self):
        """
        get's automatically called from Memacs class
        """
        # check if arbtt is installed
        if distutils.spawn.find_executable(ARBTT_STATS) is None:
            logging.error(ARBTT_STATS + ': command not found')
            sys.exit(1)

        for target in self._args.intervals:
            self.__handle_intervals(target)
