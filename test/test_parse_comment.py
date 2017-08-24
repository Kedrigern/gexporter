#!/usr/bin/env python3

import unittest

from gexport.__main__ import parse_long_comment

class ParseCommentTest(unittest.TestCase):
    comments = [ # Comments string with some metadata
    """
    *DICT-Ing. Novák Jan;*EVK-DDP-2012DDP0008455;*EVKT-FO - poplatky za komunální odpad:č.ev. 520;*PID-MUCEX0019T5J;*DUD-00000001;
    """, # 0
    """
    *DICT-Novák Jan;*EVK-DDP-2014DDP0017662;*EVKT-FO - poplatek ze psů:2039;*PID-MUCEX007ZYI; *DUD-00000001
    """, # 1
    """
    *DICT-Novák Jan;*EVK-DDP-2015DDP0021071;*EVKT-OP - Dopravní přestupky:UPOMINKY;*PID-MUCEX00C6NYK;*DUD-00000001;
    """, # 2
    """
    Střežení objektu 2016 číslo sml. 197 *DICT-Novák Jan;*EVK-KOF-20161604200101;*EVKT-Střežení objektu 2016 číslo sml. 197; *PID-MUCEX00F1EN8; *DUD-00000001;
    """, # 3
    """
    pokuta + náklady *DICT-Novák Jan;*EVK-DDP-2015DDP0022941;*EVKT-pokuta + náklady;*PID-MUCEX00EAZRT;*DUD-00000001;
    """, # 4
    """
    BIC: GIBAATWGXXX; #7 *DICT-FHU Europol;*EVK-DDP-2015DDP0023010;*EVKT-BIC: GIBAATWGXXX; #7;*PID-MUCEX00EFGFD;*DUD-00000001;
    """, # 5
    """
    *IC-70889953;*DICT-Povodí Vltavy, státní podnik;*EVK-DDP-2014DDP0019633;*EVKT-FP915-INV-00852;*PID-MUCEX00A6I5I;*DUD-00000001;
    """, # 6
    """
    Nespárovaná bankovní transakce  Příjem : 224000,00 Kč *DUD-00000001;
    """, # 7
    """
    Nespárovaná bankovní transakce  Příjem : 141000,00 Kč*EVK-UCT-2017201700390;*PID-MUCEX00K69LB;*EVKT-Nespárovaná bankovní transakce  Příjem : 141000,00 Kč*DUD-00000001;
    """]

    def test_parse(self):
        data = []
        for i in range(0, len(self.comments)):
            data.append(parse_long_comment(self.comments[i]))

        self.assertEqual(data[0], {'partner': 'Ing. Novák Jan',
            'ic': None,
            'desc': None,
            'evk': 'DDP-2012DDP0008455',
            'modul': 'DDP',
            'evkt': 'FO - poplatky za komunální odpad:č.ev. 520',
            'pid': 'MUCEX0019T5J'})

        self.assertEqual(data[1], {'partner': 'Novák Jan',
            'ic': None,
            'desc': None,
            'evk': 'DDP-2014DDP0017662',
            'modul': 'DDP',
            'evkt': 'FO - poplatek ze psů:2039',
            'pid': 'MUCEX007ZYI'})

        self.assertEqual(data[2], {'partner': 'Novák Jan',
            'ic': None,
            'desc': None,
            'evk': 'DDP-2015DDP0021071',
            'modul': 'DDP',
            'evkt': 'OP - Dopravní přestupky:UPOMINKY',
            'pid': 'MUCEX00C6NYK'})

        self.assertEqual(data[3], {'partner': 'Novák Jan',
            'ic': None,
            'desc': 'Střežení objektu 2016 číslo sml. 197',
            'evk': 'KOF-20161604200101',
            'modul': 'KOF',
            'evkt': 'Střežení objektu 2016 číslo sml. 197',
            'pid': 'MUCEX00F1EN8'})

        self.assertEqual(data[4], {'partner': 'Novák Jan',
            'ic': None,
            'desc': 'pokuta + náklady',
            'evk': 'DDP-2015DDP0022941',
            'modul': 'DDP',
            'evkt': 'pokuta + náklady',
            'pid': 'MUCEX00EAZRT'})

        self.assertEqual(data[5], {'partner': 'FHU Europol',
            'ic': None,
            'desc': 'BIC: GIBAATWGXXX; #7',
            'evk': 'DDP-2015DDP0023010',
            'modul': 'DDP',
            'evkt': 'BIC: GIBAATWGXXX; #7',
            'pid': 'MUCEX00EFGFD'})

        self.assertEqual(data[6], {'partner': 'Povodí Vltavy, státní podnik',
            'ic': '70889953',
            'desc': None,
            'evk': 'DDP-2014DDP0019633',
            'modul': 'DDP',
            'evkt': 'FP915-INV-00852',
            'pid': 'MUCEX00A6I5I'})

        self.assertEqual(data[7], {'partner': None,
            'ic': None,
            'desc': 'Nespárovaná bankovní transakce  Příjem : 224000,00 Kč',
            'evk': None,
            'modul': None,
            'evkt': None,
            'pid': None}, 'data[7] fail')

        self.assertEqual(data[8], {'partner': None,
            'ic': None,
            'desc': 'Nespárovaná bankovní transakce  Příjem : 141000,00 Kč',
            'evk': 'UCT-2017201700390',
            'modul': 'UCT',
            'evkt': 'Nespárovaná bankovní transakce  Příjem : 141000,00 Kč',
            'pid': 'MUCEX00K69LB'}, 'data[8] fail')
