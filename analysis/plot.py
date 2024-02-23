from csv_handling import load_from_csv
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

figsize = {
    "large_overview": (12, 12)
}


plt.rcParams["font.size"] = 12


def trans_quant_of_cases(cases: list):
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")
    filtered_df = overview_df[overview_df["case"].isin(cases)]
    fig, axs = plt.subplots(nrows=2, ncols=1)
    axs[0].bar(x=filtered_df["case"], height=filtered_df["trans buy quantity"])
    axs[1].bar(x=filtered_df["case"], height=filtered_df["trans sell quantity"])
    fig.tight_layout()
    plt.show()


def overview_quant_trans():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = overview_df["trans buy quantity"].max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large_overview"])

    for row, scenario in enumerate(["40_1", "40_2", "40_3"]):
        scenario_df = overview_df[overview_df["scenario"] == scenario]
        for column, month in enumerate([1, 4, 7]):
            filtered_df = scenario_df[scenario_df["month"] == month]
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["trans buy quantity"])
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Transaction Quantity")
    fig.tight_layout()
    plt.show()


def overview_cost_trans():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = overview_df["trans cost"].max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large_overview"])

    for row, scenario in enumerate(["40_1", "40_2", "40_3"]):
        scenario_df = overview_df[overview_df["scenario"] == scenario]
        for column, month in enumerate([1, 4, 7]):
            filtered_df = scenario_df[scenario_df["month"] == month]
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["trans cost"])
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Transaction Cost/Revenue")
    fig.tight_layout()
    plt.show()


def overview_quant_trans_and_to_grid():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = (overview_df["trans sell quantity"] + overview_df["to grid"]).max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large_overview"])

    for row, scenario in enumerate(["40_1", "40_2", "40_3"]):
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
    plt.show()


def overview_quant_trans_and_from_grid():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = (overview_df["trans buy quantity"] + overview_df["from grid"]).max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large_overview"])

    for row, scenario in enumerate(["40_1", "40_2", "40_3"]):
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
    plt.show()


def overview_cost_trans_and_grid():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = (overview_df["trans cost"] + overview_df["grid cost"]).max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large_overview"])

    for row, scenario in enumerate(["40_1", "40_2", "40_3"]):
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
    plt.show()


def overview_revenue_trans_and_grid():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = (overview_df["trans revenue"] + overview_df["grid revenue"]).max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large_overview"])

    for row, scenario in enumerate(["40_1", "40_2", "40_3"]):
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
    plt.show()


def overview_average_price_trans():
    ax: Axes
    fig: Figure

    overview_df = load_from_csv("overview")

    max_value = overview_df["trans avg price"].max()

    fig, ax = plt.subplots(3, 3, figsize=figsize["large_overview"])

    for row, scenario in enumerate(["40_1", "40_2", "40_3"]):
        scenario_df = overview_df[overview_df["scenario"] == scenario]
        for column, month in enumerate([1, 4, 7]):
            filtered_df = scenario_df[scenario_df["month"] == month]
            ax[row][column].bar(x=filtered_df["auction_type"], height=filtered_df["trans avg price"])
            ax[row][column].set_title(f"Scenario {scenario}, month {month}")
            ax[row][column].set_ylim([0, max_value])
    plt.ylim([0, max_value])
    fig.suptitle("Average transaction price")
    fig.tight_layout()
    plt.show()
