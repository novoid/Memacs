#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-30 03:38:09 armin>

import logging
import time
from datetime import datetime
from dateutil import parser
import os
import sys
from twython import Twython, TwythonError
from lib.orgformat import OrgFormat
from lib.memacs import Memacs
from lib.reader import UnicodeCsvReader
from lib.orgproperty import OrgProperties

class Twitter(Memacs):
    def _main(self):



        APP_KEY = self._get_config_option("APP_KEY")

        APP_SECRET = self._get_config_option("APP_SECRET")

        OAUTH_TOKEN = self._get_config_option("OAUTH_TOKEN")

        OAUTH_TOKEN_SECRET = self._get_config_option("OAUTH_TOKEN_SECRET")

        screen_name = self._get_config_option("screen_name")

        print "APP_KEY: %s\nAPP_SECRET: %s\nOAUTH_OKEN: %s\nOAUTH_TOKEN_SECRET: %s " % (APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        twitter = Twython(
            APP_KEY,
            APP_SECRET,
            OAUTH_TOKEN,
            OAUTH_TOKEN_SECRET
            )
        try:
            home_timeline = twitter.get_home_timeline(screenname=screen_name, count=50)

        except TwythonError as e:
            logging.error(e)
            sys.exit(1)

        for tweet in home_timeline:
            # strptime doesn't support timezone info, so w are using dateutils.
            date_object = parser.parse(tweet['created_at'].encode('utf-8'))

            #timestamp = OrgFormat.datetime(time.gmtime(0))
            print "Created: %s Tweet: %s" % (tweet['created_at'], tweet['text'])
            timestamp = OrgFormat.datetime(date_object)
            try:
                #output = tweet['text'].decode('utf-8')
                # Data is already Unicode, so don't try to re-encode it.
                output = tweet['text']
            except:
               logging.error(sys.exc_info()[0])
               print "Error: ", sys.exc_info()[0]

            data_for_hashing = output + timestamp + output
            properties = OrgProperties(data_for_hashing=data_for_hashing)

            properties.add("name", tweet['user']['name'].encode('utf-8'))
            properties.add("twitter_id", tweet['id'])
            properties.add("contributors", tweet['contributors'])
            properties.add("truncated", tweet['truncated'])
            properties.add("in_reply_to_status_id", tweet['in_reply_to_status_id'])
            properties.add("favorite_count", tweet['favorite_count'])
            properties.add("source", tweet['source'].encode('utf-8'))
            properties.add("retweeted", tweet['retweeted'])
            properties.add("coordinates", tweet['coordinates'])
            properties.add("entities", tweet['entities'])

            self._writer.write_org_subitem(timestamp=timestamp,
                                          output = output,
                                          properties = properties)
