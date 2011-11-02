
import unittest
from common.orgformat import OrgFormat


class TestOrgFormat(unittest.TestCase):
    
    def test_link(self):
        """
        test Org links
        """
        self.assertEqual("[[/link/][description]]", OrgFormat.link("/link/", "description"), "format error link+description")
        self.assertEqual("[[/link/]]", OrgFormat.link("/link/"), "format error link")
        self.assertEqual("[[/link%20link/]]", OrgFormat.link("/link link/"), "quote error")

    def test_date(self):
        """
        test Org date
        """
        
        date = OrgFormat.date(year=2011,
                                        month=11,
                                        day=02,
                                        hour=11,
                                        minute=12)
        self.assertEqual("<2011-11-02 11:12>",date,"date error")
        