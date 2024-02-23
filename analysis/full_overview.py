import pandas as pd

from csv_handling import load_from_csv, save_to_csv


def demand_surplus_transaction_grid(cases: str | list):
    if isinstance(cases, str):
        cases = [cases]
    case_list = list()
    for case in cases:
        case_df = load_from_csv(file_name=case, folder="case_overviews")
        case_list.append({
            "case": case,
            "scenario": case.split("-")[0],
            "month": case.split("-")[1],
            "auction_type": case.split("-")[2],
            "demand": case_df["demand"].sum(),
            "surplus": case_df["surplus"].sum(),
            "trans buy quantity": case_df["trans buy quantity"].sum(),
            "trans cost": case_df["trans cost"].sum(),
            "trans sell quantity": case_df["trans sell quantity"].sum(),
            "trans revenue": case_df["trans revenue"].sum(),
            "to grid": case_df["to grid"].sum(),
            "grid cost": case_df["grid cost"].sum(),
            "from grid": case_df["from grid"].sum(),
            "grid revenue": case_df["grid revenue"].sum(),
            "trans avg price": case_df["trans cost"].sum() / case_df["trans buy quantity"].sum()
        })
    columns = list(case_list[0].keys())
    overview_df = pd.DataFrame(data=case_list, columns=columns)
    save_to_csv(df=overview_df, file_name="overview")
