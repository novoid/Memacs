#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import xml.etree.ElementTree as etree
from datetime import datetime
from lib.orgproperty import OrgProperties
from lib.orgformat import OrgFormat
from lib.memacs import Memacs
import re
import locale

class MuMail(Memacs):
        
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
           "-d", "--date",
           dest="search_time",
           help="specify startdate or daterange for email search")

        self._parser.add_argument(
           "-m", "--maildir_name",
           dest="maildir_name",
           help="name of mu folder to get emails from")

        self._parser.add_argument(
           "-f", "--flag",
           dest="flag",
           help="fetch only messages with flag")

        self._parser.add_argument(
           "-x", "--xaccount",
           dest="sender",
           help="fetch only messages send from specific mail account x")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)

        self._search_string = []
        self._flagged = False
        self._onlySent = None
        self._sender = ""
        if self._args.search_time:
            self._search_string.append("date:"+self._args.search_time)
            
        if self._args.flag:
            self._args.flag = "\""+self._args.flag+"\""
            self._search_string.append("flag:"+self._args.flag)
            print(self._args.flag)

        if self._args.sender:
            self._args.sendern = self._args.sender.strip()
            self._sender = self._args.sender.split(" ")

        if self._args.maildir_name:
            self._search_string.append("m:"+self._args.maildir_name)

        #self._search_string = self._search_string.strip()

    def __parse_Plain(self,plain_mails):
        messages = plain_mails.decode('utf-8')
        return messages.splitlines()

    def __getTimestamp(self, time, onlyDate=False):
        """
        converts xml timestamp into org readable timestamp
        Do  6 Nov 21:22:17 2014
        """
        time = time.strip().encode('utf-8')
        #time = time.replace("Okt","Oct")
        #time = time.replace("Dez","Dec")
        #time = time.replace("Mär","Mar")
        #time = time.replace("Mai","May")

        mail_date = datetime.strptime(time,"%a %d %b %H:%M:%S %Y")
        if onlyDate is False:
            return OrgFormat.datetime(mail_date)
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
            if name is not u"":
                return (u"[[mailto:" + mail + u"][" + name + u"]]",name,mail)
            else:
                return (u"[[mailto:" + mail + u"][" + mail + u"]]",name,mail)
        return (u"Unknown",u"Unknown",u"Unknown")
        
        
    def _main(self):
        """
        get's automatically called from Memacs class
        fetches all mails out of mu database
        """
        command = ["mu","find"]
        command.extend(self._search_string)
        command.extend(["--fields=t:#:d:#:f:#:g:#:s:#:i","--format=plain"])
        #xml_mails = subprocess.check_output(["mu", "find", self._search_string ,"--fields=t:#:d:#:f:#:g:#:s:#:i","--format=plain"])
        try:
            xml_mails = subprocess.check_output(command)
        except:
            print("something goes wrong")
            exit()
        messages = self.__parse_Plain(xml_mails)

        properties = OrgProperties()
        for message in messages:
            (an,datum,von,flags,betreff,msgid) = message.split(":#:")
            if flags.find('F') >= 0:
                self._flagged = True
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
                print(vmail)

                if self._flagged:
                    date = self.__getTimestamp(datum,True)
                    notes = "SCHEDULED: "+date
                    timestamp = ""
                    if  vmail in self._sender:
                        output = "".join(["WAITING T: ",an,": [[mu4e:msgid:",msgid,"][",betreff,"]]"])
                    else:
                        output = "".join(["NEXT F: ",sender,": [[mu4e:msgid:",msgid,"][",betreff,"]]"])
                else:
                    if  vmail in self._sender:
                        output = "".join(["T: ",an,": [[mu4e:msgid:",msgid,"][",betreff,"]]"])
                    else:
                        output = "".join(["F: ",sender,": [[mu4e:msgid:",msgid,"][",betreff,"]]"])
            self._writer.write_org_subitem(timestamp,
                                               output,
                                               notes,
                                               properties)


