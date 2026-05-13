import csv
import re
import uuid
from datetime import datetime
from pathlib import Path

INPUT_FILEPATH = "export_20260423_110049.csv"
INPUT_COLS = {
    "Organisatie ID": "id",
    "Organisatienaam": "name",
    "organisationKboNumber": "kbo",
    "ovoKey": "ovo",
}

OUTPUT_FILEPATH = "../config/migrations/2026/vo-entities/"

PREFIXES = [
    "PREFIX mu: <http://mu.semte.ch/vocabularies/core/>",
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
    "PREFIX besluit: <http://data.vlaanderen.be/ns/besluit#>",
    "PREFIX skos: <http://www.w3.org/2004/02/skos/core#>",
    "PREFIX dct: <http://purl.org/dc/terms/>",
    "PREFIX org: <http://www.w3.org/ns/org#>",
]

TARGET_GRAPH = "http://mu.semte.ch/graphs/public"

BESTUURSEENHEID_BASE_URI = "http://data.lblod.info/id/bestuurseenheden/"

UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def derive_uuid(org_id: str) -> str:
    if UUID_RE.match(org_id):
        return org_id.lower()
    return str(uuid.uuid4())


def escape_str(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def read_rows() -> list[dict]:
    col_map = INPUT_COLS
    rows = []
    with open(INPUT_FILEPATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for raw in reader:
            row = {alias: raw.get(col, "").strip() for col, alias in col_map.items()}
            if row["id"] and row["ovo"]:
                rows.append(row)
    return rows


def build_triple(row: dict) -> str:
    entity_uuid = derive_uuid(row["id"])
    uri = f"{BESTUURSEENHEID_BASE_URI}{entity_uuid}"
    name = escape_str(row["name"])

    lines = [
        f"<{uri}>",
        f'  mu:uuid "{entity_uuid}" ;',
        "  rdf:type besluit:Bestuurseenheid ;",
        f'  skos:prefLabel "{name}" ;',
        f'  dct:identifier "{escape_str(row["ovo"])}" .',
    ]
    return "\n".join(lines)


def generate_migration(rows: list[dict]) -> str:
    prefix_block = "\n".join(PREFIXES)
    triples_block = "\n\n".join(build_triple(r) for r in rows)

    return (
        f"{prefix_block}\n\n"
        f"INSERT DATA {{\n"
        f"  GRAPH <{TARGET_GRAPH}> {{\n\n"
        f"{triples_block}\n\n"
        f"  }}\n"
        f"}}\n"
    )


def main():
    rows = read_rows()
    print(f"Read {len(rows)} organisations")

    if not rows:
        print("No organisations found, skipping migration file generation")
        return

    migration = generate_migration(rows)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    out_path = Path(OUTPUT_FILEPATH) / f"{timestamp}_insert-vo-bestuurseenheden.sparql"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(migration, encoding="utf-8")
    print(f"Written to {out_path}")


if __name__ == "__main__":
    main()
