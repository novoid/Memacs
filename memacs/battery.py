#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
import logging
import sys

import batinfo
from orgformat import OrgFormat

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties

ROOT = '/sys/class/power_supply'


class Battery(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
            "-b", "--battery", dest="name",
            action="store", default="BAT0",
            help="select battery to read stats from")

        self._parser.add_argument(
            "-p", "--path", dest="path",
            action="store", default=ROOT,
            help=argparse.SUPPRESS)

        self._parser.add_argument(
            "--output-format", dest="output_format",
            action="store", default="{battery.name}",
            help="format string to use for the output"
        )

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)

    def _handle_battery(self, bat):
        """
        handle single battery, e.g. BAT0
        """

        # calculate watt usage
        consumption = float(bat.current_now / 1000000.0 *
                            bat.voltage_now / 1000000.0)

        timestamp = OrgFormat.date(datetime.datetime.now(), show_time=True)
        output = self._args.output_format.format(battery=bat)

        properties = OrgProperties(data_for_hashing=timestamp)
        properties.add("CYCLE_COUNT", bat.cycle_count)
        properties.add("CAPACITY", '%s%%' % bat.capacity)
        properties.add("STATUS", bat.status.lower())

        if consumption:
            properties.add("CONSUMPTION", '%.1f W' % consumption)

        self._writer.write_org_subitem(timestamp=timestamp,
                                       output=output,
                                       properties=properties)

    def _main(self):
        """
        get's automatically called from Memacs class
        """

        try:
            batteries = batinfo.Batteries(self._args.path)

            for bat in batteries.stat:
                if self._args.name in bat.name:
                    self._handle_battery(bat)

        except OSError as e:
            logging.error("no battery present")
            sys.exit(1)
