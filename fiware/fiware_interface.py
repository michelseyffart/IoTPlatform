from filip.clients.ngsi_v2.cb import ContextBrokerClient, FiwareHeader, ContextEntity
from market.transaction import Transaction, TransactionInfo
from market.bid import Bid
from market.auction_iteration import AuctionIteration
from market.public_info import PublicInfo
import fiware.setup as setup
from requests import Session
import requests.exceptions
import openhab.create_logger as logs
import logging


class FiwareInterface:

    def __init__(self):
        self.CB_URL = "http://137.226.248.250:1026"
        self.IOTA_URL = "http://137.226.248.250:4041"
        self.FIWARE_HEADER = FiwareHeader(service="iotplatform", service_path="/")
        self.s = Session()
        self.cbc = ContextBrokerClient(url=self.CB_URL, fiware_header=self.FIWARE_HEADER, session=self.s)
        self.log = logs.get_logger(filename="fiware_interface.log", name="fiware interface", consolelevel=logging.INFO)

    def get_bid_entities(self):
        return self.cbc.get_entity_list(type_pattern="Bid")

    def update_transaction(self, transaction_info: TransactionInfo, failed_previously: bool = False):
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
        except requests.exceptions.HTTPError as e:
            if not failed_previously:
                setup.post_entity_transaction(cbc=self.cbc, building=transaction_info.id)
                self.update_transaction(transaction_info=transaction_info, failed_previously=True)
            else:
                self.log.error(f"Could not post transaction. {e}")

    def reset_bid(self, bid: Bid):
        self.cbc.update_attribute_value(entity_id=f"Bid:{bid.id}",
                                        attr_name="BidPrice",
                                        value=0)
        self.cbc.update_attribute_value(entity_id=f"Bid:{bid.id}",
                                        attr_name="BidQuantity",
                                        value=0)

    def update_auction_iteration(self, auction_iteration: AuctionIteration, failed_previously: bool = False):
        try:
            self.cbc.update_attribute_value(entity_id=f"Auction_Iteration:{auction_iteration.id}",
                                            attr_name="AuctionIterationStep",
                                            value=auction_iteration.step)
            self.cbc.update_attribute_value(entity_id=f"Auction_Iteration:{auction_iteration.id}",
                                            attr_name="AuctionIterationPrice",
                                            value=auction_iteration.price)
            self.cbc.update_attribute_value(entity_id=f"Auction_Iteration:{auction_iteration.id}",
                                            attr_name="AuctionIterationQuantity",
                                            value=auction_iteration.quantity)
        except requests.exceptions.HTTPError as e:
            if not failed_previously:
                setup.post_entity_auction_iteration(building=auction_iteration.id, cbc=self.cbc)
                self.update_auction_iteration(auction_iteration=auction_iteration, failed_previously=True)
            else:
                self.log.error(f"Could not post auction iteration. {e}")

    def update_public_info(self, public_info: PublicInfo, failed_previously: bool = False):
        try:
            self.cbc.update_attribute_value(entity_id="Public_Info", attr_name="EquilibriumPrice",
                                            value=public_info.equilibrium_price)
            self.cbc.update_attribute_value(entity_id="Public_Info", attr_name="EquilibriumQuantity",
                                            value=public_info.equilibrium_quantity)
        except requests.exceptions.HTTPError as e:
            if not failed_previously:
                setup.post_entity_public_info(cbc=self.cbc)
                self.update_public_info(public_info=public_info, failed_previously=True)
            else:
                self.log.error(f"Could not post public info. {e}")
