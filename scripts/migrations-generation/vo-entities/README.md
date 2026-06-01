# VO Entities Migration Generator

Reads `input.csv` (a semicolon-delimited export of Flemish government organisations from the Organisatieregister) and generates two SPARQL migration files under `config/migrations/2026/vo-entities/`:

- `*-insert-vo-classification.sparql` — inserts the *Vlaamse Overheid* `BestuurseenheidClassificatieCode` and links all bestuurseenheden to it via `org:classification`
- `*-insert-vo-bestuurseenheden.sparql` — inserts each organisation as a `besluit:Bestuurseenheid` with its OVO code (and KBO number if present) as `dct:identifier`; skips organisations already present in the triplestore (checked by OVO code)

## Run

```bash
python generate-vo-entities-migrations.py
```
