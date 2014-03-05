#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2014-03-05 20:08:08 vk>

import sys
import os
import re
import logging
import time
import datetime
from lib.orgformat import OrgFormat
from lib.memacs import Memacs
from lib.reader import CommonReader
from lib.orgproperty import OrgProperties
#import pdb  ## pdb.set_trace()  ## FIXXME





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
                                    "(\d+)$", flags = re.U)
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
        if not (os.path.exists(self._args.phonelogfile) or \
                     os.access(self._args.phonelogfile, os.R_OK)):
            self._parser.error("input file not found or not readable")




    def _generateOrgentry(self, e_time, e_name, e_batt, e_uptime, 
                          e_last_opposite_occurrence, e_last_occurrence, 
                          prev_office_sum, prev_office_first_begin):
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
        """

        assert e_time.__class__ == datetime.datetime
        assert e_name.__class__ == unicode
        assert e_batt.__class__ == unicode
        assert e_uptime.__class__ == unicode
        assert (e_last_opposite_occurrence.__class__ == datetime.datetime or not e_last_opposite_occurrence)
        assert (e_last_occurrence.__class__ == datetime.datetime or not e_last_occurrence)

        last_info = u''
        in_between_hms = u''
        in_between_s = u''
        ignore_occurrence = False

        ## convert parameters to be writable:
        office_sum = prev_office_sum
        office_first_begin = prev_office_first_begin

        if e_last_opposite_occurrence:

            in_between_s = (e_time - e_last_opposite_occurrence).seconds + \
                (e_time - e_last_opposite_occurrence).days * 3600 * 24
            in_between_hms = unicode(OrgFormat.get_hms_from_sec(in_between_s))

            if e_name == u'boot':
                last_info = u' (off for '
            elif e_name == u'shutdown':
                last_info = u' (on for '
            elif e_name.endswith(u'-end'):
                last_info = u' (' + e_name[0:-4].replace('wifi-','') + u' for '
            else:
                last_info = u' (not ' + e_name.replace('wifi-','') + u' for '

            ## handle special case: office hours
            additional_paren_string = ""
            if e_name == 'wifi-office-end':
                office_total = None
                ## calculate office_sum and office_total
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

                ## come up with the additional office-hours string:
                additional_paren_string = u'; today ' + OrgFormat.get_hms_from_sec(office_sum) + \
                    '; today total ' + OrgFormat.get_hms_from_sec(office_total)

            if additional_paren_string:
                last_info += unicode(OrgFormat.get_dhms_from_sec(in_between_s)) + additional_paren_string + u')'
            else:
                last_info += unicode(OrgFormat.get_dhms_from_sec(in_between_s)) + u')'

        ## handle special case: office hours
        if e_name == 'wifi-office':
            if not office_sum or not office_first_begin:
                ## new day
                office_first_begin = e_time

        ## handle special case: boot without previous shutdown = crash
        if (e_name == u'boot') and \
                (e_last_occurrence and e_last_opposite_occurrence) and \
                (e_last_occurrence > e_last_opposite_occurrence):
            ## last boot is more recent than last shutdown -> crash has happened
            last_info = u' after crash'
            in_between_hms = u''
            in_between_s = u''
            ignore_occurrence = True

        properties = OrgProperties()
        properties.add("IN-BETWEEN", in_between_hms)
        properties.add("IN-BETWEEN-S", unicode(in_between_s))
        properties.add("BATT-LEVEL", e_batt)
        properties.add("UPTIME", OrgFormat.get_hms_from_sec(int(e_uptime)))
        properties.add("UPTIME-S", e_uptime)
        self._writer.write_org_subitem(timestamp = e_time.strftime('<%Y-%m-%d %a %H:%M>'),
                                       output = e_name + last_info,
                                       properties = properties)

            ## the programmer recommends you to read "memacs/tests/simplephonelogs_test.py"
            ## test_generateOrgentry_* for less cryptic examples on how this looks:
        return u'** ' + e_time.strftime('<%Y-%m-%d %a %H:%M>') + u' ' + e_name + last_info + \
            u'\n:PROPERTIES:\n:IN-BETWEEN: ' + in_between_hms + \
            u'\n:IN-BETWEEN-S: ' + unicode(in_between_s) + \
            u'\n:BATT-LEVEL: ' + e_batt + \
            u'\n:UPTIME: ' + unicode(OrgFormat.get_hms_from_sec(int(e_uptime))) + \
            u'\n:UPTIME-S: ' + unicode(e_uptime) + u'\n:END:\n', \
            ignore_occurrence, office_sum, office_first_begin


    def _determine_opposite_eventname(self, e_name):
        """
        Takes a look at the event and returns the name of the opposite event description.
        Opposite of 'boot' is 'shutdown' (and vice versa). 
        Opposite of 'foo' is 'foo-end' (and vice versa).

        @param e_name: string of an event name/description
        """

        assert (e_name.__class__ == unicode)

        if e_name == u'boot':
            return u'shutdown'
        elif e_name == u'shutdown':
            return u'boot'
        elif e_name.endswith(u'-end'):
            return e_name[0:-4]
        else:
            return e_name + u'-end'


    def _parse_data(self, data):
        """parses the phone log data"""

        last_occurrences = { }  ## holds the last occurrences of each event

        office_day = None  ## holds the current day (in order to recognize day change)
        office_first_begin = None  ## holds the time-stamp of the first appearance of wifi-office
        office_sum = None  ## holds the sum of periods of all office-durations for this day

        for line in data.split('\n'):

            if not line:
                continue

            logging.debug("line: %s", line)

            components = re.match(self.LOGFILEENTRY_REGEX, line)
            additional_paren_string = None  ## optional string for the parenthesis (in output header)

            if components:
                logging.debug("line matches")
            else:
                logging.debug("line does not match! (skipping this line)")
                continue

            ## extracting the components to easy to use variables:
            datestamp = components.groups()[self.RE_ID_DATESTAMP].strip()
            hours = int(components.groups()[self.RE_ID_HOURS].strip())
            minutes = int(components.groups()[self.RE_ID_MINUTES].strip())
            e_name = unicode(components.groups()[self.RE_ID_NAME].strip())
            e_batt = components.groups()[self.RE_ID_BATT].strip()
            e_uptime = components.groups()[self.RE_ID_UPTIME].strip()

            ## generating a datestamp object from the time information:
            e_time = datetime.datetime(int(datestamp.split('-')[0]),
                                       int(datestamp.split('-')[1]),
                                       int(datestamp.split('-')[2]),
                                       hours, minutes)

            ## resetting office_day
            if e_name == 'wifi-office':
                if not office_day:
                    office_sum = None
                    office_day = datestamp
                elif office_day != datestamp:
                    office_sum = None
                    office_day = datestamp

            # if e_name == 'wifi-office-end':
            #     if not office_day:
            #         logging.error('On ' + datestamp + ' I found \"wifi-office-end\" without a begin. ' + \
            #                           'Please do not work after midnight ;-)')

            opposite_e_name = self._determine_opposite_eventname(e_name)
            if opposite_e_name in last_occurrences:
                e_last_opposite_occurrence = last_occurrences[opposite_e_name]
            else:
                ## no previous occurrence of the opposite event type
                e_last_opposite_occurrence = False

            if e_name in last_occurrences:
                last_time = last_occurrences[e_name]
            else:
                last_time = False

            result, ignore_occurrence, office_sum, office_first_begin = \
                self._generateOrgentry(e_time, e_name, e_batt, 
                                       e_uptime, 
                                       e_last_opposite_occurrence,
                                       last_time,
                                       office_sum, office_first_begin)

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
