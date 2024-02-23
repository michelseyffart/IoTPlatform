import data_parsing
import building_overview
import case_overview
import validity
import full_overview
import plot

from raw_data_list import *


def data_preparation():
    for file_name in file_names:
        data_parsing.parse_and_save(case=file_name[0], mqtt_file=file_name[1], python_file=file_name[2])

    data_parsing.separate_and_save_data_for_buildings(cases=case_ids, buildings=buildings)
    data_parsing.calculate_interval_and_start_of_case(cases=case_ids, buildings=buildings)
    data_parsing.accumulate_transactions(cases=case_ids, buildings=buildings)

    building_overview.supply_demand(cases=case_ids, buildings=buildings)
    building_overview.merge_bids_in_building_overview(cases=case_ids, buildings=buildings)
    building_overview.merge_transactions_in_building_overview(cases=case_ids, buildings=buildings)
    building_overview.calculate_and_merge_grid_in_building_overview(cases=case_ids, buildings=buildings)

    case_overview.demand_surplus_transaction_grid(cases=case_ids, buildings=buildings)

    validity.check_validity(cases=case_ids, buildings=buildings)

    full_overview.demand_surplus_transaction_grid(cases=case_ids)


def plot_overviews():
    plot.overview_quant_trans()
    plot.overview_cost_trans()
    plot.overview_quant_trans_and_to_grid()
    plot.overview_quant_trans_and_from_grid()
    plot.overview_cost_trans_and_grid()
    plot.overview_revenue_trans_and_grid()
    plot.overview_average_price_trans()


if __name__ == "__main__":
    data_preparation()
    plot_overviews()
