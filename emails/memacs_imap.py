#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-30 01:29:34 armin>

import sys
import os
import logging
import imaplib
# needed to import common.*
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.memacs import Memacs
from common.mailhandler import MailHandler


PROG_VERSION_NUMBER = u"0.0"
PROG_VERSION_DATE = u"2011-12-18"
PROG_SHORT_DESCRIPTION = u"Memacs for ... "
PROG_TAG = u"emails:imap"
PROG_DESCRIPTION = u"""
this class will do ....

sample-config:

[memacs-imap]
host = imap.gmail.com
port = 993
user = foo@gmail.com
password = bar
"""
CONFIG_PARSER_NAME = "memacs-imap"
COPYRIGHT_YEAR = "2011-2012"
COPYRIGHT_AUTHORS = """Karl Voit <tools@Karl-Voit.at>,
Armin Wieser <armin.wieser@gmail.com>"""


class ImapMemacs(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
           "-l", "--list-folders",
           dest="list_folders",
           action="store_true",
           help="show possible folders of connection")

        self._parser.add_argument(
           "-f", "--folder_name",
           dest="folder_name",
           help="name of folder to get emails from, " + \
            "when you don't know name call --list-folders")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)

        if not self._args.list_folders and not self._args.folder_name:
            self._parser.error("please specify a folder " + \
                                   "use --list to find a folder")

    def __fetch_mails_and_write(self, server, message_ids, folder_name):
        
        num = ",".join(message_ids)

        logging.debug(num)
        typ, data = server.uid("fetch",
                               num,
                               "(BODY[HEADER.FIELDS " + \
                                   "(Date Subject " + \
                                   "From To Cc Reply-To Message-ID)])")
        
        if typ == "OK":
            i = 0

            # we have to go in step 2 because everey second string is a ")"
            for i in range(0, len(data), 2):
                message = data[i][1]
                timestamp, output, note, properties = \
                    MailHandler.handle_message(message)
                    
                # just for debbuging in orgfile 
                # properties.add("NUM",data[i][0][:5])                
                self._writer.write_org_subitem(timestamp,
                                               output,
                                               note,
                                               properties)

        else:
            logging.error("Could not fetch mails typ - %s", typ)

    def __handle_folder(self, server, folder_name):
        logging.debug("folder: %s", folder_name)
        
        typ, data = server.select(folder_name)
        if typ != "OK":
            logging.error("could not select folde %s", folder_name)
            server.logout()

        typ, data = server.uid('search', None, 'ALL')
        if typ == "OK":
            message_ids = data[0].split()
            logging.debug("message_ids:%s", ",".join(message_ids))
            self.__fetch_mails_and_write(server, message_ids, folder_name)
        else:
            logging.error("Could not select folder %s - typ:%s",
                          folder_name, typ)
            server.logout()
            sys.exit(1)

    def __list_folders(self, server):
        """
        lists all folders and writes them to
        logging.info
        """
        typ, folder_list = server.list()
        if typ == "OK":
            logging.info("Folders:")
            for f in folder_list:
                logging.info(f[f.find("\"/\" \"") + 4:])
        else:
            logging.error("list folders was not ok: %s", typ)
            server.logout()
            sys.exit(1)

    def __login_server(self, server, username, password):
        """
        logs in to server, if failure then exit
        """
        try:
            server.login(username, password)
        except Exception, e:
            if "Invalid credentials" in e[0]:
                logging.error("Invalid credentials cannot login")
                server.logout()
                sys.exit(1)
            else:
                raise Exception(e)
                server.logout()
                sys.exit(1)

    def _main(self):
        """
        get's automatically called from Memacs class
        """
        username = self._get_config_option("user")
        password = self._get_config_option("password")
        host = self._get_config_option("host")
        port = self._get_config_option("port")
        server = imaplib.IMAP4_SSL(host, int(port))        
        self.__login_server(server, username, password)
        if self._args.list_folders == True:
            self.__list_folders(server)
        else:
            self.__handle_folder(server, self._args.folder_name)
        server.logout()


if __name__ == "__main__":
    memacs = ImapMemacs(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS,
        use_config_parser_name=CONFIG_PARSER_NAME
        )
    memacs.handle_main()
