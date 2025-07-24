import pandas as pd
import uuid
from datetime import datetime, timezone

EXCEL_FILEPATH = "20250611_Inventarisatie (kritieke) processen LB_vF.xlsx"
EXCEL_SHEET_NAME = "5. Lijst (kritieke) processen"
EXCEL_HEADER_ROW = 5
EXCEL_COLS = {
    "Categorie": "category",
    "Procesdomein": "domain",
    "Procesgroep": "group",
    "Hoofd-proces-nummer voorlopig": "number",
    "Hoofdproces": "title",
}

OUTPUT_FOLDER = "../config/migrations/2025/conceptual-processes/"

PREFIXES = [
    "@prefix mu: <http://mu.semte.ch/vocabularies/core/> .",
    "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
    "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
    "@prefix oph: <http://lblod.data.gift/vocabularies/openproceshuis/> .",
    "@prefix dct: <http://purl.org/dc/terms/> .",
    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
]

BASE_CATEGORIES = "http://data.lblod.info/process-categories/"
BASE_DOMAINS = "http://data.lblod.info/process-domains/"
BASE_GROUPS = "http://data.lblod.info/process-groups/"
BASE_PROCESSES = "http://data.lblod.info/conceptual-processes/"

SCHEME_URI_CATEGORIES = (
    "http://lblod.data.gift/concept-schemes/21fba7d7-d0f5-4133-a108-626d0eb62298"
)
SCHEME_URI_DOMAINS = (
    "http://lblod.data.gift/concept-schemes/a8108a43-44fa-4b08-9794-064941f00dc1"
)
SCHEME_URI_GROUPS = (
    "http://lblod.data.gift/concept-schemes/324e775f-2a48-4daa-9de0-9f62ef8ab22e"
)

TARGET_GRAPH = "http://mu.semte.ch/graphs/inventory"


def load_excel_data():
    df = pd.read_excel(
        EXCEL_FILEPATH,
        sheet_name=EXCEL_SHEET_NAME,
        header=EXCEL_HEADER_ROW,
        usecols=list(EXCEL_COLS.keys()),
        engine="openpyxl",
    )
    df = df.rename(columns=EXCEL_COLS)
    df["category"] = df["category"].str.strip()
    df["domain"] = df["domain"].str.strip()
    df["group"] = df["group"].str.strip()
    df["title"] = df["title"].str.strip()
    return df


def normalize_data(df):
    categories = df[["category"]].drop_duplicates().reset_index(drop=True)
    categories["category_id"] = categories.index + 1
    categories["category_uuid"] = categories["category_id"].map(
        lambda _: str(uuid.uuid4())
    )

    domains = df[["domain", "category"]].drop_duplicates().reset_index(drop=True)
    domains = domains.merge(categories, on="category", how="left")
    domains["domain_id"] = domains.index + 1
    domains["domain_uuid"] = domains["domain_id"].map(lambda _: str(uuid.uuid4()))
    domains = domains[
        ["domain_id", "domain", "category_id", "category_uuid", "domain_uuid"]
    ]

    groups = df[["group", "domain"]].drop_duplicates().reset_index(drop=True)
    groups = groups.merge(domains, on="domain", how="left")
    groups["group_id"] = groups.index + 1
    groups["group_uuid"] = groups["group_id"].map(lambda _: str(uuid.uuid4()))
    groups = groups[
        ["group_id", "group", "domain", "domain_id", "domain_uuid", "group_uuid"]
    ]

    processes = df[["number", "title", "group", "domain"]].reset_index(drop=True)
    processes["process_id"] = processes.index + 1
    processes = processes.merge(
        groups[["group", "domain", "group_id", "group_uuid"]],
        on=["group", "domain"],
        how="left",
    )
    processes["process_uuid"] = processes["process_id"].map(lambda _: str(uuid.uuid4()))
    processes = processes[
        ["process_id", "process_uuid", "number", "title", "group_id", "group_uuid"]
    ]

    return categories, domains, groups, processes


def write_migration(ttl, timestamp, description):
    output_filename = (
        f"{OUTPUT_FOLDER}{timestamp.strftime('%Y%m%d%H%M%S')}-{description}"
    )

    with open(f"{output_filename}.ttl", "w", encoding="utf-8") as f:
        f.write(ttl)
    with open(f"{output_filename}.graph", "w", encoding="utf-8") as f:
        f.write(TARGET_GRAPH)


def export_categories_ttl(categories, timestamp):
    timestamp_ttl = timestamp.strftime('"%Y-%m-%dT%H:%M:%SZ"^^xsd:dateTime')

    lines = []
    lines.extend(PREFIXES)
    lines.append("")
    for _, row in categories.iterrows():
        lines.append(f"<{BASE_CATEGORIES}{row['category_uuid']}>")
        lines.append(f'  mu:uuid "{row["category_uuid"]}" ;')
        lines.append("  rdf:type skos:Concept ;")
        lines.append(f'  skos:prefLabel "{row["category"]}"@nl ;')
        lines.append(f"  dct:created {timestamp_ttl} ;")
        lines.append(f"  dct:modified {timestamp_ttl} ;")
        lines.append(f"  skos:inScheme <{SCHEME_URI_CATEGORIES}> .")
    ttl = "\n".join(lines)

    write_migration(ttl, timestamp, "add-process-categories")


def export_domains_ttl(domains, timestamp):
    timestamp_ttl = timestamp.strftime('"%Y-%m-%dT%H:%M:%SZ"^^xsd:dateTime')

    lines = []
    lines.extend(PREFIXES)
    lines.append("")
    for _, row in domains.iterrows():
        uuid = row["domain_uuid"]
        label = row["domain"]
        category_uuid = row["category_uuid"]

        lines.append(f"<{BASE_DOMAINS}{uuid}>")
        lines.append(f'  mu:uuid "{uuid}" ;')
        lines.append("  rdf:type skos:Concept ;")
        lines.append(f'  skos:prefLabel "{label}"@nl ;')
        lines.append(f"  dct:created {timestamp_ttl} ;")
        lines.append(f"  dct:modified {timestamp_ttl} ;")
        lines.append(f"  skos:relatedMatch <{BASE_CATEGORIES}{category_uuid}> ;")
        lines.append(f"  skos:inScheme <{SCHEME_URI_DOMAINS}> .")
    ttl = "\n".join(lines)

    write_migration(ttl, timestamp, "add-process-domains")


def export_groups_ttl(groups, timestamp):
    timestamp_ttl = timestamp.strftime('"%Y-%m-%dT%H:%M:%SZ"^^xsd:dateTime')

    lines = []
    lines.extend(PREFIXES)
    lines.append("")
    for _, row in groups.iterrows():
        uuid = row["group_uuid"]
        label = row["group"]
        domain_uuid = row["domain_uuid"]

        lines.append(f"<{BASE_GROUPS}{uuid}>")
        lines.append(f'  mu:uuid "{uuid}" ;')
        lines.append("  rdf:type skos:Concept ;")
        lines.append(f'  skos:prefLabel "{label}"@nl ;')
        lines.append(f"  dct:created {timestamp_ttl} ;")
        lines.append(f"  dct:modified {timestamp_ttl} ;")
        lines.append(f"  skos:relatedMatch <{BASE_DOMAINS}{domain_uuid}> ;")
        lines.append(f"  skos:inScheme <{SCHEME_URI_GROUPS}> .")
    ttl = "\n".join(lines)

    write_migration(ttl, timestamp, "add-process-groups")


def export_processes_ttl(processes, timestamp):
    timestamp_ttl = timestamp.strftime('"%Y-%m-%dT%H:%M:%SZ"^^xsd:dateTime')

    lines = []
    lines.extend(PREFIXES)
    lines.append("")
    for _, row in processes.iterrows():
        uuid = row["process_uuid"]
        title = row["title"]
        number = row["number"]
        group_uuid = row["group_uuid"]

        lines.append(f"<{BASE_PROCESSES}{uuid}>")
        lines.append(f'  mu:uuid "{uuid}" ;')
        lines.append("  rdf:type oph:ConceptueelProces ;")
        lines.append(f'  dct:title "{title}"@nl ;')
        lines.append(f"  dct:identifier {number} ;")
        lines.append(f"  dct:created {timestamp_ttl} ;")
        lines.append(f"  dct:modified {timestamp_ttl} ;")
        lines.append(f"  oph:procesGroep <{BASE_GROUPS}{group_uuid}> .")
    ttl = "\n".join(lines)

    write_migration(ttl, timestamp, "add-conceptual-processes")


def main():
    df = load_excel_data()
    categories, domains, groups, processes = normalize_data(df)

    timestamp = datetime.now(timezone.utc)

    export_categories_ttl(categories, timestamp)
    export_domains_ttl(domains, timestamp)
    export_groups_ttl(groups, timestamp)
    export_processes_ttl(processes, timestamp)


if __name__ == "__main__":
    main()
