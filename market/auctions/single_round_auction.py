from market.transaction import Transaction


def run_auction(buying_bids: list, selling_bids: list):

    """
    Runs auction with a single trading round.
    This uses an algorithm show in chapter 2 in Chen, 2019 "https://doi.org/10.1016/j.apenergy.2019.03.094".
    It iterates through buying and selling bids until no more matches can be found. This only works properly, if the
    bids are sorted by price.
    """

    transactions = list()

    # k for k-pricing method
    k = 0.5

    if len(selling_bids) != 0 and len(buying_bids) != 0:
        # create indices
        i = 0  # position of seller
        j = 0  # position of buyer
        m = 0  # count of transaction

        # continue matching until no price matches can be found
        while selling_bids[i].price <= buying_bids[j].price:

            # determine transaction price using k-pricing method
            transaction_price = buying_bids[j].price + k * (selling_bids[i].price - buying_bids[j].price)

            # quantity is minimum of both
            transaction_quantity = min(selling_bids[i].quantity, buying_bids[j].quantity)

            # add transaction
            transactions.append(Transaction(
                id_=m,
                seller=selling_bids[i].id,
                buyer=buying_bids[j].id,
                price=transaction_price,
                quantity=transaction_quantity))
            m += 1
            selling_bids[i].quantity = selling_bids[i].quantity - transaction_quantity
            if selling_bids[i].quantity == 0:
                i += 1
            buying_bids[j].quantity = buying_bids[j].quantity - transaction_quantity
            if buying_bids[j].quantity == 0:
                j += 1
            if i == len(selling_bids) or j == len(buying_bids):
                break

    return transactions
