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


def main():
    df = load_excel_data()
    categories, domains, groups, processes = normalize_data(df)

    print(categories)
    print()
    print(domains)
    print()
    print(groups)
    print()
    print(processes)
    print()

    print(f"Number of titles in original df: {df['title'].shape[0]}")
    print(f"Length of processes df: {processes.shape[0]}")
    print()
    print(f"Number of unique groups in original df: {df['group'].nunique()}")
    print(f"Length of groups df: {groups.shape[0]}")
    print()
    print(f"Number of unique domains in original df: {df['domain'].nunique()}")
    print(f"Length of domains df: {domains.shape[0]}")
    print()
    print(f"Number of unique categories in original df: {df['category'].nunique()}")
    print(f"Length of categories df: {categories.shape[0]}")


if __name__ == "__main__":
    main()
