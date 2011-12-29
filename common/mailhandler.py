from email import message_from_string
from email.utils import parsedate
from common.orgproperty import OrgProperties
from common.orgformat import OrgFormat
import logging
import time

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
                       "Newsgroups"]
        
        # These fields are added to :PROPERTIES: drawer
        headers_to_properties = ["To"]
        
        properties = OrgProperties()
        data_for_hashing = ""
        headers = {}
        
        logging.debug("Message items:")
        logging.debug(msg.items())
        
        # fill headers and properties, and set data_for_hashing
        for key, value in msg.items():
            if key in use_headers:
                headers[key] = value
                if key in headers_to_properties:
                    properties.add(key, value)
                data_for_hashing += key + value
        
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
        
        notes = notes.replace("\r","")
        
        output_from = OrgFormat.contact_mail_mailto_link(headers["From"])
        
        time_tupel = time.gmtime(time.mktime(parsedate(headers["Date"])))
        timestamp = OrgFormat.datetime(time_tupel)
        
        if headers.has_key("Newsgroups"):
            ng_list = []
            for ng in headers["Newsgroups"].split(","):
                ng_list.append(OrgFormat.newsgroup_link(ng))
            output_ng = ", ".join(map(str,ng_list))
            output = output_from + "@" + output_ng + ": " + headers["Subject"]
        else:
            output = output_from + ": " + headers["Subject"] 
        
        return timestamp, output, notes, properties 
