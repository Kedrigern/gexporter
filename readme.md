
# Gexport

Parsování prostých textových souborů `kxx` používaných k exportu účetnictví.

## Unit tests

```
python3 -m unittest
```

## Formát

Export je ve formátu `kxx` ve dvou souborech. V jednom je účetnictví (samotné transakce) v druhém je rozpočet.

My potřebujeme:

-  **Rozpočet** – strom příjmů a výdajů dle paragrafů, kde bude vždy schválený/upravený rozpočet a jaký je stav čerpání až do detailu akce
- **Akce (ORJ)** – statická data o investičních akcích (název a ID, příp. souřadnice)
- **Rozpočet akcí**, tj. strom výdajů a rozpočtu na akci dle paragrafů
- **Faktury** – Jednotlivé doklady k akcím apod.

### Rozpočet (UCR)

```
                                5168            0000001000
G/@03120000264000231030100006171516800000000000900000010006171100000001000000000000000000 000000000003902206
                        |    § ||po|   |   UZ  || ORJ    ||   ORG     |                          39022,06 Kč
                            6171       000000009          6171100000001                              3902206
```

| Název          | Délka |  Poznámka                                                                          |
|----------------|------:|------------------------------------------------------------------------------------|
| Paragraf       |     6 |                                                                                    |
| Položka        |     4 |                                                                                    |
| Záznamová jednotka | 3 | |
| Učelový znak   |     9 | např. dotační dělení, popř. přenesená/samostatná působnost, dle číselníku [MFČR][] |
| ORJ            |    10 | organizační jednotka - dle číselníku účetní jednotky                               |
| ORG            |    13 | organizace - dle číselníku účetní jednotky                                         |
| Částka         |       | Je potřeba rozlišit desetinná místa a číslo                                        |


### Účetnictví (UCT)

```
G/@01000000001000231000000006171516800000000000900000010006171100000001000000000000000000 000000000354300000
G/@01000000001000231000000000000111100000000000100000009006171090000000000000001390000000 000000000000000000
```

| Co                 | Délka |    1. řádek   |    2. řádek   |
|--------------------|------:|--------------:|--------------:|
| Paragraf           |   4   |          6171 |          0000 |
| Položka            |   4   |          5168 |          1111 |
| Záznamová jednotka |   3   |           000 |           000 |
| Účelový znak       |   9   |     000000009 |     000000001 |
| ORJ                |  10   |    0000001000 |    0000000900 |
| ORG                |  13   | 6171100000001 | 6171090000000 |
| Částka - má dáti   |  17+2 |          0.00 |  3,543,000.00 |
| Částka - dal       |  17+2 | 13,900,000.00 |          0.00 |

[MFČR]: http://www.ucetni-portal.cz/ciselnik-ucelovych-znaku-1168-a.html
