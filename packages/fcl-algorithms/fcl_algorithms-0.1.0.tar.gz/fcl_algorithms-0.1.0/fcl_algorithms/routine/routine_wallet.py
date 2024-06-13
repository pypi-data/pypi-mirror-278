# This script will take in a specific date range and a desired "memory".
# It will produce individual files for each day with the wallets with that memory.
# Wallets are composed of all addresses that have been senders for that "memory" time frame.


# 1) Create an initial dictionary for wallets and inactivity
# 2) Add today's addresses to both (updating inactivity)
# 3) Run union algorithm on todays transactions to update wallets
# 4) Increase by one the inactivity values
# 5) For each address in wallets dictionary: If key isn't in 31 but parent is, make self parent.
# 6) Check that there are no parents in the 31 for non31s.
# 7) Eliminate all 31s from wallets and inactive dictionaries.


######## PRELIMINARY STUFF
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import sys
import json

# Set the maximum recursion limit
#print(sys.getrecursionlimit())
sys.setrecursionlimit(50000)

# A class to represent a disjoint set
class DisjointSet:
    parent = {}

    # stores the depth of trees
    rank = {}

    # perform MakeSet operation
    def makeSet(self, universe, parents=""):
        # create `n` disjoint sets (one for each item)
        if parents == "":
            for i in universe:
                self.parent[i] = i
                self.rank[i] = 0
        else:
            for i, j in zip(universe, parents):
                self.parent[i] = j
                self.rank[i] = 0

    # Find the root of the set in which element `k` belongs
    def Find(self, k):
        # if `k` is not the root
        if self.parent[k] != k:
            # path compression
            self.parent[k] = self.Find(self.parent[k])
        return self.parent[k]

    # Perform Union of two subsets
    def Union(self, a, b):
        # find the root of the sets in which elements `x` and `y` belongs
        x = self.Find(a)
        y = self.Find(b)

        # if `x` and `y` are present in the same set
        if x == y:
            return

        # Always attach a smaller depth tree under the root of the deeper tree.
        if self.rank[x] > self.rank[y]:
            self.parent[y] = x
        elif self.rank[x] < self.rank[y]:
            self.parent[x] = y
        else:
            self.parent[x] = y
            self.rank[y] = self.rank[y] + 1

def printSets(universe, ds):
    print([ds.Find(i) for i in universe])

def updateSets(universe, ds):
    new_universe = [ds.Find(i) for i in universe]
    return new_universe

# Decide what location we want to use
file_location = "../fcl_data/"
#file_location = "/Volumes/DingosDiner/fcl_data/"
# =======================================
# 0) Decide the desired dates and memory

target_day = sys.argv[1]
current_day = datetime.strptime(target_day, '%d_%m_%Y')
date_curr = current_day.strftime('%d_%m_%Y')
initial_date = date_curr
last_date = date_curr
start_day = datetime.strptime(initial_date, '%d_%m_%Y')     # This is the FIRST day we need data for.
lim_day = datetime.strptime(last_date, '%d_%m_%Y')      # This is the LAST day we need data for.

# Uncomment to hard-set the dates
#start_day = datetime.strptime('21_05_2021', '%d_%m_%Y')     # This is the FIRST day we need data for.
#lim_day = datetime.strptime('01_01_2022', '%d_%m_%Y')       # This is the LAST day we need data for.

lim_day = lim_day + timedelta(days=1)
memory = 2                                                  # This is the amount of days we want to remember.
# =======================================


current_day = start_day - timedelta(days=memory)
old_dict = {}
inactive_dict = {}
while current_day < lim_day:
    stat_old = len(old_dict)
    # 1) Load the day's transactions
    date_curr = current_day.strftime('%d_%m_%Y')
    print("1) Starting work on " + date_curr)
    rawday_path = file_location + "btc_txs/btc_tx_" + date_curr + ".csv"
    day_frame = pd.read_csv(rawday_path)
    day_frame.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']
    # 2) Get the addresses and add to the dictionaries.
    # Generate a list of addresses
    print("2) Loaded the data")
    nodes_in = day_frame["txSender"].values.tolist()
    nodes_in = [str(item) for item in nodes_in]
    nodes_out = day_frame["txReceiver"].values.tolist()
    nodes_out = [str(item) for item in nodes_out]
    nodes_all = nodes_in + nodes_out
    nodes_today = np.unique(nodes_all)
    # Populate the dictionaries
    for address in nodes_today:
        inactive_dict[address] = 0
        if address not in old_dict:
            old_dict[address] = address

    # 3) Create new disjointed set
    print("3) Creating the disjointed set")
    ds_set = list(old_dict.keys())
    ds_par = list(old_dict.values())
    ds = DisjointSet()
    ds.makeSet(ds_set, ds_par)

    # 4) Update disjointed set using the union-find algorithm
    print("4) Running the Union-Find")
    union_list = day_frame[["txHash", "txSender"]].values.tolist()
    total = len(union_list)
    # Run the union-find algorithm on all the items of union_list.
    hashBefore = '0'
    senderBefore = ''
    iter = 0
    for row in union_list:
        iter += 1
        progress = round((iter / total) * 100, 4)
        hashNew = row[0]
        senderNew = row[1]
        if hashBefore == hashNew:
            if senderBefore != senderNew:
                ds.Union(senderBefore, senderNew)
        else:
            hashBefore = hashNew
            senderBefore = senderNew

    # 5) Update days inactive dictionary.
    print("5) Updating inactivity")
    for address in ds_set:
        inactive_dict[address] = inactive_dict[address] + 1

    # 6) Get rid of old parents.
    print("6) Dealing with inactive addresses")
    for address in ds_set:
        parent = ds.Find(address)
        if ((inactive_dict[address] != (memory + 1)) and (inactive_dict[parent] == (memory + 1))):
            ds.parent[address] = address
            ds.parent[parent] = address

    stat_eli = 0
    for address in ds_set:
        if inactive_dict[address] >= (memory + 1):
            inactive_dict.pop(address)
            stat_eli += 1

    # 7) Generate a new disjointed set using the finalised version.
    print("7) Generating a new wallet mapping")
    new_keys = list(inactive_dict.keys())
    newSet = updateSets(new_keys, ds)
    # Update the dictionary with the addresses and their parents:
    old_dict = {}
    for address, wallet in zip(new_keys, newSet):
        old_dict[address] = wallet



    # 8) Create a daily dictionary which is updated and store.
    if current_day >= start_day:
        print("8) Storing mapping for " + date_curr)
        wallet_dict = {key: old_dict[key] for key in nodes_today}
        new_path = file_location + "fcl_txs/wallets_" + date_curr + ".json"
        json.dump(wallet_dict, open(new_path, 'w'))

    # 9) Update the day we are looking at.
    print("9) Review stats for " + date_curr)
    print("Number today: " + str(len(nodes_today)))
    print("Number start: " + str(stat_old))
    print("Number eliminated: " + str(stat_eli))
    print("Number end: " + str(len(new_keys)))
    current_day = current_day + timedelta(days=1)