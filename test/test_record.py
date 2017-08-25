#!/usr/bin/env python3

import unittest

from gexport.record import Record

class ParseLongComment(unittest.TestCase):
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

    res = [
        {'partner': 'Ing. Novák Jan',
        'ic': None,
        'desc': None,
        'evk': 'DDP-2012DDP0008455',
        'modul': 'DDP',
        'evkt': 'FO - poplatky za komunální odpad:č.ev. 520',
        'pid': 'MUCEX0019T5J'},
        {'partner': 'Novák Jan',
        'ic': None,
        'desc': None,
        'evk': 'DDP-2014DDP0017662',
        'modul': 'DDP',
        'evkt': 'FO - poplatek ze psů:2039',
        'pid': 'MUCEX007ZYI'},
        {'partner': 'Novák Jan',
        'ic': None,
        'desc': None,
        'evk': 'DDP-2015DDP0021071',
        'modul': 'DDP',
        'evkt': 'OP - Dopravní přestupky:UPOMINKY',
        'pid': 'MUCEX00C6NYK'},
        {'partner': 'Novák Jan',
        'ic': None,
        'desc': 'Střežení objektu 2016 číslo sml. 197',
        'evk': 'KOF-20161604200101',
        'modul': 'KOF',
        'evkt': 'Střežení objektu 2016 číslo sml. 197',
        'pid': 'MUCEX00F1EN8'},
         {'partner': 'Novák Jan',
        'ic': None,
        'desc': 'pokuta + náklady',
        'evk': 'DDP-2015DDP0022941',
        'modul': 'DDP',
        'evkt': 'pokuta + náklady',
        'pid': 'MUCEX00EAZRT'},
        {'partner': 'FHU Europol',
        'ic': None,
        'desc': 'BIC: GIBAATWGXXX; #7',
        'evk': 'DDP-2015DDP0023010',
        'modul': 'DDP',
        'evkt': 'BIC: GIBAATWGXXX; #7',
        'pid': 'MUCEX00EFGFD'},
        {'partner': 'Povodí Vltavy, státní podnik',
        'ic': '70889953',
        'desc': None,
        'evk': 'DDP-2014DDP0019633',
        'modul': 'DDP',
        'evkt': 'FP915-INV-00852',
        'pid': 'MUCEX00A6I5I'},
        {'partner': None,
        'ic': None,
        'desc': 'Nespárovaná bankovní transakce  Příjem : 224000,00 Kč',
        'evk': None,
        'modul': None,
        'evkt': None,
        'pid': None},
        {'partner': None,
        'ic': None,
        'desc': 'Nespárovaná bankovní transakce  Příjem : 141000,00 Kč',
        'evk': 'UCT-2017201700390',
        'modul': 'UCT',
        'evkt': 'Nespárovaná bankovní transakce  Příjem : 141000,00 Kč',
        'pid': 'MUCEX00K69LB'}
    ]

    def test_parse_long_comment(self):
        error = "\nParse long comment for data {i} fails. Tuple:\n{t},\nRecord class: {r}"
        for i in range(0, len(self.comments)):
            #   gid    date  odpa  pol   orj   org dati dal comment, long comment, kap
            t = (0, None, 0, 0, 0, 0, 0, 0, "", self.comments[i], 0)
            r = Record( t )

            self.assertEqual(self.res[i]['partner'], r.partner, error.format(i=i, t=t, r=r))
            self.assertEqual(self.res[i]['ic'],      r.ic,      error.format(i=i, t=t, r=r))
            self.assertEqual(self.res[i]['desc'],    r.desc,    error.format(i=i, t=t, r=r))
            self.assertEqual(self.res[i]['evk'],     r.evk,     error.format(i=i, t=t, r=r))
            self.assertEqual(self.res[i]['modul'],   r.modul,   error.format(i=i, t=t, r=r))
            self.assertEqual(self.res[i]['evkt'],    r.evkt,    error.format(i=i, t=t, r=r))
            self.assertEqual(self.res[i]['pid'],     r.pid,     error.format(i=i, t=t, r=r))

class RecordClassTest(unittest.TestCase):

    r1 = (230000002, '2017-01-02', 6171, 5182, 911, 0, 0, 3000, '',
        '''*DICT-Brynychová Gabriela;*EVK-POK-201720170300002;\n*EVKT-POK_HLA_2012_PAP V:Brynychová-záloha na celý rok 2017,týkající se plateb ZPS;\n*PID-MC07X00L6QAJ;\n*DUD-00000001;\n*DICT-Hölzelová Petra;*EVK-POK-201720170300111;\n*EVKT-POK_HLA_2012_PAP V:provozní záloha  - Hölzelová Petra - RCN;*PID-MC07X00LCIN4;\n*DUD-00000001;\n*DICT-Jasińská Lenka;*EVK-POK-201720170300184;\n*EVKT-POK_HLA_2012_PAP V:Jasińská Lenka - záloha na občerstvení -školení APERTA;*PID-MC07X00LHJBS;\n*DUD-00000001;\n*IC-24202592;*DICT-8 minut s.r.o.;*EVK-POK-201720170300285;\n*EVKT-POK_HLA_2012_PAP P:Složení kauce - VS - 5500002251;*PID-MC07X00LQ8JK;\n*DUD-00000001;\n*DICT-Louthanová Alena;*EVK-POK-201720170300383;\n*EVKT-POK_HLA_2012_PAP V:Záloha, pí. Louthanová, 4.000,-Kč, honorář za čestnou stráž při pietním aktu dne 05.05. 2017, usn.č. 0363/17-R ze dne 18.04. 2017.;\n*PID-MC07X00LV71G;\n*DUD-00000001;\n*DICT-Hýblová Anna;*EVK-POK-201720170300489;\n*EVKT-POK_HLA_2012_PAP V:Odvod do ČS na č.ú.27 - vyúčtování zálohy - Hölzelová P.- provozní záloha;\n*PID-MC07X00M25HM;\n*DUD-00000001;\n*DICT-Fiala Jaroslav;*EVK-POK-201720170300597;\n*EVKT-POK_HLA_2012_PAP P:úhrada za kartu Multisport 7/2017;*PID-MC07X00M7ABO;\n*DUD-00000001;\n*DICT-Špaček Martin;*EVK-POK-201720170300693;\n*EVKT-POK_HLA_2012_PAP P:příjem peněz za stravenky - 6/2017;*PID-MC07X00MCJNG;\n*DUD-00000001;\n''',
        0)

    def test_construct(self):
        r = Record(self.r1)
        self.assertEqual(r.gid,  230000002)
        self.assertEqual(r.date, '2017-01-02')
        self.assertEqual(r.kap,  0)
        self.assertEqual(r.odpa, 6171)
        self.assertEqual(r.pol,  5182)
        self.assertEqual(r.orj,  911)
        self.assertEqual(r.org,  0)
        self.assertEqual(r.dati, 0)
        self.assertEqual(r.dal,  3000)
        self.assertEqual(r.partner,  'Brynychová Gabriela')
        self.assertEqual(r.evk,  'POK-201720170300002')
        self.assertEqual(r.evkt, 'POK_HLA_2012_PAP V:Brynychová-záloha na celý rok 2017,týkající se plateb ZPS')
        self.assertEqual(r.pid,  'MC07X00L6QAJ' )
        self.assertEqual(r.castka, 3000)
