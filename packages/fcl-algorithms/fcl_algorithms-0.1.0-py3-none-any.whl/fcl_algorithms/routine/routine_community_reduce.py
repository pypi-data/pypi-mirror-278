# This script will take the wallet transaction data
# Then it will take the mapping to communities and reduce the transaction graph.

# PRELIMINARY STUFF

from datetime import datetime, timedelta
import pandas as pd
import networkx as nx
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


# Iterate through dates
while current_day < lim_day:
    curr_day_mill = current_day.timestamp() * 1000
    curr_day_mill = str(curr_day_mill).split('.')[0]
    date_curr = current_day.strftime('%d_%m_%Y')
    print("Working on wallets for " + date_curr)

    # Load the communities and build a dictionary for wallets to community.
    comm_path = file_location + "fcl_txs/comm_" + date_curr + ".txt"
    with open(comm_path) as json_file:
        communities = json.load(json_file)
    print("Got the communities")
    comm_dic = {}
    for cluster in communities:
        id = cluster["id"][11:]
        commune = cluster["members"]
        for wallet in commune:
            comm_dic[wallet] = id
    print("Got the communities dictionary")
    rawday_path = file_location + "fcl_txs/wallet_tx_" + date_curr + ".csv"
    with open(rawday_path, newline='') as f:
        reader = csv.reader(f)
        day_txs = list(reader)
    tx_len = len(day_txs)
    txList = []
    print("Got the transaction data")
    for link in day_txs:
        comLink = False
        try:
            txSender = comm_dic[link[3]]
            comLink = True
        except:
            txSender = link[3]
        try:
            txReceiver = comm_dic[link[4]]
            comLink = True
        except:
            txReceiver = link[4]
        if txSender != txReceiver and comLink:
            transaction = [link[0], link[1], link[2], txSender, txReceiver, link[5]]
            txList.append(transaction)
    print("Got the clean data")
    txs_df = pd.DataFrame(txList)
    txs_df.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']
    txs_df = txs_df.drop_duplicates()
    out_Path = file_location + "fcl_txs/comm_tx_" + date_curr + ".csv"
    txs_df.to_csv(out_Path, header=False, index=False)


    print("Completed reduction for " + date_curr)
    current_day = current_day + timedelta(days=1)