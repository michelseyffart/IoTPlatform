from market.transaction import TransactionInfo
from market.public_info import PublicInfo
from market.bid import Bid
import data_collection.collector as collector


class MarketBook:

    def __init__(self):
        self.all_bids = list()
        self.buying_bids = list()
        self.selling_bids = list()
        self.transactions = list()
        self.transaction_info = dict()
        self.auction_iterations = list()
        self.public_info = PublicInfo()
        self.data_collector = collector.PythonCollector()

    def add_bids(self, bids: list):
        for bid in bids:
            if bid.quantity > 0:
                self.all_bids.append(bid)

    def delete_bid(self, bid: Bid):
        try:
            self.all_bids.remove(bid)
        except ValueError:
            print("Bid not found")

    def separate_bids(self):
        for bid in self.all_bids:
            if bid.buying and bid.quantity > 0:
                self.buying_bids.append(bid)
            elif not bid.buying and bid.quantity > 0:
                self.selling_bids.append(bid)

    def sort_bids(self):
        self.buying_bids = sorted(self.buying_bids, key=lambda x: x.price, reverse=True)
        self.selling_bids = sorted(self.selling_bids, key=lambda x: x.price)

    def add_transactions(self, transactions: list):
        for transaction in transactions:
            self.transactions.append(transaction)
            next(bid.set_part_of_transaction_true() for bid in self.buying_bids if bid.id == transaction.buyer)
            next(bid.set_part_of_transaction_true() for bid in self.selling_bids if bid.id == transaction.seller)
        self.data_collector.save_data(data=transactions)

    def aggregate_transaction_info(self):
        participants = set()
        for transaction in self.transactions:
            participants.add(transaction.buyer)
            participants.add(transaction.seller)
        for participant in participants:
            self.transaction_info[participant] = TransactionInfo(id_=participant)
        for transaction in self.transactions:
            cost_or_revenue = transaction.price * transaction.quantity
            self.transaction_info[transaction.buyer].cost += cost_or_revenue
            self.transaction_info[transaction.buyer].quantity_bought += transaction.quantity
            self.transaction_info[transaction.seller].cost += cost_or_revenue
            self.transaction_info[transaction.seller].quantity_sold += transaction.quantity
        for participant in self.transaction_info:
            transaction_info = self.transaction_info[participant]
            transaction_info.cost_revenue_res = abs(transaction_info.cost - transaction_info.revenue)
            quantity = transaction_info.quantity_sold - transaction_info.quantity_bought
            transaction_info.quantity_res = abs(quantity)
            transaction_info.buying = quantity < 0

    def clear_book(self):
        self.all_bids.clear()
        self.buying_bids.clear()
        self.selling_bids.clear()
        self.transactions.clear()
        self.transaction_info.clear()
