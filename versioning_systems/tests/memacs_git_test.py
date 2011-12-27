# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import unittest
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))
from versioning_systems.memacs_git import GitMemacs
from versioning_systems.memacs_git import Commit


class TestCommit(unittest.TestCase):

    def test_commit_empty(self):
        c = Commit()
        self.assertTrue(c.is_empty())

    def test_commit(self):
        c = Commit()
        c.add_header("author Armin Wieser <armin.wieser@example.com> " + \
                     "1324422878 +0100")
        c.add_body("i'm the subject")
        c.add_body("i'm in the body")

        output, properties, note, author = c.get_output()
        self.assertEqual(output, "Armin Wieser: i'm the subject")
        self.assertEqual(note, "i'm in the body\n")
        self.assertEqual(author, "Armin Wieser")

        p = u"""   :PROPERTIES:\n   :CREATED: <2011-12-21 Wed 00:14:38>
   :AUTHOR:   Armin Wieser <armin.wieser@example.com> 1324422878 +0100
   :END:"""
        self.assertEqual(unicode(properties), p)


class TestGitMemacs(unittest.TestCase):

    def setUp(self):
        self.test_file = os.path.dirname(os.path.abspath(__file__)) + \
            os.sep + "git-rev-list-raw.txt"

    def test_from_file(self):
        argv = "-s -f " + self.test_file
        memacs = GitMemacs(argv=argv.split(), append=True,
                           identifier="COMMIT")
        data = memacs.test_get_entries()

        # generate assertEquals :)
        #for d in range(len(data)):
        #    print "self.assertEqual(\n\tdata[%d],\n\t \"%s\")" % \
        #       (d, data[d])

        self.assertEqual(
            data[0],
             "** Armin Wieser: commenting memacs_git  + editing example")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :COMMITTER:      Armin Wieser <armin.wieser@" + \
             "gmail.com> 1324423850 +0100")
        self.assertEqual(
            data[3],
             "   :PARENT:         6fb35035c5fa7ead66901073413a42742a323e89")
        self.assertEqual(
            data[4],
             "   :CREATED:       <2011-12-21 Wed 00:30:50>")
        self.assertEqual(
            data[5],
             "   :AUTHOR:         Armin Wieser <armin.wieser@" + \
             "gmail.com> 1324423850 +0100")
        self.assertEqual(
            data[6],
             "   :TREE:           6b3361c8919f432432048c0f54b4b3fab9eb5039")
        self.assertEqual(
            data[7],
             "   :SIGNED-OFF-BY: Armin Wieser <armin.wieser@" + \
             "gmail.com>")
        self.assertEqual(
            data[8],
             "   :COMMIT:         17b5cb8bc085b2dbfbab6832f056d653e3ef80b6")
        self.assertEqual(
            data[9],
             "   :END:")
        self.assertEqual(
            data[10],
             "** Armin Wieser: PEP8")
        self.assertEqual(
            data[11],
             "   :PROPERTIES:")
        self.assertEqual(
            data[12],
             "   :COMMITTER:      Armin Wieser <armin.wieser@g" + \
             "mail.com> 1324422878 +0100")
        self.assertEqual(
            data[13],
             "   :PARENT:         05ba138e6aa1481db2c815ddd2acb52d3597852f")
        self.assertEqual(
            data[14],
             "   :CREATED:       <2011-12-21 Wed 00:14:38>")
        self.assertEqual(
            data[15],
             "   :AUTHOR:         Armin Wieser <armin.wieser@" + \
             "gmail.com> 1324422878 +0100")
        self.assertEqual(
            data[16],
             "   :TREE:           7027c628031b3ad07ad5401991f5a12aead8237a")
        self.assertEqual(
            data[17],
             "   :SIGNED-OFF-BY: Armin Wieser <armin.wieser@" + \
             "gmail.com>")
        self.assertEqual(
            data[18],
             "   :COMMIT:         6fb35035c5fa7ead66901073413a42742a323e89")
        self.assertEqual(
            data[19],
             "   :END:")
        self.assertEqual(
            data[20],
             "** Armin Wieser: fixing tests + removing unessesary whitespaces")
        self.assertEqual(
            data[21],
             "   :PROPERTIES:")
        self.assertEqual(
            data[22],
             "   :COMMITTER:      Armin Wieser <armin.wieser@" + \
             "gmail.com> 1324422620 +0100")
        self.assertEqual(
            data[23],
             "   :PARENT:         4adc838fa8d3a4862f8db3eaf9b0f18c20d6352b")
        self.assertEqual(
            data[24],
             "   :CREATED:       <2011-12-21 Wed 00:10:20>")
        self.assertEqual(
            data[25],
             "   :AUTHOR:         Armin Wieser <armin.wieser@" + \
             "gmail.com> 1324422620 +0100")
        self.assertEqual(
            data[26],
             "   :TREE:           ddfe30d853aaa1c9f5af305f208a34150a85ff4c")
        self.assertEqual(
            data[27],
             "   :SIGNED-OFF-BY: Armin Wieser <armin.wieser@gmail.com>")
        self.assertEqual(
            data[28],
             "   :COMMIT:         05ba138e6aa1481db2c815ddd2acb52d3597852f")
        self.assertEqual(
            data[29],
             "   :END:")
        self.assertEqual(
            data[30],
             "** Armin Wieser: fixing tests")

    def test_number_entries_all(self):
        argv = "-s -f " + self.test_file
        memacs = GitMemacs(argv=argv.split(), append=True,
                           identifier="COMMIT")
        data = memacs.test_get_entries()
        self.assertEqual(len(data), 1081)  # 1081 commits in sum

    def test_number_entries_grep(self):
        argv = '-s -f ' + self.test_file
        argv = argv.split()
        argv.append("-g")
        argv.append("Armin Wieser")
        memacs = GitMemacs(argv=argv, append=True,
                           identifier="COMMIT")
        data = memacs.test_get_entries()
        self.assertEqual(len(data), 686)  # 686 commits from Armin Wieser
