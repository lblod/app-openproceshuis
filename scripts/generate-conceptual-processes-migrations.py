import pandas as pd

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

    domains = df[["domain", "category"]].drop_duplicates().reset_index(drop=True)
    domains = domains.merge(categories, on="category", how="left")
    domains["domain_id"] = domains.index + 1
    domains = domains[["domain_id", "domain", "category_id"]]

    groups = df[["group", "domain"]].drop_duplicates().reset_index(drop=True)
    groups = groups.merge(domains, on="domain", how="left")
    groups["group_id"] = groups.index + 1
    groups = groups[["group_id", "group", "domain", "domain_id"]]

    processes = df[["number", "title", "group", "domain"]].reset_index(drop=True)
    processes["process_id"] = processes.index + 1
    processes = processes.merge(
        groups[["group", "domain", "group_id"]], on=["group", "domain"], how="left"
    )
    processes = processes[["process_id", "number", "title", "group_id"]]

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


if __name__ == "__main__":
    main()
