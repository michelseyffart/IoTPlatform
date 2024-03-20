from csv_handling import load_from_csv, save_to_csv
import pandas as pd


def new_kpi_csv(cases: list, without_WT: bool = False):
    if without_WT:
        file_name = "KPIs_without_WT"
    else:
        file_name = "KPIs"
    case_list = list()
    for case in cases:
        case_list.append({
            "case": case,
            "scenario": case.split("-")[0],
            "month": case.split("-")[1],
            "auction_type": case.split("-")[2],
        })
    keys = list(case_list[0].keys())
    kpi_df = pd.DataFrame(case_list, columns=keys)
    save_to_csv(df=kpi_df, file_name=file_name)


def gain(cases: str | list):
    if isinstance(cases, str):
        cases = [cases]

    overview_df = load_from_csv(file_name="overview")
    overview_without_wt_df = load_from_csv(file_name="overview_without_WT")
    gains = (overview_df["trans buy quantity"] * 0.4573 - overview_df["trans cost"] +
             overview_df["trans revenue"] - overview_df["trans sell quantity"] * 0.0811)
    gains_without_wt = (overview_without_wt_df["trans buy quantity"] * 0.4573 -
                        overview_without_wt_df["trans cost"] +
                        overview_without_wt_df["trans revenue"] -
                        overview_without_wt_df["trans sell quantity"] * 0.0811)
    gains_selling_without_wt = overview_without_wt_df["trans revenue"] - overview_without_wt_df["trans sell quantity"] * 0.0811
    gains_selling = overview_df["trans revenue"] - overview_df["trans sell quantity"] * 0.0811
    gains_buying = overview_df["trans buy quantity"] * 0.4573 - overview_df["trans cost"]

    gains_wt_only = list()
    for case in cases:
        case_df = load_from_csv(file_name=case, folder="case_overviews")
        wt_df = case_df.loc[case_df["building"] == "WT"]
        gains_wt_only.append((wt_df["trans revenue"] - wt_df["trans sell quantity"] * 0.0811).values[0])

    kpi_df = load_from_csv(file_name="KPIs")
    kpi_df["gain"] = gains
    kpi_df["gain_without_wt"] = gains_without_wt
    kpi_df["gain_wt"] = gains_wt_only
    kpi_df["gain_percentage_wt"] = kpi_df["gain_wt"] / kpi_df["gain"]
    kpi_df["gain_percentage_without_wt"] = 1 - kpi_df["gain_percentage_wt"]
    kpi_df["gain_selling"] = gains_selling
    kpi_df["gain_selling_without_wt"] = gains_selling_without_wt
    kpi_df["gain_buying"] = gains_buying

    save_to_csv(df=kpi_df, file_name="KPIs")


def dcf_scf_mdcf_mscf(cases: str | list):
    if isinstance(cases, str):
        cases = [cases]

    dcf, scf, mdcf, mscf = list(), list(), list(), list()

    overview_df = load_from_csv(file_name="overview")

    for case in cases:
        opti_df = load_from_csv("all_opti", folder=f"{case}/opti")

        opti_sum = opti_df.groupby(by="n_opt")[["demand", "surplus"]].sum()
        opti_sum_min = opti_sum[["demand", "surplus"]].min(axis=1).sum()

        dcf.append(opti_sum_min / opti_sum["demand"].sum())
        scf.append(opti_sum_min / opti_sum["surplus"].sum())

        trans_buy_quant = overview_df.loc[overview_df["case"] == case]["trans buy quantity"].item()
        trans_sell_quant = overview_df.loc[overview_df["case"] == case]["trans sell quantity"].item()

        mdcf.append(trans_buy_quant / opti_sum["demand"].sum())
        mscf.append(trans_sell_quant / opti_sum["surplus"].sum())


    kpi_df = load_from_csv(file_name="KPIs")
    kpi_df["dcf"] = dcf
    kpi_df["scf"] = scf
    kpi_df["mdcf"] = mdcf
    kpi_df["mscf"] = mscf
    kpi_df["mdcf_ratio"] = kpi_df["mdcf"] / kpi_df["dcf"]
    kpi_df["mscf_ratio"] = kpi_df["mscf"] / kpi_df["scf"]
    save_to_csv(df=kpi_df, file_name="KPIs")


def mean_transaction_price(cases: str | list):
    if isinstance(cases, str):
        cases = [cases]

    mean_price_list = list()
    for case in cases:
        transactions_df = load_from_csv(file_name="all_transactions", folder=f"{case}/transactions")
        mean_price_list.append(transactions_df["price"].mean())

    kpi_df = load_from_csv(file_name="KPIs")
    kpi_df["mean_transaction_price"] = mean_price_list
    save_to_csv(df=kpi_df, file_name="KPIs")
