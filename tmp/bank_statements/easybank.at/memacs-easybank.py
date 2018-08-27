#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Time-stamp: <2013-06-13 21:52:51 vk>

import os
import sys
import re
import time
import logging
from optparse import OptionParser
import codecs ## for writing unicode file
import pdb

## TODO:
## * fix parts marked with «FIXXME»

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2011-10-09"
INVOCATION_TIME = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

## better performance if ReEx is pre-compiled:

## search for: «DD.MM.(.*)UM HH.MM»
TIMESTAMP_REGEX = re.compile(".*(([012]\d)|(30|31))\.((0\d)|(10|11|12))\..*UM ([012345]\d)\.([012345]\d).*")
## group 1: DD
TIMESTAMP_REGEX_DAYINDEX = 1  ## 2 is not always found
## group 2: DD
## group 3:
## group 4: MM
TIMESTAMP_REGEX_MONTHINDEX = 4  ## 5 is not always found
## group 5: MM
## group 6:
## group 7: HH
TIMESTAMP_REGEX_HOURINDEX = 7
## group 8: MM
TIMESTAMP_REGEX_MINUTEINDEX = 8
## group 9: nil

## search for: «DD.MM.YYYY»
DATESTAMP_REGEX = re.compile("([012345]\d)\.([012345]\d)\.([12]\d\d\d)")
DATESTAMP_REGEX_DAYINDEX = 1
DATESTAMP_REGEX_MONTHINDEX = 2
DATESTAMP_REGEX_YEARINDEX = 3

## search for: <numbers> <numbers> <nonnumbers>
BANKCODE_NAME_REGEX = re.compile("(\d\d\d\d+) (\d\d\d\d+) (.*)")

USAGE = "\n\
         " + sys.argv[0] + "\n\
\n\
This script parses bank statements «Umsatzliste» of easybank.at and generates \n\
an Org-mode file whose entry lines show the transactions in Org-mode agenda.\n\
\n\
Usage:  " + sys.argv[0] + " <options>\n\
\n\
Example:\n\
     " + sys.argv[0] + " -f ~/bank/transactions.csv -o ~/org/bank.org_archive\n\
\n\
\n\
:copyright: (c) 2011 by Karl Voit <tools@Karl-Voit.at>\n\
:license: GPL v2 or any later version\n\
:bugreports: <tools@Karl-Voit.at>\n\
:version: "+PROG_VERSION_NUMBER+" from "+PROG_VERSION_DATE+"\n"

parser = OptionParser(usage=USAGE)

parser.add_option("-f", "--file", dest="csvfilename",
                  help="a file that holds the transactions in CSV format", metavar="FILE")

parser.add_option("-o", "--output", dest="outputfile",
                  help="Org-mode file that will be generated (see above)." +\
                       " If no output file is given, result gets printed to stdout", metavar="FILE")

parser.add_option("-w", "--overwrite", dest="overwrite", action="store_true",
                  help="overwrite given output file without checking its existance")

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



def extract_datestamp_from_eventday(daystring):
    """extracts day, month, year from string like «DD.MM.YYYY»"""

    components = DATESTAMP_REGEX.match(daystring)

    if not components:
        logging.error("ERROR: could not parse date field: [" + daystring + "]")
        sys.exit(5)

    return components.group(DATESTAMP_REGEX_DAYINDEX),\
        components.group(DATESTAMP_REGEX_MONTHINDEX), \
        components.group(DATESTAMP_REGEX_YEARINDEX)


def extract_timestamp_from_timestampcomponents(timestampparts):
    """extracts the components of a time stamp from the timestampcomponents"""

    #logging.debug("found " + str(len(timestampparts.groups())) + " part(s) of timestamp within longdescription")
    month = timestampparts.group(TIMESTAMP_REGEX_MONTHINDEX)
    day = timestampparts.group(TIMESTAMP_REGEX_DAYINDEX)
    hour = timestampparts.group(TIMESTAMP_REGEX_HOURINDEX)
    minute = timestampparts.group(TIMESTAMP_REGEX_MINUTEINDEX)
    logging.debug("extracted timestamp: MM:dd [%s.%s] hh:mm [%s:%s] " % ( month, day, hour, minute) )
    return month, day, hour, minute


def generate_orgmodetimestamp(day, month, year, hour, minute):
    """generates <YYYY-MM-DD> or <YYYY-MM-DD HH:MM> from strings in arguments"""
    if hour and minute:
        timestring = " " + hour + ":" + minute
    else:
        timestring = ""
    return "<" + year + "-" + month + "-" + day + timestring + ">"


def extract_known_datasets(name, shortdescription, longdescription, descriptionparts):
    """handle known entries in the CSV file"""

    ## Auszahlung Maestro                           MC/000002270|BANKOMAT 29511 KARTE1 18.04.UM 11.34
    if descriptionparts[0].startswith('Auszahlung Maestro  '):
        logging.debug("found special case \"Auszahlung Maestro\"")
        name = None
        if len(descriptionparts)>1:
            shortdescription = descriptionparts[1].split(" ")[:2]  ## the 1st two words of the 2nd part
            shortdescription = " ".join(shortdescription)
        else:
            logging.warning("could not find descriptionparts[1]; using " + \
                                "\"Auszahlung Maestro\" instead")
            shortdescription = "Auszahlung Maestro"
        logging.debug("shortdescr.=" + str(shortdescription))
            

    ## Bezahlung Maestro      MC/000002281|2108  K1 01.05.UM 17.43|OEBB 2483 FSA\\Ebreich sdorf         2483
    ## Bezahlung Maestro      MC/000002277|2108  K1 27.04.UM 17.10|OEBB 8020 FSA\\Graz                  8020
    ## Bezahlung Maestro      MC/000002276|WIENER LINIE 3001  K1 28.04.UM 19.05|WIENER LINIEN 3001     \
    ## Bezahlung Maestro      MC/000002272|BRAUN        0001  K1 19.04.UM 23.21|BRAUN DE PRAUN         \
    ## Bezahlung Maestro      MC/000002308|BILLA DANKT  6558  K1 11.06.UM 10.21|BILLA 6558             \
    ## Bezahlung Maestro      MC/000002337|AH10  K1 12.07.UM 11.46|Ecotec Computer Dat\\T imelkam       4850
    elif descriptionparts[0].startswith('Bezahlung Maestro  ') and len(descriptionparts)>2:
        logging.debug("found special case \"Bezahlung Maestro\"")
        shortdescription = descriptionparts[2].strip()  ## the last part
        name = None
        ## does not really work well with Unicode ... (yet)
        ##if shortdescription.startswith(u"OEBB"):
        ##    logging.debug("found special case \"ÖBB Fahrscheinautomat\"")
        ##    #shortdescription.replace("\\",' ')
        ##    logging.debug("sd[2]: [" + descriptionparts[2].strip() + "]")
        ##    re.sub(ur'OEBB (\d\d\d\d) FSA\\(.*)\s\s+(\\\d)?(\d\d+).*', ur'ÖBB Fahrschein \4 \2', descriptionparts[2].strip())

    elif descriptionparts[0].startswith('easykreditkarte MasterCard '):
        logging.debug("found special case \"easykreditkarte\"")
        name = None
        shortdescription = "MasterCard Abrechnung"

    elif len(descriptionparts)>1 and descriptionparts[0].startswith('Gutschrift Überweisung ') and \
            descriptionparts[1].startswith('TECHNISCHE UNIVERSITAET GRAZ '):
        logging.debug("found special case \"Gutschrift Überweisung, TUG\"")
        name = "TU Graz"
        shortdescription = "Gehalt"

    elif len(descriptionparts)>1 and descriptionparts[1] == 'Vergütung für Kontoführung':
        logging.debug("found special case \"Vergütung für Kontoführung\"")
        name = "easybank"
        shortdescription = "Vergütung für Kontoführung"

    elif len(descriptionparts)>1 and descriptionparts[1] == 'Entgelt für Kontoführung':
        logging.debug("found special case \"Entgelt für Kontoführung\"")
        name = "easybank"
        shortdescription = "Entgelt für Kontoführung"

    if name:
        logging.debug("changed name to: " + name)
    if shortdescription:
        logging.debug("changed shortdescription to: " + shortdescription)
    return name, shortdescription


def extract_name_and_shortdescription(longdescription):
    """
    Heuristic extraction of any information useful as name or short description.
    This is highly dependent on your personal account habit/data!
    """

    name = shortdescription = None

    ## shortdescription is first part of longdescriptions before the first two spaces
    shortdescription = longdescription[:longdescription.find("  ")]

    if len(shortdescription) < len(longdescription) and len(shortdescription) > 0:
        logging.debug("     extracted short description: [" + shortdescription + "]")
    else:
        shortdescription = None

    descriptionparts = longdescription.split('|')
    if len(descriptionparts) > 1:
        logging.debug("     found " + str(len(descriptionparts)) + " part(s) within longdescription, looking for name ...")
        bankcode_name = BANKCODE_NAME_REGEX.match(descriptionparts[1])
        if bankcode_name:
            name = bankcode_name.group(3)
            logging.debug("     found bank code and name. name is: [" + name + "]")

    ## so far the general stuff; now for parsing some known lines optionally overwriting things:
    name, shortdescription = extract_known_datasets(name, shortdescription, longdescription, descriptionparts)

    return name, shortdescription


def generate_orgmodeentry(orgmodetimestamp, jumptarget, amount, currency, longdescription, shortdescription, name):
    """generates the string for the Org-mode file"""

    ## ** $timestamp $amount $currency, [[bank:$jumptarget][$description]]
    ## if shortdescription:
    ## ** $timestamp $amount $currency, [[bank:$jumptarget][$shortdescription]]
    ## if name:
    ## ** $timestamp $amount $currency, [[contact:$name][name]], [[bank:$jumptarget][$description]]
    ## if name and shortdescription:
    ## ** $timestamp $amount $currency, [[contact:$name][name]], [[bank:$jumptarget][$(short)description]]

    if currency == "EUR":
        currency = "€"    # it's shorter :-)

    entry = "** " + orgmodetimestamp + " " + amount + currency + ", "

    if name and len(name)>0:
        entry += "[[contact:" + name + "][" + name + "]], "

    if shortdescription:
        entry += "[[bank:" + jumptarget + "][" + shortdescription + "]]"
    else:
        entry += "[[bank:" + jumptarget + "][" + longdescription + "]]"

    return entry


def parse_csvfile(filename, handler):
    """parses an csv file and generates orgmode entries"""

    basename = os.path.basename(filename).strip()
    logging.debug( "--------------------------------------------")
    logging.debug("processing file \""+ filename + "\" with basename \""+ basename + "\"")

    ## please do *not* use csvreader here since it is not able to handle UTF-8/latin-1!
    inputfile = codecs.open(filename, 'rb', 'latin-1')
    for line in inputfile:

        row = line.split(";")
        logging.debug("--------------------------------------------------------")
        logging.debug("processing row: " + str(str(row)) )

        ## direct data:
        try:
            longdescription = str(row[1])
            amount = str(row[4])
            currency = str(row[5]).strip()
            jumptarget = str(row[2]) + ";" + str(row[3]) + ";" + str(row[4])
        except UnicodeDecodeError as detail:
            logging.error("Encoding error: ")
            print(detail)
            logging.error("corresponding line is: [" + str(str(row)) + "]")
            sys.exit(4)

        ## derived data:
        timestampparts = TIMESTAMP_REGEX.match(longdescription)
        year = month = day = hour = minute = None
        orgmodetimestamp = None
        name = None   ## optional
        shortdescription = None   ## optional

        ## one line contains following values separated by «;»
        #logging.debug("account number: " + row[0] )
        logging.debug("long description: [" + longdescription + "]" )
        #logging.debug("day of clearing: " + row[2] )
        logging.debug("day of event: " + row[3] )
        logging.debug("amount: " + amount )
        #logging.debug("currency: " + currency )
        day, month, year = extract_datestamp_from_eventday(str(row[3]))
        if timestampparts:
            month, day, hour, minute = extract_timestamp_from_timestampcomponents(timestampparts)

        orgmodetimestamp = generate_orgmodetimestamp(day, month, year, hour, minute)

        name, shortdescription = extract_name_and_shortdescription(longdescription)

        orgmodeentry = generate_orgmodeentry(orgmodetimestamp, jumptarget, amount, \
                                             currency, longdescription, shortdescription, name)

        write_output(handler, orgmodeentry)


def write_output(handler, string):
    """write to stdout or to outfile"""

    if options.outputfile:
        handler.write(str(string) + "\n")
    else:
        print(string)


def main():
    """Main function"""

    if options.version:
        print(os.path.basename(sys.argv[0]) + " version "+PROG_VERSION_NUMBER+" from "+PROG_VERSION_DATE)
        sys.exit(0)

    handle_logging()

    if not options.csvfilename:
        parser.error("Please provide an input file!")

    if not os.path.isfile(options.csvfilename):
    	print(USAGE)
    	logging.error("\n\nThe argument interpreted as an input file \"" + str(options.csvfilename) + \
                          "\" is not an normal file!\n")
        sys.exit(2)

    if not options.overwrite and options.outputfile and os.path.isfile(options.outputfile):
    	print(USAGE)
    	logging.error("\n\nThe argument interpreted as output file \"" + str(options.outputfile) + \
                          "\" already exists!\n")
        sys.exit(3)

    if options.outputfile:
        handler = codecs.open(options.outputfile, 'w', "utf-8")

    write_output(handler, "## -*- coding: utf-8 -*-")
    write_output(handler, "## this file is generated by " + sys.argv[0] + \
                     ". Any modifications will be overwritten upon next invocation!")
    write_output(handler, "##    parameter input filename:  " + options.csvfilename)
    if options.outputfile:
        write_output(handler, "##    parameter output filename: " + options.outputfile)
    else:
        write_output(handler, "##    parameter output filename: none, writing to stdout")
    write_output(handler, "##    invocation time:           " + INVOCATION_TIME)
    write_output(handler, "* bank transactions                          :Memacs:bank:")

    parse_csvfile(options.csvfilename, handler)

    write_output(handler, "* bank transcations above were successfully parsed by " + \
                     sys.argv[0] + " at " + INVOCATION_TIME + ".\n\n")

    if options.outputfile:
        handler.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        logging.info("Received KeyboardInterrupt")

## END OF FILE #################################################################

#end
