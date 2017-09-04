#!/usr/bin/env python3

import unittest

from gexport import lines

class RecordLabelTest(unittest.TestCase):
    t1 = 'G/$00015100001381601100023'
    t2 = 'G/$0001100000001od 22.12.2015,podle'
    t3 = 'G/$0001        0Změna drd'

    def test_match(self):
        self.assertTrue(lines.record_label.match(self.t1))
        self.assertTrue(lines.record_label.match(self.t2))
        self.assertTrue(lines.record_label.match(self.t3))
