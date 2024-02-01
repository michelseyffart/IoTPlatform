import json

import classes.datahandler as datahandler

from openhab.config.paths import path_openhab_container_scripts
from pathlib import Path


def generate_data():
    scenario_name = "empty"
    districtData = datahandler.Datahandler()
    districtData.generateDistrictComplete(scenario_name=scenario_name,
                                          calcUserProfiles=False,
                                          saveUserProfiles=True,
                                          fileName_centralSystems="central_device_WT")
    districtData.designDevicesComplete(fileName_centralSystems="central_device_WT")
    return districtData.centralDevices["renewableGeneration"]["centralWT"]


def calculate_opti_results(data, scenario):
    opti_res = dict()
    for n_opt in range(8760):
        opti_res[n_opt] = f"surplus:{data[n_opt]}, demand:0, res_soc_tes:0, res_soc_bat:0"
    dir_path = Path(path_openhab_container_scripts.joinpath("data", "opti_results", scenario))
    dir_path.mkdir(parents=True, exist_ok=True)
    with open(dir_path.joinpath("WT.json"), "w") as f:
        json.dump(opti_res, f, indent=2)


def calculate_opti_results_for_months(data, months: list, scenario):
    dir_path = Path(path_openhab_container_scripts.joinpath("data", "opti_results", scenario))
    for month in months:
        month_dir_path = dir_path.joinpath(f"month_{month}")
        month_dir_path.mkdir(parents=True, exist_ok=True)

        opti_res = dict()
        for n_opt in range(8760):
            opti_res[n_opt] = f"surplus:{data[n_opt]}, demand:0, res_soc_tes:0, res_soc_bat:0"
        with open(month_dir_path.joinpath("WT.json"), "w") as f:
            json.dump(opti_res, f, indent=2)


if __name__ == "__main__":
    elec_production = generate_data()
    calculate_opti_results_for_months(data=elec_production, scenario="40_1", months=[1, 4, 7])
    calculate_opti_results_for_months(data=elec_production, scenario="40_2", months=[1, 4, 7])
    calculate_opti_results_for_months(data=elec_production, scenario="40_3", months=[1, 4, 7])
