#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2017-02-07 19:25 manu>

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
            "-d", "--db", dest="historystore",
            action="store", type=file, required=True,
            help="""path to places.sqlite file. usually in
/home/rgrau/.mozilla/firefox/__SOMETHING__.default/places.sqlite """)

        self._parser.add_argument(
            "--output-format", dest="output_format",
            action="store", default="[[{url}][{title}]]",
            help="format string to use for the headline")


    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)

    def _handle_url(self, params):
        timestamp = datetime.datetime.fromtimestamp(int(params['timestamp']/1000000))

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

        self._writer.write_org_subitem(
            timestamp=OrgFormat.datetime(timestamp),
            output=output, properties=properties)

    def _main(self):
        """
        get's automatically called from Memacs class
        """
        conn = sqlite3.connect(os.path.abspath(self._args.historystore.name))
        query = conn.execute("""
        select guid, url, title, visit_count,
               -- datetime(last_visit_date/1000000, 'unixepoch')
                last_visit_date
        from   moz_places
        where  last_visit_date IS NOT NULL
        order by last_visit_date """)

        for row in query:
            self._handle_url({
                'guid'        : row[0],
                'url'         : row[1],
                'title'       : row[2],
                'visit_count' : row[3],
                'timestamp'   : row[4],
            })
