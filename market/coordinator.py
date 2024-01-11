import json
import time

import requests.exceptions
from filip.clients.ngsi_v2.cb import ContextBrokerClient, FiwareHeader, ContextEntity
from filip.clients.ngsi_v2.iota import IoTAClient, ServiceGroup
from requests import Session
from market.auctions import single_round_auction, iterating_auction
from fiware.config.paths import path_fiware_templates_folder
from fiware.setup import post_entity_transaction, post_entity_auction_iteration, post_entity_public_info
import datetime
import market.market_book as market_book
from market.bid import Bid
import openhab.config.config as config


class Coordinator:

    def __init__(self):

        self.CB_URL = "http://137.226.248.250:1026"
        self.IOTA_URL = "http://137.226.248.250:4041"
        self.FIWARE_HEADER = FiwareHeader(service="iotplatform", service_path="/")
        self.s = Session()
        self.cbc = ContextBrokerClient(url=self.CB_URL, fiware_header=self.FIWARE_HEADER, session=self.s)

        self.book = market_book.MarketBook()

        self.step_length = config.get_from_params("time_for_step")
        self.auction_time = config.get_from_params("auction_time")

    def collect_bids(self):
        bid_entities = self.cbc.get_entity_list(type_pattern="Bid")
        bids = [Bid(entity=bid_entity) for bid_entity in bid_entities]
        return bids

    def post_transaction_info(self):
        for participant in self.book.transaction_info:
            transaction_info = self.book.transaction_info[participant]
            try:
                self.cbc.update_attribute_value(entity_id=f"Transaction:{transaction_info.id}",
                                                attr_name="TransactionBuying",
                                                value=transaction_info.buying)
                self.cbc.update_attribute_value(entity_id=f"Transaction:{transaction_info.id}",
                                                attr_name="TransactionPrice",
                                                value=transaction_info.cost_revenue_res)
                self.cbc.update_attribute_value(entity_id=f"Transaction:{transaction_info.id}",
                                                attr_name="TransactionQuantity",
                                                value=transaction_info.quantity_res)
            except requests.exceptions.HTTPError:
                post_entity_transaction(building=transaction_info.id, cbc=self.cbc)
                self.cbc.update_attribute_value(entity_id=f"Transaction:{transaction_info.id}",
                                                attr_name="TransactionBuying",
                                                value=transaction_info.buying)
                self.cbc.update_attribute_value(entity_id=f"Transaction:{transaction_info.id}",
                                                attr_name="TransactionPrice",
                                                value=transaction_info.cost_revenue_res)
                self.cbc.update_attribute_value(entity_id=f"Transaction:{transaction_info.id}",
                                                attr_name="TransactionQuantity",
                                                value=transaction_info.quantity_res)

    def post_auction_iteration(self, auc_iter: dict):
        for building in auc_iter:
            try:
                self.cbc.update_attribute_value(entity_id=f"Auction_Iteration:{building}",
                                                attr_name="AuctionIterationStep",
                                                value=auc_iter[building]["step"])
                self.cbc.update_attribute_value(entity_id=f"Auction_Iteration:{building}",
                                                attr_name="AuctionIterationPrice",
                                                value=auc_iter[building]["price"])
                self.cbc.update_attribute_value(entity_id=f"Auction_Iteration:{building}",
                                                attr_name="AuctionIterationQuantity",
                                                value=auc_iter[building]["quant"])
            except requests.exceptions.HTTPError:
                post_entity_auction_iteration(building=building, cbc=self.cbc)
                self.cbc.update_attribute_value(entity_id=f"Auction_Iteration:{building}",
                                                attr_name="AuctionIterationStep",
                                                value=auc_iter[building]["step"])
                self.cbc.update_attribute_value(entity_id=f"Auction_Iteration:{building}",
                                                attr_name="AuctionIterationPrice",
                                                value=auc_iter[building]["price"])
                self.cbc.update_attribute_value(entity_id=f"Auction_Iteration:{building}",
                                                attr_name="AuctionIterationQuantity",
                                                value=auc_iter[building]["quant"])

    def post_public_info(self, info: dict):
        try:
            self.cbc.update_attribute_value(entity_id="Public_Info", attr_name="EquilibriumPrice",
                                            value=info["equi_price"])
            self.cbc.update_attribute_value(entity_id="Public_Info", attr_name="EquilibriumQuantity",
                                            value=info["equi_quant"])
        except requests.exceptions.HTTPError:
            post_entity_public_info(cbc=self.cbc)
            self.cbc.update_attribute_value(entity_id="Public_Info", attr_name="EquilibriumPrice",
                                            value=info["equi_price"])
            self.cbc.update_attribute_value(entity_id="Public_Info", attr_name="EquilibriumQuantity",
                                            value=info["equi_quant"])

    def whole_single_auction(self):
        print("Running auction")
        bids = self.collect_bids()
        self.book.add_bids(bids=bids)
        self.book.separate_bids()
        self.book.sort_bids()
        transactions = single_round_auction.run_auction(selling_bids=self.book.selling_bids,
                                                        buying_bids=self.book.buying_bids)
        self.book.add_transactions(transactions)
        self.book.aggregate_transaction_info()
        self.post_transaction_info()
        self.book.clear_book()
        print("Ran auction")

    def whole_iter_auction(self):
        print("Running auction")
        bids = self.collect_bids()
        auction_iter = iterating_auction.run_auction(bids)
        self.post_auction_iteration(auc_iter=auction_iter)
        print("Ran auction")

    def coordinator_loop(self, duration: int = 180):
        stop_time = datetime.datetime.now() + datetime.timedelta(seconds=duration)
        while datetime.datetime.now() < stop_time:
            seconds = int(datetime.datetime.now().strftime("%S"))
            if (seconds - self.auction_time) % self.step_length == 0:
                self.whole_single_auction()
                time.sleep(1)
            time.sleep(0.1)


if __name__ == "__main__":
    c = Coordinator()
    c.whole_single_auction()
