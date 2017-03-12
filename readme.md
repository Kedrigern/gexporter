
# Gexport

Parsování prostých textových souborů `kxx` (56Gg) používaných k exportu účetnictví.

[![Build Status](https://travis-ci.org/Kedrigern/gexporter.svg?branch=master)](https://travis-ci.org/Kedrigern/gexporter)

## Spuštění

Pouze test souboru, vygeneruje schéma souboru:
```
python3 -m gexport validate [-o <outfile.txt>] <infile.kxx>
```

Parsování:
```
python3 -m gexport parse [-r|--raw] [-o <outfile.csv>] <infile.kxx>
```

Spuštění unittestů programu:

```
python3 -m unittest
```

## Cílový formát

Podrobný [popis parsování](parsovani.md).

Naparsováním získáme SQLite všech záznamů. To se hodí pro analytiku apod.

| Název         |
|---------------|
| DOKLAD_ROK    |
| DOKLAD_DATUM  |
| DOKLAD_AGENDA |
| DOKLAD_CISLO  |
| ORJ           |
| PARAGRAF      |
| POLOZKA       |
| SUBJEKT_IC    |
| SUBJEKT_NAZEV |
| CASTKA        |
| POZNAMKA      |

A číselníky orj a org.

## TODO

- zkusit parsovat oboje
- meziroční srovnání akcí
  - potvrzování stejných čísel
  - ruční napojení rozdílných čísel
- články
- investiční mapa
