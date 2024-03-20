from csv_handling import load_from_csv, save_to_csv
import pickle
import pandas as pd
from openhab.config.paths import path_openhab_container_scripts


month_timesteps = {1: list(range(0, 744)), 4: list(range(2160, 2880)), 7: list(range(4344, 5088))}
scenarios = ["40_1", "40_2", "40_3"]
months = [1, 4, 7]


def pv_generation_overview():
    pv_sum = {month: {scenario: 0 for scenario in scenarios} for month in months}
    for scenario in scenarios:
        for building in range(40):
            with open(path_openhab_container_scripts.joinpath("data", "nodes", str(scenario), f"{building}.p"), "rb") as f:
                node = pickle.load(f)
            for month in months:
                pv_sum[month][scenario] += sum(node["pv_power"][t] for t in month_timesteps[month])
    df = pd.DataFrame(columns=["scenario", "Jan", "Apr", "Jul"])
    df["scenario"] = scenarios
    df["Jan"] = pv_sum[1].values()
    df["Apr"] = pv_sum[4].values()
    df["Jul"] = pv_sum[7].values()

    save_to_csv(df=df, file_name="pv_generation_overview", folder="opti_res")


def pv_generation_steps():
    pv = {month: {t: 0 for t in month_timesteps[month]} for month in months}
    for building in range(40):
        with open(path_openhab_container_scripts.joinpath("data", "nodes", "40_3", f"{building}.p"), "rb") as f:
            node = pickle.load(f)
        for month in months:
            for t in month_timesteps[month]:
                pv[month][t] += node["pv_power"][t]
    df_jan = pd.DataFrame(data=pv[1].items(), columns=["n_opt", "quant"])
    df_apr = pd.DataFrame(data=pv[4].items(), columns=["n_opt", "quant"])
    df_jul = pd.DataFrame(data=pv[7].items(), columns=["n_opt", "quant"])
    save_to_csv(df=df_jan, file_name="pv_generation_steps_jan", folder="opti_res")
    save_to_csv(df=df_apr, file_name="pv_generation_steps_apr", folder="opti_res")
    save_to_csv(df=df_jul, file_name="pv_generation_steps_jul", folder="opti_res")


def wt_generation():
    wt_gen = dict()
    for month in months:
        wt_opti_df = load_from_csv(file_name="WT_opti", folder=f"40_1-{month}-d/opti")
        wt_gen[month] = wt_opti_df["surplus"].sum()
    df = pd.DataFrame(data=wt_gen.items(), columns=["month", "WT generation"])
    save_to_csv(df=df, file_name="wt_generation", folder="opti_res")


if __name__ == "__main__":
    pv_generation_steps()
