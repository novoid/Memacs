# -*- coding: utf-8 -*-
# Time-stamp: <2019-11-06 15:24:33 vk>

import logging
import time
from email import message_from_string
from email.header import decode_header
from email.utils import parsedate

from orgformat import OrgFormat

from .orgproperty import OrgProperties


class MailParser(object):

    @staticmethod
    def get_value_or_empty_str(headers, key, remove_newline=False):
        """
        @param return: headers[key] if exist else ""
        """
        ret = ''
        if key in headers:
            ret = headers[key]
            if remove_newline:
                ret = ret.replace("\n", "")

            arr = []
            for item in decode_header(ret):
                value, charset = item

                if charset:
                    arr.append(value.decode(charset))
                else:
                    arr.append(value)

        return ' '.join(arr)

    @staticmethod
    def parse_message(message, add_body=False):
        """
        parses whole mail from string

        @param message: mail message
        @param add_body: if specified, body is added
        @return values for OrgWriter.write_org_subitem
        """

        msg = message_from_string(message)

        # Read only these fields
        use_headers = ["To",
                       "Date",
                       "From",
                       "Subject",
                       "Reply-To",
                       "Newsgroups",
                       "Cc",
                       ]
        # These fields are added, if found to :PROPERTIES: drawer
        not_properties = ["Date",
                          "Subject",
                          "From"
                          ]

        properties = OrgProperties()
        headers = {}

        logging.debug("Message items:")
        logging.debug(list(msg.items()))

        msg_id = None

        # fill headers and properties
        for key, value in list(msg.items()):
            value = value.replace("\r", "")
            if key in use_headers:
                headers[key] = value
                if key not in not_properties:
                    properties.add(key, MailParser.get_value_or_empty_str(headers, key, True))

            if key.upper() == "MESSAGE-ID":
                msg_id = value

        notes = ""
        # look for payload
        # if more than one payload, use text/plain payload
        if add_body:
            payload = msg.get_payload()
            if payload.__class__ == list:
                # default use payload[0]
                payload_msg = payload[0].get_payload()
                for payload_id in len(payload):
                    for param in payload[payload_id].get_params():
                        if param[0] == 'text/plain':
                            payload_msg = payload[payload_id].get_payload()
                            break
                    if payload_msg != payload[0].get_payload():
                        break
                notes = payload_msg
            else:
                notes = payload

        notes = notes.replace("\r", "")
        output_from = MailParser.get_value_or_empty_str(headers, "From")
        if output_from != "":
            output_from = OrgFormat.mailto_link(output_from)
        subject = MailParser.get_value_or_empty_str(headers, "Subject", True)

        dt = MailParser.get_value_or_empty_str(headers, "Date", False)
        timestamp = ""
        if dt != "":
            try:
                time_tuple = time.localtime(time.mktime(parsedate(dt)))
                timestamp = OrgFormat.date(time_tuple, show_time=True)
            except TypeError:
                logging.error("could not parse dateime from msg %s", dt)

        properties.add_data_for_hashing(timestamp + "_" + msg_id)

        if "Newsgroups" in headers:
            ng_list = []
            for ng in headers["Newsgroups"].split(","):
                ng_list.append(OrgFormat.newsgroup_link(ng))
            output_ng = ", ".join(map(str, ng_list))
            output = output_from + "@" + output_ng + ": " + subject
        else:
            output = output_from + ": " + subject

        return timestamp, output, notes, properties
