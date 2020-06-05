#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import time

import geocoder
import gpxpy
from orgformat import OrgFormat

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties


class GPX(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
            "-f", "--folder", dest="source",
            action="store", required=True,
            help="path to gpx file or folder")

        self._parser.add_argument(
            "-p", "--provider", dest="provider",
            action="store", default="google",
            help="geocode provider, default google")

        self._parser.add_argument(
            "-u", "--url", dest="url",
            action="store", help="url to nominatim server (osm only)")

        self._parser.add_argument(
            "--output-format", dest="output_format",
            action="store", default="{address}",
            help="format string to use for the headline")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)

        if not os.path.exists(self._args.source):
            self._parser.error("source file or folder does not exist")

        if self._args.url and not self._args.url.startswith("http"):
            self._parser.error("invalid url given")

    def reverse_geocode(self, lat, lng):
        """get address for latitude/longitude"""

        if 'google' in self._args.provider:
            geocode = geocoder.google([lat, lng], method='reverse')

        elif 'osm' in self._args.provider:
            if not self._args.url:
                geocode = geocoder.osm([lat, lng], method='reverse')
                time.sleep(1)  # Nominatim Usage Policy
            else:
                if 'localhost' in self._args.url:
                    geocode = geocoder.osm([lat, lng], method='reverse', url='http://localhost/nominatim/search')
                else:
                    geocode = geocoder.osm([lat, lng], method='reverse', url=self._args.url)

        else:
            self._parser.error("invalid provider given")
            raise ValueError('invalid provider given')

        if not geocode.ok:
            logging.error("geocoding failed or api limit exceeded")
            raise RuntimeError('geocoding failed or api limit exceeded')
        else:
            logging.debug(geocode.json)
            return geocode.json

    def write_point(self, p):
        """write a point (including geocoding)"""

        timestamp = OrgFormat.date(p.time, show_time=True)
        geocode = self.reverse_geocode(p.latitude, p.longitude)
        output = self._args.output_format.format(**geocode)

        tags = []

        properties = OrgProperties(data_for_hashing=timestamp)

        if p.latitude:
            properties.add('LATITUDE', p.latitude)

        if p.longitude:
            properties.add('LONGITUDE', p.longitude)

        if p.source:
            tags.append(p.source.lower())

        if timestamp:
            self._writer.write_org_subitem(timestamp=timestamp,
                                           output=output,
                                           properties=properties,
                                           tags=tags)

    def handle_file(self, f):
        """iterate through a file"""

        data = open(f)
        gpx = gpxpy.parse(data)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    self.write_point(point)
                    logging.debug(point)

    def _main(self):
        """
        get's automatically called from Memacs class
        """

        if os.path.isfile(self._args.source):
            self.handle_file(self._args.source)

        else:
            for root, dirs, files in os.walk(self._args.source):
                for f in files:
                    if f.endswith('.gpx'):
                        self.handle_file(os.path.join(root, f))
