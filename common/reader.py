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
            input_file = codecs.open(path, 'rb', encoding='utf-8')
            data = input_file.read()
            input_file.close()
            return data
        except IOError, e:
            logging.error("Error at opening file: %s:%s", path, e)
            sys.exit(1)

    @staticmethod
    def get_reader_from_file(path):
        """
        gets a stream of a file 
        @param path: file 
        @return: stream of file
        """
        try:
            return codecs.open(path, encoding='utf-8')
        except IOError, e:
            logging.error("Error at opening file: %s:%s", path, e)
            sys.exit(1)
        return None

    @staticmethod
    def get_data_from_url(url):
        """
        reads from a url

        @param url: url to read
        @return: returns data
        """
        try:
            req = urlopen(url, None, 10)
            return req.read()
        except HTTPError, e:
            logging.error("HTTPError: %s", e)
            sys.exit(1)
        except URLError, e:
            logging.error("URLError: %s", e)
            sys.exit(1)
        except ValueError, e:
            logging.error("ValueError: %s", e)
            sys.exit(1)

    @staticmethod
    def get_data_from_stdin():
        """
        reads from stdin
        @return: data from stdin 
        """
        input_stream = codecs.getreader('utf-8')(sys.stdin)
        data = input_stream.read()
        input_stream.close()
        return data

    @staticmethod
    def get_reader_from_stdin():
        """
        get a utf-8 stream reader for stdin
        @return: stdin-stream
        """
        return codecs.getreader('utf-8')(sys.stdin)
