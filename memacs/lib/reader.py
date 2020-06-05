# -*- coding: utf-8 -*-
# Time-stamp: <2012-05-24 19:08:10 armin>

import codecs
import csv
import logging
import sys
from collections import OrderedDict
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen


class CommonReader:
    """
    Class for reading
    * files
    * url's
    """

    @staticmethod
    def get_data_from_file(path, encoding='utf-8'):
        """
        reads a file

        @param file: path to file
        @return: returns data
        """
        try:
            input_file = codecs.open(path, 'rb', encoding=encoding)
            data = input_file.read()
            input_file.close()
            return data
        except IOError as e:
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
        except IOError as e:
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
        except HTTPError as e:
            logging.error("HTTPError: %s", e)
            sys.exit(1)
        except URLError as e:
            logging.error("URLError: %s", e)
            sys.exit(1)
        except ValueError as e:
            logging.error("ValueError: %s", e)
            sys.exit(1)
        except Exception as e:
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

    def __next__(self):
        return next(self.reader)


class UnicodeCsvReader:
    """
    from http://docs.python.org/library/csv.html

    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, delimiter=";", encoding="utf-8", **kwds):
        # f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, delimiter=delimiter, **kwds)

    def __next__(self):
        row = next(self.reader)
        return [str(s) for s in row]

    def __iter__(self):
        return self


class UnicodeDictReader:
    """
    from http://stackoverflow.com/questions/19740385/dictreader-and-unicodeerror

    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, delimiter=";", encoding="utf-8", fieldnames=None, **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.DictReader(f, delimiter=delimiter, fieldnames=fieldnames, **kwds)

    def __next__(self):
        row = next(self.reader)
        return OrderedDict((k.lower(), row[k]) for k in self.reader.fieldnames)

    def __iter__(self):
        return self

