#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import sys
import os
import logging
import time
import codecs
import xml.sax
# needed to import common.*
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.orgproperty import OrgProperties
from common.orgformat import OrgFormat
from common.memacs import Memacs
from common.reader import CommonReader


PROG_VERSION_NUMBER = u"0.0"
PROG_VERSION_DATE = u"2011-12-18"
PROG_SHORT_DESCRIPTION = u"Memacs for svn"
PROG_TAG = u"mytag"
PROG_DESCRIPTION = u"""
this class will do 
TODO
TODO
TODO

Then an Org-mode file is generated that contains ....
"""


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
    
    def __init__(self, writer):
        self.__reset()
        self._writer = writer
        
    def __reset(self):
        self.__author = ""
        self.__date = ""
        self.__msg = ""
        self.__rev = -1
        self.__on_node_name = ""  # used to store on which element we are
        
    def __write(self):
        logging.debug("msg:%s",self.__msg)
        self.__msg = self.__msg.splitlines()
        subject = ""
        notes = ""
        if len(self.__msg) > 0 :
            start_notes = 0
            for i in range(len(self.__msg)):
                if self.__msg[i].strip() != "":
                    subject = self.__msg[i].strip()
                    start_notes = i+1
                    break
                    
            if len(self.__msg) > start_notes:
                for n in self.__msg[start_notes:]:
                    if n != "": 
                        notes += n + "\n"
        
        output = "%s (r%d): %s" % (self.__author, self.__rev, subject)

        properties = OrgProperties()
        dt = OrgFormat.datetime(OrgFormat.datetupelutctimestamp(self.__date))
        properties.add("CREATED", dt)
        
        self._writer.write_org_subitem(output=output,
                                       note=notes,
                                       properties=properties)
    
    def startDocument(self):
        logging.debug("Handler @startDocument")
    
    def startElementNS(self, name, qname, attrs):
        logging.debug("Handler @startElementNS")
        print name, qname 
    
    def characters(self, content):
        logging.debug("Handler @characters @%s , content=%s", self.__on_node_name, content)
        if self.__on_node_name == "author":
            self.__author += content
        elif self.__on_node_name == "date":
            self.__date += content
        elif self.__on_node_name == "msg":
            self.__msg += content    

    def startElement(self, name, attrs):
        logging.debug("Handler @startElement name=%s,attrs=%s", name, attrs)
        
        if name == "logentry":
            self.__rev = int(attrs['revision'])
        
        self.__on_node_name = name
        
    
    def endElement(self, name):
        logging.debug("Handler @endElement name=%s", name)
        self.__on_node_name = ""
        if name == "logentry":
            self.__write()
            self.__reset()
            
    
        
    def endDocument(self):
        logging.debug("Handler @endDocument")
        pass



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
            logging.info("ATTENTION: Using stdin as input_stream")
            data = CommonReader.get_data_from_stdin()

        xml.sax.parseString(data.encode('utf-8'), SvnSaxHandler(self._writer))


if __name__ == "__main__":
    memacs = SvnMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG)
    memacs.handle_main()
