# -*- coding: utf-8 -*-
# Time-stamp: <2014-01-28 16:17:20 vk>

import os
import re
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter


class MemacsArgumentParser(ArgumentParser):
    """
    Inherited from Argumentparser

    MemacsArgumentParser handles default arguments which are needed for every
    Memacs module and gives a nicer output for help message.
    """

    def __init__(self,
                 prog_version,
                 prog_version_date,
                 prog_description,
                 copyright_year,
                 copyright_authors,
                 use_config_parser_name=""
                 ):

        self.__version = "%(prog)s v" + prog_version + " from " + \
            prog_version_date

        # format copyright authors:
        # indent from second author
        copyright_authors = copyright_authors.splitlines()
        for i in range(len(copyright_authors)):
            copyright_authors[i] = "            " + copyright_authors[i]
        copyright_authors = "\n".join(map(str, copyright_authors))

        epilog = ":copyright: (c) " + copyright_year + " by \n" + \
        copyright_authors + \
        "\n:license: GPL v2 or any later version\n" + \
        ":bugreports: https://github.com/novoid/Memacs\n" + \
        ":version: " + prog_version + " from " + prog_version_date + "\n"

        self.__use_config_parser_name = use_config_parser_name

        ArgumentParser.__init__(self,
                              description=prog_description,
                              add_help=True,
                              epilog=epilog,
                              formatter_class=RawDescriptionHelpFormatter
                              )
        self.__add_arguments()

    def __add_arguments(self):
        """
        Add's all standard arguments of a Memacs module
        """
        self.add_argument('--version',
                          action='version',
                          version=self.__version)

        self.add_argument("-v", "--verbose",
                          dest="verbose",
                          action="store_true",
                          help="enable verbose mode")

        self.add_argument("-s", "--suppress-messages",
                          dest="suppressmessages",
                          action="store_true",
                          help="do not show any log message " + \
                              "- helpful when -o not set")

        self.add_argument("-o", "--output",
                          dest="outputfile",
                          help="Org-mode file that will be generated " + \
                              " (see above). If no output file is given, " + \
                              "result gets printed to stdout",
                          metavar="FILE")

        self.add_argument("-a", "--append",
                          dest="append",
                          help="""when set and outputfile exists, then
                          only new entries are appendend.
                          criterion: :ID: property""",
                          action="store_true")

        self.add_argument("-t", "--tag",
                          dest="tag",
                          help="overriding tag: :Memacs:<tag>: (on top entry)")

        self.add_argument("--autotagfile",
                          dest="autotagfile",
                          help="file containing autotag information, see " + \
                          "doc file FAQs_and_Best_Practices.org",
                          metavar="FILE")

        self.add_argument("--number-entries",
                          dest="number_entries",
                          help="how many entries should be written?",
                          type=int)

        self.add_argument("--columns-header",
                          dest="columns_header",
                          help="if you want to add an #+COLUMNS header, please specify " + \
                          "its content as STRING",
                          metavar="STRING")

        self.add_argument("--custom-header",
                          dest="custom_header",
                          help="if you want to add an arbitrary header line, please specify " + \
                          "its content as STRING",
                          metavar="STRING")

        self.add_argument("--add-to-time-stamps",
                          dest="timestamp_delta",
                          help="if data is off by, e.g., two hours, you can specify \"+2\" " + \
                              "or \"-2\" here to correct it with plus/minus two hours",
                          metavar="STRING")

        self.add_argument("--inactive-time-stamps",
                          dest="inactive_timestamps",
                          help="""inactive time-stamps are written to the output file 
                          instead of active time-stamps. Helps to move modules with many entries
                          to the inactive layer of the agenda.""",
                          action="store_true")

        # ---------------------
        # Config parser
        # ---------------------
        if self.__use_config_parser_name:
            self.add_argument("-c", "--config",
                              dest="configfile",
                              help="path to config file",
                              metavar="FILE")

    def parse_args(self, args=None, namespace=None):
        """
        overwriting ArgParser's parse_args and
        do checking default argument outputfile
        """
        args = ArgumentParser.parse_args(self, args=args, namespace=namespace)
        if args.outputfile:
            if not os.path.exists(os.path.dirname(args.outputfile)):
                self.error("Output file path(%s) does not exist!" %
                           args.outputfile)
            if not os.access(os.path.dirname(args.outputfile), os.W_OK):
                self.error("Output file %s is not writeable!" %
                           args.outputfile)
        else:
            if args.append:
                self.error("cannot set append when no outputfile specified")

        if args.suppressmessages == True and args.verbose == True:
            self.error("cannot set both verbose and suppress-messages")

        if args.autotagfile:
            if not os.path.exists(os.path.dirname(args.autotagfile)):
                self.error("Autotag file path(%s) doest not exist!" %
                           args.autotagfile)
            if not os.access(args.autotagfile, os.R_OK):
                self.error("Autotag file (%s) is not readable!" %
                           args.autotagfile)

        if args.timestamp_delta:
            timestamp_components = re.match('[+-]\d\d?', args.timestamp_delta)
            if not timestamp_components:
                self.error("format of \"--add-to-time-stamps\" is not recognized. Should be similar " + \
                           "to ,e.g., \"+1\" or \"-3\".")

        # ---------------------
        # Config parser
        # ---------------------
        if self.__use_config_parser_name:
            xdg = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
            configdir = os.path.join(xdg, 'memacs')

            if os.path.isdir(configdir):
                for filename in os.listdir(configdir):
                    if self.__use_config_parser_name == os.path.splitext(filename)[0]:
                        args.configfile = os.path.join(configdir, filename)
                        continue

            if args.configfile:
                if not os.path.exists(args.configfile):
                    self.error("Config file (%s) does not exist" %
                        args.configfile)
                if not os.access(args.configfile, os.R_OK):
                    self.error("Config file (%s) is not readable!" %
                        args.configfile)
            else:
                self.error("please specify a config file")
        return args
