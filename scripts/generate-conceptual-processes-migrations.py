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


def load_excel_data(filepath, sheet_name):
    df = pd.read_excel(
        filepath,
        sheet_name=sheet_name,
        header=EXCEL_HEADER_ROW,
        usecols=list(EXCEL_COLS.keys()),
    )
    df = df.rename(columns=EXCEL_COLS)
    return df


def main():
    df = load_excel_data(EXCEL_FILEPATH, EXCEL_SHEET_NAME)
    print(df.head())


if __name__ == "__main__":
    main()
