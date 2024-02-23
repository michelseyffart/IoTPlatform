import pandas as pd
import pickle

from csv_handling import load_from_csv, save_to_csv
from openhab.config.paths import path_analysis_data


def supply_demand(cases: str | list, buildings: str | list, replace: bool = True):
    if isinstance(cases, str):
        cases = [cases]
    if isinstance(buildings, str):
        buildings = [buildings]
    for case in cases:
        for building in buildings:
            if replace:
                building_df = pd.DataFrame()
            else:
                building_df = load_from_csv(file_name=building, folder=f"{case}/building_overviews")
            opti_df = load_from_csv(file_name=f"{building}_opti", folder=f"{case}/opti")
            building_df["n_opt"] = opti_df["n_opt"]
            building_df["time_received"] = opti_df["time_received"]
            building_df["demand"] = opti_df["demand"]
            building_df["surplus"] = opti_df["surplus"]

            save_to_csv(df=building_df, file_name=building, folder=f"{case}/building_overviews")
        print(f"Saved building overviews demand and surplus {case}.")


def merge_bids_in_building_overview(cases: str | list, buildings: str | list):
    if isinstance(cases, str):
        cases = [cases]
    if isinstance(buildings, str):
        buildings = [buildings]
    for case in cases:
        for building in buildings:
            building_df = load_from_csv(file_name=building, folder=f"{case}/building_overviews")
            bids_df = load_from_csv(file_name=f"{building}_all_bids",
                                    folder=f"{case}/bids")
            building_df = (pd.merge_asof(building_df, bids_df[["time_received", "buying", "price", "quantity"]],
                                         on="time_received", direction="forward")
                           .rename(columns={"quantity": "bid quantity",
                                            "buying": "bid buying",
                                            "price": "bid price"}))
            save_to_csv(df=building_df, file_name=building, folder=f"{case}/building_overviews")
        print(f"Saved building overviews bids {case}.")


def merge_transactions_in_building_overview(cases: str | list, buildings: str | list):
    if isinstance(cases, str):
        cases = [cases]
    if isinstance(buildings, str):
        buildings = [buildings]
    for case in cases:
        with open(path_analysis_data.joinpath(case, "interval_and_start.p"), "rb") as f:
            interval_and_start = pickle.load(f)
            tolerance = pd.Timedelta(seconds=interval_and_start["interval"])
        for building in buildings:
            building_df = load_from_csv(file_name=building, folder=f"{case}/building_overviews")
            quant_trans_buy_df = load_from_csv(file_name=f"{building}_grouped_buying_quantity",
                                               folder=f"{case}/transactions")
            quant_trans_sell_df = load_from_csv(file_name=f"{building}_grouped_selling_quantity",
                                                folder=f"{case}/transactions")
            building_df = pd.merge_asof(building_df, quant_trans_buy_df.reset_index(drop=True), on="time_received",
                                        direction="backward", tolerance=tolerance).rename(
                                        columns={"quantity": "trans buy quantity",
                                                 "cost": "trans cost"})
            building_df = pd.merge_asof(building_df, quant_trans_sell_df.reset_index(drop=True), on="time_received",
                                        direction="backward", tolerance=tolerance).rename(
                                        columns={"quantity": "trans sell quantity",
                                                 "revenue": "trans revenue"})
            building_df = building_df.fillna(0)
            save_to_csv(df=building_df, file_name=building, folder=f"{case}/building_overviews")
        print(f"Saved building overviews transactions {case}.")


def calculate_and_merge_grid_in_building_overview(cases: str | list, buildings: str | list):
    if isinstance(cases, str):
        cases = [cases]
    if isinstance(buildings, str):
        buildings = [buildings]
    for case in cases:
        for building in buildings:
            building_df = load_from_csv(file_name=building, folder=f"{case}/building_overviews")
            building_df["from grid"] = building_df["demand"] - building_df["trans buy quantity"]
            building_df["cost grid"] = building_df["from grid"] * 0.4573
            building_df["to grid"] = building_df["surplus"] - building_df["trans sell quantity"]
            building_df["revenue grid"] = building_df["to grid"] * 0.0811
            save_to_csv(df=building_df, file_name=building, folder=f"{case}/building_overviews")
        print(f"Saved building overviews grid {case}.")
