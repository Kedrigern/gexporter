#!/usr/bin/env python3

import unittest

from gexport.lines import parse_invoice_id

class DescTest(unittest.TestCase):
    lid1 = 'G/$00015100001371601110102'
    lid2 = 'G/$00015100001381601100023'
    lid3 = 'G/$00015100001391601100025'
    id1 = 1601110102
    id2 = 1601100023
    id3 = 1601100025

    def test_id_1(self):
        x = parse_invoice_id(self.lid1)
        self.assertEqual(self.id1,x)

    def test_id_2(self):
        x = parse_invoice_id(self.lid2)
        self.assertEqual(self.id2,x)

    def test_id_3(self):
        x = parse_invoice_id(self.lid3)
        self.assertEqual(self.id3,x)
