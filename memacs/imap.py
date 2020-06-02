#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2012-09-06 19:54:04 armin>

import imaplib
import logging
import sys

from memacs.lib.mailparser import MailParser
from memacs.lib.memacs import Memacs


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
        """
        Fetches All headers, let Mailparser parse each mail,
        write to outputfile

        @param server: imaplib IMAP4_SLL object
        @param message_ids: list of ids to fetch
        @param folder_name: folder name of connection
        """
        num = ",".join(message_ids)

        logging.debug(num)
        typ, data = server.uid("fetch",
                               num,
                               "(BODY.PEEK[HEADER.FIELDS " + \
                                   "(Date Subject " + \
                                   "From To Cc Reply-To Message-ID)])")

        if typ == "OK":
            i = 0

            # we have to go in step 2 because every second string is a ")"
            for i in range(0, len(data), 2):
                message = data[i][1]
                timestamp, output, note, properties = \
                    MailParser.parse_message(message)

                # just for debbuging in orgfile
                # properties.add("NUM",data[i][0][:5])
                self._writer.write_org_subitem(timestamp,
                                               output,
                                               note,
                                               properties)

        else:
            logging.error("Could not fetch mails typ - %s", typ)
            server.logout(1)
            sys.exit(1)

    def __handle_folder(self, server, folder_name):
        """
        Selects the folder, gets all ids, and calls
        self.__fetch_mails_and_write(...)

        @param server: imaplib IMAP4_SLL object
        @param folder_name: folder to select
        """
        logging.debug("folder: %s", folder_name)

        # selecting the folder
        typ, data = server.select(folder_name)
        if typ != "OK":
            logging.error("could not select folder %s", folder_name)
            server.logout()
            sys.exit(1)

        # getting all
        typ, data = server.uid('search', None, 'ALL')
        if typ == "OK":
            message_ids = data[0].split()
            logging.debug("message_ids:%s", ",".join(message_ids))

            # if number_entries is set we have to adapt messages_ids
            if self._args.number_entries:
                if len(message_ids) > self._args.number_entries:
                    message_ids = message_ids[-self._args.number_entries:]

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

        @param server: imaplib IMAP4_SSL object
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
        @param server: imaplib IMAP4_SSL object
        @param username
        @param password
        """
        try:
            typ, dat = server.login(username, password)
            if typ != "OK":
                logging.warning("Could not log in")
                server.logout()
                sys.exit(1)
        except Exception as e:
            if "Invalid credentials" in e[0]:
                logging.error("Invalid credentials cannot login")
                server.logout()
                sys.exit(1)
            else:
                logging.warning("Could not log in")
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

        try:
            server = imaplib.IMAP4_SSL(host, int(port))
        except Exception as e:
            logging.warning("could not connect to server %s", host)
            sys.exit(1)

        self.__login_server(server, username, password)

        if self._args.list_folders == True:
            self.__list_folders(server)
        else:
            self.__handle_folder(server, self._args.folder_name)

        server.logout()
