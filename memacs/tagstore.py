#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2012-03-30 15:43:15 daniel>

import os.path
from lib.memacs import Memacs
from lib.reader import CommonReader
from lib.orgproperty import OrgProperties


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

        store_data = store_file.split('\n')
        del store_data[len(store_data)-1]
        pars_count = 0
        for data_part in store_data:
            data = data_part.split('\\')
            
            if pars_count == 0:
                output = data[0]      
                tags = data[1][5:]
                pars_count += 1
            elif pars_count == 1:
                timestamp = data[1][10:]
                pars_count += 1
            else:
                category = data[1][10:]
                category = category.replace('"', "")
                pars_count = 0;
                output = output.decode("utf-8","replace")
                data_for_hashing = output.decode("utf-8","replace") 
                properties = OrgProperties(data_for_hashing=data_for_hashing) 
                
                if len(tags) >= len(category):                 
                    tags = tags.split(",")
                else:
                    tags = category.split(",")    
                    
                self._writer.write_org_subitem(timestamp=timestamp,
                                               output=output,
                                               tags=tags,
                                               properties=properties,
                                               )
                
    def _main(self):
        """
        get's automatically called from Memacs class
        """
        if self._args.store_file:
            data = CommonReader.get_data_from_file(self._args.store_file)
            data = data.decode("utf-8","replace")
            data = data.encode("utf-8")
            self.__read_store_and_write(data)
            