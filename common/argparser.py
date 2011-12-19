# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-19 15:13:31 aw>

from argparse import ArgumentParser
import os

EPILOG=""":copyright: (c) 2011 by Karl Voit <tools@Karl-Voit.at>
:license: GPL v2 or any later version
:bugreports: <tools@Karl-Voit.at>
:version: """
class MemacsArgumentParser(ArgumentParser):
    
    def __init__(self,prog_version,prog_version_date,prog_description):
        version="%(prog)s v" +prog_version + " from " + prog_version_date 
        
        ArgumentParser.__init__(self,
                              description=prog_description,
                              add_help=True,
                              epilog=EPILOG + prog_version + " from "+prog_version_date + "\n",
                              )
     
        self.add_argument('--version', action='version', version=version)
        
        self.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="enable verbose mode")
        
        self.add_argument("-s", "--suppress-messages", dest="suppressmessages", action="store_true",
                          help="do not show any log message - helpful when -o not set")
        
        self.add_argument("-o", "--output", dest="outputfile",
                          help="Org-mode file that will be generated (see above)." +\
                         "If no output file is given, result gets printed to stdout",
                         metavar="FILE")
        
    def format_epilog(self,formatter):
        """
        overwriting ArgParser's format_epilog for correct formatting of \n
        """
        return "\n" + self.epilog
    
    def format_description(self,formatter):
        """
        overwriting ArgParser's format_description for correct formatting of \n
        """
        return self.description
    
    def get_version(self):
        return self.version
    
    def parse_args(self, args=None, namespace=None):
        """
        overwriting ArgParser's parse_args and do checking default argument outputfile
        """
        args = ArgumentParser.parse_args(self, args=args, namespace=namespace)
        if args.outputfile:
            if not os.path.exists(os.path.dirname(args.outputfile)):
                self.error("Output file path(%s) does not exist!" % args.outputfile)
            if os.access(args.outputfile, os.W_OK):
                self.error("Output file %s is not writeable!" % args.outputfile)
            
        if args.suppressmessages == True and args.verbose == True:
            self.error("cannot set both verbose and suppress-messages")
        return args
        