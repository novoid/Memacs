#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-19 15:13:31 aw>

import logging
import traceback
from common.argparser import MemacsArgumentParser
from common.orgwriter import OrgOutputWriter
from common.loggingsettings import handle_logging
import sys

class Memacs(object):
    
    def __init__(self
                 , prog_version
                 , prog_version_date
                 , prog_description
                 , prog_short_description
                 , prog_tag
                 , argv = sys.argv
                 , write_footer=False
                 ):
        self.__prog_version = prog_version
        self.__prog_version_date = prog_version_date
        self.__prog_description = prog_description
        self.__prog_short_description = prog_short_description
        self.__prog_tag = prog_tag
        self.__write_footer = write_footer
        self.__argv = argv
    def __init(self):
        self._parser = MemacsArgumentParser(prog_version=self.__prog_version,
                                  prog_version_date=self.__prog_version_date,
                                  prog_description=self.__prog_description,
                                  )
        # add additional arguments
        self._parser_add_arguments()
        # parse all arguments
        self._parser_parse_args()
        # set logging configuration
        handle_logging(self._args.verbose, self._args.suppressmessages, self._args.outputfile)
        
        logging.debug("args specified:") 
        logging.debug(self._args)
        
        self._writer = OrgOutputWriter(file_name=self._args.outputfile,
                                      short_description=self.__prog_short_description,
                                      tag=self.__prog_tag);
    def __main(self):
        pass
    
    def _parser_add_arguments(self):
        """
        does nothing in super class,
        In subclass we add arguments to the parser 
        """
        pass
    
    def _parser_parse_args(self):
        """
        In subclass we do additional parsing on arguments
        """
        self._args = self._parser.parse_args(self.__argv[1:]) 
        
    #__parser_add_arguments = _parser_add_arguments
    #__parser_parse_args = parser_parse_args
    
    def handle_main(self):    
        try:
            self.__init()
            self._main()
            self._writer.close(self.__write_footer)
        except KeyboardInterrupt:
            logging.info("Received KeyboardInterrupt")
        except SystemExit:
            # if we get an sys.exit() do exit!
            pass
        except:
            error_lines = traceback.format_exc().splitlines()
            logging.error("\n   ".join(map(str, error_lines)))
            raise # re raise exception   
