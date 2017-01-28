#!/usr/bin/env python3

import unittest

from gexport.lines import parse_comment

class DescTest(unittest.TestCase):

    empty = 'G/#0001120000264'
    line = 'G/#0001120000264Smlouva GINIS 491/2012 MUCX - podpora SLA1 10-12/2015'
    res = 'Smlouva GINIS 491/2012 MUCX - podpora SLA1 10-12/2015'

    def test_desc(self):
        x = parse_comment(self.line)
        self.assertEqual(self.res,x)

    def test_desc_empty(self):
        x = parse_comment(self.empty)
        self.assertEqual('',x)
