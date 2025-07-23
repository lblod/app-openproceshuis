import pandas as pd
import uuid

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

CONCEPT_PREFIXES = [
    "@prefix mu: <http://mu.semte.ch/vocabularies/core/> .",
    "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
    "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
]
SCHEME_URI_CATEGORIES = (
    "http://lblod.data.gift/concept-schemes/21fba7d7-d0f5-4133-a108-626d0eb62298"
)
SCHEME_URI_DOMAINS = (
    "http://lblod.data.gift/concept-schemes/a8108a43-44fa-4b08-9794-064941f00dc1"
)
SCHEME_URI_GROUPS = (
    "http://lblod.data.gift/concept-schemes/324e775f-2a48-4daa-9de0-9f62ef8ab22e"
)
CONCEPT_BASE = "http://lblod.data.gift/concepts/"


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


def export_categories_ttl(categories):
    lines = []
    lines.extend(CONCEPT_PREFIXES)
    lines.append("")
    for _, row in categories.iterrows():
        uuid = row["category_uuid"]
        label = row["category"]

        lines.append(f"<{CONCEPT_BASE}{uuid}>")
        lines.append(f'  mu:uuid "{uuid}" ;')
        lines.append("  rdf:type skos:Concept ;")
        lines.append(f'  skos:prefLabel "{label}"@nl ;')
        lines.append(f"  skos:inScheme <{SCHEME_URI_CATEGORIES}> .")
    ttl = "\n".join(lines)
    with open("categories.ttl", "w", encoding="utf-8") as f:
        f.write(ttl)


def export_domains_ttl(domains):
    lines = []
    lines.extend(CONCEPT_PREFIXES)
    lines.append("")
    for _, row in domains.iterrows():
        uuid = row["domain_uuid"]
        label = row["domain"]
        category_uuid = row["category_uuid"]

        lines.append(f"<{CONCEPT_BASE}{uuid}>")
        lines.append(f'  mu:uuid "{uuid}" ;')
        lines.append("  rdf:type skos:Concept ;")
        lines.append(f'  skos:prefLabel "{label}"@nl ;')
        lines.append(f"  skos:relatedMatch <{CONCEPT_BASE}{category_uuid}> ;")
        lines.append(f"  skos:inScheme <{SCHEME_URI_DOMAINS}> .")
    ttl = "\n".join(lines)
    with open("domains.ttl", "w", encoding="utf-8") as f:
        f.write(ttl)


def export_groups_ttl(groups):
    lines = []
    lines.extend(CONCEPT_PREFIXES)
    lines.append("")
    for _, row in groups.iterrows():
        uuid = row["group_uuid"]
        label = row["group"]
        domain_uuid = row["domain_uuid"]

        lines.append(f"<{CONCEPT_BASE}{uuid}>")
        lines.append(f'  mu:uuid "{uuid}" ;')
        lines.append("  rdf:type skos:Concept ;")
        lines.append(f'  skos:prefLabel "{label}"@nl ;')
        lines.append(f"  skos:relatedMatch <{CONCEPT_BASE}{domain_uuid}> ;")
        lines.append(f"  skos:inScheme <{SCHEME_URI_GROUPS}> .")
    ttl = "\n".join(lines)
    with open("groups.ttl", "w", encoding="utf-8") as f:
        f.write(ttl)


def export_processes_ttl(processes):
    lines = []
    lines.extend(CONCEPT_PREFIXES)
    lines.append("")
    for _, row in processes.iterrows():
        uuid = row["group_uuid"]
        label = row["group"]
        domain_uuid = row["domain_uuid"]

        lines.append(f"<{CONCEPT_BASE}{uuid}>")
        lines.append(f'  mu:uuid "{uuid}" ;')
        lines.append("  rdf:type skos:Concept ;")
        lines.append(f'  skos:prefLabel "{label}"@nl ;')
        lines.append(f"  skos:relatedMatch <{CONCEPT_BASE}{domain_uuid}> ;")
        lines.append(f"  skos:inScheme <{SCHEME_URI_GROUPS}> .")
    ttl = "\n".join(lines)
    with open("groups.ttl", "w", encoding="utf-8") as f:
        f.write(ttl)


def main():
    df = load_excel_data()

    categories, domains, groups, processes = normalize_data(df)

    export_categories_ttl(categories)
    export_domains_ttl(domains)
    export_groups_ttl(groups)


if __name__ == "__main__":
    main()
