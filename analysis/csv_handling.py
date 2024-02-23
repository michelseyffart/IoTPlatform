from openhab.config.paths import path_analysis_data
import pandas as pd

separator = ";"
decimal = ","


def save_to_csv(df: pd.DataFrame, file_name: str, folder: str = None):
    if ".csv" in file_name:
        file_name = file_name.split(".csv")[0]
    if folder:
        folder_path = path_analysis_data.joinpath(folder)
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path.joinpath(file_name).with_suffix(".csv")
    else:
        file_path = path_analysis_data.joinpath(file_name).with_suffix(".csv")
    df.to_csv(file_path, sep=separator, decimal=decimal, index=False)


def load_from_csv(file_name: str, folder: str = None):
    types = {
        "building": "str",
        "buyer": "str",
        "seller": "str"
    }
    if ".csv" in file_name:
        file_name = file_name.split(".csv")[0]
    if folder:
        file_path = path_analysis_data.joinpath(folder, file_name).with_suffix(".csv")
    else:
        file_path = path_analysis_data.joinpath(file_name).with_suffix(".csv")
    try:
        df = pd.read_csv(file_path, sep=separator, decimal=decimal)
    except FileNotFoundError:
        return pd.DataFrame()
    columns = df.columns
    for col, dtype in types.items():
        if col in columns:
            df[col] = df[col].astype(dtype)
    if "time_received" in columns:
        df["time_received"] = pd.to_datetime(df["time_received"], format="%Y-%m-%d %H:%M:%S.%f")
    if "bid_time" in columns:
        df["bid_time"] = pd.to_datetime(df["bid_time"], format="%Y-%m-%d %H:%M:%S.%f")
    return df
