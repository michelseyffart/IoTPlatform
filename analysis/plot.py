import matplotlib

from csv_handling import load_from_csv
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np
import matplotlib.font_manager as font_manager
from rwth_colors import colors

x_width = 6.1
figsize = {
    "large": (x_width, 5),
    "small": (x_width/2, 2),
    "small_square": (.45*x_width, .45*x_width),
    "generation_profile_half": (.45*x_width, 3),
    "dcf_scf_half": (x_width*0.45, 3)
}

font_path = "J:/heuristica-cufonfonts/Heuristica-Regular.otf"
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)
matplotlib.rc("font", family="sans-serif")

params = {
    "legend.fontsize": "medium",
    "axes.titlesize": "medium",
    "axes.labelsize": "medium",
    "font.size": 11,
    "font.sans-serif": prop.get_name()
}
matplotlib.rcParams.update(params)

erc_colors = {
    "red": "#E53027",
    "blue": "#1058B0",
    "orange": "#E07328",
    "violett": "#5F379B",
    "darkred": "#73231E",
    "pink": "#BE4198",
    "darkgreen": "#008746"
}

#chosen_colors = [colors["turqoise"], colors["orange"], colors["darkred"], colors["lavender"]]
#chosen_colors = [erc_colors["red"], erc_colors["blue"], erc_colors["pink"], erc_colors["darkgreen"]]
chosen_colors = ["#DD402D", "#F6A800", "#006165", "#7A6FAC", "#460A01", "#5A3D07", "#032C2C", "#271849"] # "#BDCD00"
dark_colors = ["#460A01", "#5A3D07", "#032C2C", "#271849"]

plt.rcParams["axes.prop_cycle"] = plt.cycler(color=chosen_colors)

#scenarios = ["40_1", "40_2", "40_3"]
scenarios = ["fixed_1", "fixed_2", "fixed_3"]

def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)
    plt.setp(bp['fliers'], markeredgecolor=color)


def trans_quant_of_cases(cases: list):
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")
    filtered_df = overview_df[overview_df["case"].isin(cases)]
    fig, axs = plt.subplots(nrows=2, ncols=1)
    axs[0].bar(x=filtered_df["case"], height=filtered_df["trans buy quantity"])
    axs[1].bar(x=filtered_df["case"], height=filtered_df["trans sell quantity"])
    fig.tight_layout()
    plt.savefig("analysis/figures/trans_quant.png")
    plt.show()


def overview_quant_trans():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = overview_df["trans buy quantity"].max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large"])

    for row, scenario in enumerate(scenarios):
        scenario_df = overview_df[overview_df["scenario"] == scenario]
        for column, month in enumerate([1, 4, 7]):
            filtered_df = scenario_df[scenario_df["month"] == month]
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["trans buy quantity"])
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Transaction Quantity")
    fig.tight_layout()
    plt.savefig("analysis/figures/overview_quant_trans.png")
    plt.show()


def overview_cost_trans():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = overview_df["trans cost"].max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large"])

    for row, scenario in enumerate(scenarios):
        scenario_df = overview_df[overview_df["scenario"] == scenario]
        for column, month in enumerate([1, 4, 7]):
            filtered_df = scenario_df[scenario_df["month"] == month]
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["trans cost"])
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Transaction Cost/Revenue")
    fig.tight_layout()
    plt.savefig("analysis/figures/overview_cost_trans.png")
    plt.show()


def overview_quant_trans_and_to_grid():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = (overview_df["trans sell quantity"] + overview_df["to grid"]).max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large"])

    for row, scenario in enumerate(scenarios):
        scenario_df = overview_df[overview_df["scenario"] == scenario]
        for column, month in enumerate([1, 4, 7]):
            filtered_df = scenario_df[scenario_df["month"] == month]
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["trans sell quantity"])
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["to grid"],
                                bottom=filtered_df["trans sell quantity"])
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Transaction and to grid quantity")
    fig.tight_layout()
    plt.savefig("analysis/figures/overview_quant_trans_and_to_grid.png")
    plt.show()


def overview_quant_trans_and_from_grid():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = (overview_df["trans buy quantity"] + overview_df["from grid"]).max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large"])

    for row, scenario in enumerate(scenarios):
        scenario_df = overview_df[overview_df["scenario"] == scenario]
        for column, month in enumerate([1, 4, 7]):
            filtered_df = scenario_df[scenario_df["month"] == month]
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["trans buy quantity"])
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["from grid"],
                                bottom=filtered_df["trans buy quantity"])
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Transaction and from grid quantity")
    fig.tight_layout()
    plt.savefig("analysis/figures/overview_quant_trans_and_from_grid.png")
    plt.show()


def overview_cost_trans_and_grid():

    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = (overview_df["trans cost"] + overview_df["grid cost"]).max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large"])

    for row, scenario in enumerate(scenarios):
        scenario_df = overview_df[overview_df["scenario"] == scenario]
        for column, month in enumerate([1, 4, 7]):
            filtered_df = scenario_df[scenario_df["month"] == month]
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["trans cost"])
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["grid cost"],
                                bottom=filtered_df["trans cost"])
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Transaction and from grid cost")
    fig.tight_layout()
    plt.savefig("analysis/figures/overview_cost_trans_and_grid.png")
    plt.show()


def overview_revenue_trans_and_grid():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = (overview_df["trans revenue"] + overview_df["grid revenue"]).max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large"])

    for row, scenario in enumerate(scenarios):
        scenario_df = overview_df[overview_df["scenario"] == scenario]
        for column, month in enumerate([1, 4, 7]):
            filtered_df = scenario_df[scenario_df["month"] == month]
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["trans revenue"])
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["grid revenue"],
                                bottom=filtered_df["trans revenue"])
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Transaction and from grid revenue")
    fig.tight_layout()
    plt.savefig("analysis/figures/overview_revenue_trans_and_grid.png")
    plt.show()


def overview_average_price_trans():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = overview_df["trans avg price"].max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large"])

    for row, scenario in enumerate(scenarios):
        scenario_df = overview_df[overview_df["scenario"] == scenario]
        for column, month in enumerate([1, 4, 7]):
            filtered_df = scenario_df[scenario_df["month"] == month]
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["trans avg price"])
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Average transaction price")
    fig.tight_layout()
    plt.savefig("analysis/figures/overview_average_price_trans.png")
    plt.show()


def overview_trans_prices():
    ax: Axes

    auction_types = ["d", "c", "i", "i2"]

    fig, ax = plt.subplots(3, 3, figsize=figsize["large"])

    for row, scenario in enumerate(scenarios):
        for column, month in enumerate([1, 4, 7]):
            trans_prices = list()
            for auction_type in auction_types:
                trans_prices.append(load_from_csv(file_name="all_transactions",
                                                  folder=f"{scenario}-{month}-{auction_type}/transactions")["price"])
            ax[row][column].boxplot(trans_prices, labels=auction_types)
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, 0.4573])
    fig.suptitle("Transaction prices")
    fig.tight_layout()
    plt.savefig("analysis/figures/overview_trans_prices.png")
    plt.show()


def overview_supply_cover_factors():
    ax: Axes
    fig: Figure

    kpi_df = load_from_csv("KPIs")

    max_value = max(kpi_df["scf"].max(), kpi_df["mscf"].max())
    x = np.arange(4)
    fig, ax = plt.subplots(3, 3, figsize=figsize["large"])

    for row, scenario in enumerate(scenarios):
        for column, month in enumerate([1, 4, 7]):
            filtered_df = kpi_df[kpi_df["case"].str.contains(f"{scenario}-{month}")]
            ax[row][column].bar(x=x - 0.1, height=filtered_df["scf"], width=0.2)
            ax[row][column].bar(x=x + 0.1, height=filtered_df["mscf"], width=0.2)
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Supply cover factor")
    fig.tight_layout()
    plt.savefig("analysis/figures/overview_supply_cover_factors.png")
    plt.show()


def overview_demand_cover_factors():
    ax: Axes
    fig: Figure

    kpi_df = load_from_csv("KPIs")

    max_value = max(kpi_df["dcf"].max(), kpi_df["mdcf"].max())
    x = np.arange(4)
    fig, ax = plt.subplots(3, 3, figsize=figsize["large"])

    for row, scenario in enumerate(scenarios):
        for column, month in enumerate([1, 4, 7]):
            filtered_df = kpi_df[kpi_df["case"].str.contains(f"{scenario}-{month}")]
            ax[row][column].bar(x=x - 0.1, height=filtered_df["dcf"], width=0.2)
            ax[row][column].bar(x=x + 0.1, height=filtered_df["mdcf"], width=0.2)
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Demand cover factor")
    fig.tight_layout()
    plt.savefig("analysis/figures/overview_demand_cover_factors.png")
    plt.show()


def overview_gain():

    kpi_df = load_from_csv("KPIs")

    max_value = kpi_df["gain"].max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large"])

    for row, scenario in enumerate(scenarios):
        for column, month in enumerate([1, 4, 7]):
            filtered_df = kpi_df[kpi_df["case"].str.contains(f"{scenario}-{month}")]
            ax[row][column].bar(x=filtered_df["case"], height=filtered_df["gain"])
            #ax[row][column].set_xticklabels(filtered_df["case"])
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Gain")
    fig.tight_layout()
    plt.savefig("figures/overview_gain.png")
    plt.show()


def box_plot_trans_prices(cases: list):
    ax: Axes
    fig: Figure

    trans_prices = list()
    for case in cases:
        trans_df = load_from_csv(file_name="all_transactions", folder=f"{case}/transactions")
        trans_prices.append(trans_df["price"])

    fig, ax = plt.subplots()
    ax.boxplot(trans_prices, labels=cases)
    plt.ylim([0, 0.4573])
    plt.savefig("analysis/figures/box_plot_trans_prices.png")
    plt.show()


def overview_new_wt():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = overview_df["trans buy quantity"].max()

    fig, ax = plt.subplots(3, 1, figsize=(4, 12))

    for row, scenario in enumerate(["new_WT_1", "new_WT_2", "new_WT_3"]):
        scenario_df = overview_df[overview_df["scenario"] == scenario]
        for column, month in enumerate([1]):
            filtered_df = scenario_df[scenario_df["month"] == month]
            ax[row].bar(x=filtered_df["auction_type"], height=filtered_df["trans buy quantity"])
            ax[row].set_title(f"Scenario {scenario}, month {month}")
            ax[row].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Transaction Quantity")
    fig.tight_layout()
    plt.savefig("figures/new_WT_trans_quant.png")
    plt.show()


def overview_new_wt_2():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = overview_df["trans avg price"].max()

    fig, ax = plt.subplots(3, 1, figsize=(4, 12))

    for row, scenario in enumerate(["new_WT_1", "new_WT_2", "new_WT_3"]):
        scenario_df = overview_df[overview_df["scenario"] == scenario]
        for column, month in enumerate([1]):
            filtered_df = scenario_df[scenario_df["month"] == month]
            ax[row].bar(x=filtered_df["auction_type"], height=filtered_df["trans avg price"])
            ax[row].set_title(f"Scenario {scenario}, month {month}")
            ax[row].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Transaction Average Price")
    fig.tight_layout()
    plt.savefig("figures/new_WT_avg_price.png")
    plt.show()


def wt_generation_profile():
    fig, ax = plt.subplots(3, 1, figsize=figsize["generation_profile_half"])
    df1 = load_from_csv(file_name="WT_opti", folder="40_1-1-d/opti")
    df2 = load_from_csv(file_name="WT_opti", folder="40_1-4-d/opti")
    df3 = load_from_csv(file_name="WT_opti", folder="40_1-7-d/opti")

    max_value = 6

    ax[0].bar(x=df1["n_opt"], height=df1["surplus"]/1e6)
    ax[0].set_title("January")
    ax[0].set_xlim([df1["n_opt"].min(), df1["n_opt"].max()])
    ax[1].bar(x=df2["n_opt"], height=df2["surplus"]/1e6)
    ax[1].set_title("April")
    ax[1].set_xlim([df2["n_opt"].min(), df2["n_opt"].max()])
    ax[2].bar(x=df3["n_opt"], height=df3["surplus"]/1e6)
    ax[2].set_title("July")
    ax[2].set_xlim([df3["n_opt"].min(), df3["n_opt"].max()])

    for a in ax:
        a.set_ylim([0, max_value])
        a.set_yticks([0, 6])
        a.set_ylabel("MW")
        a.set_xticks([])
    #fig.suptitle("Electricity production of wind turbine")
    fig.tight_layout()
    plt.savefig("figures/WT_generation_profile.pdf")
    plt.show()


def pv_generation_profile():
    fig, ax = plt.subplots(3, 1, figsize=figsize["generation_profile_half"])
    df1 = load_from_csv(file_name="pv_generation_steps_jan", folder="opti_res")
    df2 = load_from_csv(file_name="pv_generation_steps_apr", folder="opti_res")
    df3 = load_from_csv(file_name="pv_generation_steps_jul", folder="opti_res")

    max_value = max(df1["quant"].max(), df2["quant"].max(), df3["quant"].max())/1e6

    ax[0].bar(x=df1["n_opt"], height=df1["quant"]/1e6)
    ax[0].set_title("January")
    ax[0].set_xlim([df1["n_opt"].min(), df1["n_opt"].max()])
    ax[1].bar(x=df2["n_opt"], height=df2["quant"]/1e6)
    ax[1].set_title("April")
    ax[1].set_xlim([df2["n_opt"].min(), df2["n_opt"].max()])
    ax[2].bar(x=df3["n_opt"], height=df3["quant"]/1e6)
    ax[2].set_title("July")
    ax[2].set_xlim([df3["n_opt"].min(), df3["n_opt"].max()])

    for a in ax:
        a.set_ylim([0, max_value])
        a.set_yticks([0, 0.3])
        a.set_ylabel("MW")
        a.set_xticks([])
    #fig.suptitle("Electricity production of wind turbine")
    fig.tight_layout()
    plt.savefig("figures/PV_generation_profile.pdf")
    plt.show()


def dcf():
    fig, ax = plt.subplots(1, 1, figsize=figsize["dcf_scf_half"])
    width = 0.3
    x = np.arange(3)
    kpi_df = load_from_csv("KPIs")

    ax.bar(x=x - width,
           height=kpi_df.loc[kpi_df["case"].isin(["fixed_1-1-d", "fixed_1-4-d", "fixed_1-7-d"])]["dcf"]*100,
           width=width, label="1")
    ax.bar(x=x,
           height=kpi_df.loc[kpi_df["case"].isin(["fixed_2-1-d", "fixed_2-4-d", "fixed_2-7-d"])]["dcf"]*100,
           width=width, label="2")
    ax.bar(x=x + width,
           height=kpi_df.loc[kpi_df["case"].isin(["fixed_3-1-d", "fixed_3-4-d", "fixed_3-7-d"])]["dcf"]*100,
           width=width, label="3")

    ax.set_xticks(ticks=x, labels=["January", "April", "July"])

    ax.set_yticks(ticks=np.arange(start=0, stop=90, step=10))
    ax.set_ylabel("DCF in %")

    ax.grid(axis="y", linestyle="--")

    line, labels = ax.get_legend_handles_labels()
    plt.figlegend(handles=line, labels=labels, loc="center", title="Scenario:", bbox_to_anchor=(0.55, 0.1), ncol=3)
    fig.tight_layout(rect=(0, 0.14, 1, 1))
    plt.savefig("figures/dcf.pdf")
    plt.show()


def scf():
    fig, ax = plt.subplots(1, 1, figsize=figsize["dcf_scf_half"])
    width = 0.3
    x = np.arange(3)
    kpi_df = load_from_csv("KPIs")

    ax.bar(x=x - width,
           height=kpi_df.loc[kpi_df["case"].isin(["fixed_1-1-d", "fixed_1-4-d", "fixed_1-7-d"])]["scf"]*100,
           width=width, label="1")
    ax.bar(x=x,
           height=kpi_df.loc[kpi_df["case"].isin(["fixed_2-1-d", "fixed_2-4-d", "fixed_2-7-d"])]["scf"]*100,
           width=width, label="2")
    ax.bar(x=x + width,
           height=kpi_df.loc[kpi_df["case"].isin(["fixed_3-1-d", "fixed_3-4-d", "fixed_3-7-d"])]["scf"]*100,
           width=width, label="3")

    ax.set_xticks(ticks=x, labels=["January", "April", "July"])

    ax.set_yticks(ticks=np.arange(start=0, stop=8, step=1))

    ax.grid(axis="y", linestyle="--")
    ax.set_ylabel("SCF in %")

    line, labels = ax.get_legend_handles_labels()
    plt.figlegend(handles=line, labels=labels, loc="center", title="Scenario:", bbox_to_anchor=(0.55, 0.1), ncol=3)
    fig.tight_layout(rect=(0, 0.14, 1, 1))
    plt.savefig("figures/scf.pdf")
    plt.show()


def dcf_scf():
    ax: list[Axes]
    fig: Figure

    fig, ax = plt.subplots(1, 2, figsize=(11.7, 3.5))
    width = 0.3
    x = np.arange(3)
    kpi_df = load_from_csv("KPIs")

    ax[0].bar(x=x - width, height=kpi_df.loc[kpi_df["case"].isin(["40_1-1-d", "40_1-4-d", "40_1-7-d"])]["dcf"],
              width=width, label="Scenario 1")
    ax[0].bar(x=x, height=kpi_df.loc[kpi_df["case"].isin(["40_2-1-d", "40_2-4-d", "40_2-7-d"])]["dcf"],
              width=width, label="Scenario 2")
    ax[0].bar(x=x + width, height=kpi_df.loc[kpi_df["case"].isin(["40_3-1-d", "40_3-4-d", "40_3-7-d"])]["dcf"],
              width=width, label="Scenario 3")

    ax[1].bar(x=x - width, height=kpi_df.loc[kpi_df["case"].isin(["40_1-1-d", "40_1-4-d", "40_1-7-d"])]["scf"],
              width=width, label="Scenario 1")
    ax[1].bar(x=x, height=kpi_df.loc[kpi_df["case"].isin(["40_2-1-d", "40_2-4-d", "40_2-7-d"])]["scf"],
              width=width, label="Scenario 2")
    ax[1].bar(x=x + width, height=kpi_df.loc[kpi_df["case"].isin(["40_3-1-d", "40_3-4-d", "40_3-7-d"])]["scf"],
              width=width, label="Scenario 3")

    ax[0].set_xticks(ticks=x, labels=["January", "April", "July"])
    ax[1].set_xticks(ticks=x, labels=["January", "April", "July"])

    ax[0].set_yticks(ticks=np.arange(start=0, stop=0.9, step=0.1))
    ax[1].set_yticks(ticks=np.arange(start=0, stop=0.08, step=0.01))

    ax[0].grid(axis="y", linestyle="--")
    ax[1].grid(axis="y", linestyle="--")

    ax[0].set_title("DCF")
    ax[1].set_title("SCF")

    line, labels = ax[0].get_legend_handles_labels()
    plt.figlegend(handles=line, labels=labels, loc="upper right")
    fig.tight_layout()
    plt.savefig("figures/scf_dcf.pdf")
    plt.show()


def pv_wt_profiles():
    fig, ax = plt.subplots(3, 2, figsize=(11.7, 4))
    df1 = load_from_csv(file_name="WT_opti", folder="40_1-1-d/opti")
    df2 = load_from_csv(file_name="WT_opti", folder="40_1-4-d/opti")
    df3 = load_from_csv(file_name="WT_opti", folder="40_1-7-d/opti")

    max_value = 6

    ax[0][0].bar(x=df1["n_opt"], height=df1["surplus"]/1e6)
    ax[0][0].set_title("January")
    ax[0][0].set_xlim([df1["n_opt"].min(), df1["n_opt"].max()])
    ax[1][0].bar(x=df2["n_opt"], height=df2["surplus"]/1e6)
    ax[1][0].set_title("April")
    ax[1][0].set_xlim([df2["n_opt"].min(), df2["n_opt"].max()])
    ax[2][0].bar(x=df3["n_opt"], height=df3["surplus"]/1e6)
    ax[2][0].set_title("July")
    ax[2][0].set_xlim([df3["n_opt"].min(), df3["n_opt"].max()])

    for a in ax[0]:
        a.set_ylim([0, max_value])
        a.set_yticks([0, 3, 6])
        a.set_ylabel("MWh")
        a.set_xticks([])
    #fig.suptitle("Electricity production of wind turbine")
    fig.tight_layout()
    plt.savefig("figures/WT_generation_profile.pdf")
    plt.show()


def overview_wt_bid_prices():
    ax: list[list[Axes]]

    auction_types = ["d", "c", "i", "i2"]

    fig, ax = plt.subplots(3, 3, figsize=figsize["small_square"])

    for row, scenario in enumerate(scenarios):
        for column, month in enumerate([1, 4, 7]):
            bid_prices = list()
            for auction_type in auction_types:
                bid_prices.append(load_from_csv(file_name="WT_selling_bids",
                                                  folder=f"{scenario}-{month}-{auction_type}/bids")["price"])
            ax[row][column].boxplot(bid_prices, labels=auction_types)
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, 0.4573])
    fig.suptitle("WT bid prices")
    fig.tight_layout()
    plt.savefig("figures/overview_wt_bid_prices.png")
    plt.show()


def overview_mdcf_ratio():

    kpi_df = load_from_csv("KPIs")

    max_value = 1.1

    fig, ax = plt.subplots(3, 3, figsize=figsize["large"])

    for row, scenario in enumerate(scenarios):
        for column, month in enumerate([1, 4, 7]):
            filtered_df = kpi_df[kpi_df["case"].str.contains(f"{scenario}-{month}")]
            ax[row][column].bar(x=filtered_df["case"], height=filtered_df["mdcf_ratio"])
            #ax[row][column].set_xticklabels(filtered_df["case"])
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    #fig.suptitle("Gain")
    fig.tight_layout()
    plt.savefig("figures/overview_mdcf_ratio.png")
    plt.show()


def df_ratio():
    ax: list[Axes]
    fig: Figure

    kpi_df = load_from_csv("KPIs")
    fig, ax = plt.subplots(3, 1, figsize=figsize["large"])

    x = np.arange(3)
    spacing = 0.2
    width = 0.2

    for row, scenario in enumerate(scenarios):
        scenario_df = kpi_df[kpi_df["scenario"] == scenario]
        ax[row].bar(x=x - 1.5 * spacing,
                    height=scenario_df[scenario_df["auction_type"] == "d"]["mdcf_ratio"]*100,
                    width=width, label="DA")
        ax[row].bar(x=x - 0.5 * spacing,
                    height=scenario_df[scenario_df["auction_type"] == "c"]["mdcf_ratio"]*100,
                    width=width, label="CDA")
        ax[row].bar(x=x + 0.5 * spacing,
                    height=scenario_df[scenario_df["auction_type"] == "i"]["mdcf_ratio"]*100,
                    width=width, label="IDA1")
        ax[row].bar(x=x + 1.5 * spacing,
                    height=scenario_df[scenario_df["auction_type"] == "i2"]["mdcf_ratio"]*100,
                    width=width, label="IDA2")

    ax[0].set_title("Scenario 1")
    ax[1].set_title("Scenario 2")
    ax[2].set_title("Scenario 3")

    for a in ax:
        a.set_ylim([0, 110])
        a.set_xticks(ticks=x, labels=["January", "April", "July"])
        a.set_yticks(np.arange(0, 120, 20))
        a.grid(axis="y", linestyle="--")
        a.set_ylabel("mCFR in %")

    line, labels = ax[0].get_legend_handles_labels()
    plt.figlegend(handles=line, labels=labels, loc="center", bbox_to_anchor=(0.53, 0.02), ncol=4)

    fig.tight_layout(rect=(0, 0.02, 1, 1))
    plt.savefig("figures/cf_ratio.pdf")

    plt.show()


def ratio_bid_correlation():
    fig: Figure
    ax: Axes

    overview_df = load_from_csv("overview")
    kpi_df = load_from_csv("KPIs")
    fig, ax = plt.subplots(1, 1, figsize=figsize["small_square"])

    prices = overview_df[overview_df["auction_type"].isin(["d", "c", "i"])]["wt bid price mean"]
    ratios = kpi_df[~kpi_df["case"].str.contains("i2")]["mdcf_ratio"]

    a, b = np.polyfit(x=prices, y=ratios, deg=1)

    ax.scatter(x=prices, y=ratios, marker="x", s=10)
    ax.plot(prices, a*prices+b, color=colors["orange"], linewidth=1)
    ax.set_xlabel("WT bid price mean")
    ax.set_ylabel("Cover-factor ratio")
    fig.tight_layout()
    plt.savefig("figures/ratio_bid_correlation.pdf")
    plt.show()


def bandwidth():
    fig: Figure
    ax: Axes

    fig, ax = plt.subplots(1, 1, figsize=figsize["small"])

    cases = ["DA", "CDA", "IDA"]
    values = [2, 2.3, 3.5]

    ax.bar("DA", 2)
    ax.bar("CDA", 2.3)
    ax.bar("IDA", 3.5)
    ax.set_ylabel("kbit/s")
    ax.grid(axis="y", linestyle="--")
    fig.tight_layout()
    plt.savefig("figures/bandwidth.pdf")
    plt.show()


def gains():
    ax: list[Axes]
    fig: Figure

    kpi_df = load_from_csv("KPIs")  # € to k€
    fig, ax = plt.subplots(3, 1, figsize=figsize["large"])

    x = np.arange(3)
    spacing = 0.21
    width = 0.2

    for row, scenario in enumerate(scenarios):
        scenario_df = kpi_df[kpi_df["scenario"] == scenario]
        ax[row].bar(x=x - 1.5 * spacing, height=scenario_df[scenario_df["auction_type"] == "d"]["gain"],
                    width=width, label="DA")
        ax[row].bar(x=x - 0.5 * spacing, height=scenario_df[scenario_df["auction_type"] == "c"]["gain"],
                    width=width, label="CDA")
        ax[row].bar(x=x + 0.5 * spacing, height=scenario_df[scenario_df["auction_type"] == "i"]["gain"],
                    width=width, label="IDA1")
        ax[row].bar(x=x + 1.5 * spacing, height=scenario_df[scenario_df["auction_type"] == "i2"]["gain"],
                    width=width, label="IDA2")

    ax[0].set_title("Scenario 1")
    ax[1].set_title("Scenario 2")
    ax[2].set_title("Scenario 3")

    for a in ax:
        a.set_xticks(ticks=x, labels=["January", "April", "July"])
        a.set_ylim([0, 17])
        a.set_yticks(np.arange(0, 16, 5))
        a.set_ylabel("k€")
        a.grid(axis="y", linestyle="--")

    line, labels = ax[0].get_legend_handles_labels()
    plt.figlegend(handles=line, labels=labels, loc="center", bbox_to_anchor=(0.92, 0.25))

    fig.tight_layout()
    plt.savefig("figures/gains.pdf")

    plt.show()


def gains_participants_wt():
    ax: list[Axes]
    fig: Figure

    kpi_df = load_from_csv("KPIs")  # € to k€
    fig, ax = plt.subplots(3, 1, figsize=figsize["large"])

    x = np.arange(3)
    spacing = 0.2
    width = 0.2

    for row, scenario in enumerate(scenarios):
        scenario_df = kpi_df[kpi_df["scenario"] == scenario]
        ax[row].bar(x=x - 1.5 * spacing,
                    height=scenario_df[scenario_df["auction_type"] == "d"]["gain_wt"] / 1000,
                    width=width, label="_DA (WT)",
                    bottom=scenario_df[scenario_df["auction_type"] == "d"]["gain_without_wt"] / 1000,
                    hatch="//",
                    color=chosen_colors[4])
        ax[row].bar(x=x - 1.5 * spacing,
                    height=scenario_df[scenario_df["auction_type"] == "d"]["gain_without_wt"] / 1000,
                    width=width, label="DA",
                    color=chosen_colors[0])

        ax[row].bar(x=x - 0.5 * spacing,
                    height=scenario_df[scenario_df["auction_type"] == "c"]["gain_wt"] / 1000,
                    width=width, label="_CDA (WT)",
                    bottom=scenario_df[scenario_df["auction_type"] == "c"]["gain_without_wt"] / 1000,
                    hatch="//",
                    color=chosen_colors[5])
        ax[row].bar(x=x - 0.5 * spacing,
                    height=scenario_df[scenario_df["auction_type"] == "c"]["gain_without_wt"] / 1000,
                    width=width, label="CDA",
                    color=chosen_colors[1])

        ax[row].bar(x=x + 0.5 * spacing,
                    height=scenario_df[scenario_df["auction_type"] == "i"]["gain_wt"] / 1000,
                    width=width, label="_IDA1 (WT)",
                    bottom=scenario_df[scenario_df["auction_type"] == "i"]["gain_without_wt"] / 1000,
                    hatch="//",
                    color=chosen_colors[6])
        ax[row].bar(x=x + 0.5 * spacing,
                    height=scenario_df[scenario_df["auction_type"] == "i"]["gain_without_wt"] / 1000,
                    width=width, label="IDA1",
                    color=chosen_colors[2])

        ax[row].bar(x=x + 1.5 * spacing,
                    height=scenario_df[scenario_df["auction_type"] == "i2"]["gain_wt"] / 1000,
                    width=width, label="_IDA2 (WT)",
                    bottom=scenario_df[scenario_df["auction_type"] == "i2"]["gain_without_wt"] / 1000,
                    hatch="//",
                    color=chosen_colors[7])
        ax[row].bar(x=x + 1.5 * spacing,
                    height=scenario_df[scenario_df["auction_type"] == "i2"]["gain_without_wt"] / 1000,
                    width=width, label="IDA2",
                    color=chosen_colors[3])

    #texture_legend = matplotlib.lines.Line2D([0], [0], linestyle='None', marker="//", color='gray', markersize=10, label='Texture')
    ax[0].bar(x=1.5, height=0, color="gray", hatch="//", label="Gains of  WT")


    ax[0].set_title("Scenario 1")
    ax[1].set_title("Scenario 2")
    ax[2].set_title("Scenario 3")

    for a in ax:
        a.set_xticks(ticks=x, labels=["January", "April", "July"])
        a.set_ylim([0, 17])
        a.set_yticks(np.arange(0, 16, 5))
        a.set_ylabel("Gain in k€")
        a.grid(axis="y", linestyle="--")

    handles, labels = ax[0].get_legend_handles_labels()
    #handles.append(texture_legend)
    #labels.append("WT")
    plt.figlegend(handles=handles, labels=labels, loc="center", bbox_to_anchor=(0.53, 0.05), ncols=5)

    fig.tight_layout(rect=(0, 0.08, 1, 1))
    plt.savefig("figures/gains_participants_wt.pdf")

    plt.show()


def transaction_prices():
    ax: list[Axes]

    auction_types = ["d", "c", "i", "i2"]

    fig, ax = plt.subplots(3, 1, figsize=figsize["large"])

    x = np.arange(3)
    spacing = 0.2
    width = 0.15

    flierprops = {
        "markersize": 5,
        #"markeredgewidth": 0.5
    }
    medianprops = {
        "color": "black",
        "linestyle": "--"
    }
    meanpointprops = {
        "marker": "v",
        "markerfacecolor": "white",
        "markeredgecolor": "black",
        "markersize": 4
    }

    for row, scenario in enumerate(scenarios):
        bid_prices = {x: list() for x in auction_types}
        for month in [1, 4, 7]:
            for auction_type in auction_types:
                bid_prices[auction_type].append(list(load_from_csv(file_name="all_transactions",
                                                folder=f"{scenario}-{month}-{auction_type}/transactions")["price"]))


        bp1 = ax[row].boxplot(bid_prices["d"], positions=x-1.5*spacing, widths=width,
                              flierprops=flierprops, showfliers=False,
                              patch_artist=True, medianprops=medianprops,
                              showmeans=True, meanline=False, meanprops=meanpointprops)
        bp2 = ax[row].boxplot(bid_prices["c"], positions=x - 0.5 * spacing, widths=width,
                              flierprops=flierprops, showfliers=False,
                              patch_artist=True, medianprops=medianprops,
                              showmeans=True, meanline=False, meanprops=meanpointprops)
        bp3 = ax[row].boxplot(bid_prices["i"], positions=x + 0.5 * spacing, widths=width,
                              flierprops=flierprops, showfliers=False,
                              patch_artist=True, medianprops=medianprops,
                              showmeans=True, meanline=False, meanprops=meanpointprops)
        bp4 = ax[row].boxplot(bid_prices["i2"], positions=x + 1.5 * spacing, widths=width,
                              flierprops=flierprops, showfliers=False,
                              patch_artist=True, medianprops=medianprops,
                              showmeans=True, meanline=False, meanprops=meanpointprops)

        #set_box_color(bp1, chosen_colors[0])
        #set_box_color(bp2, chosen_colors[1])
        #set_box_color(bp3, chosen_colors[2])
        #set_box_color(bp4, chosen_colors[3])

        for color, bp in enumerate([bp1, bp2, bp3, bp4]):
            for patch in bp["boxes"]:
                patch.set_facecolor(chosen_colors[color])

        #bp1["boxes"].set_facecolor(chosen_colors[0])
        #bp2["boxes"].set_facecolor(chosen_colors[1])
        #bp3["boxes"].set_facecolor(chosen_colors[2])
        #bp4["boxes"].set_facecolor(chosen_colors[3])

    ax[0].set_title("Scenario 1")
    ax[1].set_title("Scenario 2")
    ax[2].set_title("Scenario 3")

    for a in ax:
        a.set_xlim([0-2.5*spacing, 2+3*spacing])
        a.set_xticks(ticks=x, labels=["January", "April", "July"])
        a.set_ylim([0, 0.5])
        a.set_yticks([0.08, 0.45])
        a.set_ylabel("€/kWh")
        a.grid(axis="y", linestyle="--")

    handles = [bp1["boxes"][0], bp2["boxes"][0], bp3["boxes"][0], bp4["boxes"][0]]
    labels = ["DA", "CDA", "IDA1", "IDA2"]
    plt.figlegend(handles=handles, labels=labels, loc="center", bbox_to_anchor=(0.54, 0.03), ncols=4)

    fig.tight_layout(rect=(0, 0.03, 1, 1))
    plt.savefig("figures/trans_prices.pdf")  # , dpi=400
    plt.show()


def ratio_new_wt_strategy():

    ax: Axes
    fig: Figure

    x = np.arange(3)
    spacing = 0.3
    width = 0.3

    DA_ratios = [0.64221, 0.65871, 0.65119]
    CDA_ratios = [0.7131, 0.69625, 0.70823]
    IDA2_ratios = [1, 1, 1]

    fig, ax = plt.subplots(1, 1, figsize=figsize["small_square"])

    ax.bar(x=x - spacing, height=DA_ratios, label="DA", width=width)
    ax.bar(x=x, height=CDA_ratios, label="CDA", width=width)
    ax.bar(x=x + spacing, height=IDA2_ratios, label="IDA2", width=width)

    ax.set_xticks(x, ["1", "2", "3"])
    ax.set_xlabel("Scenario")
    ax.set_yticks(ticks=np.arange(start=0, stop=1.1, step=0.2))
    ax.grid(axis="y", linestyle="--")
    ax.legend(loc="lower right")

    fig.tight_layout()
    plt.savefig("figures/ratio_new_WT_strategy.pdf")
    plt.show()


if __name__ == "__main__":
    #bandwidth()
    #wt_generation_profile()
    #pv_generation_profile()
    #dcf()
    #scf()
    df_ratio()
    gains_participants_wt()
    #ratio_bid_correlation()
    #transaction_prices()
    #ratio_new_wt_strategy()
