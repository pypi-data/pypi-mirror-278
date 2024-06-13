# This is step 3 (of 4) in the operation.
# it goes through the wallet network and finds the communities.
# It then stores the reduced graph for later use. Also the members list for reference.


import networkx as nx
from cdlib import algorithms
import glob
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


##### STEP 0: Get the known address lists and set where to get the daily transactions data.

# known address lists
db_exchange = pd.concat([pd.read_csv(f, header=None) for f in glob.glob("/Users/diegolara/PycharmProjects/btc-wallet-tag/ex_*.csv")], ignore_index=True)
db_miners = pd.concat([pd.read_csv(f, header=None) for f in glob.glob("/Users/diegolara/PycharmProjects/btc-wallet-tag/mn_*.csv")], ignore_index=True)
db_black = pd.concat([pd.read_csv(f, header=None) for f in glob.glob("/Users/diegolara/PycharmProjects/btc-wallet-tag/bm_*.csv")], ignore_index=True)
db_origin = {0}


cd_nodeList = []
cd_edgeList = []

links_bm_bm = 0
links_bm_ex = 0
links_bm_mn = 0
links_bm_ot = 0

links_mn_mn = 0
links_mn_ex = 0
links_mn_bm = 0
links_mn_ot = 0

links_ex_ex = 0
links_ex_mn = 0
links_ex_bm = 0
links_ex_ot = 0

links_ot_ot = 0
links_ot_ex = 0
links_ot_mn = 0
links_ot_bm = 0


var_bm_bm = []
var_bm_ex = []
var_bm_mn = []
var_bm_ot = []

var_mn_mn = []
var_mn_ex = []
var_mn_bm = []
var_mn_ot = []

var_ex_ex = []
var_ex_mn = []
var_ex_bm = []
var_ex_ot = []

var_ot_ot = []
var_ot_ex = []
var_ot_mn = []
var_ot_bm = []

days = []

comm_template = '{comm_address},{comm_id}'


# Get the last day we have reduced.
last_day = datetime.strptime('01_01_2021', '%d_%m_%Y') # This is the last day that is complete.
today = datetime.today() - timedelta(days=1)
lim_day = datetime.strptime('04_01_2021', '%d_%m_%Y')  # This is the last day missing.
current_day = last_day

while current_day < lim_day:
    current_day = current_day + timedelta(days=1)
    curr_day_mill = current_day.timestamp() * 1000
    curr_day_mill = str(curr_day_mill).split('.')[0]
    date_curr = current_day.strftime('%d_%m_%Y')
    print("The current day I am working on is: " + date_curr)

    ##### STEP 1: Load the network of transactions
    rawday_path = "/Users/diegolara/PycharmProjects/play-btc-comsite/web_txs/wallet_tx_" + date_curr + ".csv"
    day_frame = pd.read_csv(rawday_path)
    day_frame.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']

    ##### STEP 2: Generate the necesary data for the graph
    # generate a list of nodes
    nodes_in = day_frame["txSender"].values.tolist()
    nodes_in = [str(item) for item in nodes_in]
    nodes_out = day_frame["txReceiver"].values.tolist()
    nodes_out = [str(item) for item in nodes_out]
    nodes_all = nodes_in + nodes_out
    cd_nodeList = np.unique(nodes_all)
    # generate a list of transactions
    tx_list = day_frame["txHash"].values.tolist()
    tx_list = [str(item) for item in tx_list]
    cd_txList = np.unique(tx_list)
    cd_txs = len(cd_txList)
    # generate a list of edges
    cd_edgeList = day_frame[["txSender", "txReceiver"]].values.tolist()
    df_edges = day_frame[["txSender", "txReceiver"]]
    # generate the NetworkX graph
    G = nx.Graph()
    G.add_nodes_from(cd_nodeList)
    G.add_edges_from(cd_edgeList)
    ##### STEP 3: Build the Louvain communities and generate mapping from wallet to communities.
    db_types = pd.DataFrame(cd_nodeList)
    db_types.columns = ['address']
    db_types["type"] = np.nan
    cd_communities = algorithms.louvain(G)
    commune_num = 0
    for commune in cd_communities.communities:
        if len(commune) >= 100:
            commune_num += 1
            #Find what type of community this is:
            overlap_mn = set.intersection(set(commune), set(db_miners[0]))
            overnum_mn = len(overlap_mn)
            overlap_ex = set.intersection(set(commune), set(db_exchange[0]))
            overnum_ex = len(overlap_ex)
            overlap_bm = set.intersection(set(commune), set(db_black[0]))
            overnum_bm = len(overlap_bm)
            overlap = [overnum_mn, overnum_ex, overnum_bm, 1]
            ed_dic = {0: "mining", 1: "exchange", 2: "black", 3: commune_num}
            commune_type = ed_dic[3]
            is_origin = len(set.intersection(set(commune), '0'))
            if is_origin > 0:
                commune_type = 'mining'
            db_commune = pd.DataFrame(commune)
            db_commune.columns = ['address']
            db_commune["type_com"] = commune_type
            db_types = db_types.merge(db_commune, how='left', on='address')
            db_types['type'] = db_types['type_com'].fillna(db_types['type'])
            db_types = db_types.drop('type_com', axis=1)
    db_types['type'] = db_types['type'].fillna(db_types['address'])
    dic_types = db_types.set_index('address')['type'].to_dict()
    ##### STEP 4: Reduce the network with the communities and store it.
    day_frame['sender_com'] = df_edges['txSender'].map(dic_types)
    day_frame['receiver_com'] = df_edges['txReceiver'].map(dic_types)
    day_frame = day_frame[['txTime', 'txHash', 'txFee', 'sender_com', 'receiver_com', 'txValue']]
    comm_frame = day_frame[day_frame.sender_com != day_frame.receiver_com]
    comNet_Path = "/Users/diegolara/PycharmProjects/play-btc-comsite/web_txs/comm_tx_" + date_curr + ".csv"
    comm_frame.to_csv(comNet_Path, header=False, index=False)
    ##### STEP 5: Store the dictionary with the communities.
    comList_Path = "comm_dic_" + date_curr + ".txt"
    outputFile = open(comList_Path, "w")
    for key, value in dic_types.items():
        outputFile.write(comm_template.format(
            comm_address=key,
            comm_id=value
        ) + '\n')
    outputFile.close()