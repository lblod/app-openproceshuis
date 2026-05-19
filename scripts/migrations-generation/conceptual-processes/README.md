# Conceptual Processes Migration Generator

Reads `input.xlsx` (sheet *5. Lijst (kritieke) processen*) and generates four paired Turtle + graph migration files under `config/migrations/2025/conceptual-processes/`:

- `*-add-process-categories.ttl` — inserts process categories as `skos:Concept` entries
- `*-add-process-domains.ttl` — inserts process domains, linked to their category
- `*-add-process-groups.ttl` — inserts process groups, linked to their domain
- `*-add-conceptual-processes.ttl` — inserts conceptual processes as `oph:ConceptueelProces`, linked to their group

Each `.ttl` file is accompanied by a `.graph` file that specifies the target named graph.

## Dependencies

```bash
pip install pandas openpyxl
```

## Run

```bash
python generate-conceptual-processes-migrations.py
```
