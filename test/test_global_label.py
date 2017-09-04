#!/usr/bin/env python3

import unittest

from gexport import lines

class RecordLabelTest(unittest.TestCase):
    t1 = 'G/#0001510000138Smlouva GINIS 491/2012 MUCX - podpora SLA1 10-12/2015'
    t2 = 'G/#0001100000011ěščřžýáíéů'
    t3 = 'G/#0001100000011:;=-.'
    t4 = 'G/#0001100000011line1\nline2'
    t5 = 'G/#0001   080000*DUD-00000001;'

    def test_match(self):
        self.assertTrue(lines.global_label.match(self.t1))
        self.assertTrue(lines.global_label.match(self.t2), "Chars: ěščřžýáíéů in global label")
        self.assertTrue(lines.global_label.match(self.t3), "Chars: :;=-. in Global label")
        self.assertTrue(lines.global_label.match(self.t4), "Newline in Global label")
        self.assertTrue(lines.global_label.match(self.t5), "Spaces in gid")
