# This script will download and store the data for the last day of transactions.
import sys
from datetime import datetime, timedelta
import requests
import json
import pandas as pd
import os

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Decide what location we want to use
file_location = "../fcl_data/"
#file_location = "/Volumes/DingosDiner/fcl_data/"
#===================================
# 1) SET THE DATE TO GET
#===================================

target_day = sys.argv[1]
#target_day = '02_05_2022'
current_day = datetime.strptime(target_day, '%d_%m_%Y')
date_curr = current_day.strftime('%d_%m_%Y')

# Uncomment to hard-set the date
#target_day = "03_04_2022"
#current_day = datetime.strptime(target_day, '%d_%m_%Y')
#date_curr = current_day.strftime('%d_%m_%Y')

#===================================
# 2) OBTAIN RELEVANT BLOCK HASHES
#===================================
blockList = []
blk_cnt = 0

curr_day_mill = current_day.timestamp() * 1000
curr_day_mill = str(curr_day_mill).split('.')[0]
# Connect to blockchain.com and obtain the JSON for the block hashes for the day of interest.
url = "https://blockchain.info/blocks/" + curr_day_mill + "?format=json"
results = requests.get(url)
if results.status_code != 200:
    print("There was an error connecting for the block hashes, status code isn't correct!")
    exit()

blocks_info = results.json()
for b in blocks_info:
    block_hash = b['hash']
    blockList.append(block_hash)

# ===================================
# 3) GET ALL TRANSACTIONS BY BLOCK
# ===================================

for block in blockList:
    txList = []
    print("Starting to work on block: " + str(block))
    blk_cnt += 1
    block_url = "https://blockchain.info/rawblock/" + str(block)
    block_results = requests.get(block_url)
    if block_results.status_code != 200:
        print("There was an error connecting for a specific block transactions, status code isn't correct!")
        break

    block_time = block_results.json()['time']
    block_txs = block_results.json()['tx']
    for tx in block_txs:
        for sender in tx['inputs']:
            sender_info = sender['prev_out']
            if sender_info['script'] =='':
                txSender = '000000000000000000000000'
            else:
                try:
                    txSender = sender_info['addr']
                except:
                    txSender = txSender
            for receiver in tx['out']:
                if receiver['value'] != 0:
                    try:
                        txReceiver = receiver['addr']
                    except:
                        txReceiver = '000000000000000000000000'
                    txValue = receiver['value']
                    transaction = [block_time, tx['hash'], tx['fee'], txSender, txReceiver, txValue]
                    txList.append(transaction)
    print("I have completed " + str(round((blk_cnt/len(blockList))*100, 2)) + "% of the blocks for day " + date_curr + ".")
    txs_df = pd.DataFrame(txList)
    txs_df.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']
    out_Path = file_location + "btc_txs/btc_tx_" + date_curr + ".csv"

    if not os.path.isfile(out_Path):
        txs_df.to_csv(out_Path, header=False, index=False)
    else:  # else it exists so append without writing the header
        txs_df.to_csv(out_Path, mode='a', header=False, index=False)