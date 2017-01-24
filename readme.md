
# Gexport

Parsování prostých textových souborů `kxx` používaných k exportu účetnictví.

## Unit tests

```
python3 -m unittest
```

## Formát

Export je ve formátu `kxx` ve dvou souborech. V jednom je účetnictví (samotné transakce) v druhém je rozpočet.

Podrobný [popis parsování](parsovani.md).

My potřebujeme:

-  **Rozpočet** – strom příjmů a výdajů dle paragrafů, kde bude vždy schválený/upravený rozpočet a jaký je stav čerpání až do detailu akce
- **Akce (ORJ)** – statická data o investičních akcích (název a ID, příp. souřadnice)
- **Rozpočet akcí**, tj. strom výdajů a rozpočtu na akci dle paragrafů
- **Faktury** – Jednotlivé doklady k akcím apod.

## TODO

- meziroční srovnání akcí
  - potvrzování stejných čísel
  - ruční napojení rozdílných čísel
- články
- investiční mapa
