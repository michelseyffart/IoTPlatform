import pickle

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


def calculate_opti_results(data):
    opti_res = dict()
    for n_opt in range(8760):
        opti_res[n_opt] = f"surplus:{data[n_opt]}, demand:0, res_soc:0"
    return opti_res


def save_opti_results(opti_res: dict, scenario: str):
    dir_path = Path(path_openhab_container_scripts.joinpath("data", "opti_results", scenario))
    dir_path.mkdir(parents=True, exist_ok=True)
    with open(dir_path.joinpath("WT.p"), "wb") as f:
        pickle.dump(opti_res, f)


if __name__ == "__main__":
    elec_production = generate_data()
    opti_results = calculate_opti_results(data=elec_production)
    save_opti_results(opti_res=opti_results, scenario="half_pv")
