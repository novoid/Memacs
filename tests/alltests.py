#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2011-10-26 22:13:31 awieser>

import unittest
from tests.common.test_outputwriter import TestOutputWriter


def main():
    unittest.TestLoader.loadTestsFromTestCase(TestOutputWriter)    
    
if __name__ == "__main__":
    main()