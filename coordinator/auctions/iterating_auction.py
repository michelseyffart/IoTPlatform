import random


def run_auction(bids: dict):
    iteration = dict()

    for bid in bids:
        iteration[bid] = {
            "step": 5,
            "price": random.randint(0,30)/100,
            "quant": bids[bid]["quant"]
        }
    return iteration
