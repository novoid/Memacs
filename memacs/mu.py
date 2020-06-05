#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
import re
import subprocess
from datetime import datetime

from orgformat import OrgFormat

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties

# Sets this script's locale to be the same as system locale
locale.setlocale(locale.LC_TIME, '')

class MuMail(Memacs):

    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
           "-q", "--query",
           dest="query",
           help="mu search query")

        self._parser.add_argument(
           "-m", "--me",
           dest="sender",
           help="space seperated list of mail addresses that belongs to you")

        self._parser.add_argument(
            "-d", "--delegation",
            dest="todo",
            action='store_true',
            help="adds NEXT or WAITING state to flagged messages")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs
        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)

        self._query = []

        if self._args.sender:
            self._args.sendern = self._args.sender.strip()
            self._sender = list(self._args.sender.split(" "))
        else:
            raise ValueError('You have to specify at least one e mail adress')

        if self._args.query:
            self._query = self._args.query

        if self._args.todo:
            self._todo = True
        else:
            self._todo = False

    def __parse_Plain(self,plain_mails):
        messages = plain_mails.decode('utf-8')
        return messages.splitlines()

    def __getTimestamp(self, time, onlyDate=False):
        """
        converts xml timestamp into org readable timestamp
        Do  6 Nov 21:22:17 2014
        """
        time = time.strip()

        mail_date = datetime.strptime(time,"%c")
        if onlyDate is False:
            return OrgFormat.date(mail_date, show_time=True)
        return OrgFormat.date(mail_date)

    def __create_mail_link(self, sender):
        """
        creates well formated org mail link from message 'from' field.
        """
        rex = re.compile('([\w\s.,-]*?)[\s<"]*([\w.-]+@[\w.-]+)',re.UNICODE)
        m = rex.search(sender)
        if m:
            name = m.group(1).strip()
            mail = m.group(2).strip()
            if name is not "":
                return ("[[mailto:" + mail + "][" + name + "]]",name,mail)
            else:
                return ("[[mailto:" + mail + "][" + mail + "]]",name,mail)
        return ("Unknown","Unknown","Unknown")


    def _main(self):
        """
        get's automatically called from Memacs class
        fetches all mails out of mu database
        """
        command = self._query
        # command.extend(self._query)
        command = command+" --fields=t:#:d:#:f:#:g:#:s:#:i --format=plain"
        try:
            xml_mails = subprocess.check_output(command, shell=True)
        except:
            print("something goes wrong")
            exit()
        messages = self.__parse_Plain(xml_mails)

        properties = OrgProperties()
        for message in messages:
            (an,datum,von,flags,betreff,msgid) = message.split(":#:")
            betreff = betreff.replace("[","<")
            betreff = betreff.replace("]",">")
            properties.add('TO',an)
            if von != "":
                (sender,vname,vmail) = self.__create_mail_link(von)
                (an,aname,amail) = self.__create_mail_link(an)
                timestamp = self.__getTimestamp(datum)
                properties.add_data_for_hashing(timestamp + "_" + msgid)
                properties.add("FROM",sender)
                notes = ""
                if any(match in vmail for match in self._sender):
                    output = output = "".join(["T: ",an,": [[mu4e:msgid:",msgid,"][",betreff,"]]"])
                    pre = 'WAITING '
                else:
                    output = "".join(["F: ",sender,": [[mu4e:msgid:",msgid,"][",betreff,"]]"])
                    pre = 'NEXT '
                if (flags.find('F') >= 0 and self._todo):
                    date = self.__getTimestamp(datum,True)
                    notes = "SCHEDULED: "+date
                    timestamp = ""
                    output = pre+output
            self._writer.write_org_subitem(timestamp, output, notes, properties)
