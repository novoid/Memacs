#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-30 15:43:15 daniel>
import time
import os.path
import logging
from email.utils import parsedate
from lib.orgformat import OrgFormat
from lib.memacs import Memacs
from lib.reader import CommonReader
from lib.orgproperty import OrgProperties

from ConfigParser import SafeConfigParser


class TagstoreMemacs(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)
        self._parser.add_argument(
           "-f", "--store_file",
           dest="store_file",
           help="path to store.tgs file"
                "path/to/store.tgs")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if not self._args.store_file:
            self._parser.error("please specify the path to "
                               "store.tgs")           
        if not (os.path.exists(self._args.store_file) or \
            os.access(self._args.store_file, os.R_OK)):
            self._parser.error("path not found")
            
    
    def __read_store_and_write(self, store_file):     
        """
        Reads needed infos of .tagstore/store.tgs,
        parse the infos,
        write to outputfile

        @param store_file: string contains the input from store.tgs
        """
          
        parser = SafeConfigParser()
        parser.read(store_file)
        sections =  parser.sections()
        options = parser.options(sections[1])
        
        for i in range(0,len(options),3): 
            filename = options[i].split('\\')
            
            filename = filename[0]
            tags = parser.get(sections[1],options[i])
            timestamp = parser.get(sections[1],options[i+1])
            category = parser.get(sections[1],options[i+2])
                  
            tags = tags.replace('"','')
            tags = tags.replace(' ','_')
            tags = tags.replace(':','_')
            category = category.replace('"','')
            category = category.replace(' ','_')
            category = category.replace(':','_')
            tags = tags.split(",")
            category = category.split(",")
            timestamp = timestamp[0:16]
            tagstoring = []
            
            tagstoring.extend(tags)
            tagstoring.extend(category)
            
            x = 0
            while x < len(tagstoring):
                if tagstoring[x] == '':
                    tagstoring.pop(x)
                else:
                    y = x + 1
                    while y < len(tagstoring):
                        if tagstoring[x] == tagstoring[y]:
                            tagstoring.pop(y)
                        else:      
                            y = y + 1
                    x = x + 1

            timestamp = OrgFormat.strdatetime(timestamp)   
            output = filename.decode("utf-8","replace")
            data_for_hashing = output.decode("utf-8","replace") 
            properties = OrgProperties(data_for_hashing=data_for_hashing)
            self._writer.write_org_subitem(timestamp=timestamp,
                                           output=output,
                                           tags=tagstoring,
                                           properties=properties
                                           )
            
            


    def _main(self):
        """
        get's automatically called from Memacs class
        """
        if self._args.store_file:
            self.__read_store_and_write(self._args.store_file)
            