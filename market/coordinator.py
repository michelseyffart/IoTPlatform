import time
from market.auctions import single_round_auction, iterating_auction
import datetime
import market.market_book as market_book
from market.bid import Bid
import openhab.config.config as config
from fiware.fiware_interface import FiwareInterface
import logs.create_logger as logs
import logging
from market.transaction import TransactionInfo
from market.public_info import PublicInfo


class Coordinator:

    def __init__(self):

        self.log = logs.get_logger(filename="run.log", name="coordinator", consolelevel=logging.INFO)

        self.fiware = FiwareInterface()
        self.book = market_book.MarketBook()

        self.step_length = config.get_from_params("time_for_step")
        self.auction_time = config.get_from_params("auction_time")
        self.bid_expiration_time = config.get_from_params("bid_expiration_time")

        self.log.info("Created coordinator")

    def collect_bids(self):
        bid_entities = self.fiware.get_bid_entities()
        bids = [Bid(entity=bid_entity) for bid_entity in bid_entities]
        return bids

    def publish_transaction_info(self):
        for participant in self.book.transaction_info:
            transaction_info = self.book.transaction_info[participant]
            self.fiware.update_transaction(transaction_info=transaction_info)

    def reset_all_recorded_bids(self):
        for bid in self.book.all_bids:
            self.fiware.reset_bid(bid=bid)

    def post_auction_iteration(self):
        for auction_iteration in self.book.auction_iterations:
            self.fiware.update_auction_iteration(auction_iteration=auction_iteration)

    def post_public_info(self):
        self.fiware.update_public_info(self.book.public_info)

    def reset_and_delete_expired_bids(self):
        expiration_time = datetime.datetime.now() - datetime.timedelta(seconds=self.bid_expiration_time)
        expired_bids = [bid for bid in self.book.all_bids if bid.datetime <= expiration_time]
        for bid in expired_bids:
            self.fiware.reset_bid(bid=bid)
            self.book.delete_bid(bid=bid)

    def update_bids(self):
        for bid in self.book.all_bids:
            if bid.part_of_transaction:
                self.fiware.update_bid_quantity(bid=bid)

    def whole_single_auction(self):
        self.log.info("Running discrete auction")
        bids = self.collect_bids()
        self.book.add_bids(bids=bids)
        self.book.separate_bids()
        self.book.sort_bids()
        transactions = single_round_auction.run_auction(selling_bids=self.book.selling_bids,
                                                        buying_bids=self.book.buying_bids)
        self.book.add_transactions(transactions)
        self.book.aggregate_transaction_info()
        self.publish_transaction_info()
        self.reset_all_recorded_bids()
        self.book.clear_book()
        self.log.info("Auction complete")

    def whole_continuous_auction(self):
        self.log.info("Running continuous auction")
        bids = self.collect_bids()
        self.book.add_bids(bids=bids)
        self.reset_and_delete_expired_bids()
        self.book.separate_bids()
        self.book.sort_bids()
        transactions = single_round_auction.run_auction(selling_bids=self.book.selling_bids,
                                                        buying_bids=self.book.buying_bids)
        self.book.add_transactions(transactions)
        self.book.aggregate_transaction_info()
        self.update_bids()
        self.publish_transaction_info()
        self.book.clear_book()
        self.log.info("Auction complete")

    def whole_iter_auction(self):
        self.log.info("Running iterating auction")
        auction_iteration = 0
        iteration_limit = 3
        while auction_iteration < iteration_limit:
            bids = self.collect_bids()
            self.book.add_bids(bids=bids)
            self.book.separate_bids()
            self.book.sort_bids()
            public_info = iterating_auction.calculate_equilibrium(buying_bids=self.book.buying_bids,
                                                                  selling_bids=self.book.selling_bids)
            self.book.update_public_info(public_info=public_info)
            self.post_public_info()
            self.book.clear_book()
            auction_iteration += 1
            time.sleep(2)
        self.whole_single_auction()
        self.log.info("Auction complete")

    def dummy_auction(self):

        public_info = PublicInfo(equilibrium_price=0.3, equilibrium_quantity=3000)
        for i in range(5):
            self.fiware.update_public_info(public_info=public_info)
            time.sleep(3)
        for i in range(3):
            transaction_info = TransactionInfo(id_="0")
            transaction_info.cost_revenue_res = 300
            transaction_info.quantity_res = 1000
            transaction_info.buying = True
            self.fiware.update_transaction(transaction_info=transaction_info)
            time.sleep(10)

    def coordinator_loop(self, start_time: datetime.datetime, clearing_mechanism: str, duration: int = 180):
        self.log.info("Starting coordinator")
        stop_time = start_time + datetime.timedelta(seconds=duration)
        auction_time = start_time + datetime.timedelta(seconds=self.auction_time)
        if clearing_mechanism in ["discrete", "d"]:
            while datetime.datetime.now() < stop_time:
                if datetime.datetime.now() >= auction_time:
                    auction_time = auction_time.replace(microsecond=0) + datetime.timedelta(seconds=self.step_length)
                    self.whole_single_auction()
                    time.sleep(2)
                time.sleep(0.1)
        elif clearing_mechanism in ["f"]:
            while datetime.datetime.now() < stop_time:
                if datetime.datetime.now() >= auction_time:
                    auction_time = auction_time.replace(microsecond=0) + datetime.timedelta(
                        seconds=self.step_length)
                    self.dummy_auction()
                    time.sleep(2)
                time.sleep(0.1)
        elif clearing_mechanism in ["continuous", "c"]:
            while datetime.datetime.now() < stop_time:
                self.whole_continuous_auction()
        elif clearing_mechanism in ["iterative", "iterating", "i"]:
            while datetime.datetime.now() < stop_time:
                if datetime.datetime.now() >= auction_time:
                    auction_time = auction_time.replace(microsecond=0) + datetime.timedelta(seconds=self.step_length)
                    self.whole_iter_auction()
                    time.sleep(1)
                time.sleep(0.1)


if __name__ == "__main__":
    c = Coordinator()
    c.dummy_auction()
