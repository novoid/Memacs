#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2018-07-21 15:23:55 vk>

import sqlite3
import datetime
import sys
import os
import re

from lib.orgproperty import OrgProperties
from lib.orgformat import OrgFormat
from lib.memacs import Memacs

reload(sys)
sys.setdefaultencoding('utf8')

class Firefox(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
            "-f", "--file", dest="historystore",
            action="store", type=file, required=True,
            help="""path to places.sqlite file. usually in
/home/rgrau/.mozilla/firefox/__SOMETHING__.default/places.sqlite """)

        self._parser.add_argument(
            "--output-format", dest="output_format",
            action="store", default="[[{url}][{title}]]",
            help="format string to use for the headline")

        self._parser.add_argument(
            "--omit-drawer", dest="omit_drawer",
            action="store_true", required=False,
            help="""Use a minimal output format that omits the PROPERTIES drawer.""")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)

    def _handle_url(self, params):
        timestamp = datetime.datetime.fromtimestamp(int(params['timestamp']/1000000))

        if not self._args.omit_drawer:
            properties = OrgProperties()
            if (params['title'] == "") :
                params['title'] = params['url']
            properties.add('URL', params['url'])
            properties.add('VISIT_COUNT', params['visit_count'])

        output = ""
        try:
            output = self._args.output_format.decode('utf-8').format(**params)
        except Exception:
            pass

        if self._args.omit_drawer:
            self._writer.write_org_subitem(
                timestamp=OrgFormat.datetime(timestamp),
                output=output, properties=None)
        else:
            self._writer.write_org_subitem(
                timestamp=OrgFormat.datetime(timestamp),
                output=output, properties=properties)


    def _main(self):
        """
        get's automatically called from Memacs class
        """
        conn = sqlite3.connect(os.path.abspath(self._args.historystore.name))
        query = conn.execute("""
        select url, title, visit_count,
               -- datetime(last_visit_date/1000000, 'unixepoch')
                last_visit_date
        from   moz_places
        where  last_visit_date IS NOT NULL
        order by last_visit_date """)

        for row in query:
            self._handle_url({
                'url'         : row[0],
                'title'       : row[1],
                'visit_count' : row[2],
                'timestamp'   : row[3],
            })
