#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-11-06 15:28:28 vk>

import logging
import sys

from dateutil import parser
from orgformat import OrgFormat
from twython import Twython, TwythonError

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties


class Twitter(Memacs):
    def _main(self):
        APP_KEY = self._get_config_option("APP_KEY")

        APP_SECRET = self._get_config_option("APP_SECRET")

        OAUTH_TOKEN = self._get_config_option("OAUTH_TOKEN")

        OAUTH_TOKEN_SECRET = self._get_config_option("OAUTH_TOKEN_SECRET")

        screen_name = self._get_config_option("screen_name")

        count = self._get_config_option("count")

        twitter = Twython(
            APP_KEY,
            APP_SECRET,
            OAUTH_TOKEN,
            OAUTH_TOKEN_SECRET
            )
        try:
            home_timeline = twitter.get_home_timeline(screenname=screen_name, count=count)

        except TwythonError as e:
            logging.error(e)
            sys.exit(1)

        for tweet in home_timeline:
            # strptime doesn't support timezone info, so we are using dateutils.
            date_object = parser.parse(tweet['created_at'])

            timestamp = OrgFormat.date(date_object, show_time=True)
            try:
                # Data is already Unicode, so don't try to re-encode it.
                output = tweet['text']
            except:
               logging.error(sys.exc_info()[0])
               print("Error: ", sys.exc_info()[0])

            data_for_hashing = output + timestamp + output
            properties = OrgProperties(data_for_hashing=data_for_hashing)

            properties.add("name", tweet['user']['name'])
            properties.add("twitter_id", tweet['id'])
            properties.add("contributors", tweet['contributors'])
            properties.add("truncated", tweet['truncated'])
            properties.add("in_reply_to_status_id", tweet['in_reply_to_status_id'])
            properties.add("favorite_count", tweet['favorite_count'])
            properties.add("source", tweet['source'])
            properties.add("retweeted", tweet['retweeted'])
            properties.add("coordinates", tweet['coordinates'])
            properties.add("entities", tweet['entities'])

            self._writer.write_org_subitem(timestamp=timestamp,
                                          output = output,
                                          properties = properties)
