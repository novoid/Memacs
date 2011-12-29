# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-28 20:27:27 armin>

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import os


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
                 copyright_authors):

        self.__version = "%(prog)s v" + prog_version + " from " + \
            prog_version_date

        # format copyright authors:
        # indent from second author
        copyright_authors = copyright_authors.splitlines()
        for i in range(len(copyright_authors)):
            copyright_authors[i] = "            " + copyright_authors[i]
        copyright_authors = "\n".join(map(unicode, copyright_authors))

        epilog = ":copyright: (c) " + copyright_year + " by \n" + \
        copyright_authors + \
        "\n:license: GPL v2 or any later version\n" + \
        ":bugreports: https://github.com/novoid/Memacs\n" + \
        ":version: " + prog_version + " from " + prog_version_date + "\n"

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
        return args
