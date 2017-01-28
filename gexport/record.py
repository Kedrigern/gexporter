#!/usr/bin/env python3
"""Parsing of one transaction record"""

from decimal import *

# (starts at, size, zerofill)
para = (26, 6)
polo = (32, 4)
zj =   (36, 3)  # zerofill
uz =   (39, 9)  # zerofill
orj =  (48, 10)
org =  (58, 13)
amount1a = (71, 16)
amount1b = (88, 2)
amount2a = (90, 16)
amount2b = (106, 2)

def parse_record(result, s):
    result['para'] = int(s[para[0]: para[0]+para[1]])
    result['polo'] = int(s[polo[0]: polo[0]+polo[1]])
    result['zj']   = int(s[zj[0]: zj[0]+zj[1]])
    result['uz']   = int(s[uz[0]: uz[0]+uz[1]])
    result['orj']  = int(s[orj[0]: orj[0]+orj[1]])
    result['org']  = int(s[org[0]: org[0]+org[1]])
    parse_amounts(result, s)

def parse_amounts(result, s):
    # TODO: decimal instead string
    result['amount1a'] = Decimal(s[amount1a[0]: amount1a[0]+amount1a[1]])
    result['amount1b'] = int(s[amount1b[0]: amount1b[0]+amount1b[1]])
    result['amount1'] = result['amount1a'] + Decimal(result['amount1b']) / Decimal(100)
    # TODO: decimal isntead string
    result['amount2a'] = Decimal(s[amount2a[0]: amount2a[0]+amount2a[1]])
    result['amount2b'] = int(s[amount2b[0]: amount2b[0]+amount2b[1]])
    result['amount2'] = result['amount2a'] + Decimal(result['amount2b']) / Decimal(100)
