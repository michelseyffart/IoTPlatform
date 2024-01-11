class Transaction:

    def __init__(self, id_: int, buyer: int, seller: int, quantity: float, price: float):
        self.id = id_
        self.buyer = buyer
        self.seller = seller
        self.quantity = quantity
        self.price = price


class TransactionInfo:

    def __init__(self, id_: int):
        self.id = id_
        self.cost = 0
        self.revenue = 0
        self.cost_revenue_res = 0
        self.quantity_bought = 0
        self.quantity_sold = 0
        self.quantity_res = 0
        self.buying: bool

