# This script will take the communities list and then update their type based on the users result.

from datetime import datetime, timedelta
import networkx as nx
import pandas as pd
import numpy as np
import json
import sys

# Decide what location we want to use
file_location = "../fcl_data/"
#file_location = "/Volumes/DingosDiner/fcl_data/"
# ===================================
# 1) SET THE DATE TO GET AND ITER
# ===================================

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

while current_day < lim_day:
    curr_day_mill = current_day.timestamp() * 1000
    curr_day_mill = str(curr_day_mill).split('.')[0]
    date_curr = current_day.strftime('%d_%m_%Y')
    print(date_curr)

    ########################################
    # 2) Load each day's wallet types.
    ########################################

    # Reading the data from the file
    wallet_path = file_location + "fcl_txs/types_" + date_curr + ".json"
    wallet_dict = json.load(open(wallet_path))

    # ===================================================
    # 3) GET THE COMMUNITIES AND ITERATE THROUGH EACH ONE
    # ===================================================

    comm_path = file_location + "fcl_txs/comm_" + date_curr + ".txt"
    with open(comm_path) as json_file:
        communities = json.load(json_file)

    for cluster in communities:
        id = cluster["id"][11:]
        commune = cluster["members"]
        commune_types = [0] * 7
        commune_type = 0
        for address in commune:
            address_type = wallet_dict[address]
            #Type references
            # 0 -> Unknown
            # 1 -> Miners
            # 2 -> Exchange
            # 3 -> Black Markets
            # 4 -> Origin
            # 5 -> State Backed Illicit
            # 6 -> Scams and Ransomware
            # Assign the community type based on presence of wallets.
            commune_types[address_type] += 1
            if commune_types[5] != 0:
                commune_type = 5
            elif commune_types[6] != 0:
                commune_type = 6
            elif commune_types[3] != 0:
                commune_type = 3
            elif commune_types[4] != 0:
                commune_type = 4
            elif commune_types[1] != 0:
                commune_type = 1
            elif commune_types[2] != 0:
                commune_type = 2
            else:
                commune_type = 0
            # uncomment to change community type selection into max type.
            #if max(commune_types[1:]) != 0:
            #    commune_type = np.argmax(commune_types[1:]) + 1
        cluster["type"] = commune_type


    comm_path = file_location + "fcl_txs/comm_" + date_curr + ".txt"
    with open(comm_path, "w") as write_file:
        json.dump(communities, write_file, indent=1)

    current_day = current_day + timedelta(days=1)