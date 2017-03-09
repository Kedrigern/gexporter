
# Parsování souborů kxx

Jedná se o speciální formát Gordicu (56Gg). Relevantní je soubor `uct`, kde je všechno. Tento soubor má v Černošicích za rok 2016 1 496 371 řádek. Doklad je na 5-10 řádek. Čísla jsou zarovnána nulami.

## Typy řádků

Jsou popsány v souboru `gexport/lines.py`, číselníky v `geexport/enums.py`

## Parsování

Řádky se záznamy dávám do SQLite tabulky record. Datum, má dáti a dal musím sestavit.
Poté následuje řádek s komentářem pro záznam, ten přidám k příslušnému řádku do DB.

Globální komentáře dávám do zvláštní tabulky.

Díky SQLite mám data následně přehledně uložená, mohu nad nimi dělat analytiku apod. A jsou připravena pro další zpracování.

### TODO

Některé měsíce se vyskytují víckrát. Jedná se o měsíce 1 a 3. Při prvním výskutu mají type 00 (běžný měsíc), při druhém 01 (počáteční stavy).

## Export

[MFČR]: http://www.ucetni-portal.cz/ciselnik-ucelovych-znaku-1168-a.html
