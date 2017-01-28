#!/usr/bin/env python3

import unittest
from decimal import *

from gexport.record import parse_record

class UCTtest(unittest.TestCase):
    s1 = 'G/@03120000264000231030100006171516800000000000900000010006171100000001000000000000000000 000000000003902206'

    def setUp(self):
        self.res = {}
        uct = parse_record(self.res, self.s1)

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
        self.assertEqual(Decimal(0), self.res['amount1a'])
        self.assertEqual(0, self.res['amount1b'])
        self.assertEqual(Decimal(0.0), self.res['amount1'])

    def test_amount2(self):
        self.assertEqual(Decimal("0000000000039022"), self.res['amount2a'])
        self.assertEqual(Decimal(39022), self.res['amount2a'])
        self.assertEqual(6, self.res['amount2b'])
        self.assertEqual(Decimal("39022.06"), self.res['amount2'])
