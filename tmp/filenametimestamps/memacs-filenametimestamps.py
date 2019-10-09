#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import logging
from optparse import OptionParser

PROG_VERSION_NUMBER = "0.2"
PROG_VERSION_DATE = "2011-10-10"
INVOCATION_TIME = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
MATCHING_LEVEL = {'day': 1, 'minutes': 2, 'seconds': 3, 'notmatching': 4}

# better performance if pre-compiled:
TIMESTAMP_REGEX = re.compile("([12]\d{3})-([01]\d)-([0123]\d)T([012]\d).([012345]\d)(.([012345]\d))?")
DATESTAMP_REGEX = re.compile("([12]\d{3})-([01]\d)-([0123]\d)")

# RegEx matches more exactly:
#         reason: avoid 2011-01-00 (day is zero) or month is >12, ...
#         problem: mathing groups will change as well!
#   also fix in: vktimestamp2filedate
# dd = 01..31: ( ([12]\d) | (01|02|03|04|05|05|06|07|08|09|30|31) )
# mm = 01..12: ( ([0]\d) | (10|11|12) )
# hh = 00..23: ( ([01]\d) | (20|21|22|23) )

USAGE = "\n\
         "+sys.argv[0]+"\n\
\n\
This script parses a text file containing absolute paths to files\n\
with ISO datestamps and timestamps in their file names:\n\
\n\
Examples:  \"2010-03-29T20.12 Divegraph.tiff\"\n\
           \"2010-12-31T23.59_Cookie_recipies.pdf\"\n\
           \"2011-08-29T08.23.59_test.pdf\"\n\
\n\
Then an Org-mode file is generated that contains links to the files.\n\
\n\
Usage:  "+sys.argv[0]+" <options>\n\
\n\
Example:\n\
     ## generating a file containing all ISO timestamp filenames:\n\
     find $HOME -name '[12][0-9][0-9][0-9]-[01][0-9]-[0123][0-9]*' \ \n\
                                         -type f > $HOME/files.log\n\
     ## invoking this script:\n\
     "+sys.argv[0]+" -f $HOME/files.log -o result.org\n\
\n\
\n\
:copyright: (c) 2011 by Karl Voit <tools@Karl-Voit.at>\n\
:license: GPL v2 or any later version\n\
:bugreports: <tools@Karl-Voit.at>\n\
:version: "+PROG_VERSION_NUMBER+" from "+PROG_VERSION_DATE+"\n"

parser = OptionParser(usage=USAGE)

parser.add_option("-f", "--filelist", dest="filelistname",
                  help="file that holds the list of files (see above)", metavar="FILE")

parser.add_option("-o", "--output", dest="outputfile",
                  help="Org-mode file that will be generated (see above)", metavar="FILE")

parser.add_option("-w", "--overwrite", dest="overwrite", action="store_true",
                  help="overwrite given output file without checking its existance")

parser.add_option("--version", dest="version", action="store_true",
                  help="display version and exit")

parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                  help="enable verbose mode")

(options, args) = parser.parse_args()
# if we found a timestamp too, take hours,minutes and optionally seconds from this timestamp


def handle_logging():
    """Log handling and configuration"""

    if options.verbose:
        FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    else:
        FORMAT = "%(message)s"
        logging.basicConfig(level=logging.INFO, format=FORMAT)


def get_timestamp_from_file(filename):
    """returns mtime of file"""
    return time.localtime(os.path.getmtime(filename))


def check_if_days_in_timestamps_are_same(filename, basename, filenamedatestampcomponents):
    """handles timestamp differences for timestamps containing only day information (and not times)"""

    filetimestamp = get_timestamp_from_file(filename)[0:3]
    logging.debug("filetimestamp " + str(filetimestamp))

    filenamedatestampcomponentslist = [int(x) for x in filenamedatestampcomponents.groups()]  # converts strings to integers
    filenamedatestampcomponentslist = list(filenamedatestampcomponentslist)  # converts tuple to list

    logging.debug("filenamedatestampcomponentslist " + str(filenamedatestampcomponentslist))
    # logging.debug( "filenamedatestampcomponentslist[0] " + str( filenamedatestampcomponentslist[0] ))

    if filenamedatestampcomponentslist[0] == filetimestamp[0] and \
            filenamedatestampcomponentslist[1] == filetimestamp[1] and \
            filenamedatestampcomponentslist[2] == filetimestamp[2]:
        logging.debug("matches only date YYYY-MM-DD")
        return True
    else:
        logging.debug("filetimestamp and filename differs: " + filename)
        return False




def generate_orgmode_file_timestamp(filename):
    """generates string for a file containing ISO timestamp in Org-mode"""

    # Org-mode timestamp: <2011-07-16 Sat 9:00>
    # also working in Org-mode agenda: <2011-07-16 9:00>

    basename = os.path.basename(filename)
    timestampcomponents = TIMESTAMP_REGEX.match(basename)
    # "2010-06-12T13.08.42_test..." -> ('2010', '06', '12', '13', '08', '.42', '42')
    # filenametimestampcomponents.group(1) -> '2010'

    datestampcomponents = DATESTAMP_REGEX.match(basename)

    if timestampcomponents:

        datestamp = "<" + str(timestampcomponents.group(1)) + "-" + str(timestampcomponents.group(2)) + "-" + str(timestampcomponents.group(3)) + \
            " " + str(timestampcomponents.group(4)) + ":" + str(timestampcomponents.group(5)) + ">"

        logging.debug("datestamp (time): " + datestamp)

        return "** " + datestamp + " [[file:" + filename + "][" + basename + "]]\n"

    elif datestampcomponents:

        if check_if_days_in_timestamps_are_same(filename, basename, datestampcomponents):
            logging.debug("day of timestamps is different, have to assume time")

            assumedtime = ""  # no special time assumed; file gets shown as time-independent
            # assumedtime = " 12:00" ## files with no special time gets shown at noon

            datestamp = "<" + str(datestampcomponents.group(1)) + "-" + str(datestampcomponents.group(2)) + \
                "-" + str(datestampcomponents.group(3)) + assumedtime + ">"

            logging.debug("datestamp (day): " + datestamp)

            return "** " + datestamp + " [[file:" + filename + "][" + basename + "]]\n"

        else:
            logging.debug("day of timestamps is same, can use file time")

            filetimestampcomponents = get_timestamp_from_file(filename)
            timestamp = str(filetimestampcomponents[3]).zfill(2) + ":" + str(filetimestampcomponents[4]).zfill(2)

            datestamp = "<" + str(datestampcomponents.group(1)) + "-" + str(datestampcomponents.group(2)) + \
                "-" + str(datestampcomponents.group(3)) + " " + str(timestamp) + ">"

            logging.debug("datestamp (day): " + datestamp)

            return "** " + datestamp + " [[file:" + filename + "][" + basename + "]]\n"

    else:
        logging.warning("FIXXME: this point should never be reached. not recognizing datestamp or timestamp")
        return False


def handle_filelist_line(line, output):
    """handles one line of the list of files to check"""

    filename = line.strip()
    basename = os.path.basename(line).strip()
    logging.debug("--------------------------------------------")
    logging.debug("processing line \"" + filename + "\" with basename \"" + basename + "\"")

    if filename == "":
        logging.debug("ignoring empty line")

    elif not os.path.isfile(filename):
        logging.warn("ignoring \"" + filename + "\" because it is no file")

    elif TIMESTAMP_REGEX.match(basename) or DATESTAMP_REGEX.match(basename):

        output.write(generate_orgmode_file_timestamp(filename))

    else:
        logging.warn("ignoring \"" + filename + "\" because its file name does not match ISO date YYYY-MM-DDThh.mm(.ss)")


def main():
    """Main function"""

    if options.version:
        print(os.path.basename(sys.argv[0]) + " version "+PROG_VERSION_NUMBER+" from "+PROG_VERSION_DATE)
        sys.exit(0)

    handle_logging()

    if not options.filelistname:
        parser.error("Please provide an input file!")

    if not options.outputfile:
        parser.error("Please provide an output file!")

    if not os.path.isfile(options.filelistname):
        print(USAGE)
        logging.error("\n\nThe argument interpreted as an input file \"" + str(options.filelistname) + "\" is not an normal file!\n")
        sys.exit(2)

    if not options.overwrite and os.path.isfile(options.outputfile):
        print(USAGE)
        logging.error("\n\nThe argument interpreted as output file \"" + str(options.outputfile) + "\" already exists!\n")
        sys.exit(3)

    output = open(options.outputfile, 'w')

    output.write("## this file is generated by " + sys.argv[0] + ". Any modifications will be overwritten upon next invocation!\n")
    output.write("* Memacs file name datestamp                      :Memacs:filedatestamps:\n")

    for line in open(options.filelistname, 'r'):

        handle_filelist_line(line, output)

    output.write("* this file is successfully generated by " + sys.argv[0] + " at " + INVOCATION_TIME + ".\n")
    output.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Received KeyboardInterrupt")

# END OF FILE #################################################################
# end
