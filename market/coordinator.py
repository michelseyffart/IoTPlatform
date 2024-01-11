import time
from market.auctions import single_round_auction, iterating_auction
import datetime
import market.market_book as market_book
from market.bid import Bid
import openhab.config.config as config
from fiware.fiware_interface import FiwareInterface


class Coordinator:

    def __init__(self):

        self.fiware = FiwareInterface()
        self.book = market_book.MarketBook()

        self.step_length = config.get_from_params("time_for_step")
        self.auction_time = config.get_from_params("auction_time")

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
        self.publish_transaction_info()
        self.reset_all_recorded_bids()
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
