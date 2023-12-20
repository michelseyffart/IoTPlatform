import json
import time

import requests.exceptions
from filip.clients.ngsi_v2.cb import ContextBrokerClient, FiwareHeader, ContextEntity
from filip.clients.ngsi_v2.iota import IoTAClient, ServiceGroup
from requests import Session
from auctions import dummy, iterating_auction
from fiware.config.paths import path_fiware_templates_folder
from fiware.setup import post_entity_transaction, post_entity_auction_iteration, post_entity_public_info
import datetime


CB_URL = "http://137.226.248.250:1026"
IOTA_URL = "http://137.226.248.250:4041"
FIWARE_HEADER = FiwareHeader(service="iotplatform", service_path="/")
s = Session()
cbc = ContextBrokerClient(url=CB_URL, fiware_header=FIWARE_HEADER, session=s)

step_length = 10
auction_time = 7


def collect_bids():
    bids = dict()
    entities = cbc.get_entity_list(type_pattern="Bid")
    for entity in entities:
        bids[entity.id.strip("Bid:")] = {
            "buying": entity.get_attribute("BidBuying").value,
            "price": entity.get_attribute("BidPrice").value,
            "quant": entity.get_attribute("BidQuantity").value,
        }
    return bids


def post_transactions(results: dict):
    for building in results:
        try:
            cbc.update_attribute_value(entity_id=f"Transaction:{building}", attr_name="TransactionBuying",
                                       value=results[building]["buying"])
            cbc.update_attribute_value(entity_id=f"Transaction:{building}", attr_name="TransactionPrice",
                                       value=results[building]["price"])
            cbc.update_attribute_value(entity_id=f"Transaction:{building}", attr_name="TransactionQuantity",
                                       value=results[building]["quant"])
        except requests.exceptions.HTTPError:
            post_entity_transaction(building=building, cbc=cbc)
            cbc.update_attribute_value(entity_id=f"Transaction:{building}", attr_name="TransactionBuying",
                                       value=results[building]["buying"])
            cbc.update_attribute_value(entity_id=f"Transaction:{building}", attr_name="TransactionPrice",
                                       value=results[building]["price"])
            cbc.update_attribute_value(entity_id=f"Transaction:{building}", attr_name="TransactionQuantity",
                                       value=results[building]["quant"])


def post_auction_iteration(auc_iter: dict):
    for building in auc_iter:
        try:
            cbc.update_attribute_value(entity_id=f"Auction_Iteration:{building}", attr_name="AuctionIterationStep",
                                       value=auc_iter[building]["step"])
            cbc.update_attribute_value(entity_id=f"Auction_Iteration:{building}", attr_name="AuctionIterationPrice",
                                       value=auc_iter[building]["price"])
            cbc.update_attribute_value(entity_id=f"Auction_Iteration:{building}", attr_name="AuctionIterationQuantity",
                                       value=auc_iter[building]["quant"])
        except requests.exceptions.HTTPError:
            post_entity_auction_iteration(building=building, cbc=cbc)
            cbc.update_attribute_value(entity_id=f"Auction_Iteration:{building}", attr_name="AuctionIterationStep",
                                       value=auc_iter[building]["step"])
            cbc.update_attribute_value(entity_id=f"Auction_Iteration:{building}", attr_name="AuctionIterationPrice",
                                       value=auc_iter[building]["price"])
            cbc.update_attribute_value(entity_id=f"Auction_Iteration:{building}", attr_name="AuctionIterationQuantity",
                                       value=auc_iter[building]["quant"])


def post_public_info(info: dict):
    try:
        cbc.update_attribute_value(entity_id="Public_Info", attr_name="EquilibriumPrice",
                                   value=info["equi_price"])
        cbc.update_attribute_value(entity_id="Public_Info", attr_name="EquilibriumQuantity",
                                   value=info["equi_quant"])
    except requests.exceptions.HTTPError:
        post_entity_public_info(cbc=cbc)
        cbc.update_attribute_value(entity_id="Public_Info", attr_name="EquilibriumPrice",
                                   value=info["equi_price"])
        cbc.update_attribute_value(entity_id="Public_Info", attr_name="EquilibriumQuantity",
                                   value=info["equi_quant"])


def whole_single_auction():
    print("Running auction")
    bids = collect_bids()
    transactions = dummy.run_auction(bids=bids)
    post_transactions(transactions)
    print("Ran auction")


def whole_iter_auction():
    print("Running auction")
    bids = collect_bids()
    auction_iter = iterating_auction.run_auction(bids)
    post_auction_iteration(auc_iter=auction_iter)
    print("Ran auction")


def coordinator_loop():
    while True:
        seconds = int(datetime.datetime.now().strftime("%S"))
        if (seconds - auction_time) % step_length == 0:
            whole_single_auction()
            time.sleep(1)
        time.sleep(0.1)


if __name__ == "__main__":
    coordinator_loop()
