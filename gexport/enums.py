#!/usr/bin/env python3
"""Define enums"""
from enum import Enum

class LineType(Enum):
    N = 0   # None
    S = 1   # Start souboru
    M = 2   # Start měsíce
    R = 3   # Record
    c = 4   # Record comment (small)
    C = 5   # Global comment

type = {        # Druh dokladu
 0: 'běžný měsíc',
 1: 'počáteční stavy',
 2: 'rozpočet schválený',
 3: 'rozpočet upravený (interní)',
 4: 'závěrečné zápisy',
 5: 'uzavírací zápisy',
 6: 'blokace rozpočtu',
 7: 'rozpočet resortní',
 8: 'rozpočet vládní',
 9: 'požadavek na rozpočet'
}

input = {       # Identifikator vstupu
 0: 'připojí doklad k existujícímu dokladu',
 1: 'připojí doklad k existujícímu dokladu',
 2: 'přepíše existující doklad se stejnou licencí',
 3: 'přepíše existující doklad bez ohledu na licenci',
 4: 'před vstupem vymaže kompletní měsíční data',
 5: 'před vstupem vymaže kompletní měsíční data a po vstupu přepočte stavy',
 6: 'před vstupem vymaže data podle měsíce a druhu dokladu',
 7: 'před vstupem vymaže data podle měsíce a druhu dokladu a po vstupu přepočte stavy'
}
