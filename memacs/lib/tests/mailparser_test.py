# -*- coding: utf-8 -*-
# Time-stamp: <2011-12-30 12:16:47 armin>

import unittest
from memacs.lib.mailparser import MailParser


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
        timestamp, output, notes, properties = \
            MailParser.parse_message(message)

        self.assertEqual(timestamp, "<2011-12-28 Wed 14:02>")
        self.assertEqual(output, "[[mailto:alice@ally.com]" + \
                         "[Alice Ally]]: Bob sends a mesage")
        self.assertEqual(notes, "")
        self.assertEqual(
            properties.get_value('TO'), 'Bob Bobby <Bob@bobby.com>'
        )
        for key in ('FROM', 'SUBJECT', 'DATE', 'MESSAGE-ID', 'X-SCANNED-BY'):
            with self.assertRaises(KeyError):
                properties.get_value(key)

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
Bob"""
        timestamp, output, notes, properties = \
            MailParser.parse_message(message,
                                     True)

        self.assertEqual(timestamp, "<2011-12-28 Wed 14:02>")
        self.assertEqual(output, "[[mailto:alice@ally.com]" + \
                         "[Alice Ally]]: Bob sends a mesage")
        self.assertEqual(notes, "Hi!\n\nHope you can read my message\n" + \
                            "\nkind reagards,\nBob")
        self.assertEqual(
            properties.get_value('TO'), 'Bob Bobby <Bob@bobby.com>'
        )
        for key in ('FROM', 'SUBJECT', 'DATE', 'MESSAGE-ID', 'X-SCANNED-BY'):
            with self.assertRaises(KeyError):
                properties.get_value(key)

    def test_parse_ng_with_body(self):
        message = """Path: news.tugraz.at!not-for-mail
From: Alice Ally <alice@ally.com>
Newsgroups: tu-graz.betriebssysteme.linux
Subject: I love Memacs
Date: Thu, 17 Nov 2011 22:02:06 +0100
Message-ID: <2011-11-17T21-58-27@ally.com>
Reply-To: news@ally.com
Content-Type: text/plain; charset=utf-8

i just want to say that i love Memacs
"""
        timestamp, output, notes, properties = \
            MailParser.parse_message(message,
                                     True)

        self.assertEqual(timestamp, "<2011-11-17 Thu 22:02>")
        self.assertEqual(output,
                         "[[mailto:alice@ally.com][Alice Ally]]@[[news:tu-" + \
                         "graz.betriebssysteme.linux]" + \
                         "[tu-graz.betriebssysteme.linux]]: I love Memacs")
        self.assertEqual(notes, "i just want to say that i love Memacs\n")
        self.assertEqual(
            properties.get_value('NEWSGROUPS'), 'tu-graz.betriebssysteme.linux'
        )
        self.assertEqual(
            properties.get_value('REPLY-TO'), 'news@ally.com'
        )
        for key in ('FROM', 'SUBJECT', 'DATE', 'MESSAGE-ID', 'CONTENT-TYPE'):
            with self.assertRaises(KeyError):
                properties.get_value(key)
