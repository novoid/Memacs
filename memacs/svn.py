#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2019-11-06 15:28:04 vk>

import logging
import os
import sys
import xml.sax

from orgformat import OrgFormat
from xml.sax._exceptions import SAXParseException

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties
from memacs.lib.reader import CommonReader


class SvnSaxHandler(xml.sax.handler.ContentHandler):
    """
    Sax handler for following xml's:

    <?xml version="1.0"?>
    <log>
    <logentry
       revision="13">
    <author>bob</author>
    <date>2011-11-05T18:18:22.936127Z</date>
    <msg>Bugfix.</msg>
    </logentry>
    </log>
    """

    def __init__(self, writer, grepauthor):
        """
        Ctor

        @param writer: orgwriter
        """
        self.__reset()
        self._writer = writer
        self.__grepauthor = grepauthor

    def __reset(self):
        """
        resets all variables
        """
        self.__author = ""
        self.__date = ""
        self.__msg = ""
        self.__rev = -1
        self.__on_node_name = ""  # used to store on which element we are
        self.__id_prefix = "rev-"

    def __write(self):
        """
        write attributes to writer (make an org_sub_item)
        """
        logging.debug("msg:%s", self.__msg)
        self.__msg = self.__msg.splitlines()
        subject = ""
        notes = ""

        # idea: look for the first -nonempty- message
        if len(self.__msg) > 0:
            start_notes = 0
            for i in range(len(self.__msg)):
                if self.__msg[i].strip() != "":
                    subject = self.__msg[i].strip()
                    start_notes = i + 1
                    break

            if len(self.__msg) > start_notes:
                for n in self.__msg[start_notes:]:
                    if n != "":
                        notes += n + "\n"

        output = "%s (r%d): %s" % (self.__author, self.__rev, subject)

        properties = OrgProperties(data_for_hashing=self.__author + subject)
        timestamp = OrgFormat.date(
            OrgFormat.parse_basic_iso_datetime(self.__date), show_time=True)
        properties.add("REVISION", self.__rev)

        if self.__grepauthor == None or \
        (self.__author.strip() == self.__grepauthor.strip()):
            self._writer.write_org_subitem(output=output,
                                           timestamp=timestamp,
                                           note=notes,
                                           properties=properties)

    def characters(self, content):
        """
        handles xml tags:
        - <author/>
        - <date/>
        - <msg/>

        and set those attributes
        """
        logging.debug("Handler @characters @%s , content=%s",
                      self.__on_node_name, content)
        if self.__on_node_name == "author":
            self.__author += content
        elif self.__on_node_name == "date":
            self.__date += content
        elif self.__on_node_name == "msg":
            self.__msg += content

    def startElement(self, name, attrs):
        """
        at every <tag> remember the tagname
        * sets the revision when in tag "logentry"
        """
        logging.debug("Handler @startElement name=%s,attrs=%s", name, attrs)

        if name == "logentry":
            self.__rev = int(attrs['revision'])

        self.__on_node_name = name

    def endElement(self, name):
        """
        at every </tag> clear the remembered tagname
        if we are at </logentry> then we can write a entry to stream
        """
        logging.debug("Handler @endElement name=%s", name)
        self.__on_node_name = ""
        if name == "logentry":
            self.__write()
            self.__reset()


class SvnMemacs(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
            "-f", "--file", dest="svnlogxmlfile",
            action="store",
            help="path to a an file which contains output from " + \
                " following svn command: svn log --xml")

        self._parser.add_argument(
           "-g", "--grep-author", dest="grepauthor",
           action="store",
           help="if you wanna parse only messages from a specific person. " + \
           "format:<author> of author to grep")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if self._args.svnlogxmlfile and not \
                (os.path.exists(self._args.svnlogxmlfile) or \
                     os.access(self._args.svnlogxmlfile, os.R_OK)):
            self._parser.error("input file not found or not readable")

    def _main(self):
        """
        get's automatically called from Memacs class
        read the lines from svn xml file, parse and write them to org file
        """

        # read file
        if self._args.svnlogxmlfile:
            logging.debug("using as %s input_stream", self._args.svnlogxmlfile)
            data = CommonReader.get_data_from_file(self._args.svnlogxmlfile)
        else:
            logging.info("Using stdin as input_stream")
            data = CommonReader.get_data_from_stdin()

        try:
            xml.sax.parseString(data.encode('utf-8'),
                                SvnSaxHandler(self._writer,
                                              self._args.grepauthor))
        except SAXParseException:
            logging.error("No correct XML given")
            sys.exit(1)
