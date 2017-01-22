#!/usr/bin/env python3

import unittest
from decimal import *

from gexport.__main__ import GParserUCR

class UCRtest1(unittest.TestCase):

    s1 = 'G/@01000000001000231000000006171516800000000000900000010006171100000001000000000000000000 000000000354300000'

    def setUp(self):
        uct = GParserUCR(self.s1)
        self.res = uct.get_result()

    def test_para(self):
        self.assertEqual(6171, self.res['para'])

    def test_polo(self):
        self.assertEqual(5168, self.res['polo'])

    def test_zj(self):
        self.assertEqual(0, self.res['zj'])

    def test_uz(self):
        self.assertEqual(9, self.res['uz'])

    def test_orj(self):
        self.assertEqual(1000, self.res['orj'])

    def test_org(self):
        self.assertEqual(6171100000001, self.res['org'])

    def test_amount1(self):
        self.assertEqual(Decimal("0000000000000000"), self.res['amount1a'])
        self.assertEqual(0, self.res['amount1b'])
        self.assertEqual(Decimal("0.0"), self.res['amount1'])

    def test_amount2(self):
        self.assertEqual(Decimal("0000000003543000"), self.res['amount2a'])
        self.assertEqual(0, self.res['amount2b'])
        self.assertEqual(Decimal("3543000.0"), self.res['amount2'])

class UCRtest2(unittest.TestCase):
    s2 = 'G/@01000000001000231000000000000111100000000000100000009006171090000000000000001390000000 000000000000000000'

    def setUp(self):
        uct = GParserUCR(self.s2)
        self.res = uct.get_result()

    def test_para(self):
        self.assertEqual(0000, self.res['para'])

    def test_polo(self):
        self.assertEqual(1111, self.res['polo'])

    def test_zj(self):
        self.assertEqual(0, self.res['zj'])

    def test_uz(self):
        self.assertEqual(1, self.res['uz'])

    def test_orj(self):
        self.assertEqual(900, self.res['orj'])

    def test_org(self):
        self.assertEqual(6171090000000, self.res['org'])

    def test_amount1(self):
        self.assertEqual(Decimal("0000000013900000"), self.res['amount1a'])
        self.assertEqual(0, self.res['amount1b'])

    def test_amount2(self):
        self.assertEqual(Decimal("0000000000000000"), self.res['amount2a'])
        self.assertEqual(0, self.res['amount2b'])
