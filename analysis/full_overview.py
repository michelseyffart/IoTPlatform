import pandas as pd

from csv_handling import load_from_csv, save_to_csv


def demand_surplus_transaction_grid(cases: str | list, without_WT: bool = False):
    if isinstance(cases, str):
        cases = [cases]
    case_list = list()
    if without_WT:
        folder = f"case_overviews_without_WT"
    else:
        folder = "case_overviews"
    for case in cases:
        case_df = load_from_csv(file_name=case, folder=folder)
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
    if without_WT:
        file_name = f"overview_without_WT"
    else:
        file_name = "overview"
    save_to_csv(df=overview_df, file_name=file_name)


def wt_bid_price_mean(cases: str | list):
    if isinstance(cases, str):
        cases = [cases]
    case_list = list()
    overview_df = load_from_csv("overview")
    mean_prices = list()
    for case in cases:
        bid_df = load_from_csv(file_name="WT_selling_bids", folder=f"{case}/bids")
        mean_prices.append(bid_df["price"].mean())
    overview_df["wt bid price mean"] = mean_prices
    save_to_csv(df=overview_df, file_name="overview")
