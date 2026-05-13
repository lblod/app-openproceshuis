import csv
import re
import uuid
from datetime import datetime
from pathlib import Path

INPUT_FILEPATH = "export_20260423_110049.csv"
INPUT_COLS = {
    "Organisatie ID": "id",
    "Organisatienaam": "name",
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

VO_CLASSIFICATION_UUID = "d89e882b-4f22-4d25-a63e-17eb246a18e2"
VO_CLASSIFICATION_URI = f"http://data.vlaanderen.be/id/concept/BestuurseenheidClassificatieCode/{VO_CLASSIFICATION_UUID}"
VO_CLASSIFICATION_LABEL = "Vlaamse Overheid"
VO_CLASSIFICATION_TYPES = [
    "http://lblod.data.gift/vocabularies/organisatie/BestuurseenheidClassificatieCode",
    "http://mu.semte.ch/vocabularies/ext/OrganizationClassificationCode",
]

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


def bestuurseenheid_uri(entity_uuid: str) -> str:
    return f"{BESTUURSEENHEID_BASE_URI}{entity_uuid}"


def read_rows() -> list[dict]:
    rows = []
    with open(INPUT_FILEPATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for raw in reader:
            row = {alias: raw.get(col, "").strip() for col, alias in INPUT_COLS.items()}
            if row["id"] and row["ovo"]:
                rows.append(row)
    return rows


def generate_bestuurseenheden_query(rows: list[dict]) -> str:
    values_rows = "\n".join(
        f'    (<{bestuurseenheid_uri(entity_uuid)}> "{entity_uuid}" "{escape_str(r["name"])}" "{escape_str(r["ovo"])}")'
        for r in rows
        for entity_uuid in [derive_uuid(r["id"])]
    )

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
        f"}}"
    )


def generate_classification_query() -> str:
    types = " ,\n               ".join(f"<{t}>" for t in VO_CLASSIFICATION_TYPES)

    return (
        f"INSERT DATA {{\n"
        f"  GRAPH <{TARGET_GRAPH}> {{\n"
        f"    <{VO_CLASSIFICATION_URI}>\n"
        f"      rdf:type {types} ;\n"
        f'      skos:prefLabel "{VO_CLASSIFICATION_LABEL}" ;\n'
        f'      mu:uuid "{VO_CLASSIFICATION_UUID}" .\n'
        f"  }}\n"
        f"}}"
    )


def generate_link_classification_query(rows: list[dict]) -> str:
    uris = "\n".join(
        f"    (<{bestuurseenheid_uri(derive_uuid(r['id']))}>)"
        for r in rows
    )

    return (
        f"INSERT {{\n"
        f"  GRAPH <{TARGET_GRAPH}> {{\n"
        f"    ?uri org:classification <{VO_CLASSIFICATION_URI}> .\n"
        f"  }}\n"
        f"}}\n"
        f"WHERE {{\n"
        f"  VALUES (?uri) {{\n"
        f"{uris}\n"
        f"  }}\n"
        f"}}"
    )


def write_migration(path: Path, *queries: str) -> None:
    prefix_block = "\n".join(PREFIXES)
    content = prefix_block + "\n\n" + " ;\n\n".join(queries) + "\n"
    path.write_text(content, encoding="utf-8")
    print(f"Written to {path}")


def main():
    rows = read_rows()
    print(f"Read {len(rows)} organisations")

    if not rows:
        print("No organisations found, skipping migration file generation")
        return

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    out_dir = Path(OUTPUT_FILEPATH)
    out_dir.mkdir(parents=True, exist_ok=True)

    write_migration(
        out_dir / f"{timestamp}-insert-vo-classification.sparql",
        generate_classification_query(),
        generate_link_classification_query(rows),
    )

    write_migration(
        out_dir / f"{timestamp}-insert-vo-bestuurseenheden.sparql",
        generate_bestuurseenheden_query(rows),
    )


if __name__ == "__main__":
    main()
