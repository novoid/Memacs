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

    def test_ID_empty(self):
        c = Commit()
        self.assertTrue(c.is_empty())

    def test_ID(self):
        c = Commit()
        c.add_header("author Armin Wieser <armin.wieser" + \
                     "@example.com> 1324422878 +0100")
        c.add_body("i'm the subject")
        c.add_body("i'm in the body")

        output, properties, note, author = c.get_output()
        self.assertEqual(output, "Armin Wieser: i'm the subject")
        self.assertEqual(note, "i'm in the body\n")
        self.assertEqual(author, "Armin Wieser")

        p = "   :PROPERTIES:\n"
        p += "   :CREATED: <2011-12-21 Wed 00:14:38>\n"
        p += "   :AUTHOR:  Armin Wieser <armin.wieser@example.com>"
        p += " 1324422878 +0100\n"
        p += "   :ID:      2d0b1b4a127e7e81c510c4bd16ea249408a7e6aa\n"
        p += "   :END:"

        self.assertEqual(unicode(properties), p)


class TestGitMemacs(unittest.TestCase):

    def setUp(self):
        self.test_file = os.path.dirname(os.path.abspath(__file__)) + \
            os.sep + "git-rev-list-raw.txt"

    def test_from_file(self):
        argv = "-s -f " + self.test_file
        memacs = GitMemacs(argv=argv.split(), append=True)
        data = memacs.test_get_entries()

        # generate assertEquals :)
        #for d in range(len(data)):
        #    print "self.assertEqual(\n\tdata[%d],\n\t \"%s\")" % \
        #       (d, data[d])
        self.assertEqual(
            data[0],
             "** Karl Voit: corrected cron-info for OS X")
        self.assertEqual(
            data[1],
             "   :PROPERTIES:")
        self.assertEqual(
            data[2],
             "   :COMMITTER: Karl Voit <git" + \
             "@example.com> 1321699855 +0100")
        self.assertEqual(
            data[3],
             "   :PARENT:    62f20271b87e8574370f1ded29938dad0313a399")
        self.assertEqual(
            data[4],
             "   :CREATED:   <2011-11-19 Sat 11:50:55>")
        self.assertEqual(
            data[5],
             "   :AUTHOR:    Karl Voit <git" + \
             "@example.com> 1321699855 +0100")
        self.assertEqual(
            data[6],
             "   :TREE:      0c785721ff806d2570cb7d785adf294b0406609b")
        self.assertEqual(
            data[7],
             "   :COMMIT:    052ffa660ce1d8b0f9dd8f8fc794222e2463dce1")
        self.assertEqual(
            data[8],
             "   :ID:        76395e98e385f546a09c3db358cc3d5a4b4221a5")
        self.assertEqual(
            data[9],
             "   :END:")
        self.assertEqual(
            data[10],
             "** Karl Voit: added RSS module description")
        self.assertEqual(
            data[11],
             "   :PROPERTIES:")
        self.assertEqual(
            data[12],
             "   :COMMITTER: Karl Voit <git" + \
             "@example.com> 1321699830 +0100")
        self.assertEqual(
            data[13],
             "   :PARENT:    638e81c55daf0a69c78cc3af23a9e451ccea44ab")
        self.assertEqual(
            data[14],
             "   :CREATED:   <2011-11-19 Sat 11:50:30>")
        self.assertEqual(
            data[15],
             "   :AUTHOR:    Karl Voit <git" + \
             "@example.com> 1321699830 +0100")
        self.assertEqual(
            data[16],
             "   :TREE:      906b8b7e4bfd08850aef8c15b0fc4d5f6e9cc9a7")
        self.assertEqual(
            data[17],
             "   :COMMIT:    62f20271b87e8574370f1ded29938dad0313a399")
        self.assertEqual(
            data[18],
             "   :ID:        7c12d1ead7176aed0f8cdbf72f1837ba9a9c165c")
        self.assertEqual(
            data[19],
             "   :END:")
        self.assertEqual(
            data[20],
             "** Armin Wieser: added Orgformate.date()")
        self.assertEqual(
            data[21],
             "   :PROPERTIES:")
        self.assertEqual(
            data[22],
             "   :COMMITTER:     Armin Wieser <armin.wieser" + \
             "@example.com> 1320270366 +0100")
        self.assertEqual(
            data[23],
             "   :PARENT:        7ddaa9839611662c5c0dbf2bb2740e362ae4d566")
        self.assertEqual(
            data[24],
             "   :CREATED:       <2011-11-02 Wed 22:46:06>")
        self.assertEqual(
            data[25],
             "   :AUTHOR:        Armin Wieser <armin.wieser" + \
             "@example.com> 1320270366 +0100")
        self.assertEqual(
            data[26],
             "   :TREE:          2d440e6b42b917e9a69d5283b9d1ed4a77797ee9")
        self.assertEqual(
            data[27],
             "   :SIGNED-OFF-BY: Armin Wieser <armin.wieser" + \
             "@example.com>")
        self.assertEqual(
            data[28],
             "   :COMMIT:        9b4523b2c4542349e8b4ca3ca595701a50b3c315")
        self.assertEqual(
            data[29],
             "   :ID:            9064b3363d7ef522c695e38eeb1a80f09b161acf")
        self.assertEqual(
            data[30],
             "   :END:")
        self.assertEqual(
            data[31],
             "** Armin Wieser: orgformat added for orgmode-syntax")
        self.assertEqual(
            data[32],
             "   :PROPERTIES:")
        self.assertEqual(
            data[33],
             "   :COMMITTER:     Armin Wieser <armin.wieser" + \
             "@example.com> 1320260312 +0100")
        self.assertEqual(
            data[34],
             "   :PARENT:        f845d8c1f1a4194e3b27b5bf39bac1b30bd095f6")
        self.assertEqual(
            data[35],
             "   :CREATED:       <2011-11-02 Wed 19:58:32>")
        self.assertEqual(
            data[36],
             "   :AUTHOR:        Armin Wieser <armin.wieser" + \
             "@example.com> 1320260312 +0100")
        self.assertEqual(
            data[37],
             "   :TREE:          663a7c370b985f3b7e9794dec07f28d4e6ff3936")

    def test_number_entries_all(self):
        argv = "-s -f " + self.test_file
        memacs = GitMemacs(argv=argv.split(), append=True)
        data = memacs.test_get_entries()
        self.assertEqual(len(data), 120)  # 120 lines in sum

    def test_number_entries_grep(self):
        argv = '-s -f ' + self.test_file
        argv = argv.split()
        argv.append("-g")
        argv.append("Armin Wieser")
        memacs = GitMemacs(argv=argv, append=True)
        data = memacs.test_get_entries()
        self.assertEqual(len(data), 100)  # 100 lines from Armin Wieser
