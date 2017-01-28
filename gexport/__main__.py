#!/usr/bin/env python3

import re
import sys

from . import lines
from . import record

def loop_count(infile):
    """Count of lines in file"""
    i = 0
    for line in infile:
        i += 1
    print(i)

def loop_stats(infile):
    """Primitive stats about lines"""
    i = 0
    for line in infile:
        i += 1
        if re.match(lines.num1, line):
            print('1', end='')
        elif re.match(lines.num2, line):
            print('2')
        elif re.match(lines.record1, line):
            print('R', end='')
        elif re.match(lines.short1, line):
            print('s', end='')
        elif re.match(lines.dud, line):
            print('|')
        elif re.match(lines.record2, line):
            print('x')
        elif re.match(lines.short2, line) or re.match(lines.short3, line):
            print('.', end='')
        elif re.match(lines.comment, line):
            print('c', end='')
        else:
            print('?|%s|\n' % line, end='')

def loop_parse(infile):
    """Extracts data from kxx files"""
    ids = set([])
    records = []
    previous = None
    find_id=True
    find_dud=True
    find_record=False
    find_comment=False
    i = 0
    res = {}

    for line in infile:
        i += 1
        if find_id and re.match(lines.short1, line):
            id = lines.parse_invoice_id(line)
            if id in ids:
                res = {}        # clean previous data
                res['id'] = id  # add invoice id
                record.parse_record(res, previous)
                find_comment = True
                find_dud = False
                find_id = False
            else:
                ids.add(id)
                find_id = False
                find_comment = False
                find_dud = True
        if find_dud and re.match(lines.dud, line):
            find_id = True
            find_dud = False
            find_comment = False
        if find_comment and re.match(lines.comment, line):
            res['comment'] = lines.parse_comment(line)
            records.append(res)
            find_dud = True
            find_comment = False
        previous = line
    print(records)

def main():
    filename = 'test/data.kxx'
    with open(filename, encoding="cp1250") as infile:
        loop_stats(infile)
        #loop_parse(infile)

if __name__ == '__main__':
    sys.exit(main())
