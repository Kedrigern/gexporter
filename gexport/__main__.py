#!/usr/bin/env python3

from decimal import *

def main():
    pass

class GParser():
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

    def __init__(self, s):
        self.result = {}
        self.__one_record(s)

    def __parse_file(self, filename):
        with open(filename) as infile:
            self.__parse_fileobject(infile)

    def __parse_fileobject(self, infile):
        for line in infile:
            if line.startswith('G/@'):
                self.__one_record(line)

    def __one_record(self, s):
        self.result['para'] = int(s[self.para[0]: self.para[0]+self.para[1]])
        self.result['polo'] = int(s[self.polo[0]: self.polo[0]+self.polo[1]])
        self.result['zj']   = int(s[self.zj[0]: self.zj[0]+self.zj[1]])
        self.result['uz']   = int(s[self.uz[0]: self.uz[0]+self.uz[1]])
        self.result['orj']  = int(s[self.orj[0]: self.orj[0]+self.orj[1]])
        self.result['org']  = int(s[self.org[0]: self.org[0]+self.org[1]])
        self.__parse_amounts(s)

    def __parse_amounts(self, s):
        # TODO: decimal instead string
        self.result['amount1a'] = Decimal(s[self.amount1a[0]: self.amount1a[0]+self.amount1a[1]])
        self.result['amount1b'] = int(s[self.amount1b[0]: self.amount1b[0]+self.amount1b[1]])
        self.result['amount1'] = self.result['amount1a'] + Decimal(self.result['amount1b']) / Decimal(100)
        # TODO: decimal isntead string
        self.result['amount2a'] = Decimal(s[self.amount2a[0]: self.amount2a[0]+self.amount2a[1]])
        self.result['amount2b'] = int(s[self.amount2b[0]: self.amount2b[0]+self.amount2b[1]])
        self.result['amount2'] = self.result['amount2a'] + Decimal(self.result['amount2b']) / Decimal(100)

    def get_result(self):
        return self.result

class GParserUCT(GParser):
    pass

class GParserUCR(GParser):
    pass

if __name__ == '__main__':
    print('Hello world')
