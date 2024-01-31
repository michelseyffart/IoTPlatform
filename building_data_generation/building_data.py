import json
import classes.datahandler as datahandler
import numpy as np
import pickle
import openhab.openhab_container_scripts.opti as opti
from openhab.config.paths import path_openhab_container_scripts
from pathlib import Path


def calculate_nodes():
    dir_path = Path(path_openhab_container_scripts.joinpath("data", "nodes", scenario_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    nodes = {}
    nb_bes = districtData.district.__len__()
    pv_exists = np.zeros(shape=(nb_bes, 1))
    for n in range(nb_bes):
        nodes[n] = {
            "elec": districtData.district[n]['user'].elec,
            "heat": districtData.district[n]['user'].heat,
            "dhw": districtData.district[n]['user'].dhw,
            "T_air": districtData.site['T_e'],
            "type": districtData.district[n]['user'].building,
            "pv_power": districtData.district[n]['generationPV'],
            "devs": {}
        }
        nodes[n]["devs"]["COP_sh35"] = np.zeros(len(nodes[0]["T_air"]))
        nodes[n]["devs"]["COP_sh55"] = np.zeros(len(nodes[0]["T_air"]))
        pv_exists[n] = districtData.scenario.PV[n]

        # Check small demand values
        for t in range(len(nodes[0]["heat"])):
            if nodes[n]["heat"][t] < 0.01:
                nodes[n]["heat"][t] = 0
            if nodes[n]["dhw"][t] < 0.01:
                nodes[n]["dhw"][t] = 0
            if nodes[n]["elec"][t] < 0.01:
                nodes[n]["elec"][t] = 0
            if nodes[n]["pv_power"][t] < 0.01:
                nodes[n]["pv_power"][t] = 0

            # Calculation of Coefficient of Power
            nodes[n]["devs"]["COP_sh35"][t] = 0.4 * (273.15 + 35) / (35 - nodes[n]["T_air"][t])
            nodes[n]["devs"]["COP_sh55"][t] = 0.4 * (273.15 + 55) / (55 - nodes[n]["T_air"][t])

    devs = {}

    T_e_mean = np.mean(nodes[0]["T_air"])  # mean of outdoor temperature

    for n in range(nb_bes):
        devs[n] = {}
        """
            - eta = Q/P
            - omega = (Q+P) / E
        """
        # BATTERY
        devs[n]["bat"] = dict(cap=0.0, min_soc=0.05, max_ch=0.6, max_dch=0.6, max_soc=0.95, eta_bat=0.97, k_loss=0)
        # BOILER
        devs[n]["boiler"] = dict(cap=0.0, eta_th=0.97)
        # HEATPUMP
        devs[n]["hp35"] = dict(cap=0.0, dT_max=15, exists=0, mod_lvl=1)
        devs[n]["hp55"] = dict(cap=0.0,dT_max=15, exists=0, mod_lvl=1)
        # CHP FOR MULTI-FAMILY HOUSES
        devs[n]["chp"] = dict(cap=0.0, eta_th=0.62, eta_el=0.30, mod_lvl=0.6)
        devs[n]["bz"] = dict(cap=0.0, eta_th=0.53, eta_el=0.39)
        # ELECTRIC HEATER
        devs[n]["eh"] = dict(cap=0.0)
        # THERMAL ENERGY STORAGE
        devs[n]["tes"] = dict(cap=0.0, dT_max=35, min_soc=0.0, eta_tes=0.98, eta_ch=1, eta_dch=1)

        devs[n]["tes"]["cap"] = districtData.district[n]['capacities']['TES']

        if districtData.district[n]['capacities']['FC']:
            devs[n]["bz"]["cap"] = districtData.district[n]['capacities']['FC']

        if districtData.scenario.heater[n] == "BOI":
            devs[n]["boiler"]["cap"] = districtData.district[n]['capacities']['BOI']

        elif districtData.scenario.heater[n] == "HP":
            if ((districtData.district[n]['envelope'].construction_year > 1994) or
                    (districtData.district[n]['envelope'].construction_year > 1983 and
                     districtData.district[n]['envelope'].retrofit ==1) or
                    (districtData.district[n]['envelope'].construction_year > 1958 and
                     districtData.district[n]['envelope'].retrofit ==2)):
                # heat pump with 35C supply temperature
                devs[n]["eh"]["cap"] = districtData.district[n]['capacities']['EH']
                devs[n]["hp35"]["cap"] = districtData.district[n]['capacities']['HP']
                devs[n]["hp35"]["exists"] = 1

            else: # heat pump with 55C supply temperature
                devs[n]["eh"]["cap"] = districtData.district[n]['capacities']['EH']
                devs[n]["hp55"]["cap"] = districtData.district[n]['capacities']['HP']
                devs[n]["hp55"]["exists"] = 1

        elif districtData.scenario.heater[n] == "CHP":
            devs[n]["chp"]["cap"] = districtData.district[n]['capacities']['CHP']

        else:
            pass

        nodes[n]["devs"]["bat"] = devs[n]["bat"]
        nodes[n]["devs"]["eh"] = devs[n]["eh"]
        nodes[n]["devs"]["hp35"] = devs[n]["hp35"]
        nodes[n]["devs"]["hp55"] = devs[n]["hp55"]
        nodes[n]["devs"]["tes"] = devs[n]["tes"]
        nodes[n]["devs"]["chp"] = devs[n]["chp"]
        nodes[n]["devs"]["boiler"] = devs[n]["boiler"]
        nodes[n]["devs"]["bz"] = devs[n]["bz"]

        with open(dir_path.joinpath(f"{n}.p"), "wb") as f:
            pickle.dump(nodes[n], f)

    return nodes, devs


def calculate_opti_results(nodes):
    dir_path = Path(path_openhab_container_scripts.joinpath("data", "opti_results", scenario_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    with open(path_openhab_container_scripts.joinpath("data/par_rh.p"), "rb") as f:
        par_rh = pickle.load(f)
    with open(path_openhab_container_scripts.joinpath("data/params.json"), "rb") as f:
        params = json.load(f)
    with open(path_openhab_container_scripts.joinpath("data/options.json"), "rb") as f:
        options = json.load(f)

    init_val = {
        "soc": {
            "tes": 0.0,
            "bat": 0
        }}

    for n in range(40):
        opti_res = {}
        for n_opt in range(8760):
            return_string = opti.compute(node=nodes[n], params=params, par_rh=par_rh, init_val=init_val,
                                         options=options, n_opt=n_opt)
            init_val["soc"]["tes"] = float(return_string.split("res_soc:")[1])
            opti_res[n_opt] = return_string
            print(f"Finished building {n}, step {n_opt}.")
        print(f"Finished building {n}.")
        with open(dir_path.joinpath(f"{n}.p"), "wb") as f:
            pickle.dump(opti_res, f)


if __name__ == "__main__":
    scenario_name = "40_buildings"
    districtData = datahandler.Datahandler()
    districtData.generateDistrictComplete(scenario_name, calcUserProfiles=False, saveUserProfiles=True, )
    districtData.designDevicesComplete(saveGenerationProfiles=True)

    nodes, devs = calculate_nodes()

    #calculate_opti_results(nodes=nodes)
