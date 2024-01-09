import random
import sys

p_min = 4
p_max = 30


def compute_bid():
    if demand * surplus != 0:
        print("Either demand or surplus need to be zero!")
        return None
    elif demand > 0:
        buying = True
        quant = demand
        price = random.randint(p_min, p_max)/100
    elif surplus > 0:
        buying = False
        quant = surplus
        price = random.randint(p_min, p_max) / 100
    else:
        buying = False
        quant = 0
        price = 0
    print(f"buying:{buying}, quant:{quant}, price:{price},")


if __name__ == "__main__":
    number_of_args = len(sys.argv) - 1
    if number_of_args == 2:
        demand = float(sys.argv[1])
        surplus = float(sys.argv[2])
        compute_bid()
    elif number_of_args == 4:
        demand = float(sys.argv[1])
        surplus = float(sys.argv[2])
        p_min = int(sys.argv[3])
        p_max = int(sys.argv[4])
        compute_bid()
    else:
        print(f"Expected 2 or 4 args (required: demand and surplus, optional: p_min and p_max in Cent), "
              f"received {number_of_args}")
