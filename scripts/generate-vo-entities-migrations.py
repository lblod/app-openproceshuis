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

VO_CLASSIFICATION_UUID = "d89e882b-4f22-4d25-a63e-17eb246a18e2"
VO_CLASSIFICATION_URI = f"http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/{VO_CLASSIFICATION_UUID}"
VO_CLASSIFICATION_LABEL = "Vlaamse Overheid"

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


def build_values_row(row: dict) -> str:
    entity_uuid = derive_uuid(row["id"])
    uri = f"http://data.lblod.info/id/bestuurseenheden/{entity_uuid}"
    name = escape_str(row["name"])
    ovo = escape_str(row["ovo"])

    return f'    (<{uri}> "{entity_uuid}" "{name}" "{ovo}")'


def generate_migration(rows: list[dict]) -> str:
    values_rows = "\n".join(build_values_row(r) for r in rows)

    return (
        f"INSERT {{\n"
        f"  GRAPH <{TARGET_GRAPH}> {{\n"
        f"    ?uri\n"
        f"      mu:uuid ?uuid ;\n"
        f"      rdf:type besluit:Bestuurseenheid ;\n"
        f"      skos:prefLabel ?name ;\n"
        f"      dct:identifier ?ovo .\n"
        f"  }}\n"
        f"}}\n"
        f"WHERE {{\n"
        f"  VALUES (?uri ?uuid ?name ?ovo) {{\n"
        f"{values_rows}\n"
        f"  }}\n"
        f"  FILTER NOT EXISTS {{\n"
        f"    GRAPH <{TARGET_GRAPH}> {{\n"
        f"      ?existing dct:identifier ?ovo .\n"
        f"    }}\n"
        f"  }}\n"
        f"}}\n"
    )


def generate_classification_query() -> str:
    return (
        f"INSERT DATA {{\n"
        f"  GRAPH <{TARGET_GRAPH}> {{\n"
        f"    <{VO_CLASSIFICATION_URI}>\n"
        f"      rdf:type <http://lblod.data.gift/vocabularies/organisatie/BestuurseenheidClassificatieCode> ,\n"
        f"               <http://mu.semte.ch/vocabularies/ext/OrganizationClassificationCode> ;\n"
        f'      skos:prefLabel "{VO_CLASSIFICATION_LABEL}" ;\n'
        f'      mu:uuid "{VO_CLASSIFICATION_UUID}" .\n'
        f"  }}\n"
        f"}}"
    )


def main():
    rows = read_rows()
    print(f"Read {len(rows)} organisations")

    if not rows:
        print("No organisations found, skipping migration file generation")
        return

    prefix_block = "\n".join(PREFIXES) + "\n\n"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    out_dir = Path(OUTPUT_FILEPATH)
    out_dir.mkdir(parents=True, exist_ok=True)

    classification_path = out_dir / f"{timestamp}-insert-vo-classification.sparql"
    classification_path.write_text(prefix_block + generate_classification_query() + "\n", encoding="utf-8")
    print(f"Written to {classification_path}")

    bestuurseenheden_path = out_dir / f"{timestamp}-insert-vo-bestuurseenheden.sparql"
    bestuurseenheden_path.write_text(prefix_block + generate_migration(rows) + "\n", encoding="utf-8")
    print(f"Written to {bestuurseenheden_path}")


if __name__ == "__main__":
    main()
