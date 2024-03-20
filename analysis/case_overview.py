import pandas as pd
from csv_handling import load_from_csv, save_to_csv


def demand_surplus_transaction_grid(cases: str | list, buildings: str | list, without_WT: bool = False):
    if isinstance(cases, str):
        cases = [cases]
    if isinstance(buildings, str):
        buildings = [buildings]

    if without_WT:
        buildings.remove("WT")

    for case in cases:
        case_list = list()
        for building in buildings:
            building_df = load_from_csv(file_name=building, folder=f"{case}/building_overviews")
            case_list.append({
                "building": building,
                "demand": building_df["demand"].sum(),
                "surplus": building_df["surplus"].sum(),
                "trans buy quantity": building_df["trans buy quantity"].sum(),
                "trans sell quantity": building_df["trans sell quantity"].sum(),
                "trans cost": building_df["trans cost"].sum(),
                "trans revenue": building_df["trans revenue"].sum(),
                "to grid":  building_df["to grid"].sum(),
                "from grid": building_df["from grid"].sum(),
                "grid cost": building_df["cost grid"].sum(),
                "grid revenue": building_df["revenue grid"].sum()
            })
        case_columns = list(case_list[0].keys())
        case_df = pd.DataFrame(case_list, columns=case_columns)
        if without_WT:
            folder = f"case_overviews_without_WT"
        else:
            folder = "case_overviews"
        save_to_csv(df=case_df, file_name=case, folder=folder)
        print(f"Saved case overview {case}.")
