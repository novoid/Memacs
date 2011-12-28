#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-20 15:13:31 aw>

import sys
import os
import logging
import time
import codecs
# needed to import common.*
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.orgproperty import OrgProperties
from common.orgformat import OrgFormat
from common.memacs import Memacs


PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2011-12-20"
PROG_SHORT_DESCRIPTION = u"Memacs for git files "
PROG_TAG = u"git"
PROG_DESCRIPTION = u"""
This class will parse files from git rev-parse output

use following command to generate input file
$ git rev-list --all --pretty=raw > /path/to/input file

Then an Org-mode file is generated that contains all commit message

If outputfile is specified, only non-existing commits are appended
"""
COPYRIGHT_YEAR = "2011-2012"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""

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
        self.__timestamp = OrgFormat.datetime(
                            time.localtime(seconds_since_epoch))
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
        @return tupel: output,properties,body for Orgwriter.write_sub_item()
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

    def _main(self):
        """
        get's automatically called from Memacs class
        read the lines from git-rev-list file,parse and write them to org file
        """

        # read file
        if self._args.gitrevfile:
            logging.debug("using as %s input_stream", self._args.gitrevfile)
            input_stream = codecs.open(self._args.gitrevfile, encoding='utf-8')
        else:
            logging.debug("using sys.stdin as input_stream")
            input_stream = codecs.getreader('utf-8')(sys.stdin)

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

        line = input_stream.readline()

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

            line = input_stream.readline()

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

if __name__ == "__main__":
    memacs = GitMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS
        )
    memacs.handle_main()
