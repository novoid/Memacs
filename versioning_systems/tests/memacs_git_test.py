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

        output, properties, note = c.get_output()
        self.assertEqual(output, "Armin Wieser: i'm the subject")
        self.assertEqual(note, "i'm in the body\n")

        p = """  :PROPERTIES:
  :AUTHOR:  Armin Wieser <armin.wieser@example.com> 1324422878 +0100
  :CREATED: <2011-12-21 Wed 00:14:38>
  :END:"""

        self.assertEqual(unicode(properties), p)
        print


class TestGitMemacs(unittest.TestCase):

    def test_from_file(self):
        test_file = os.path.dirname(os.path.abspath(__file__)) + \
            os.sep + "git-rev-list-raw.txt"
        argv = "-s -f " + test_file
        memacs = GitMemacs(argv=argv.split())
        data = memacs.test_get_entries()

        # generate assertEquals :)
        # for d in range(len(data)):
        #     print "self.assertEqual(data[%d], \"%s\")" % \
        #        (d, data[d])

        self.assertEqual(
            data[1],
            "  :PROPERTIES:")
        self.assertEqual(
            data[2],
            "  :COMMIT:        17b5cb8bc085b2dbfbab6832f056d653e3ef80b6")
        self.assertEqual(
            data[3],
            "  :TREE:          6b3361c8919f432432048c0f54b4b3fab9eb5039")
        self.assertEqual(
            data[4],
            "  :PARENT:        6fb35035c5fa7ead66901073413a42742a323e89")
        self.assertEqual(
            data[5],
            "  :AUTHOR:        Armin Wieser <armin.wieser@" + \
            "gmail.com> 1324423850 +0100")
        self.assertEqual(
            data[6],
            "  :CREATED:       <2011-12-21 Wed 00:30:50>")
        self.assertEqual(
            data[7],
            "  :COMMITTER:     Armin Wieser <armin.wieser@" + \
            "gmail.com> 1324423850 +0100")
        self.assertEqual(
            data[9],
            "  :END:")
        self.assertEqual(
            data[10],
            "** Armin Wieser: PEP8")
        self.assertEqual(
            data[11],
            "  :PROPERTIES:")
        self.assertEqual(
            data[12],
            "  :COMMIT:        6fb35035c5fa7ead66901073413a42742a323e89")
        self.assertEqual(
            data[13],
            "  :TREE:          7027c628031b3ad07ad5401991f5a12aead8237a")
        self.assertEqual(
            data[14],
            "  :PARENT:        05ba138e6aa1481db2c815ddd2acb52d3597852f")
        self.assertEqual(
            data[15],
            "  :AUTHOR:        Armin Wieser <armin.wieser@" + \
            "gmail.com> 1324422878 +0100")
        self.assertEqual(
            data[16],
            "  :CREATED:       <2011-12-21 Wed 00:14:38>")
        self.assertEqual(
            data[17],
            "  :COMMITTER:     Armin Wieser <armin.wieser@" + \
            "gmail.com> 1324422878 +0100")
        self.assertEqual(
            data[19],
            "  :END:")
