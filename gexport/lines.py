#!/usr/bin/env python3
"""Define types of lines per regular expresion in kxx files"""

import re

# Numbered line (je jich málo)
# 5/@002411210012000MUCE
num1 = r'^[0-9]/@[0-9]{15}[A-Z]{4}$'
# 6/@002411210100 2 2016
num2 = r'^[0-9]/@[0-9]{12} [0-9] [0-9]{4}$'
# Record line (záznam transakce)
# G/@19510000138000518030000000000000000000000000000000000000000000000000000000000003902206 000000000000000000
record1 = r'^G/@[0-9]{86}[ -][0-9]{18}[ -]$'
# ???
record2 = r'^G/@[0-9]{2}[ ]{8}[0-9]{76}[ -][0-9]{18}[ -]$'
# Short line (z ní parsuji číslo dokladu)
# G/$00015100001381601100023
short1 = r'^G/\$[0-9]{23}$'
short2 = r'^G/\$[0-9]{4}[ ]{8}' # G/$0001        0Storno rezervace
# Type line (skladba)
# G/$0001000000001DDHM OISM
# G/$0001000000001knihy, tisk
short3 = r'^G/\$[0-9]{13}'
# DUD line (oddělovač)
# G/#0005510000137*DUD-00000001;
dud = r'^G/#[0-9]{13}\*DUD-[0-9]{8};$'
# Comment line
# G/#0001510000138Smlouva GINIS 491/2012 MUCX - podpora SLA1 10-12/2015
comment = r'^G/#[0-9]{13}'


def parse_invoice_id(line):
    if not re.match(short1, line):
        raise Exception("Not invoice id line")
    return int(line[16:26])

def parse_comment(line):
    if re.match(dud, line):
        raise Exception("Try parse DUD as comment")
    if not re.match(comment, line):
        raise Exception("Not comment line")
    return line[16:]
