#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-29 15:38:01 armin>

import sys
import os
import logging
import imaplib
# needed to import common.*
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.memacs import Memacs
from common.reader import CommonReader
from common.mailhandler import MailHandler


PROG_VERSION_NUMBER = u"0.0"
PROG_VERSION_DATE = u"2011-12-18"
PROG_SHORT_DESCRIPTION = u"Memacs for ... "
PROG_TAG = u"emails:imap"
PROG_DESCRIPTION = u"""
this class will do ....

Then an Org-mode file is generated that contains ....
"""
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
           help="name of folder to get emails from" + \
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

    def __fetch_mail(self, server, num):
        typ, data = server.fetch(num,
            "(BODY[HEADER.FIELDS " + \
            "(Date Subject From To Cc Reply-To Message-ID)])")
        if typ == "OK":
            message = data[0][1]
            timestamp, output, note, properties = \
                MailHandler.handle_message(message)

            self._writer.write_org_subitem(timestamp,
                                           output,
                                           note,
                                           properties)
        else:
            logging.error("Could not fetch mail number:%d, typ - %s", num, typ)

    def __handle_folder(self, server, folder_name):
        logging.debug("folder")
        server.select(folder_name)
        typ, data = server.search(None, 'ALL')
        if typ == "OK":
            messages_ids = data[0].split()
            for num in messages_ids:
                self.__fetch_mail(server, num)
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

    def _main(self):
        """
        get's automatically called from Memacs class
        """

        data = CommonReader.get_data_from_file("/tmp/pw.txt").splitlines()
        username = data[0]
        password = data[1]

        server = imaplib.IMAP4_SSL('imap.gmail.com')
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
        copyright_authors=COPYRIGHT_AUTHORS
        )
    memacs.handle_main()
