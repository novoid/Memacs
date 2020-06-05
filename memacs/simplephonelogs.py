#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2018-08-25 15:07:57 vk>

import datetime
import logging
import os
import re
import time

from orgformat import OrgFormat

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties
from memacs.lib.reader import CommonReader


class SimplePhoneLogsMemacs(Memacs):

    _REGEX_SEPARATOR = " *?# *?"

    ## match for example: "2012-11-20 # 19.59 # shutdown #   72 # 35682"
    ##                     0            1  2    3            4    5
    LOGFILEENTRY_REGEX = re.compile("([12]\d\d\d-[012345]\d-[012345]\d)" +
                                    _REGEX_SEPARATOR +
                                    "([ 012]\d)[:.]([012345]\d)" +
                                    _REGEX_SEPARATOR +
                                    "(.+)" +
                                    _REGEX_SEPARATOR +
                                    "(\d+)" +
                                    _REGEX_SEPARATOR +
                                    "(\d+)$", flags=re.U)
    RE_ID_DATESTAMP = 0
    RE_ID_HOURS = 1
    RE_ID_MINUTES = 2
    RE_ID_NAME = 3
    RE_ID_BATT = 4
    RE_ID_UPTIME = 5

    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
            "-f", "--file", dest="phonelogfile",
            action="store", required=True,
            help="path to phone log file")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if not (os.path.exists(self._args.phonelogfile) or
                os.access(self._args.phonelogfile, os.R_OK)):
            self._parser.error("input file not found or not readable")

    def _generateOrgentry(self, e_time, e_name, e_batt, e_uptime,
                          e_last_opposite_occurrence, e_last_occurrence,
                          prev_office_sum, prev_office_first_begin, office_lunchbreak,
                          battery_percentage_when_booting):
        """
        takes the data from the parameters and generates an Org-mode entry.

        @param e_time: time-stamp of the entry
        @param e_name: entry name/description
        @param e_batt: battery level
        @param e_uptime: uptime in seconds
        @param e_last_opposite_occurrence: time-stamp of previous opposite occurrence (if not False)
        @param e_last_occurrence: time-stamp of previous occurrence
        @param additional_paren_string: string that gets appended to the parenthesis
        @param prev_office_sum: holds the sum of all previous working duration today
        @param prev_office_first_begin: holds the first time-stamp of wifi-office for today
        @param office_lunchbreak: array of begin- and end-time-stamp of lunch-break (if any)
        @param battery_percentage_when_booting: battery level of previous boot (only set if no charge event was in-between)
        """

        assert e_time.__class__ == datetime.datetime
        assert e_name.__class__ == str
        assert e_batt.__class__ == str
        assert e_uptime.__class__ == str
        assert (e_last_opposite_occurrence.__class__ == datetime.datetime or not e_last_opposite_occurrence)
        assert (e_last_occurrence.__class__ == datetime.datetime or not e_last_occurrence)
        assert (not battery_percentage_when_booting or battery_percentage_when_booting.__class__ == int)

        last_info = ''
        in_between_hms = ''
        in_between_s = ''
        ignore_occurrence = False

        # convert parameters to be writable:
        office_sum = prev_office_sum
        office_first_begin = prev_office_first_begin

        if e_last_opposite_occurrence:

            in_between_s = (e_time - e_last_opposite_occurrence).seconds + \
                (e_time - e_last_opposite_occurrence).days * 3600 * 24
            in_between_hms = str(OrgFormat.hms_from_sec(in_between_s))

            if e_name == 'boot':
                last_info = ' (off for '
            elif e_name == 'shutdown':
                last_info = ' (on for '
            elif e_name.endswith('-end'):
                last_info = ' (' + e_name[0:-4].replace('wifi-', '') + ' for '
            else:
                last_info = ' (not ' + e_name.replace('wifi-', '') + ' for '

            # handle special case: office hours
            additional_paren_string = ""
            if e_name == 'wifi-office-end':
                office_total = None
                # calculate office_sum and office_total
                if not office_sum:
                    office_sum = (e_time - e_last_opposite_occurrence).seconds
                    office_total = office_sum
                else:
                    assert(office_first_begin)
                    assert(office_sum)
                    office_sum = office_sum + (e_time - e_last_opposite_occurrence).seconds
                    office_total = int(time.mktime(e_time.timetuple()) - time.mktime(office_first_begin.timetuple()))

                assert(type(office_total) == int)
                assert(type(office_sum) == int)
                assert(type(in_between_s) == int)

                # come up with the additional office-hours string:
                additional_paren_string = '; today ' + OrgFormat.hms_from_sec(office_sum) + \
                    '; today total ' + OrgFormat.hms_from_sec(office_total)

            if additional_paren_string:
                last_info += str(OrgFormat.dhms_from_sec(in_between_s)) + additional_paren_string + ')'
            else:
                last_info += str(OrgFormat.dhms_from_sec(in_between_s)) + ')'

        elif e_last_occurrence:

            in_between_s = (e_time - e_last_occurrence).seconds + \
                (e_time - e_last_occurrence).days * 3600 * 24
            in_between_hms = str(OrgFormat.hms_from_sec(in_between_s))

        # handle special case: office hours
        if e_name == 'wifi-office':
            if not office_sum or not office_first_begin:
                # new day
                office_first_begin = e_time
            else:
                # check if we've found a lunch-break (first wifi-office between 11:30-13:00 where not office for > 17min)
                if e_time.time() > datetime.time(11, 30) and e_time.time() < datetime.time(13, 00) and e_last_opposite_occurrence:
                    if e_last_opposite_occurrence.date() == e_time.date() and in_between_s > (17 * 60) and in_between_s < (80 * 60):
                        office_lunchbreak = [e_last_opposite_occurrence.time(), e_time.time()]

        # handle special case: boot without previous shutdown = crash
        if (e_name == 'boot') and \
                (e_last_occurrence and e_last_opposite_occurrence) and \
                (e_last_occurrence > e_last_opposite_occurrence):
            # last boot is more recent than last shutdown -> crash has happened
            last_info = ' after crash'
            in_between_hms = ''
            in_between_s = ''
            ignore_occurrence = True

        properties = OrgProperties()
        if in_between_s == 0:  # omit in-between content of property when it is zero
            in_between_s = ''
            in_between_hms = ''
        properties.add("IN-BETWEEN", in_between_hms)
        properties.add("IN-BETWEEN-S", str(in_between_s))
        properties.add("BATT-LEVEL", e_batt)
        properties.add("UPTIME", OrgFormat.hms_from_sec(int(e_uptime)))
        properties.add("UPTIME-S", e_uptime)

        if e_name == 'wifi-office-end' and office_lunchbreak:
            properties.add("OFFICE-SUMMARY",
                           e_last_opposite_occurrence.strftime('| %Y-%m-%d | %a ') +
                           prev_office_first_begin.strftime('| %H:%M ') +
                           office_lunchbreak[0].strftime('| %H:%M ') +
                           office_lunchbreak[1].strftime('| %H:%M ') +
                           e_time.strftime('| %H:%M | | |'))
        elif e_name == 'wifi-office-end' and not office_lunchbreak:
            properties.add("OFFICE-SUMMARY",
                           e_last_opposite_occurrence.strftime('| %Y-%m-%d | %a ') +
                           prev_office_first_begin.strftime('| %H:%M | 11:30 | 12:00 ') +
                           e_time.strftime('| %H:%M | | |'))
        elif e_name == 'shutdown':
            if battery_percentage_when_booting:
                batt_diff_from_boot_to_shutdown =  battery_percentage_when_booting - int(e_batt)
                if batt_diff_from_boot_to_shutdown >= 20:
                    # hypothetical run-time (in hours; derived from boot to shutdown) of the device for 100% battery capacity
                    # Note: battery_percentage_when_booting is set to False when a "charge-start"-event is recognized between boot and shutdown
                    # Note: only calculated when at least 20 percent difference of battery level between boot and shutdown
                    runtime_extrapolation = 100 * int(e_uptime) // batt_diff_from_boot_to_shutdown // 3600
                    properties.add("HOURS_RUNTIME_EXTRAPOLATION", runtime_extrapolation)

        self._writer.write_org_subitem(timestamp=e_time.strftime('<%Y-%m-%d %a %H:%M>'),
                                       output=e_name + last_info,
                                       properties=properties)

        return '** ' + e_time.strftime('<%Y-%m-%d %a %H:%M>') + ' ' + e_name + last_info + \
            '\n:PROPERTIES:\n:IN-BETWEEN: ' + in_between_hms + \
            '\n:IN-BETWEEN-S: ' + str(in_between_s) + \
            '\n:BATT-LEVEL: ' + e_batt + \
            '\n:UPTIME: ' + str(OrgFormat.hms_from_sec(int(e_uptime))) + \
            '\n:UPTIME-S: ' + str(e_uptime) + '\n:END:\n', \
            ignore_occurrence, office_sum, office_first_begin, office_lunchbreak

    def _determine_opposite_eventname(self, e_name):
        """
        Takes a look at the event and returns the name of the opposite event description.
        Opposite of 'boot' is 'shutdown' (and vice versa).
        Opposite of 'foo' is 'foo-end' (and vice versa).

        @param e_name: string of an event name/description
        """

        assert (e_name.__class__ == str)

        if e_name == 'boot':
            return 'shutdown'
        elif e_name == 'shutdown':
            return 'boot'
        elif e_name.endswith('-end'):
            return e_name[0:-4]
        else:
            return e_name + '-end'

    def _parse_data(self, data):
        """parses the phone log data"""

        last_occurrences = {}      # holds the previous occurrences of each event
        office_day = None          # holds the current day (in order to recognize day change)
        office_first_begin = None  # holds the time-stamp of the first appearance of wifi-office
        office_sum = None          # holds the sum of periods of all office-durations for this day
        office_lunchbreak = []     # array of begin and end time of lunch break
        battery_percentage_when_booting = False  # percentage of battery status of previous boot (only set if no charging event happened)

        for line in data.split('\n'):

            if not line:
                continue

            logging.debug("line: %s", line)

            components = re.match(self.LOGFILEENTRY_REGEX, line)

            if components:
                logging.debug("line matches")
            else:
                logging.debug("line does not match! (skipping this line)")
                continue

            # extracting the components to easy to use variables:
            datestamp = components.groups()[self.RE_ID_DATESTAMP].strip()
            hours = int(components.groups()[self.RE_ID_HOURS].strip())
            minutes = int(components.groups()[self.RE_ID_MINUTES].strip())
            e_name = str(components.groups()[self.RE_ID_NAME].strip())
            opposite_e_name = self._determine_opposite_eventname(e_name)
            e_batt = components.groups()[self.RE_ID_BATT].strip()
            e_uptime = components.groups()[self.RE_ID_UPTIME].strip()

            # generating a datestamp object from the time information:
            e_time = datetime.datetime(int(datestamp.split('-')[0]),
                                       int(datestamp.split('-')[1]),
                                       int(datestamp.split('-')[2]),
                                       hours, minutes)

            if e_name == 'boot':
                battery_percentage_when_booting = int(e_batt)
            elif e_name == 'charging-start':
                # set to False when a charging event is detected between boot and shutdown (which would render H_RUNTIME_EXTRAPOLATION useless)
                battery_percentage_when_booting = False
            elif e_name == 'shutdown' and opposite_e_name not in last_occurrences:
                # set to False when there is no boot in-between two shutdown events
                battery_percentage_when_booting = False

            # resetting office_day
            if e_name == 'wifi-office':
                if not office_day:
                    office_sum = None
                    office_day = datestamp
                    office_lunchbreak = []
                elif office_day != datestamp:
                    office_sum = None
                    office_day = datestamp
                    office_lunchbreak = []

            if opposite_e_name in last_occurrences:
                e_last_opposite_occurrence = last_occurrences[opposite_e_name]
            else:
                # no previous occurrence of the opposite event type
                e_last_opposite_occurrence = False

            if e_name in last_occurrences:
                last_time = last_occurrences[e_name]
            else:
                last_time = False

            result, ignore_occurrence, office_sum, office_first_begin, office_lunchbreak = \
                self._generateOrgentry(e_time, e_name, e_batt,
                                       e_uptime,
                                       e_last_opposite_occurrence,
                                       last_time,
                                       office_sum, office_first_begin, office_lunchbreak,
                                       battery_percentage_when_booting)

            ## update last_occurrences-dict
            if not ignore_occurrence:
                last_occurrences[e_name] = e_time

    def _main(self):
        """
        gets called automatically from Memacs class.
        read the lines from phonecalls backup xml file,
        parse and write them to org file
        """

        self._parse_data(CommonReader.get_data_from_file(self._args.phonelogfile))


# Local Variables:
# mode: flyspell
# eval: (ispell-change-dictionary "en_US")
# End:
