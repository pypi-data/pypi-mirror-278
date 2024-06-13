# This is step 2 (of 4) in the operation.
# It looks at the daily transaction networks and reduces them using the latest wallet mapping.
# It then stores the latest wallet networks.

# 1 Load the wallet mapping
# 2 Load the transaction network for each day
# 3 For each transaction update the sender and receiver using the mapping. Save in new df if s-r different.
# 4 Store the reduced transaction data.

import os
import csv
import pandas as pd
from datetime import datetime, timedelta


# Load the existing mapping of addresses to wallets identified.
#wallets = {'17CzhyqsmXFKByFuDWWi728quGLK1K6iWX':'17CzhyqsmXFKByFuDWWi728quGLK1K6iWX'}
reader = csv.reader(open("raw_wallets.txt", 'r'))
for k, v in reader:
    wallets = dict(reader)

# Get the last day we have reduced.
last_day = datetime.strptime('01_01_2021', '%d_%m_%Y') # This is the last day that is complete.
today = datetime.today() - timedelta(days=1)
lim_day = datetime.strptime('04_01_2021', '%d_%m_%Y')  # This is the last day missing.
current_day = last_day

# Loop through every period of 24h that we need.
while current_day < lim_day:
    current_day = current_day + timedelta(days=1)
    curr_day_mill = current_day.timestamp() * 1000
    curr_day_mill = str(curr_day_mill).split('.')[0]
    date_curr = current_day.strftime('%d_%m_%Y')
    print("The current day I am working on is: " + date_curr)

    rawday_path = "/Users/diegolara/PycharmProjects/play-btc-comsite/web_txs/btc_tx_" + date_curr + ".csv"
    with open(rawday_path, newline='') as f:
        reader = csv.reader(f)
        day_txs = list(reader)

    num_txs = len(day_txs)
    print("Starting work on the day's " + str(num_txs) + " transactions.")
    #day_frame.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']
    txList = []
    for link in day_txs:
        sender = link[3]
        txSender = wallets[link[3]]
        try:
            txReceiver = wallets[link[4]]
        except:
            txReceiver = link[4]
        if txSender != txReceiver:
            transaction = [link[0], link[1], link[2], txSender, txReceiver, link[5]]
            txList.append(transaction)
    print("Finished the reductions, storing the data...")
    txs_df = pd.DataFrame(txList)
    txs_df.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']
    out_Path = "/Users/diegolara/PycharmProjects/play-btc-comsite/web_txs/wallet_tx_" + date_curr + ".csv"
    txs_df.to_csv(out_Path, header=False, index=False)
