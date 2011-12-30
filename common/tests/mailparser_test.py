import unittest
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))))
from common.mailparser import MailParser


class TestMailParser(unittest.TestCase):
    
    def test_parse_mail_without_body(self):
        message = """Date: Wed, 28 Dec 2011 14:02:00 +0100
From: Alice Ally <alice@ally.com>
To: Bob Bobby <Bob@bobby.com>
Subject: Bob sends a mesage
Message-ID: f2c1165a321d0e0@foo.com
X-Scanned-By: MIMEDefang 2.71 on 129.27.10.2

Hi!

Hope you can read my message

kind reagards, 
Bob        
        """
        timestamp, output, notes, properties = MailParser.parse_message(message)
        
        self.assertEqual(timestamp, "<2011-12-28 Wed 14:02>")
        self.assertEqual(output, "[[mailto:alice@ally.com][Alice Ally]]: ")
        self.assertEqual(notes, "")
        p="""   :PROPERTIES:
   :TO:         Bob Bobby <Bob@bobby.com>
   :ID:         f2c1165a321d0e0@foo.com
   :END:"""
        
        self.assertEqual(unicode(properties), p)
        
    
    def test_parse_mail_with_body(self):
        message = """Date: Wed, 28 Dec 2011 14:02:00 +0100
From: Alice Ally <alice@ally.com>
To: Bob Bobby <Bob@bobby.com>
Subject: Bob sends a mesage
Message-ID: f2c1165a321d0e0@foo.com
X-Scanned-By: MIMEDefang 2.71 on 129.27.10.2

Hi!

Hope you can read my message

kind reagards, 
Bob        
        """
        timestamp, output, notes, properties = \
            MailParser.parse_message(message,
                                     True)
        
        self.assertEqual(timestamp, "<2011-12-28 Wed 14:02>")
        self.assertEqual(output, "[[mailto:alice@ally.com][Alice Ally]]: ")
        self.assertEqual(notes, "Hi!\n\nHope you can read my message\n" + \
                            "\nkind reagards, \nBob        \n        ")
        p="""   :PROPERTIES:
   :TO:         Bob Bobby <Bob@bobby.com>
   :ID:         f2c1165a321d0e0@foo.com
   :END:"""
        
        self.assertEqual(unicode(properties), p)
        
    