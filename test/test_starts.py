#!/usr/bin/env python3

import re
import unittest

from gexport import lines

class FileStartTest(unittest.TestCase):
    #       5/@xxxxxxxx00yy000cccc
    line = '5/@002411210012000MUCE'

    def test_parse(self):
        res = lines.file_start.search(self.line)
        self.assertEqual(res.group('IC'), '00241121')

class MothStartTest(unittest.TestCase):
    #       6/@xxxxxxxxyyzz_t_rrrr
    line = '6/@002411210100 2 2016'

    def test_parse(self):
        res = lines.month_start.search(self.line)
        self.assertEqual(res.group('IC'), '00241121')
        self.assertEqual(res.group('month'), '01')
        self.assertEqual(res.group('type'),  '00')
        self.assertEqual(res.group('input'),     '2')
        self.assertEqual(res.group('year'),  '2016')
