# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-28 15:13:31 aw>

import unittest
import os
from memacs.git import GitMemacs
from memacs.git import Commit


class TestCommit(unittest.TestCase):

    def test_ID_empty(self):
        c = Commit()
        self.assertTrue(c.is_empty())

    def test_ID(self):
        c = Commit()
        c.add_header("author Armin Wieser <armin.wieser" + \
                     "@example.com> 1324422878 +0100")
        c.add_body("i'm the subject")
        c.add_body("i'm in the body")

        output, properties, note, author, timestamp = c.get_output()
        self.assertEqual(output, "Armin Wieser: i'm the subject")
        self.assertEqual(note, "i'm in the body\n")
        self.assertEqual(author, "Armin Wieser")
        self.assertEqual(timestamp, "<2011-12-21 Wed 00:14>")

        #for p in unicode(properties).splitlines():
        #    print "\"" + p + "\\n\""
        p = "   :PROPERTIES:\n"
        p += "   :AUTHOR:     Armin Wieser <armin.wieser@example.com> " + \
        "1324422878 +0100\n"
        p += "   :ID:         2bcf0df19183b508b7d52e38ee1d811aabd207f5\n"
        p += "   :END:"

        self.assertEqual(str(properties), p)


class TestGitMemacs(unittest.TestCase):

    def setUp(self):
        self.test_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data', 'git-rev-list-raw.txt'
        )

    def test_from_file(self):
        argv = "-s -f " + self.test_file
        memacs = GitMemacs(argv=argv.split())
        data = memacs.test_get_entries()

        self.assertEqual(
            data[0],
             "** <2011-11-19 Sat 11:50> Karl Voit:" + \
             " corrected cron-info for OS X")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :COMMIT:     052ffa660ce1d8b0f9dd8f8fc794222e2463dce1")
        self.assertEqual(
            data[3],
             "   :TREE:       0c785721ff806d2570cb7d785adf294b0406609b")
        self.assertEqual(
            data[4],
             "   :PARENT:     62f20271b87e8574370f1ded29938dad0313a399")
        self.assertEqual(
            data[5],
             "   :AUTHOR:     Karl Voit <git@example." + \
             "com> 1321699855 +0100")

        self.assertEqual(
            data[6],
             "   :COMMITTER:  Karl Voit <git@example.com> 1321699855" + \
             " +0100")
        self.assertEqual(
            data[7],
             "   :ID:         e77d956db6f5720f6b30e2d7fd608807c7a75f9f")
        self.assertEqual(
            data[8],
             "   :END:")
        self.assertEqual(
            data[9],
             "** <2011-11-19 Sat 11:50> Karl Voit: added RSS " + \
             "module description")
        self.assertEqual(
            data[10],
             "   :PROPERTIES:")
        self.assertEqual(
            data[11],
             "   :COMMIT:     62f20271b87e8574370f1ded29938dad0313a399")
        self.assertEqual(
            data[12],
             "   :TREE:       906b8b7e4bfd08850aef8c15b0fc4d5f6e9cc9a7")
        self.assertEqual(
            data[13],
             "   :PARENT:     638e81c55daf0a69c78cc3af23a9e451ccea44ab")
        self.assertEqual(
            data[14],
             "   :AUTHOR:     Karl Voit <git@example.com> 132" + \
             "1699830 +0100")
        self.assertEqual(
            data[15],
             "   :COMMITTER:  Karl Voit <git@example.c" + \
             "om> 1321699830 +0100")
        self.assertEqual(
            data[16],
             "   :ID:         d5f45fc44e23a7f042d56e09ccfe7772614afe97")
        self.assertEqual(
            data[17],
             "   :END:")
        self.assertEqual(
            data[18],
             "** <2011-11-02 Wed 22:46> Armin Wieser: add" + \
             "ed Orgformate.date()")
        self.assertEqual(
            data[19],
             "   :PROPERTIES:")
        self.assertEqual(
            data[20],
             "   :COMMIT:        9b4523b2c4542349e8b4ca3ca595701a50b3c315")
        self.assertEqual(
            data[21],
             "   :TREE:          2d440e6b42b917e9a69d5283b9d1ed4a77797ee9")
        self.assertEqual(
            data[22],
             "   :PARENT:        7ddaa9839611662c5c0dbf2bb2740e362ae4d566")
        self.assertEqual(
            data[23],
             "   :AUTHOR:        Armin Wieser <armin.wieser@ex" + \
             "ample.com> 1320270366 +0100")
        self.assertEqual(
            data[24],
             "   :COMMITTER:     Armin Wieser <armin.wieser@" + \
             "example.com> 1320270366 +0100")
        self.assertEqual(
            data[25],
             "   :SIGNED-OFF-BY: Armin Wieser <armin.wieser@example.com>")
        self.assertEqual(
            data[26],
             "   :ID:            8c806b9e28cacb7bb540fc921a0bda15b34289ee")
        self.assertEqual(
            data[27],
             "   :END:")
        self.assertEqual(
            data[28],
             "** <2011-11-02 Wed 19:58> Armin Wieser: orgf" + \
             "ormat added for orgmode-syntax")
        self.assertEqual(
            data[29],
             "   :PROPERTIES:")
        self.assertEqual(
            data[30],
             "   :COMMIT:        7ddaa9839611662c5c0dbf2bb2740e362ae4d566")
        self.assertEqual(
            data[31],
             "   :TREE:          663a7c370b985f3b7e9794dec07f28d4e6ff3936")
        self.assertEqual(
            data[32],
             "   :PARENT:        f845d8c1f1a4194e3b27b5bf39bac1b30bd095f6")
        self.assertEqual(
            data[33],
             "   :AUTHOR:        Armin Wieser <armin.wieser@" + \
             "example.com> 1320260312 +0100")
        self.assertEqual(
            data[34],
             "   :COMMITTER:     Armin Wieser <armin.wieser@e" + \
             "xample.com> 1320260312 +0100")
        self.assertEqual(
            data[35],
             "   :SIGNED-OFF-BY: Armin Wieser <armin.wieser@example.com>")
        self.assertEqual(
            data[36],
             "   :ID:            50d3dd0e8c02857c5ceff3c04bff732a2ad67d04")
        self.assertEqual(
            data[37],
             "   :END:")

    def test_number_entries_all(self):
        argv = "-s -f " + self.test_file
        memacs = GitMemacs(argv=argv.split())
        data = memacs.test_get_entries()
        self.assertEqual(len(data), 109)  # 109 lines in sum

    def test_number_entries_grep(self):
        argv = '-s -f ' + self.test_file
        argv = argv.split()
        argv.append("-g")
        argv.append("Armin Wieser")
        memacs = GitMemacs(argv=argv)
        data = memacs.test_get_entries()
        self.assertEqual(len(data), 91)  # 91 lines from Armin Wieser
