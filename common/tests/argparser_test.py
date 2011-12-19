import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.argparser import MemacsArgumentParser

class TestArgParser(unittest.TestCase):
    def setUp(self):
        self.prog_version = "0.1"                
        self.prog_version_date = "2011-12-19"   
        self.description = "descriptionbla"
        self.parser = MemacsArgumentParser(
            prog_version=self.prog_version,
            description=self.description,
            prog_version_date=self.prog_version_date)
        self.TMPFOLDER = os.path.normpath(os.path.dirname(os.path.abspath(__file__))
                                           + os.path.sep + "tmp") + os.sep
        if not os.path.exists(self.TMPFOLDER):
            os.makedirs(self.TMPFOLDER)
    def test_verbose(self):
        """
        testing MemacsArgumentParser's argument verbose
        """
        args = self.parser.parse_args('-v'.split())
        args2 = self.parser.parse_args('--verbose'.split())
        
        self.assertEqual(args, args2, "-v and --verbose do different things")
        self.assertEqual(args.outputfile, None, "verbose - args.outputfile should be None")
        self.assertEqual(args.suppressmessages, False, "verbose - args.suppressmessages should be False")
        self.assertEqual(args.verbose, True, "verbose - args.verbose should be True")
        
    def test_suppress(self):
        """
        testing MemacsArgumentParser's suppress-messages
        """
        args = self.parser.parse_args('-s'.split())
        args2 = self.parser.parse_args('--suppress-messages'.split())
        
        self.assertEqual(args, args2, "-s and --suppress-messages do different things")
        self.assertEqual(args.outputfile, None, "suppressmessages - args.outputfile should be None")
        self.assertEqual(args.suppressmessages, True, "suppressmessages - args.suppressmessages should be True")
        self.assertEqual(args.verbose, False, "suppressmessages - args.verbose should be False")

    
    def test_outputfile(self):
        #args = self.parser.parse_args('-o'.split())
        outputfile_path = self.TMPFOLDER + "outputfile"
        outputfile_argument = "-o " + outputfile_path
        outputfile_argument2 = "--output " + outputfile_path
        args = self.parser.parse_args(outputfile_argument.split())
        args2 = self.parser.parse_args(outputfile_argument2.split())
        self.assertEqual(args, args2, "-o and --output do different things")
        
    def test_nonexistingoutputdir(self):
        outputfile_path = self.TMPFOLDER + "NONEXISTING" + os.sep + "outputfile"
        outputfile_argument = "-o " + outputfile_path
        
        try:
            args = self.parser.parse_args(outputfile_argument.split())
            self.assertTrue(False, "parsing was correct altough nonexisting outputfile")
        except SystemExit:
            pass

    def test_verbose_suppress_both(self):
        try:
            args = self.parser.parse_args('-s -v'.split())
            self.assertTrue(False, "parsing was correct altough both suppress and verbose was specified")
        except SystemExit:
            pass
