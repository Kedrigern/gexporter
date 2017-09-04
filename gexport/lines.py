#!/usr/bin/env python3
"""Define types of lines per regular expresion in kxx files for 56Gg format"""

import re

file_start = re.compile(''' # 5/@xxxxxxxx00yy000cccc
^5/@                        # začátek řetězce
(?P<IC> \d{8})00            # IC zpracovatelské organizace, pokud nemá IC, tak je to 10 místné
        \d{2}000            # Období (lze ignorovat)
        [a-zA-Z0-9]{4}      # Licence
$''', re.VERBOSE)

month_start = re.compile('''# 6/@xxxxxxxxyyzz_t_rrrr
^6/@                        # začátek řetězce
(?P<IC>     \d{8})          # IC uctující organizace, pokud není IČ, tak je to 10 místné
(?P<month>  \d{2})          # aktuální účetní období
(?P<type>   \d{2})          # druh dokladu, číselník je v enums.py
\ (?P<input>\d)\            # identifikator vstupu, číselník je v enums.py
(?P<year>   \d{4})          # účetní rok
$''', re.VERBOSE)

record = re.compile('''# G/@ddccccccccc000sssaaaakkoooooollllzzzuuuuuuuuujjjjjjjjjjgggggggggggggmmmmmmmmmmmmmmmmmm_dddddddddddddddddd_
^G/@                        # Start, účetní záznam
(?P<day>    \d{2})          # 0 Den zaúčtování
(?P<gid>    [ 0-9]{9})000    # 1 Číslo dokladu (a 3 nuly), P7 začíná číslo nulami pomocí mezer
(?P<su>     \d{3})          # 2 Syntetika (SU)
(?P<au>     \d{4})          # 3 Analytika (AU)
(?P<kap>    \d{2})          # 4 Kapiola (KAP)
(?P<odpa>   \d{6})          # 5 Oddíl, paragraf (ODPA)
(?P<pol>    \d{4})          # 6 Položka (POL)
(?P<zj>     \d{3})          # 7 Záznamová jednotka (ZJ)
(?P<uz>     \d{9})          # 8 Účelový znak (UZ)
(?P<orj>    \d{10})         # 9 Organizační jednotka
(?P<org>    \d{13})         # 10 Organizace
(?P<dat>    \d{16})         # 11 Má dáti
(?P<sdat>   \d{2})          # 12 Má dáti - haléře  TODO: lepší název
(?P<sig_dat> -|C|\ )        # 13 Má dáti - znamenéko, mezera: kladné, - nebo C záporné
(?P<dal>    \d{16})         # 14 Dal
(?P<sdal>   \d{2})          # 15 Dal - haléře
(?P<sig_dal> -|C|\ )        # 16 Dal - znaménko
$''', re.VERBOSE)

record_label = re.compile('''# G/$rrrrccccccccctttttttttttttttttttttttttttttttttttttttt...
^G/\$                       # Start, následuje vždy jen za G/@ (record)
(?P<line>   \d{4})          # 0 jednoznačné číslo řádky v dokladu v rámci dokladu
(?P<gid>   [ \d]{9})        # 1 číslo dokladu
(?P<text>  [\w -;:,*=\n]*)  # 2 text k řádku dokladu
''', re.VERBOSE)            # Konec řádku je \r\n, ale \n je ve výrazu => nelze doplnit $

global_label = re.compile('''# G/#rrrrcccccccccttttttttttttttttttttttttttttttttttttttt...
^G/\#                       # Start, následuje vždy jen za G/$ (record_label)
(?P<line>   \d{4})          # jednoznačné číslo řádky v dokladu v rámci dokladu
(?P<gid>   [ \d]{9})        # číslo dokladu
(?P<text>  [\w -/;:,*=\n]*) # text k řádku dokladu
''', re.VERBOSE)            # Konec řádku je \r\n, ale \n je ve výrazu => nelze doplnit $
