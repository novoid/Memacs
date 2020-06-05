#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-11-06 15:23:39 vk>

import logging
import os
import sys
import time

from orgformat import OrgFormat

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties


class Commit(object):
    """
    class for representing one commit
    """

    def __init__(self):
        """
        Ctor
        """
        self.__empty = True
        self.__subject = ""
        self.__body = ""
        self.__timestamp = ""
        self.__author = ""
        self.__properties = OrgProperties()

    def __set_author_timestamp(self, line):
        """
        extracts the date + time from line:
        author Forename Lastname <mail> 1234567890 +0000
        @param line
        """
        self.__empty = False
        date_info = line[-16:]  # 1234567890 +0000
        seconds_since_epoch = float(date_info[:10])
        #timezone_info = date_info[11:]
        self.__timestamp = OrgFormat.date(
                            time.localtime(seconds_since_epoch), show_time=True)
        self.__author = line[7:line.find("<")].strip()

    def add_header(self, line):
        """
        adds line to the header

        if line contains "author" this method
        calls self.__set_author_timestamp(line)
        for setting right author + datetime created

        every line will be added as property
        i.e:
        commit <hashtag>
        would then be following property:
        :COMMIT: <hashtag>
        @param line:
        """
        self.__empty = False

        if line != "":
            whitespace = line.find(" ")
            tag = line[:whitespace].upper()
            value = line[whitespace:]
            self.__properties.add(tag, value)

            if tag == "AUTHOR":
                self.__set_author_timestamp(line)

    def add_body(self, line):
        """
        adds a line to the body

        if line starts with Signed-off-by,
        also a property of that line is added
        """

        line = line.strip()
        if line != "":
            if line[:14] == "Signed-off-by:":
                self.__properties.add("SIGNED-OFF-BY", line[15:])
            elif self.__subject == "":
                self.__subject = line
            else:
                self.__body += line + "\n"

    def is_empty(self):
        """
        @return: True  - empty commit
                 False - not empty commit
        """
        return self.__empty

    def get_output(self):
        """
        @return tuple: output,properties,body for Orgwriter.write_sub_item()
        """
        output = self.__author + ": " + self.__subject
        return output, self.__properties, self.__body, self.__author, \
                self.__timestamp


class GitMemacs(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
           "-f", "--file", dest="gitrevfile",
           action="store",
           help="path to a an file which contains output from " + \
           " following git command: git rev-list --all --pretty=raw")

        self._parser.add_argument(
           "-g", "--grep-user", dest="grepuser",
           action="store",
           help="if you wanna parse only commit from a specific person. " + \
           "format:<Forname Lastname> of user to grep")

        self._parser.add_argument(
           "-e", "--encoding", dest="encoding",
           action="store",
           help="default encoding utf-8, see " + \
           "http://docs.python.org/library/codecs.html#standard-encodings" + \
           "for possible encodings")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if self._args.gitrevfile and not \
                (os.path.exists(self._args.gitrevfile) or \
                     os.access(self._args.gitrevfile, os.R_OK)):
            self._parser.error("input file not found or not readable")

        if not self._args.encoding:
            self._args.encoding = "utf-8"

    def get_line_from_stream(self, input_stream):
        try:
            return input_stream.readline()
        except UnicodeError as e:
            logging.error("Can't decode to encoding %s, " + \
                          "use argument -e or --encoding see help",
                          self._args.encoding)
            sys.exit(1)

    def _main(self):
        """
        get's automatically called from Memacs class
        read the lines from git-rev-list file,parse and write them to org file
        """

        # read file
        if self._args.gitrevfile:
            logging.debug("using as %s input_stream",
                          self._args.gitrevfile)
            input_stream = open(self._args.gitrevfile)
        else:
            logging.debug("using sys.stdin as input_stream")
            input_stream = sys.stdin

        # now go through the file
        # Logic (see example commit below)
        # first we are in an header and not in an body
        # every newline toggles output
        # if we are in body then add the body to commit class
        # if we are in header then add the header to commit class
        #
        # commit 6fb35035c5fa7ead66901073413a42742a323e89
        # tree 7027c628031b3ad07ad5401991f5a12aead8237a
        # parent 05ba138e6aa1481db2c815ddd2acb52d3597852f
        # author Armin Wieser <armin.wieser@example.com> 1324422878 +0100
        # committer Armin Wieser <armin.wieser@example.com> 1324422878 +0100
        #
        #     PEP8
        #     Signed-off-by: Armin Wieser <armin.wieser@gmail.com>

        was_in_body = False
        commit = Commit()
        commits = []

        line = self.get_line_from_stream(input_stream)

        while line:
            line = line.rstrip()  # removing \n
            logging.debug("got line: %s", line)
            if line.strip() == "" or len(line) != len(line.lstrip()):
                commit.add_body(line)
                was_in_body = True
            else:
                if was_in_body:
                    commits.append(commit)
                    commit = Commit()
                commit.add_header(line)
                was_in_body = False

            line = self.get_line_from_stream(input_stream)

        # adding last commit
        if not commit.is_empty():
            commits.append(commit)

        logging.debug("got %d commits", len(commits))
        if len(commits) == 0:
            logging.error("Is there an error? Because i found no commits.")

        # time to write all commits to org-file
        for commit in commits:
            output, properties, note, author, timestamp = commit.get_output()

            if not(self._args.grepuser) or \
            (self._args.grepuser and self._args.grepuser == author):
                # only write to stream if
                # * grepuser is not set or
                # * grepuser is set and we got an entry with the right author
                self._writer.write_org_subitem(output=output,
                                               timestamp=timestamp,
                                               properties=properties,
                                               note=note)

        if self._args.gitrevfile:
            input_stream.close()
