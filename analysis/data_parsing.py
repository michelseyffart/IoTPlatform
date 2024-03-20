import pandas as pd
import pickle
from datetime import datetime
import datetime as dt

from market.transaction import Transaction
from market.public_info import PublicInfo

from openhab.config.paths import path_rawdata_MQTT_folder, path_rawdata_python_folder, path_analysis_data
from csv_handling import load_from_csv, save_to_csv

possible_steps = [x for x in range(0, 744)] + [x for x in range(2160, 2880)] + [x for x in range(4344, 5088)]


def load_pickle_data(file: str):
    data = list()
    with open(file, "rb") as f:
        try:
            while True:
                data.append(pickle.load(f))
        except EOFError:
            pass
    return data


def parse_rawdata_mqtt_to_pandas_df(file_name: str):
    file = path_rawdata_MQTT_folder.joinpath(file_name)
    data = load_pickle_data(file=file)

    bids = list()
    optis = list()
    grids = list()
    for entry in data:
        if "bid" in entry[0]:
            bid = {
                "building": str(entry[0].split("bid/")[1].split("/attrs")[0]),
                "buying": (entry[1].split('"bid_buying":')[1].split(',"bid_price"')[0] == "true"),
                "price": float(entry[1].split('"bid_price":"')[1].split('","bid_quantity"')[0]),
                "quantity": float(entry[1].split('"bid_quantity":"')[1].split('","bid_time"')[0]),
                "bid_time": datetime.fromtimestamp(float(entry[1].split('"bid_time":')[1].split('}')[0])/1000),
                "time_received": entry[2]
            }
            bids.append(bid)
        elif "opti" in entry[0]:
            opti = {
                "building": str(entry[0].split("opti/")[1]),
                "n_opt": int(entry[1].split('"n_opt":')[1].split(',"dem"')[0]),
                "demand": float(entry[1].split('"dem":')[1].split(',"sur"')[0]),
                "surplus": float(entry[1].split('"sur":')[1].split(',"soc"')[0]),
                "soc_tes": float(entry[1].split('"tes":')[1].split(',"bat"')[0]),
                "soc_bat": float(entry[1].split('"bat":')[1].split('}')[0]),
                "time_received": entry[2]
            }
            if opti["n_opt"] in possible_steps:
                optis.append(opti)
            else:
                print(f"{opti['n_opt']} out of range.")
                break

    bid_columns = ["building", "buying", "price", "quantity", "bid_time", "time_received"]
    bid_df = pd.DataFrame(data=bids, columns=bid_columns)

    opti_columns = ["building", "n_opt", "demand", "surplus", "soc_tes", "soc_bat", "time_received"]
    opti_df = pd.DataFrame(data=optis, columns=opti_columns)

    grid_columns = ["building", "n_opt", "from_grid", "to_grid", "time_received"]
    grid_df = pd.DataFrame(data=grids, columns=grid_columns)

    return bid_df, opti_df, grid_df


def parse_rawdata_python_to_pandas_df(file_name: str):
    file = path_rawdata_python_folder.joinpath(file_name)
    data = load_pickle_data(file=file)

    transactions = list()
    public_infos = list()

    for entry in data:
        if isinstance(entry[0], list):
            for list_entry in entry[0]:
                if isinstance(list_entry, Transaction):
                    transaction = {
                        "buyer": str(list_entry.buyer),
                        "seller": str(list_entry.seller),
                        "quantity": float(list_entry.quantity),
                        "price": float(list_entry.price),
                        "time_received": entry[1]
                    }
                    transactions.append(transaction)
                if isinstance(list_entry, PublicInfo):
                    public_info = {
                        "equilibrium_price": float(list_entry.equilibrium_price),
                        "equilibrium_quantity": float(list_entry.equilibrium_quantity),
                        "time_received": entry[1]
                    }
                    public_infos.append(public_info)

    transaction_columns = ["buyer", "seller", "quantity", "price", "time_received"]
    transaction_df = pd.DataFrame(data=transactions, columns=transaction_columns).astype(
                                  {"buyer": "str", "seller": "str"})

    public_info_columns = ["equilibrium_price", "equilibrium_quantity", "time_received"]
    public_info_df = pd.DataFrame(data=public_infos, columns=public_info_columns)

    return transaction_df, public_info_df


def parse_and_save(case: str, mqtt_file: str, python_file: str):
    bid_df, opti_df, grid_df = parse_rawdata_mqtt_to_pandas_df(mqtt_file)
    save_to_csv(df=bid_df, file_name="all_bids", folder=f"{case}/bids")
    save_to_csv(df=opti_df, file_name="all_opti", folder=f"{case}/opti")
    save_to_csv(df=grid_df, file_name="all_grid", folder=f"{case}/grid")
    transaction_df, public_info_df = parse_rawdata_python_to_pandas_df(python_file)
    save_to_csv(df=transaction_df, file_name="all_transactions", folder=f"{case}/transactions")
    save_to_csv(df=public_info_df, file_name="all_public_info", folder=f"{case}/public_info")
    print(f"Saved csv files for case {case}.")


def separate_and_save_data_for_buildings(cases: str | list, buildings: str | list):
    if isinstance(cases, str):
        cases = [cases]
    if isinstance(buildings, str):
        buildings = [buildings]
    for case in cases:
        transaction_df = load_from_csv(file_name="all_transactions", folder=f"{case}/transactions")
        opti_df = load_from_csv(file_name="all_opti", folder=f"{case}/opti")
        grid_df = load_from_csv(file_name="all_grid", folder=f"{case}/grid")
        bid_df = load_from_csv(file_name="all_bids", folder=f"{case}/bids")
        for building in buildings:
            building_buying_transactions_df = (transaction_df[transaction_df["buyer"] == building]
                                               .reset_index(drop=True))
            building_buying_transactions_df["cost"] = (building_buying_transactions_df["quantity"] *
                                                       building_buying_transactions_df["price"])
            building_selling_transactions_df = (transaction_df[transaction_df["seller"] == building]
                                                .reset_index(drop=True))
            building_selling_transactions_df["revenue"] = (building_selling_transactions_df["quantity"] *
                                                           building_selling_transactions_df["price"])
            building_opti_df = opti_df[opti_df["building"].astype("str") == building].reset_index(drop=True)
            building_grid_df = grid_df[grid_df["building"].astype("str") == building].reset_index(drop=True)
            building_bids_df = bid_df[bid_df["building"].astype("str") == building].reset_index(drop=True)
            building_buying_bids_df = building_bids_df[building_bids_df["buying"] == True].reset_index(drop=True)
            building_selling_bids_df = building_bids_df[building_bids_df["buying"] == False].reset_index(drop=True)

            save_to_csv(df=building_buying_transactions_df, file_name=f"{building}_buying_transactions",
                        folder=f"{case}/transactions")
            save_to_csv(df=building_selling_transactions_df, file_name=f"{building}_selling_transactions",
                        folder=f"{case}/transactions")
            save_to_csv(df=building_opti_df, file_name=f"{building}_opti", folder=f"{case}/opti")
            save_to_csv(df=building_grid_df, file_name=f"{building}_grid", folder=f"{case}/grid")
            save_to_csv(df=building_bids_df, file_name=f"{building}_all_bids", folder=f"{case}/bids")
            save_to_csv(df=building_buying_bids_df, file_name=f"{building}_buying_bids", folder=f"{case}/bids")
            save_to_csv(df=building_selling_bids_df, file_name=f"{building}_selling_bids", folder=f"{case}/bids")
        print(f"Separated and saved building data for case {case}")


def accumulate_transactions(cases: str | list, buildings: str | list):
    if isinstance(cases, str):
        cases = [cases]
    if isinstance(buildings, str):
        buildings = [buildings]
    for case in cases:
        with open(path_analysis_data.joinpath(case, "interval_and_start.p"), "rb") as f:
            interval_and_start = pickle.load(f)
        interval_length = interval_and_start["interval"]
        for building in buildings:
            start = interval_and_start["building_start"][building] - pd.Timedelta("0.3s")
            grouper = pd.Grouper(key="time_received", freq=f"{interval_length}s", origin=start)
            buying_transaction_df = load_from_csv(file_name=f"{building}_buying_transactions",
                                                  folder=f"{case}/transactions")
            selling_transaction_df = load_from_csv(file_name=f"{building}_selling_transactions",
                                                   folder=f"{case}/transactions")
            buying_group = buying_transaction_df.groupby(grouper)[["quantity", "cost"]].sum().reset_index()
            selling_group = selling_transaction_df.groupby(grouper)[["quantity", "revenue"]].sum().reset_index()
            save_to_csv(df=buying_group, file_name=f"{building}_grouped_buying_quantity",
                        folder=f"{case}/transactions")
            save_to_csv(df=selling_group, file_name=f"{building}_grouped_selling_quantity",
                        folder=f"{case}/transactions")


def calculate_interval_and_start_of_case(cases: str | list, buildings: str | list, len_buildings: int = 41):
    if isinstance(cases, str):
        cases = [cases]
    if isinstance(buildings, str):
        buildings = [buildings]
    for case in cases:
        opti_df = load_from_csv(file_name=f"all_opti", folder=f"{case}/opti")
        case_start = opti_df.iloc[0]["time_received"].floor(freq="s")
        intervals = pd.to_datetime(opti_df["time_received"]).diff(periods=len_buildings)
        intervals_mean = intervals.iloc[len_buildings:100*len_buildings].mean()
        if intervals_mean.microseconds < 200000:
            interval_length = intervals_mean.seconds
        elif intervals_mean.microseconds > 800000:
            interval_length = intervals_mean.seconds + 1
        else:
            print(f"Can not get interval length of {case} with enough confidence: {intervals_mean}.")
            interval_length = None
        building_start = dict()
        for building in buildings:
            start_time = (opti_df.loc[opti_df["building"] == building].iloc[2]["time_received"] -
                          2 * dt.timedelta(seconds=interval_length))
            building_start[building] = start_time
        payload = {
            "interval": interval_length,
            "case_start": case_start,
            "building_start": building_start
        }
        with open(path_analysis_data.joinpath(case, "interval_and_start.p"), "wb") as f:
            pickle.dump(payload, f)
