from filip.clients.ngsi_v2.cb import ContextBrokerClient, FiwareHeader
from market.transaction import TransactionInfo
from market.bid import Bid
from market.auction_iteration import AuctionIteration
from market.public_info import PublicInfo
import fiware.setup as setup
from requests import Session
from requests.exceptions import ReadTimeout, HTTPError, ConnectionError
import logs.create_logger as logs
import logging
import fiware.config.config as fiware_config


class FiwareInterface:

    def __init__(self):
        url_fiware = fiware_config.get_from_config("url_fiware")
        self.CB_URL = f"http://{url_fiware}:1026"
        self.IOTA_URL = f"http://{url_fiware}:4041"
        self.FIWARE_HEADER = FiwareHeader(service="iotplatform", service_path="/")
        self.s = Session()
        self.cbc = ContextBrokerClient(url=self.CB_URL, fiware_header=self.FIWARE_HEADER, session=self.s)
        self.log = logs.get_logger(filename="fiware_interface.log", name="fiware interface", consolelevel=logging.INFO)

    def get_bid_entities(self):
        try:
            return self.cbc.get_entity_list(type_pattern="Bid")
        except ReadTimeout as e:
            self.log.error(f"Could not get bid entities. {e}")
            return list()
        except ConnectionError as e:
            self.log.error(f"Could not get bid entities. {e}")
            return list()

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
        except HTTPError as e:
            if not failed_previously:
                setup.post_entity_transaction(cbc=self.cbc, building=transaction_info.id)
                self.update_transaction(transaction_info=transaction_info, failed_previously=True)
            else:
                self.log.error(f"Could not post transaction. {e}")
        except ConnectionError as e:
            self.log.error(f"Could not post transaction. {e}")

    def reset_bid(self, bid: Bid):
        try:
            self.cbc.update_attribute_value(entity_id=f"Bid:{bid.id}",
                                            attr_name="BidPrice",
                                            value=0)
            self.cbc.update_attribute_value(entity_id=f"Bid:{bid.id}",
                                            attr_name="BidQuantity",
                                            value=0)
        except ConnectionError as e:
            self.log.error(f"Could not reset bid {bid.id}. {e}")

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
        except HTTPError as e:
            if not failed_previously:
                setup.post_entity_auction_iteration(building=auction_iteration.id, cbc=self.cbc)
                self.update_auction_iteration(auction_iteration=auction_iteration, failed_previously=True)
            else:
                self.log.error(f"Could not post auction iteration. {e}")
        except ConnectionError as e:
            self.log.error(f"Could not post auction iteration. {e}")

    def update_public_info(self, public_info: PublicInfo, failed_previously: bool = False):
        try:
            self.cbc.update_attribute_value(entity_id="Public_Info",
                                            attr_name="EquilibriumPrice",
                                            value=public_info.equilibrium_price)
            self.cbc.update_attribute_value(entity_id="Public_Info",
                                            attr_name="EquilibriumQuantity",
                                            value=public_info.equilibrium_quantity)
        except HTTPError as e:
            if not failed_previously:
                setup.post_entity_public_info(cbc=self.cbc)
                self.update_public_info(public_info=public_info, failed_previously=True)
            else:
                self.log.error(f"Could not post public info. {e}")
        except ConnectionError as e:
            self.log.error(f"Could not post public info. {e}")

    def update_bid_quantity(self, bid: Bid):
        try:
            self.cbc.update_attribute_value(entity_id=f"Bid:{bid.id}",
                                            attr_name="BidQuantity",
                                            value=bid.quantity)
        except ConnectionError as e:
            self.log.error(f"Could not update bid quantity {bid.id}. {e}")
