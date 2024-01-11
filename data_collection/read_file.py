import pickle

file_name = "rawdata/2024-01-11-16-38-01.p"


def read_file():
    with open(file_name, "rb") as f:
        res = list()
        try:
            while True:
                res.append(pickle.load(f))
        except EOFError:
            pass
    return res


def parse_opti_from_data():
    opti_res = {}
    for data_point in data:
        if data_point[0].split("data/")[1].split("/")[0] == "opti":
            building = int(data_point[0].split("data/opti/")[1])
            if building not in opti_res:
                opti_res[building] = list()
            payload = data_point[1]
            res = {
                "n_opt": int(payload.split("surplus")[0]),
                "surplus": float(payload.split("surplus:")[1].split(",")[0]),
                "demand": float(payload.split("demand:")[1].split(",")[0]),
                "res_soc": float(payload.split("res_soc:")[1])
            }
            opti_res[building].append(res)
    return opti_res


if __name__ == "__main__":
    data = read_file()
    opti = parse_opti_from_data()
    print()
