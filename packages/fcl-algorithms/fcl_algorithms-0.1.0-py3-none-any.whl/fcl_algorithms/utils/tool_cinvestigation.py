# This script will go through the communities for a given day and try to assign a type.

import networkx as nx
import json
from datetime import datetime, timedelta
import pandas as pd
import glob
import numpy as np

class Community:
    def __init__(self, id, c_type, members):
        self.id = id
        self.type = c_type
        self.members = members

class Merge:
    def __init__(self, old, new):
        self.old = old
        self.new = new

# ===================================
# 1) SET THE DATE TO GET
# ===================================

#current_day = datetime.today() - timedelta(days=1)
current_day = datetime.strptime('31_12_2021', '%d_%m_%Y') # FOR TESTING
current_day =  datetime.today() - timedelta(days=1)
yester_day = current_day - timedelta(days=1)
curr_day_mill = current_day.timestamp() * 1000
curr_day_mill = str(curr_day_mill).split('.')[0]
date_curr = current_day.strftime('%d_%m_%Y')

yest_day_mill = yester_day.timestamp() * 1000
yest_day_mill = str(yest_day_mill).split('.')[0]
yesterday = yester_day.strftime('%d_%m_%Y')

# ===================================
# 2) LOAD ALL THE COMMUNITIES
# ===================================

comm_path = "../fcl_data/comm_" + date_curr + ".txt"
with open(comm_path) as json_file:
    communities = json.load(json_file)

comm_path = "../fcl_data/comm_" + yesterday + ".txt"
with open(comm_path) as json_file:
    yesterday_comms = json.load(json_file)



# ===================================
# 3) LOAD THE LISTS OF KNOWN TYPES
# ===================================

# POPULATE KNOWN ADDRESSES LISTS
# A) MINERS
db_known_a = pd.concat([pd.read_csv(f, header=None) for f in glob.glob("/Users/diegolara/PycharmProjects/btc-wallet-tag/mn_*.csv")], ignore_index=True)
db_known_a = set(db_known_a[0])
# B) EXCHANGES
db_known_b = pd.concat([pd.read_csv(f, header=None) for f in glob.glob("/Users/diegolara/PycharmProjects/btc-wallet-tag/ex_*.csv")], ignore_index=True)
db_known_b = set(db_known_b[0])
# C) BLACK MARKETS
db_known_c = pd.concat([pd.read_csv(f, header=None) for f in glob.glob("/Users/diegolara/PycharmProjects/btc-wallet-tag/bm_*.csv")], ignore_index=True)
db_known_c = set(db_known_c[0])
# D) ORIGIN
db_known_d = {'000000000000000000000000'}


transitions = np.zeros((len(communities), len(yesterday_comms)))
i = 0
for cluster in communities:
    i += 1
    j = 0
    commune = cluster["members"]
    # ===================================
    # 3) TRY TO MATCH TO PAST CLUSTER
    # ===================================
    for yest_com in yesterday_comms:
        j += 1
        yest_commune = yest_com["members"]
        overlap_y = set.intersection(set(commune), set(yest_commune))
        overnum_y = len(overlap_y)

        # insert the number of node overlap in matrix
        transitions[(i-1), (j-1)] = overnum_y

    # ===================================
    # 4) TRY TO ASSIGN TYPES USING KNOWN
    # ===================================
    # FIND PARTICIPATION BY TYPES:
    # A) MINERS
    overlap_a = set.intersection(set(commune), db_known_a)
    overnum_a = len(overlap_a)
    # B) EXCHANGES
    overlap_b = set.intersection(set(commune), db_known_b)
    overnum_b = len(overlap_b)
    # C) BLACK MARKETS
    overlap_c = set.intersection(set(commune), db_known_c)
    overnum_c = len(overlap_c)
    # D) ORIGIN
    overlap_d = set.intersection(set(commune), db_known_d)
    overnum_d = len(overlap_d)

    # MAX TYPE ALLOCATION:
    overlap = [overnum_a, overnum_b, overnum_c, overnum_d]
    max_value = max(overlap)
    if max_value != 0:
        com_type = overlap.index(max_value) + 1
    else:
        com_type = 0
    cluster["type"] = com_type

# ===================================
# 5) STORE UPDATED COMMUNITY DATA
# ===================================

comm_path = "../fcl_data/comm_" + date_curr + ".txt"
with open(comm_path, "w") as write_file:
    json.dump(communities, write_file, indent=1)

merges_Path = "../fcl_data/comm_merges_" + date_curr + ".csv"
np.savetxt(merges_Path, transitions, delimiter=",")