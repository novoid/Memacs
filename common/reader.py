# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-19 15:13:31 aw>

import codecs
import logging
import sys
from urllib2 import urlopen
from urllib2 import HTTPError
from urllib2 import URLError


class CommonReader:
    """
    Class for reading
    * files
    * url's
    """

    @staticmethod
    def get_data_from_file(path):
        """
        reads a file

        @param file: path to file
        @return: returns data
        """
        try:
            input_file = codecs.open(path, 'rb')
            data = input_file.read()
            input_file.close()
            return data
        except IOError:
            logging.error("Error at opening file: %s" % path)
            sys.exit(1)

    @staticmethod
    def get_data_from_url(url):
        """
        reads from a url

        @param url: url to read
        @returns: returns data
        """
        try:
            req = urlopen(url, None, 10)
            return req.read()
        except HTTPError:
            logging.error("ValueError: " % url)
            sys.exit(1)
        except URLError:
            logging.error("ValueError: " % url)
            sys.exit(1)
        except ValueError:
            logging.error("ValueError: %s" % url)
            sys.exit(1)
