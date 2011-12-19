import re
import os
from common.memacs import Memacs

class Foo(Memacs):
        
    def _parser_add_arguments(self):
        Memacs._parser_add_arguments(self)
        # add additional arguments 
        
#        self._parser.add_argument("-f", "--folder", dest="filenametimestamps_folder", action="append", \
#                        help="path to a folder to search for filenametimestamps, " + 
#                        "multiple folders can be specified: -f /path1 -f /path2")
    
    
    def _parser_parse_args(self):
        Memacs._parser_parse_args(self)
        # parse additional modules
    
    def _main(self):
        # do all the stupff 
        self._writer.write_org_subitem("foo")
        self._writer.write_org_subitem("bar")