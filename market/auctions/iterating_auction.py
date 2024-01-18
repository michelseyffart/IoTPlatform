from market.transaction import Transaction
from market.public_info import PublicInfo
import numpy as np
import pandas as pd


def calculate_equilibrium(buying_bids: list, selling_bids: list):
    df_buy_bids, df_sell_bids = create_bids_dataframe(buying_bids, selling_bids)
    equilibrium_quantity, equilibrium_price = uniform_pricing(df_buy_bids, df_sell_bids)
    return PublicInfo(equilibrium_price=equilibrium_price, equilibrium_quantity=equilibrium_quantity)


def create_bids_dataframe(buying_bids: list, selling_bids: list):
    col_names = ["price", "quantity"]
    buying_bids_list = [(bid.price, bid.quantity) for bid in buying_bids]
    selling_bids_list = [(bid.price, bid.quantity) for bid in selling_bids]
    df_buy_bids = pd.DataFrame(buying_bids_list, columns=col_names)
    df_sell_bids = pd.DataFrame(selling_bids_list, columns=col_names)
    return df_buy_bids, df_sell_bids


def uniform_pricing(df_buy_bids, df_sell_bids):

    # Creates demand and supply curves from bids
    demand_curve, index_buying, supply_curve, index_selling = stepwise_function(df_buy_bids, df_sell_bids)

    # TODO: plt der Treppenfunktionen zur Kontrolle

    # q_ is the quantity at which supply and demand meet
    # price is the price at which that happens
    # b_ is the index of the buyer in that position
    # s_ is the index of the seller in that position
    q_, b_, s_, price = intersect_stepwise(demand_curve, supply_curve, 0.5)
    if s_ is None or b_ is None:
        q_ = 0
        price = 0.3
    return q_, price
'''
    # Sort bids df in ascending order for selling bids and descending order for buying bids
    buying_bids = df_buy_bids.sort_values('price', ascending=False)
    selling_bids = df_sell_bids.sort_values('price', ascending=True)

    # check if bids are there
    if b_ == None or s_ == None:
        extra = {'clearing quantity': "no trading",
                 'clearing price': "no trading"}
        transactions = {}
    else:
        # Filter bids to be traded
        buying_bids = buying_bids.iloc[: b_ + 1, :]
        selling_bids = selling_bids.iloc[: s_ + 1, :]

        # Find the long side of the market
        buying_quantity = buying_bids.quantity.sum()
        selling_quantity = selling_bids.quantity.sum()

        if buying_quantity > selling_quantity:
            long_side = buying_bids
            short_side = selling_bids
        else:
            long_side = selling_bids
            short_side = buying_bids

        traded_quantity = short_side.quantity.sum()

        col_names_trans = ['user_id', 'quantity', 'price', 'side']
        transactions = pd.DataFrame(columns=col_names_trans)

        ## All the short side will trade at `price`
        ## The -1 is there because there is no clear 1 to 1 trade.
        # TODO: ist i die user_id? --> Nein, Index des bids aus bid_list --> Lsg.: df["user_id"][i].value ?!
        for i, x in short_side.iterrows():
            transactions = add_transaction(transactions, short_side["user_id"][i], x.quantity, price,
                                           buying_quantity, selling_quantity, "short_side")

        ## The long side has to trade only up to the short side
        quantity_added = 0
        for i, x in long_side.iterrows():

            if x.quantity + quantity_added <= traded_quantity:
                x_quantity = x.quantity
            else:
                x_quantity = traded_quantity - quantity_added
            transactions = add_transaction(transactions, long_side["user_id"][i], x_quantity, price,
                                           buying_quantity, selling_quantity, "long_side")
            quantity_added += x.quantity

        extra = {
            'clearing quantity': q_,
            'clearing price': price
        }

    return extra, transactions
'''


def stepwise_function(df_buy_bids, df_sell_bids):
    """
    Creates a stepwise constant demand curve from a set of  bids.

    Parameters
    ----------
    bids: list of bids in the market.

    Returns
    ---------
    demand_curve: np.ndarray

    index : np.ndarray
        The order of the identifier of each bid in the demand curve.
    """

    # sort buying bids in descending order
    buying = df_buy_bids.sort_values('price', ascending=False)
    buying['acum'] = buying.quantity.cumsum()
    demand_curve = buying[['acum', 'price']].values
    demand_curve = np.vstack([demand_curve, [np.inf, 0]])
    index_buying = buying.index.values.astype('int64')

    # sort selling bids in ascending order
    selling = df_sell_bids.sort_values('price')
    selling['acum'] = selling.quantity.cumsum()
    supply_curve = selling[['acum', 'price']].values
    supply_curve = np.vstack([supply_curve, [np.inf, np.inf]])
    index_selling = selling.index.values.astype('int64')

    return demand_curve, index_buying, supply_curve, index_selling


def intersect_stepwise(f, g, k=0.5):
    """
    Finds the intersection of two stepwise constants functions
    where f is assumed to be bigger at 0 than g.
    If no intersection is found, None is returned.

    Parameters
    ----------
    f: np.ndarray
        Stepwise constant function

    g: np.ndarray
        Stepwise constant function
    k : float
        If the intersection is empty or an interval,
        a convex combination of the y-values of f and g
        will be returned and k will be used to determine
        hte final value. `k=1` will be the value of g
        while `k=0` will be the value of f.

    Returns
    --------
    x_ast : float or None (if intersection is empty)
        Axis coordinate of the intersection of both functions.
    f_ast : int or None (if intersection is empty)
        Index of the rightmost extreme
        of the interval of `f` involved in the
        intersection.
    g_ast : int or None (if intersection is empty)
        Index of the rightmost extreme
        of the interval of `g` involved in the
        intersection.
    v : float or None (if intersection is empty)
        Ordinate of the intersection or the k-convex combination of the
        y values of `f` and `g` in the last point

    """
    x_max = np.min([f.max(axis=0)[0], g.max(axis=0)[0]])
    xs = sorted([x for x in set(g[:, 0]).union(set(f[:, 0])) if x <= x_max])
    fext = [get_value_stepwise(x, f) for x in xs]
    gext = [get_value_stepwise(x, g) for x in xs]
    x_ast = None
    for i in range(len(xs) - 1):
        if (fext[i] >= gext[i]) and (fext[i + 1] < gext[i + 1]):  # Joel: >= ?!
            x_ast = xs[i]

    f_ast = np.argmax(f[:, 0] >= x_ast) if x_ast is not None else None
    g_ast = np.argmax(g[:, 0] >= x_ast) if x_ast is not None else None

    g_val = g[g_ast, 1] if g_ast is not None else get_value_stepwise(xs[-1], g)
    f_val = f[f_ast, 1] if f_ast is not None else get_value_stepwise(xs[-1], f)

    intersect_domain_both = x_ast in f[:, 0] and x_ast in g[:, 0]
    if not (intersect_domain_both) and (x_ast is not None):
        v = g_val if x_ast in f[:, 0] else f_val
    else:
        v = g_val * k + (1 - k) * f_val

    return x_ast, f_ast, g_ast, v


def get_value_stepwise(x, f):
    """
    Returns the value of a stepwise constant function defined by the right extrems
    of its interval Functions are assumed to be defined in (0, inf).

    Parameters
    ----------
    x: float
        Value in which the function is to be evaluated
    f: np.ndarray
        Stepwise function
    Returns
    --------
    float or None
        The image of x under f: `f(x)`.

    """
    if x < 0:
        return None

    for step in f:
        if x <= step[0]:
            return step[1]