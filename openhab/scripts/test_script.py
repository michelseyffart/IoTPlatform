import pickle
import sys
from pathlib import Path

folder = Path(__file__).parent.resolve()


def save_to_pickle():
    data_dict = {
        "d": 15,
        "s": 20
    }
    file = folder.joinpath("example_data.p")
    if not file.exists():
        file.touch()
    with file.open("wb") as f:
        pickle.dump(data_dict, f)


def read_from_pickle():
    file = folder.joinpath("example_data.p")
    with file.open("rb") as f:
        data = pickle.load(f)
    demand = data["d"]
    surplus = data["s"]
    return_val = f"demand:{demand}, surplus:{surplus}"
    print(return_val)


def print_path():
    path = Path(__file__).parent.resolve()
    print(path)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "r":
            read_from_pickle()
        if sys.argv[1] == "s":
            save_to_pickle()
        if sys.argv[1] == "p":
            print_path()
