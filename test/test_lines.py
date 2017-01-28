#!/usr/bin/env python3

import re
import unittest

from gexport import lines

class Num1Test(unittest.TestCase):
    line1 = '5/@002411210012000MUCE'
    line2 = '6/@002411210100 2 2016'

    def test_num1(self):
        self.assertTrue(re.match(lines.num1, self.line1))

    def test_num1_neq(self):
        self.assertFalse(re.match(lines.num2, self.line1))

    def test_num2(self):
        self.assertTrue(re.match(lines.num2, self.line2))

    def test_num2_neq(self):
        self.assertFalse(re.match(lines.num1, self.line2))

class RecordTest(unittest.TestCase):

    def test_record1(self):
        line = 'G/@19510000138000518030000000000000000000000000000000000000000000000000000000000003902206 000000000000000000 '
        self.assertTrue(re.match(lines.record1, line))

    def test_record1_neq(self):
        line = 'G/@19510000138000518030000000000000000000000000000000000000000000000000000000000003902206 000000000000000000 '
        self.assertFalse(re.match(lines.record2, line))

    def test_record2(self):
        line = 'G/@09        0000231000000003636536200000000000000000000000000000000000000000000000050000 000000000000000000 '
        self.assertTrue(re.match(lines.record2, line))

    def test_record2_neq(self):
        line = 'G/@09        0000231000000003636536200000000000000000000000000000000000000000000000050000 000000000000000000 '
        self.assertFalse(re.match(lines.record1, line))

class ShortTest(unittest.TestCase):
    line1 = 'G/$00015100001381601100023'
    line2 = 'G/$0001        0Storno rezervace'
    line3 = 'G/$0001000000001DDHM OISM'

    def test_short1(self):
        self.assertTrue(re.match(lines.short1, self.line1))

    def test_short2(self):
        self.assertTrue(re.match(lines.short2, self.line2))

    def test_short3(self):
        self.assertTrue(re.match(lines.short3, self.line3))

    def test_neq_1(self):
        self.assertFalse(re.match(lines.short1, self.line2))
        self.assertFalse(re.match(lines.short1, self.line3))

    def test_neq_2(self):
        self.assertFalse(re.match(lines.short2, self.line1))
        self.assertFalse(re.match(lines.short2, self.line3))

    def test_neq_3(self):
        #self.assertFalse(re.match(lines.short3, self.line1))
        self.assertFalse(re.match(lines.short3, self.line2))

class CommentTest(unittest.TestCase):
    comment = 'G/#0001510000138Smlouva GINIS 491/2012 MUCX - podpora SLA1 10-12/2015'
    dud = 'G/#0005510000137*DUD-00000001;'

    def test_comment(self):
        self.assertTrue(re.match(lines.comment, self.comment))

    def test_dud(self):
        self.assertTrue(re.match(lines.dud, self.dud))
