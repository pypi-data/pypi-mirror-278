# This is step 1 (of 4) in the operation.
# It goes through the daily transactions and finds wallets, updates the existing mapping.
# It then stores the mapping list for later reduction of addresses.

import os
import glob
import csv
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import dask.bag as db

wallet_template = '{wallet_address},{wallet_owner}'


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
    day_frame = pd.read_csv(rawday_path)
    day_frame.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']
    tx_senders = day_frame.groupby('txHash')['txSender'].apply(list)
    len_txs = len(tx_senders)
    print("Starting work on the " + str(len_txs) + " transactions of the day.")
    i = 0
    # Find and update the existing mapping with the transactions for the day.
    for tx in tx_senders:
        i += 1
        alert = i % 1000
        if alert == 0:
            progress = (i*100)/len_txs
            progress = round(progress, 1)
            print("Progress on day's transactions: " + str(progress) + "%")
        owner = tx[0]
        if owner in wallets:
            owner = wallets[owner]
        for addr in tx:
            subject = addr
            if subject in wallets:
                old_owner = wallets[subject]
                if owner != old_owner:
                    for k, v in wallets.items():
                        if v == old_owner:
                            wallets[k] = owner
            else:
                wallets[subject] = owner

    # Store the updated version of the mapping.
    outputFile = open("raw_wallets.txt", "w")
    for key, value in wallets.items():
        outputFile.write(wallet_template.format(
            wallet_address=key,
            wallet_owner=value
        ) + '\n')
    outputFile.close()
