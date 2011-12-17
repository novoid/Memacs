#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-27 15:13:31 aw>

from argparse import ArgumentParser

EPILOG=""":copyright: (c) 2011 by Karl Voit <tools@Karl-Voit.at>
:license: GPL v2 or any later version
:bugreports: <tools@Karl-Voit.at>
:version: """
class MemacsArgumentParser(ArgumentParser):
    
    def __init__(self,prog_version,prog_version_date,description):
        version="%prog v" +prog_version + " from " + prog_version_date 
        
        ArgumentParser.__init__(self,
                              description=description,
                              add_help=True,
                              epilog=EPILOG + prog_version + " from "+prog_version_date + "\n")
     
        self.add_argument('--version', action='version', version=version)
        
        self.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                          help="enable verbose mode")
        self.add_argument("-o", "--output", dest="outputfile",
                          help="Org-mode file that will be generated (see above)." +\
                         "If no output file is given, result gets printed to stdout",
                         metavar="FILE")
        
    def format_epilog(self,formatter):
        """
        overwriting OptionParser's format_epilog for correct formatting of \n
        """
        return "\n" + self.epilog
    
    def format_description(self,formatter):
        """
        overwriting OptionParser's format_description for correct formatting of \n
        """
        return self.description
    
    def get_version(self):
        return self.version