from filip.clients.ngsi_v2.cb import ContextEntity
import datetime


class Bid:

    def __init__(self, entity: ContextEntity):
        self.id = int(entity.id.strip("Bid:"))
        self.buying = entity.get_attribute("BidBuying").value
        self.price = entity.get_attribute("BidPrice").value
        self.quantity = entity.get_attribute("BidQuantity").value
        self.time = int(entity.get_attribute("BidTime").value)
        self.datetime = datetime.datetime.fromtimestamp(self.time / 1000)
        self.part_of_transaction = False

    def set_part_of_transaction_true(self):
        self.part_of_transaction = True
