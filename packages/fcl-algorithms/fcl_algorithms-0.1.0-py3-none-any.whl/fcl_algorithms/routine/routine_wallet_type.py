# This script will look at all the addresses as assign them a type if possible. Using the Wallet explorer.
# Then it will take the mapping to wallets and reduce the transaction graph.


# 1) Load the dictionaries of known addresses.
# 2) Load each day's address => wallet mapping.
# 3) Assign types if possible, building a dictionary for wallets.
# 4) Load the complete graph, reduce using the wallets.

# PRELIMINARY STUFF

from datetime import datetime, timedelta
import pandas as pd
import glob
import csv
import numpy as np
import sys
import json


# Decide what location we want to use
file_location = "../fcl_data/"
#file_location = "/Volumes/DingosDiner/fcl_data/"
# ===================================
# 0) Decide the desired dates
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

########################################
# 1) Load the identification dictionary
########################################

# Load know addresses and types dictionary.
taggs = []
for f in glob.glob(file_location + "tags/tagged_db_*.txt"):
    with open(f) as json_file:
        tag_list = json.load(json_file)
        taggs.extend(tag_list)

tags_dict = {item['id']:item for item in taggs}

# Iterate through dates
while current_day < lim_day:
    curr_day_mill = current_day.timestamp() * 1000
    curr_day_mill = str(curr_day_mill).split('.')[0]
    date_curr = current_day.strftime('%d_%m_%Y')
    print("Working on wallets for " + date_curr)

    ########################################
    # 2) Load each day's address => wallet mapping.
    ########################################

    # Reading the data from the file
    wallet_path = file_location + "fcl_txs/wallets_" + date_curr + ".json"
    wallet_dict = json.load(open(wallet_path))

    ########################################
    # 3) Assign types if possible, building a dictionary for wallets.
    ########################################

    # Create wallet type dictionary
    type_dict = {}

    for address in wallet_dict:
        # Check whether we know the type of this address
        if address in tags_dict:
            adr_type = tags_dict[address]["type"]
        else:
            adr_type = 0

        # Assign type to the parent of the wallet, based on type.
        parent = wallet_dict[address]
        if parent in type_dict:
            if adr_type != 0:
                type_dict[parent] = adr_type
        if parent not in type_dict:
            type_dict[parent] = adr_type

    # Store the new dictionary in file
    new_path = file_location + "fcl_txs/types_" + date_curr + ".json"
    json.dump(type_dict, open(new_path, 'w'))
    print("Wallet type complete")

    ########################################
    # 4) Load the complete graph, reduce using the wallets.
    ########################################

    rawday_path = file_location + "btc_txs/btc_tx_" + date_curr + ".csv"
    with open(rawday_path, newline='') as f:
        reader = csv.reader(f)
        day_txs = list(reader)
    tx_len = len(day_txs)
    txList = []
    for link in day_txs:
        sender = link[3]
        txSender = wallet_dict[link[3]]
        try:
            txReceiver = wallet_dict[link[4]]
        except:
            print("I couldn't find address: " + str(link[4]))
            txReceiver = link[4]
        if txSender != txReceiver:
            transaction = [link[0], link[1], link[2], txSender, txReceiver, link[5]]
            txList.append(transaction)
    print("Finished the reductions, storing the data...")
    wallet_len = len(txList)
    print("Number of connections: " + str(tx_len))
    print("New number of links: " + str(wallet_len))
    print("Number of addresses: " + str(len(wallet_dict)))
    print("New number of nodes: " + str(len(type_dict)))
    txs_df = pd.DataFrame(txList)
    txs_df.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']
    out_Path = file_location + "fcl_txs/wallet_tx_" + date_curr + ".csv"
    txs_df.to_csv(out_Path, header=False, index=False)

    current_day = current_day + timedelta(days=1)

    print("Date complete")

