import random


def run_auction(bids: dict):
    res = dict()
    for bid in bids:

        res[bid] = {
            "quant": bids[bid]["quant"],
            "price": random.randint(0, 30)/100,
            "buying": "True"
        }
    return res
