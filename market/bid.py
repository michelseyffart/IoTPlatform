from filip.clients.ngsi_v2.cb import ContextEntity


class Bid:

    def __init__(self, entity: ContextEntity):
        self.id = int(entity.id.strip("Bid:"))
        self.buying = entity.get_attribute("BidBuying").value
        self.price = entity.get_attribute("BidPrice").value
        self.quantity = entity.get_attribute("BidQuantity").value
