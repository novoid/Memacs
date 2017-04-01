#!/usr/bin/python2
# -*- coding: utf-8 -*-

import time
import datetime
import logging
import sys

import pylast

from lib.orgproperty import OrgProperties
from lib.orgformat import OrgFormat
from lib.memacs import Memacs


class LastFM(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
            '--output-format', dest='output_format',
            action='store', default=u'{title}',
            help='formt string to use for the output'
        )

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)

        if self._args.output_format:
            self._args.output_format = self._args.output_format.decode('utf-8')

    def _handle_recent_tracks(self, tracks):
        """parse recent tracks"""
        logging.debug(tracks)

        for t in tracks:
            timestamp = datetime.datetime.fromtimestamp(int(t.timestamp))

            output = self._args.output_format.format(title=t.track.title,
                                                     artist=t.track.artist,
                                                     album=t.album)

            properties = OrgProperties(data_for_hashing=t.timestamp)
            properties.add('ARTIST', t.track.artist)
            properties.add('ALBUM', t.album)

            self._writer.write_org_subitem(timestamp=OrgFormat.datetime(timestamp),
                                           output=output,
                                           properties=properties)

    def _main(self):
        """
        get's automatically called from Memacs class
        """

        options = {
            'api_secret': self._get_config_option('api_secret'),
            'api_key': self._get_config_option('api_key'),
            'password_hash': pylast.md5(self._get_config_option('password')),
            'username': self._get_config_option('username')
        }

        try:

            if 'lastfm' in self._get_config_option('network'):
                network = pylast.get_lastfm_network(**options)

            if 'librefm' in self._get_config_option('network'):
                network = pylast.get_librefm_network(**options)

            user = network.get_user(options['username'])

            self._handle_recent_tracks(user.get_recent_tracks(limit=100))

        except pylast.WSError, e:
            logging.error('an issue with the network web service occured: %s' % e)
            sys.exit(1)
