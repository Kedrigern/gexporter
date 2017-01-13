
# Gexport

Parsování prostých textových souborů `kxx` používaných k exportu účetnictví.

## Formát

```
                                5168            0000001000
G/@03120000264000231030100006171516800000000000900000010006171100000001000000000000000000 000000000003902206
                            |§ ||po|   |   UZ  || ORJ    ||   ORG     |                          39022,06 Kč
                            6171       000000009          6171100000001                              3902206
```

| Název    | Délka |  Poznámka          |
|----------|------:|--------------------|
| Paragraf |     4 |                    |
| Položka  |     4 |                    |
| UZ       |     9 |                    |
| ORJ      |    10 |                    |
| ORG      |    13 |                    |
| Částka   |       | Je potřeba rozlišit desetinná místa a číslo |
