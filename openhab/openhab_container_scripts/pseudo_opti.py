from pathlib import Path
import sys
import json
import pickle

folder = Path(__file__).parent.resolve()
data_folder = folder.joinpath("data")


def main():
    n_opt = 0
    if len(sys.argv) > 1:
        n_opt = int(sys.argv[1])
    n_building = 0
    if len(sys.argv) > 2:
        n_building = int(sys.argv[2])
    if len(sys.argv) > 3:
        scenario = sys.argv[3]
    else:
        scenario = ""
    with data_folder.joinpath("opti_results").joinpath(scenario).joinpath(f"{n_building}.p").open("rb") as f:
        opti_res = pickle.load(f)
    print(opti_res[n_opt])


if __name__ == "__main__":
    main()
