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
"""


class Commit(object):
    """
    class for representing one commit
    """

    def __init__(self):
        """
        Ctor
        """
        self.__subject = ""
        self.__body = ""
        self.__properties = OrgProperties()
        self.__datetime = ""

    def __set_created(self, line):
        """
        extracts the date + time from line:
        author Forename Lastname <mail> 1234567890 +0000
        @param line
        """
        date_info = line[-16:]  # 1234567890 +0000
        seconds_since_epoch = float(date_info[:10])
        timezone_info = date_info[11:]
        #os.environ['tz'] = timezone_info
        self.__datetime = OrgFormat.datetime(
                            time.localtime(seconds_since_epoch))
        self.__author = line[7:line.find("<")].strip()
        self.__properties.add_property("CREATED", self.__datetime)

    def add_header(self, line):
        """
        adds line to the header

        if line contains "author" this method
        calls self.__set_created(line)
        for setting right author + datetime created

        every line will be added as property
        i.e:
        commit <hashtag>
        would then be following property:
        :COMMIT: <hashtag>
        @param line:
        """
        whitespace = line.find(" ")
        tag = line[:whitespace].upper()
        value = line[whitespace:]
        self.__properties.add_property(tag, value)
        if tag == "AUTHOR":
            self.__set_created(line)

    def add_body(self, line):
        """
        adds a line to the body

        if line starts with Signed-off-by,
        also a property of that line is added
        """
        line = line.strip()
        if line != "":
            if line[:14] == "Signed-off-by:":
                self.__properties.add_property("SIGNED-OFF-BY", line[15:])
            elif self.__subject == "":
                self.__subject = line
            else:
                self.__body += line + "\n"

    def get_output(self):
        """
        @return tupel: output,properties,body for Orgwriter.write_sub_item()
        """
        output = self.__author + ": " + self.__subject
        return output, self.__properties, self.__body


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

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if not self._args.gitrevfile:
            self._parser.error("no input file specified")
        if not os.path.exists(self._args.gitrevfile) or not \
            os.access(self._args.gitrevfile, os.R_OK):
            self._parser.error("input file not found or not readable")

    def _main(self):
        """
        get's automatically called from Memacs class
        read the lines from git-rev-list file,parse and write them to org file
        """

        # read file
        file = codecs.open(self._args.gitrevfile)
        data = file.read()
        file.close()

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
        # author Armin Wieser <armin.wieser@gmail.com> 1324422878 +0100
        # committer Armin Wieser <armin.wieser@gmail.com> 1324422878 +0100
        #
        #     PEP8
        #     Signed-off-by: Armin Wieser <armin.wieser@gmail.com>

        in_header = True
        in_body = False
        commit = Commit()
        commits = []

        for line in data.splitlines():
            if line == "" and in_header:
                in_header = False
                in_body = True
            elif line == "" and in_body:
                in_header = True
                in_body = False
                commits.append(commit)
                commit = Commit()
            elif in_body:
                commit.add_body(line)
            elif in_header:
                commit.add_header(line)

        logging.debug("got %d commits", len(commits))

        # time to write all commits to org-file
        for commit in commits:
            output, properties, note = commit.get_output()

            self._writer.write_org_subitem(output=output,
                                           properties=properties,
                                           note=note)

if __name__ == "__main__":
    memacs = GitMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG)
    memacs.handle_main()
