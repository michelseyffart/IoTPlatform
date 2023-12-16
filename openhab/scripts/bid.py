import random
import sys


def compute_bid():
    if demand > 0:
        buying = True
        quant = demand
        price = random.randint(4, 30)/100
    elif surplus > 0:
        buying = False
        quant = surplus
        price = random.randint(4, 30) / 100
    else:
        buying = False
        quant = 0
        price = 0
    print(f"buying:{buying}, quant:{quant}, price:{price},")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        demand = float(sys.argv[1])
        surplus = float(sys.argv[2])
        compute_bid()
    else:
        print("Missing args")
