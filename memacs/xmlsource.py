#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-10-26 18:21:26 armin>

import re
import os
import sys
import time
import xml.sax
import logging
import ConfigParser
from lib.memacs import Memacs
from lib.orgformat import OrgFormat
from lib.reader import CommonReader
from lib.orgproperty import OrgProperties
from xml.sax._exceptions import SAXParseException
from email.utils import parsedate


class XmlSaxHandler(xml.sax.handler.ContentHandler):
    """
    Sax handler for diverse xml's:
    """

    def __init__(self, writer, paras, split):
        """
        Ctor

        @param writer: orgwriter
        """
        self._writer = writer
        self.__split = split
        self.__timestamp = paras[0]
        self.__output = paras[1]
        self.__note = paras[2]
        self.__properties = paras[3]
        self.__tags = paras[4]
        self.__end = paras[5]
        self.__time = paras[6]
        self.__attimestamp = paras[7]
        self.__atoutput = paras[8]
        self.__atnote = paras[9]
        self.__atproperties = paras[10]
        self.__attags = paras[11]
        self.__reset()

    def __reset(self):
        """
        resets all variables
        """
        self.__author = ""
        self.__date = ""
        self.__msg = ""
        self.__notes = ""
        self.__taging = ""
        self.__on_node_name = ""
        self.__attroutput = ""
        self.__attrnote = ""
        self.__attrtags = ""
        self.__attrproperties = ""
        self.__attrtime = ""

    def characters(self, content):
        """
        handles xml tags that are specified in xml.ini
        """
        logging.debug("Handler @characters @%s , content=%s",
                      self.__on_node_name, content)

        if (self.__output
            and self.__on_node_name == self.__output):
            self.__author += content
        elif (self.__timestamp
              and self.__on_node_name == self.__timestamp):
            self.__date += content
        elif (self.__properties
              and self.__on_node_name == self.__properties):
            self.__msg += content
        elif (self.__note
              and self.__on_node_name == self.__note):
            self.__notes += content
        elif (self.__tags
              and self.__on_node_name == self.__tags):
            self.__taging += content

    def startElement(self, name, attrs):
        """
        at every <tag> remember the tagname

        read nodes that are specified in xml.ini
        """
        logging.debug("Handler @startElement name=%s,attrs=%s", name, attrs)

        if name == self.__output:
            if self.__atoutput:
                for item in self.__atoutput:
                    self.__attroutput = self.__attroutput + \
                                        + ' ' + attrs.get(item, "")
        elif name == self.__timestamp:
            if self.__attimestamp:
                for item in self.__attimestamp:
                    self.__attrtime = self.__attrtime + attrs.get(item, "")
        elif name == self.__note:
            if self.__atnote:
                for item in self.__atnote:
                    self.__attrnote = self.__attrnote + \
                                      + ' ' + attrs.get(item, "")
        elif name == self.__tags:
            if self.__attags:
                for item in self.__attags:
                    self.__attrtags = self.__attrtags + \
                                      + ' ' + attrs.get(item, "")
        elif name == self.__properties:
            if self.__atproperties:
                for item in self.__atproperties:
                    self.__attrproperties = self.__attrproperties + \
                                            + ' ' + attrs.get(item, "")

        self.__on_node_name = name

    def endElement(self, name):
        """
        at every </tag> clear the remembered tagname

        if we are at end tag that is specified in xml.ini
        we write all defined tags and attributes to output-file
        with __write function
        """
        logging.debug("Handler @endElement name=%s", name)
        self.__on_node_name = ""

        if name == self.__end:
            self.__write()
            self.__reset()

    def __write(self):
        """
        write attributes to writer (make an org_sub_item)
        """
        logging.debug("msg:%s", self.__msg)

        #getting tags
        if self.__attrtags:
            tags = self.__attrtags
            if self.__split:
                tags = tags.split(self.__split)
            else:
                tags = tags.split(' ')
            tags = tags[1:]
        elif self.__taging:
            tags = self.__taging
            if self.__split:
                tags = tags.split(self.__split)
            else:
                tags = tags.split(' ')
        else:
            tags = []
        for item in tags:
            if item == '':
                tags.remove(item)

        #getting output
        if not self.__attroutput:
            output = "%s: %s" % (self.__author, self.__msg)
        else:
            output = self.__attroutput

        part = output.split(" ")
        output = ""
        for item in part:
            if re.search("http[s]?://", item) != None:
                unformatted_link = item
                short_link = OrgFormat.link(unformatted_link, "link")
                output = output + " " + short_link + ": " + item
            else:
                output = output + " " + item
        output = output[1:]

        #getting properties
        if not self.__attrproperties:
            properties = OrgProperties(data_for_hashing=self.__author \
                                       + self.__msg + self.__date)
        else:
            properties = OrgProperties(data_for_hashing=self.__attrproperties)

        #getting notes
        if self.__attrnote:
            notes = self.__attrnote
        elif self.__notes:
            notes = self.__notes
        else:
            notes = ""

        if notes:
            parts = notes.split(" ")
            notes = ""
            for item in parts:
                if re.search("http[s]?://", item) != None:
                    unformatted_link = item
                    short_link = OrgFormat.link(unformatted_link,
                                                "link")
                    notes = notes + " " + short_link + ": " + item
                else:
                    notes = notes + " " + item
            notes = notes[1:]

        #prepare for most time formats + getting timestamp
        if self.__attrtime:
            self.__date = self.attrtime

        try:
            if (self.__time == 'YYYYMMDD' or self.__time == 'YYYY'
                or self.__time == 'YYYYMMDDTHHMMSSZ'
                or self.__time == 'YYYYMMDDTHHMMSST'):
                timestamp = OrgFormat.datetime(
                                      OrgFormat.datetupelutctimestamp(
                                      self.__date))
            elif (self.__time == ('YYYY-MM-DD')):
                timestamp = OrgFormat.datetime(
                                      OrgFormat.datetupeliso8601(
                                      self.__date))
            elif (self.__time == 'YYYY-MM-DDTHH.MM.SS' or
                  self.__time == 'YYYY-MM-DDTHH.MM'):
                timestamp = OrgFormat.datetime(
                                      OrgFormat.datetimetupeliso8601(
                                      self.__date))
            elif (self.__time == 'timetuple'):
                time_tupel = time.localtime(time.mktime(
                                            parsedate(self.__date)))
                timestamp = OrgFormat.datetime(time_tupel)

        except:
                logging.debug("Write functione @timestamp timestamp=%s",
                              self.__date)
                logging.error("A timestamp problem occured")
                sys.exit(2)
        self._writer.write_org_subitem(output=output,
                                       timestamp=timestamp,
                                       note=notes,
                                       tags=tags,
                                       properties=properties)


class XmlMemacs(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
           "-u", "--url", dest="url",
           action="store",
           help="url to xml file")

        self._parser.add_argument(
           "-f", "--file", dest="file",
           action="store",
           help="path to xml file")

        self._parser.add_argument(
           "-i", "--ini", dest="ini",
           action="store",
           help="path to xml config file")

        self._parser.add_argument(
           "-co", "--section", dest="section",
           action="store",
           help="section of config file")

        self._parser.add_argument(
           "-de", "--delimiter", dest="splitcriterion",
           action="store",
           help="you can set this to specify a " +
                "splitting-criterion for tags(" " is default")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if self._args.url and self._args.file:
            self._parser.error("you cannot set both url and file")
        if not self._args.url and not self._args.file:
            self._parser.error("please specify a file or url")
        if self._args.url and not self._args.ini:
            self.parser.error("please specify the xml.ini file")
        if self._args.file and not self._args.ini:
            self.parser.error("please specify the xml.ini file")
        if self._args.file and not (os.path.exists
                                        (self._args.file) or \
            os.access(self._args.file, os.R_OK)):
            self._parser.error("file not found or not readable")
        if self._args.ini and not (os.path.exists
                                        (self._args.ini) or \
            os.access(self._args.ini, os.R_OK)):
            self._parser.error("config file not found or not readable")

    def _main(self):
        """
        get's automatically called from Memacs class
        """
        if self._args.file:
            data = CommonReader.get_data_from_file(self._args.file)
        elif self._args.url:
            data = CommonReader.get_data_from_url(self._args.url)

        section = self._args.section
        conf = self._args.ini
        self.__get_data_of_conf(section, conf)
        split = self._args.splitcriterion

        data = data.decode("utf-8", "replace")
        try:
            xml.sax.parseString(data.encode('utf-8'),
                                XmlSaxHandler(self._writer,
                                              self.__paras,
                                              split))

        except SAXParseException:
            logging.error("No correct XML given")
            sys.exit(1)

    def __read_config_section(self, conf, section):
        """
        reads defined section of config file
        """
        para = {}
        try:
            options = conf.options(section)
        except:
            logging.error("Section does not exist")
            sys.exit(2)
        for item in options:
            try:
                para[item] = conf.get(section, item)
            except:
                para[item] = None
        return para

    def __get_data_of_conf(self, section, conf):
        '''
        reads the nodes and attributes that
        are defined in specified section of xml.ini
        '''
        config = ConfigParser.ConfigParser()
        config.read(conf)
        sectioncount = len(config.sections()) - 1
        sectionnumber = int(section)

        if (sectioncount < sectionnumber):
            section = []

        if not section:
            logging.error("Section does not exist")
            sys.exit(2)
        else:
            section = 'Section' + section

        self.__paras = []
        self.__paras.append(self.__read_config_section(config,
                                                       section)['timestamp'])
        self.__paras.append(self.__read_config_section(config,
                                                       section)['output'])
        self.__paras.append(self.__read_config_section(config,
                                                       section)['note'])
        self.__paras.append(self.__read_config_section(config,
                                                       section)['properties'])
        self.__paras.append(self.__read_config_section(config,
                                                       section)['tags'])
        self.__paras.append(self.__read_config_section(config,
                                                       section)['end'])
        self.__paras.append(self.__read_config_section(config,
                                                       section)['timevalue'])
        attimestamp = self.__read_config_section(config,
                                                 section)['attimestamp']
        atoutput = self.__read_config_section(config,
                                              section)['atoutput']
        atnote = self.__read_config_section(config,
                                            section)['atnote']
        atproperties = self.__read_config_section(config,
                                                  section)['atproperties']
        attags = self.__read_config_section(config,
                                            section)['attags']

        if attimestamp:
            self.__paras.append(attimestamp.split(','))
        else:
            self.__paras.append(None)
        if atoutput:
            self.__paras.append(atoutput.split(','))
        else:
            self.__paras.append(None)
        if atnote:
            self.__paras.append(atnote.split(','))
        else:
            self.__paras.append(None)
        if atproperties:
            self.__paras.append(atproperties.split(','))
        else:
            self.__paras.append(None)
        if attags:
            self.__paras.append(attags.split(','))
        else:
            self.__paras.append(None)

        if not self.__paras[6] in ('YYYYMMDD', 'YYYYMMDDTHHMMSSZ',
                                   'YYYY-MM-DD', 'YYYYMMDDTHHMMSST',
                                   'YYYY-MM-DDTHH.MM.SS', 'YYYY',
                                   'YYYY-MM-DDTHH.MM', 'timetuple'):
            logging.error("No correct timevalue given")
            sys.exit(2)
