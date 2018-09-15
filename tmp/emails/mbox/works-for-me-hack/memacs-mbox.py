#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import logging
from optparse import OptionParser

# TODO:
# - add command line argument to define link name to real content
#   currently: "file:INPUTFILE::ID" is used
#   desired:   "mylinkname:INPUTFILE::ID" should be used
#   additional: add explanation to readme (setq org-link-abbrev-alist)

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2011-09-16"
INVOCATION_TIME = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

# better performance if pre-compiled:
SUBJECT_REGEX = re.compile("Subject: (.*)")
FROM_REGEX = re.compile("From: (.*) <(.*)>")
NEWSGROUPS_REGEX = re.compile("Newsgroups: (.*)")
MESSAGEID_REGEX = re.compile("Message-I(d|D): (.*)")
HEADERSTART_REGEX = re.compile("From (.*) (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (([12]\d)|( 1| 2| 3| 4| 5| 5| 6| 7| 8| 9|30|31)) (([01]\d)|(20|21|22|23)):([012345]\d):([012345]\d) ([12]\d{3})")

# group 1: email: foo@gmx.at
# group 2: day: Fri
# group 3: month: May
# group 4: day: " 7"
# group 5: -
# group 6: day: " 7"
# group 7: hour: 13
# group 8: hour: 13
# group 9: -
# group 10: minutes: 54
# group 11: seconds: 15
# group 12: year: 2010

# From foo@gmx.at Fri May  7 13:54:15 2010
# From foo@bar-Voit.at Wed May 19 09:58:08 2010
# From foo@gmx.at Tue May 18 12:03:01 2010
# From foo@htu.tugraz.at Thu May  6 08:16:54 2010
# From foo@student.tugraz.at Fri May 21 16:01:09 2010
# From foo@bank.at Wed May  5 20:15:27 2010

# dd = " 1"..31: (([12]\d)|( 1| 2| 3| 4| 5| 5| 6| 7| 8| 9|30|31))
# hh = 01..24: (([01]\d)|(20|21|22|23))
# mm = 00..59: ([012345]\d)
# ss = 00..59: ([012345]\d)
# yyyy = 1000...2999: ([12]\d{3})

USAGE = "\n\
         "+sys.argv[0]+"\n\
\n\
This script parses mbox files (or newsgroup postings) and generates \n\
an Org-mode file whose entry lines show the emails in Org-mode agenda.\n\
\n\
Usage:  "+sys.argv[0]+" <options>\n\
\n\
Example:\n\
     ## simple example converting one mbox file:\n\
     "+sys.argv[0]+" -f ~/mails/business.mbox -o mails.org_archive\n\
\n\
     ## more advanced example with multiple files at once:\n\
     for myfile in ~/mails/*mbox\n\
        do "+sys.argv[0]+" -f \"${myfile}\" >> mails.org_archive\n\
     done\n\
\n\
\n\
:copyright: (c) 2011 by Karl Voit <tools@Karl-Voit.at>\n\
:license: GPL v2 or any later version\n\
:bugreports: <tools@Karl-Voit.at>\n\
:version: "+PROG_VERSION_NUMBER+" from "+PROG_VERSION_DATE+"\n"

parser = OptionParser(usage=USAGE)

parser.add_option("-f", "--file", dest="mboxname",
                  help="a file that holds the emails in mbox format", metavar="FILE")

parser.add_option("-o", "--output", dest="outputfile",
                  help="Org-mode file that will be generated (see above)." +
                  " If no output file is given, result gets printed to stdout", metavar="FILE")

parser.add_option("-w", "--overwrite", dest="overwrite", action="store_true",
                  help="overwrite given output file without checking its existance")

parser.add_option("-n", "--newsgroup", dest="newsgroup", action="store_true",
                  help="mbox file contains newsgroup postings: ignore \"From:\", add \"Newsgroups:\"")

parser.add_option("--version", dest="version", action="store_true",
                  help="display version and exit")

parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                  help="enable verbose mode")

(options, args) = parser.parse_args()


def handle_logging():
    """Log handling and configuration"""

    if options.verbose:
        FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    else:
        FORMAT = "%(message)s"
        logging.basicConfig(level=logging.INFO, format=FORMAT)


def get_timestamp_from_components(components):
    """returns orgmode timestamp of regex components"""

    # resetting contact dictionary
    monthsdict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',
                  'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

    # group 1: email: foo@gmx.at
    # group 2: day: Fri
    daystrid = 2
    # group 3: month: May
    monthid = 3
    # group 4: day: " 7"
    dayid = 4
    # group 5: -
    # group 6: day: " 7"
    # group 7: hour: 13
    hourid = 7
    # group 8: hour: 13
    # group 9: -
    # group 10: minutes: 54
    minuteid = 10
    # group 11: seconds: 15
    # group 12: year: 2010
    yearid = 12

    try:
        string = "<" + components.group(yearid) + "-" + monthsdict[components.group(monthid)] + \
           "-" + components.group(dayid).strip().zfill(2) + " " + components.group(daystrid) + \
           " " + components.group(hourid) + ":" + components.group(minuteid) + ">"
    except IndexError as e:
        logging.error("Sorry, there were some problems parsing the timestamp of the current from line.")
        string = "ERROR"

    return string


def generate_output_line(timestamp, fromline, emailaddress, filename, messageid, subject):
    """generates an orgmode entry for an email"""

    if fromline == "":
        fromline = emailaddress

    string = "** " + timestamp
    if options.newsgroup:
        string += " " + fromline + ": "
    else:
        string += " [[contact:" + fromline + "][" + fromline + "]]: "

    string += "[[file:" + filename + "::" + messageid + "][" + subject + "]]"

    return string


def parse_mbox(filename, outputfile):
    """parses an mbox and generates orgmode entries"""

    basename = os.path.basename(filename).strip()
    logging.debug("--------------------------------------------")
    logging.debug("processing line \""+ filename + "\" with basename \"" + basename + "\"")

    was_empty_line = True
    is_header = False
    last_firstline = ""  # holds the "From .*" line which is the first line of a new email/posting
    last_from = ""  # holds real name for emails OR newsgroup name(s) for postings
    last_email = ""
    last_subject = ""
    last_message_id = ""
    last_orgmodetimestamp = ""

    for line in open(filename, 'r', encoding='LATIN-1'):  # my personal archive files seem to be encoded in LATIN-1. FIXXME: proper error handling with detecting encoding
            line = line.strip()

            if was_empty_line:
                # logging.debug("was_empty_line is True")
                fromlinecomponents = HEADERSTART_REGEX.match(line)

            if is_header:
                logging.debug("parsing header line: " + line)
                # logging.debug("is_header is True")
                subjectcomponents = SUBJECT_REGEX.match(line)
                if options.newsgroup:
                    fromcomponents = NEWSGROUPS_REGEX.match(line)
                else:
                    fromcomponents = FROM_REGEX.match(line)
                messageidcomponents = MESSAGEID_REGEX.match(line)

            if not is_header and was_empty_line and fromlinecomponents:
                logging.debug("new header: " + line)
                # here the beginning of a new email header is assumed when an empty line
                # is followed by a line that matches HEADERSTART_REGEX
                is_header = True
                last_email = fromlinecomponents.group(1)
                last_firstline = line
                last_from = ""
                last_subject = ""
                last_message_id = ""
                subjectcomponents = None
                messageidcomponents = None
                last_orgmodetimestamp = get_timestamp_from_components(fromlinecomponents)
                logging.debug("new email: " + last_email + " ... at " + last_orgmodetimestamp)

            elif is_header and subjectcomponents:
                last_subject = subjectcomponents.group(1).replace('[', '|').replace("]", "|")
                logging.debug("subject: " + last_subject)

            elif is_header and fromcomponents:
                last_from = fromcomponents.group(1).replace('"', '').replace("'", "")
                logging.debug("from: " + last_from)

            elif is_header and messageidcomponents:
                last_message_id = messageidcomponents.group(2).replace('<', '').replace(">", "")
                if last_message_id == "":
                    logging.error("Sorry, this entry had no correct message-id and is not jumpable in Orgmode.")
                logging.debug(last_message_id)

            if is_header and last_orgmodetimestamp != "" and last_subject != "" and last_message_id != "":
                logging.debug("entry written")
                if outputfile:
                    outputfile.write(generate_output_line(last_orgmodetimestamp, last_from, last_email,
                                                          filename, last_message_id, last_subject))
                    if options.newsgroup:
                        outputfile.write('\n')  # FIXXME: Sorry for this but there seems to be different behaviour when doing newsgroups
                else:
                    print(generate_output_line(last_orgmodetimestamp, last_from, last_email,
                                               filename, last_message_id, last_subject).strip())
                is_header = False

            if line == "":
                was_empty_line = True
                if is_header and last_message_id == "":
                    # recover if only message-id was not found:
                    # (some NNTP-clients do not generate those and let the NNTP-server do it)
                    last_message_id = last_firstline
                    logging.warn("Current entry does not provide a Message-ID, using first From-line instead: " + last_firstline)
                elif is_header:
                    logging.error("Current entry was not recognized as an entry. Missing value(s)?")
                    if last_orgmodetimestamp:
                        logging.error("  timestamp:  " + last_orgmodetimestamp)
                    else:
                        logging.error("  NO timestamp recognized!")
                    logging.error("  subject:    " + last_subject)
                    logging.error("  message-id: " + last_message_id)
                    is_header = False
            else:
                was_empty_line = False


def main():
    """Main function"""

    if options.version:
        print(os.path.basename(sys.argv[0]) + " version "+PROG_VERSION_NUMBER+" from "+PROG_VERSION_DATE)
        sys.exit(0)

    handle_logging()

    if not options.mboxname:
        parser.error("Please provide an input file!")

    if not os.path.isfile(options.mboxname):
        print(USAGE)
        logging.error("\n\nThe argument interpreted as an input file \"" + str(options.mboxname) + \
                      "\" is not an normal file!\n")
        sys.exit(2)

    if not options.overwrite and options.outputfile and os.path.isfile(options.outputfile):
        print(USAGE)
        logging.error("\n\nThe argument interpreted as output file \"" + str(options.outputfile) + \
                      "\" already exists!\n")
        sys.exit(3)

    string = "## this file is generated by " + sys.argv[0] + \
                     ". Any modifications will be overwritten upon next invocation!\n"

    if options.newsgroup:
        string += "* Memacs module for newsgroup postings: " + options.mboxname + "                    :Memacs:news:"
    else:
        string += "* Memacs module for mbox emails: " + options.mboxname + "                         :Memacs:mbox:email:"

    if options.outputfile:
        output = open(options.outputfile, 'w')
        output.write(string + "\n")
    else:
        output = None
        print(string)

    parse_mbox(options.mboxname, output)

    string = "* this mbox is successfully parsed by " + sys.argv[0] + " at " + INVOCATION_TIME + "."

    if options.outputfile:
        output.write(string + "\n")
        output.close()
    else:
        print(string)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Received KeyboardInterrupt")

# END OF FILE #################################################################
# end
