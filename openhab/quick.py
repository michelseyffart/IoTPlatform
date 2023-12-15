import pickle

my0 = 319470.82658848213
my1 = 39969.470000000016
my2 = 384852.9158444202
my3 = 326808.3904623354

old1 = 313808.9248473435

with open("scenario3.p", "rb") as f:
    data = pickle.load(f)
demand = [0, 0, 0, 0]
for n in range(4):
    for n_opt in range(102):
        demand[n] += data[n_opt][4][n][n_opt]
print(demand)
