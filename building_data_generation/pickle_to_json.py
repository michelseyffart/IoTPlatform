import pickle
import json
from openhab.config.paths import path_openhab_container_scripts


def convert_pickle_to_python(fp):
    with open(fp, "rb") as f:
        data = pickle.load(f)

    new_file = str(file).replace(".p", ".json")
    with open(new_file, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    scenario = "40_1"
    data_dir = path_openhab_container_scripts.joinpath("data", "opti_results", scenario)
    for month in [1, 4, 7]:
        for building in range(40):
            file = data_dir.joinpath(f"month_{month}", f"{building}.p")
            convert_pickle_to_python(fp=file)
    