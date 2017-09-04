#!/usr/bin/env python3

import unittest
from decimal import *

from gexport import lines
from gexport.parsing import parse_record

class RecordParseTest(unittest.TestCase):
    s1 = 'G/@03120000264000231030100006171516800000000000900000010006171100000001000000000000000000 000000000003902206 '
    s2 = 'G/@03120000264000231030100006171516800000000000900000010006171100000001000000000000000000-000000000003902206-'
    s3 = 'G/@03120000264000231030100006171516800000000000900000010006171100000001000000000000000000C000000000003902206C'
    s4 = 'G/@01   080000000241001000000000000000000000000000000098000000000000000000000000000005400 000000000000000000 ' # From Praha 7

    def test_match(self):
        self.assertTrue(lines.record.match(self.s1))
        self.assertTrue(lines.record.match(self.s2))
        self.assertTrue(lines.record.match(self.s3))

    def test_parse_1(self):
        res = lines.record.search(self.s1)
        self.assertEqual(res.group('day'),  '03')
        self.assertEqual(res.group('gid'),  '120000264')
        self.assertEqual(res.group('su'),   '231')
        self.assertEqual(res.group('au'),   '0301')
        self.assertEqual(res.group('kap'),  '00')
        self.assertEqual(res.group('odpa'), '006171')
        self.assertEqual(res.group('pol'),  '5168')
        self.assertEqual(res.group('zj'),   '000')
        self.assertEqual(res.group('uz'),   '000000009')
        self.assertEqual(res.group('orj'),  '0000001000')
        self.assertEqual(res.group('org'),  '6171100000001')
        self.assertEqual(res.group('dat'),  '0000000000000000')
        self.assertEqual(res.group('sdat'), '00')
        self.assertEqual(res.group('sig_dat'),' ')
        self.assertEqual(res.group('dal'),  '0000000000039022')
        self.assertEqual(res.group('sdal'), '06')
        self.assertEqual(res.group('sig_dal'),' ')

    def test_parse_2(self):
        res = lines.record.search(self.s2)
        self.assertEqual(res.group('sig_dat'),'-')

    def test_parse_3(self):
        res = lines.record.search(self.s3)
        self.assertEqual(res.group('sig_dat'),'C')

    def test_parse_4(self):
        res = lines.record.search(self.s4)
        self.assertEqual(res.group('gid'), '   080000')

class RecordTest(unittest.TestCase):
    s1 = 'G/@03120000264000231030100006171516800000000000900000010006171100000001000000000000000000 000000000003902206 '
    s2 = 'G/@03120000264000231030100006171516800000000000900000010006171100000001000000000000000000-000000000003902206-'
    s4 = 'G/@01   080000000241001000000000000000000000000000000098000000000000000000000000000005400 000000000000000000 ' # From Praha 7

    def setUp(self):
        self.res = {}
        self.res2 = {}
        self.res4 = {}
        parse_record(self.res, self.s1)
        parse_record(self.res2, self.s2)
        parse_record(self.res4, self.s4)

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
        self.assertEqual(Decimal(0.0), self.res['amount1'])

    def test_amount1_neq(self):
        self.assertEqual(Decimal(-0.0), self.res2['amount1'])

    def test_amount2(self):
        self.assertEqual(Decimal("39022.06"), self.res['amount2'])

    def test_amount2_neq(self):
        self.assertEqual(Decimal("-39022.06"), self.res2['amount2'])
