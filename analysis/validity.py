from csv_handling import load_from_csv


def check_validity(cases: str | list, buildings: str | list):
    if isinstance(cases, str):
        cases = [cases]
    if isinstance(buildings, str):
        buildings = [buildings]
    for case in cases:
        print(f"Validity check {case}:", end="\t")
        print(f"Transaction balance: {transaction_balance(case=case, buildings=buildings)}", end="\t")
        print(f"Positive grid: {positive_grid(case=case, buildings=buildings)}")


def transaction_balance(case: str, buildings: list):
    buying = 0
    selling = 0
    passed = True
    for building in buildings:
        building_df = load_from_csv(file_name=building, folder=f"{case}/building_overviews")
        buying += building_df["trans buy quantity"].sum()
        selling += building_df["trans sell quantity"].sum()
    if abs(buying-selling) > 1:
        print(f"Transaction balance {case}: {buying-selling}.")
        passed = False
    return passed


def positive_grid(case: str, buildings: list):
    passed = True
    for building in buildings:
        building_df = load_from_csv(file_name=building, folder=f"{case}/building_overviews")
        if building_df["to grid"].min() < -1:
            print(f"To grid {case} building {building}: {building_df['to grid'].min()}")
            passed = False
        if building_df["from grid"].min() < -1:
            print(f"From grid {case} building {building}: {building_df['from grid'].min()}")
            passed = False
    return passed
