# -*- coding: utf-8 -*-
# Time-stamp: <2012-01-02 21:23:13 armin>

import codecs
import logging
import sys
import csv
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
        except Exception, e:
            logging.error("Exception: %s", e)
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


class UTF8Recoder:
    """
    from http://docs.python.org/library/csv.html
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeCsvReader:
    """
    from http://docs.python.org/library/csv.html

    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, delimiter=";", encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, delimiter=delimiter, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self
