import data_parsing
import building_overview
import case_overview
import validity
import full_overview
import plot
import kpis
import time

from raw_data_list import *


def data_preparation(fn: list, c_ids: list, b: list):

    for file_name in fn:
        data_parsing.parse_and_save(case=file_name[0], mqtt_file=file_name[1], python_file=file_name[2])

    data_parsing.separate_and_save_data_for_buildings(cases=c_ids, buildings=b)
    data_parsing.calculate_interval_and_start_of_case(cases=c_ids, buildings=b)
    data_parsing.accumulate_transactions(cases=c_ids, buildings=b)

    building_overview.supply_demand(cases=c_ids, buildings=b)
    building_overview.merge_bids_in_building_overview(cases=c_ids, buildings=b)
    building_overview.merge_transactions_in_building_overview(cases=c_ids, buildings=b)
    building_overview.calculate_and_merge_grid_in_building_overview(cases=c_ids, buildings=b)

    case_overview.demand_surplus_transaction_grid(cases=c_ids, buildings=b)
    case_overview.demand_surplus_transaction_grid(cases=c_ids, buildings=b, without_WT=True)

    full_overview.demand_surplus_transaction_grid(cases=c_ids)
    full_overview.demand_surplus_transaction_grid(cases=c_ids, without_WT=True)


def calculate_kpis(c_ids: list):
    kpis.new_kpi_csv(cases=c_ids)
    kpis.gain(cases=c_ids)
    kpis.dcf_scf_mdcf_mscf(cases=c_ids)
    kpis.mean_transaction_price(cases=c_ids)


def plot_overviews():
    plot.overview_quant_trans()
    plot.overview_cost_trans()
    plot.overview_quant_trans_and_to_grid()
    plot.overview_quant_trans_and_from_grid()
    plot.overview_cost_trans_and_grid()
    plot.overview_revenue_trans_and_grid()
    plot.overview_average_price_trans()
    plot.overview_trans_prices()
    plot.overview_supply_cover_factors()
    plot.overview_demand_cover_factors()


if __name__ == "__main__":
    data_preparation(fn=fixed_filenames, c_ids=fixed_case_ids, b=buildings)
    validity.check_validity(cases=fixed_case_ids, buildings=buildings)
    calculate_kpis(c_ids=fixed_case_ids)

