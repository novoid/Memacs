# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-30 00:30:57 armin>

import time
import logging
from email import message_from_string
from email.utils import parsedate
from common.orgproperty import OrgProperties
from common.orgformat import OrgFormat


class MailHandler(object):
    pass

    @staticmethod
    def handle_message(message,
                       add_body=False):

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
        logging.debug(msg.items())

        # fill headers and properties
        for key, value in msg.items():
            value = value.replace("\r","")
            if key in use_headers:
                headers[key] = value
                if key not in not_properties:
                    properties.add(key, value.replace("\n",""))
            if key == "Message-ID":
                properties.set_id(value)

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

        output_from = ""
        if "From" in headers:
            output_from = OrgFormat.contact_mail_mailto_link(headers["From"])

        time_tupel = time.localtime(time.mktime(parsedate(headers["Date"])))
        timestamp = OrgFormat.datetime(time_tupel)

        subject = ""
        if "Subject" in headers:
            subject = headers["Subject"].replace("\n","")

        if "Newsgroups" in headers:
            ng_list = []
            for ng in headers["Newsgroups"].split(","):
                ng_list.append(OrgFormat.newsgroup_link(ng))
            output_ng = ", ".join(map(str, ng_list))
            output = output_from + "@" + output_ng + ": " + subject
        else:
            output = output_from + ": " + subject

        return timestamp, output, notes, properties
