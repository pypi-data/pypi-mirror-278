# This script will take the desired address and produce all the necesary analysis and statistics to build the report.

# Outputs:
# 1) Address Level: address, date, addr_id, addr_txs, addr_vols, addr_deg
# 2) Wallet Level: addr_inwallet, wallet_type, wallet_size, wallet_txs, wallet_volumes, wallet_bnocs
# 3) Community Level: inCommunity, comm_id, comm_size, comm_rank, comm_volumes, comm_bnocs


# Import libraries
from datetime import datetime, timedelta
import pandas as pd
import json
import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt
import math
import subprocess
import sys
import glob
import os

startTime = time.time()

# Decide what location we want to use
file_location = "../fcl_data/"
#file_location = "/Volumes/DingosDiner/fcl_data/"
#######################
#       INPUTS
#######################

date = sys.argv[1]                          # "yyyy-mm-dd"
address = sys.argv[2]                       # 'address'
request_id = sys.argv[3]                    # "4"

target_day = datetime.strptime(date, '%Y-%m-%d')
target_date = target_day.strftime('%d_%m_%Y')


#######################
# 0) REMOVE DATA
dir = "../fcl_data/btc_txs"
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = "../fcl_data/fcl_txs"
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))
#######################


#######################
#   1) GET DATA
# Assume that we don't have the data. Download the necessary days.
memory = 2
date_start = target_day - timedelta(days=memory)
date_list = pd.date_range(date_start, periods=(memory+1))
date_list = date_list.strftime("%d_%m_%Y").tolist()

for date_target in date_list:
    try:
        subprocess.run(['python', 'routine_data.py', date_target], check=True, capture_output=True)
    except subprocess.CalledProcessError as err:
        print('ERROR:', err)
        exit(-1)

program_list = ['routine_wallet.py', 'routine_wallet_type.py',
                'routine_community.py', 'routine_community_type.py', 'routine_community_reduce.py']
for program in program_list:
    try:
        subprocess.run(['python', program, target_date], check=True, capture_output=True)
        print("Finished: " + program)
    except subprocess.CalledProcessError as err:
        print('ERROR:', err)
        print(err.output)
        exit(-1)
#######################


#######################
#   2) ADDRESS LEVEL
# Load the complete transactions of networks
rawday_path = file_location + "btc_txs/btc_tx_" + target_date + ".csv"
day_frame = pd.read_csv(rawday_path)
day_frame.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']

# Check if the address exists:
check = len(day_frame.loc[day_frame['txSender'] == address]) + len(day_frame.loc[day_frame['txReceiver'] == address])
if check == 0:
    quit()

# Form a dataframe with links where it is a sender
sending_df = day_frame.loc[day_frame['txSender'] == address]
sending_df = sending_df.drop_duplicates('txHash')
addr_vol_out = sending_df['txValue'].sum()                          #Variable to extract
addr_txs_out = len(sending_df)                                      #Variable to extract
sending_df = day_frame.loc[day_frame['txSender'] == address]
sending_df = sending_df.drop_duplicates('txReceiver')
addr_deg_out = len(sending_df)                                      #Variable to extract

# Form a dataframe with links where it is a receiver
receiving_df = day_frame.loc[day_frame['txReceiver'] == address]
receiving_df = receiving_df.drop_duplicates('txHash')
addr_vol_in = receiving_df['txValue'].sum()                           #Variable to extract
addr_txs_in = len(receiving_df)                                       #Variable to extract
receiving_df = day_frame.loc[day_frame['txReceiver'] == address]
receiving_df = receiving_df.drop_duplicates('txSender')
addr_deg_in = len(receiving_df)                                     #Variable to extract
#######################

#######################
#   3) WALLET LEVEL
wallet_path = file_location + "fcl_txs/wallets_" + target_date + ".json"
wallet_dict = json.load(open(wallet_path))
# Get the parent of the wallet.
parent = wallet_dict[address]
# Find how many other addresses have the same parent
wallet_size = 0
wallet_membs = []
for node in wallet_dict:
    if wallet_dict[node] == parent:
        wallet_size += 1                                                #Variable to extract
        wallet_membs.append(node)                                       #Variable to extract

# Flag that this address is part of a wallet
addr_wallet = False
if wallet_size > 1:
    addr_wallet = True                                                  #Variable to extract

# Get the wallet's type
types_path = file_location + "fcl_txs/types_" + target_date + ".json"
types_dict = json.load(open(types_path))
wallet_type = types_dict[parent]                                        #Variable to extract

# Get the wallet's network
cd_edgeList = day_frame[["txSender", "txReceiver", "txValue"]].values.tolist()
G = nx.DiGraph()
G.add_nodes_from(wallet_membs)
G.add_weighted_edges_from(cd_edgeList)
S = G.subgraph(wallet_membs)

wallet_full_out = list(G.out_degree(wallet_membs, weight="weight"))
wallet_full_in = list(G.in_degree(wallet_membs, weight="weight"))
wallet_intra_out = list(S.out_degree(wallet_membs, weight="weight"))
wallet_intra_in = list(S.in_degree(wallet_membs, weight="weight"))

wallet_full_out.sort(key=lambda a: a[1], reverse=True)
wallet_full_in.sort(key=lambda a: a[1], reverse=True)
wallet_intra_out.sort(key=lambda a: a[1], reverse=True)
wallet_intra_in.sort(key=lambda a: a[1], reverse=True)

wallet_full_out_stat = [x[0] for x in wallet_full_out[:3]]
wallet_full_in_stat = [x[0] for x in wallet_full_in[:3]]
wallet_intra_out_stat = [x[0] for x in wallet_intra_out[:3]]
wallet_intra_in_stat = [x[0] for x in wallet_intra_in[:3]]

wallet_voterank = nx.voterank(S, number_of_nodes=5)

rawday_path = file_location + "fcl_txs/wallet_tx_" + target_date + ".csv"
day_frame_w = pd.read_csv(rawday_path)
day_frame_w.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']

# Form a dataframe with links where it is a sender
w_sending_df = day_frame_w.loc[day_frame_w['txSender'] == parent]
w_sending_df = w_sending_df.drop_duplicates('txHash')
w_addr_vol_out = w_sending_df['txValue'].sum()                          #Variable to extract
w_addr_txs_out = len(w_sending_df)                                      #Variable to extract
w_sending_df = day_frame_w.loc[day_frame_w['txSender'] == parent]
w_sending_df = w_sending_df.drop_duplicates('txReceiver')
w_addr_deg_out = len(w_sending_df)                                      #Variable to extract

# Form a dataframe with links where it is a receiver
w_receiving_df = day_frame_w.loc[day_frame_w['txReceiver'] == parent]
w_receiving_df = w_receiving_df.drop_duplicates('txHash')
w_addr_vol_in = w_receiving_df['txValue'].sum()                           #Variable to extract
w_addr_txs_in = len(w_receiving_df)                                       #Variable to extract
w_receiving_df = day_frame_w.loc[day_frame_w['txReceiver'] == parent]
w_receiving_df = w_receiving_df.drop_duplicates('txSender')
w_addr_deg_in = len(w_receiving_df)
#######################


#######################
#  4) COMMUNITY LEVEL
comm_path = file_location + "fcl_txs/comm_" + target_date + ".txt"
with open(comm_path) as json_file:
    communities = json.load(json_file)

is_commune = False
for cluster in communities:
    id = cluster["id"][11:]
    commune = cluster["members"]
    type = cluster["type"]

    if parent in commune:
        is_commune = True
        break

comm_rank = 0
comm_type = 0
comm_size = 0
comm_voterank = []
comm_intra_out_stat = []
comm_intra_in_stat = []
comm_intra_in_max = ''
comm_full_in_stat = []
comm_full_out_stat = []


if is_commune == True:
    comm_rank = id
    comm_type = type

    w_edgeList = day_frame_w[["txSender", "txReceiver", "txValue"]].values.tolist()
    G = nx.DiGraph()
    G.add_nodes_from(commune)
    G.add_weighted_edges_from(w_edgeList)
    H = G.subgraph(commune)

    comm_size = H.order()
    comm_full_out = list(G.out_degree(commune, weight="weight"))
    comm_full_in = list(G.in_degree(commune, weight="weight"))
    comm_intra_out = list(H.out_degree(commune, weight="weight"))
    comm_intra_in = list(H.in_degree(commune, weight="weight"))

    comm_full_out.sort(key=lambda a: a[1], reverse=True)
    comm_full_in.sort(key=lambda a: a[1], reverse=True)
    comm_intra_out.sort(key=lambda a: a[1], reverse=True)
    comm_intra_in.sort(key=lambda a: a[1], reverse=True)

    comm_full_out_stat = [x[0] for x in comm_full_out[:3]]
    comm_full_in_stat = [x[0] for x in comm_full_in[:3]]
    comm_intra_out_stat = [x[0] for x in comm_intra_out[:3]]
    comm_intra_in_stat = [x[0] for x in comm_intra_in[:3]]

    comm_voterank = nx.voterank(H, number_of_nodes=5)
else:
    H = G.subgraph(parent)
    comm_rank = 0
    comm_type = 0
    comm_size = 0

#######################

################################
# 5) CLEAN AND EXPORT STATS
type_translate = {0:"Unknown", 1:"Miners", 2:"Exchanges", 3:"Black Market", 4:"Origin",
                  5:"State Backed Illicit", 6:"Scams and Ransomware"}
wallet_type = type_translate[wallet_type]
comm_type = type_translate[comm_type]

wallet_intra_key = wallet_voterank + wallet_intra_out_stat + wallet_intra_in_stat
wallet_intra_key = list(set(wallet_intra_key))
wallet_intra_key = wallet_intra_key[:3]
wallet_full_key = wallet_full_out_stat + wallet_full_in_stat
wallet_full_key = list(set(wallet_full_key))
wallet_full_key = wallet_full_key[:3]

comm_intra_key = comm_voterank + comm_intra_out_stat + comm_intra_in_stat
#comm_intra_key.append(comm_intra_in_max)
comm_intra_key = list(set(comm_intra_key))
comm_intra_key = comm_intra_key[:3]
comm_full_key = comm_full_out_stat + comm_full_in_stat
comm_full_key = list(set(comm_full_key))
comm_full_key = comm_full_key[:3]

if is_commune == False:
    comm_intra_key = [0]*3
    comm_full_key = [0]*3

stats_dic = {'address': address,
             'date': target_date,
             'addr_wallet': addr_wallet,
             'wallet_size': str(wallet_size),
             'wallet_type': wallet_type,
             'w_addr_vol_out': str(round(w_addr_vol_out*0.00000001, 4)),
             'w_addr_deg_out': str(w_addr_deg_out),
             'w_addr_vol_in': str(round(w_addr_vol_in*0.00000001, 4)),
             'w_addr_deg_in': str(w_addr_deg_in),
             'wallet_intra_key': wallet_intra_key,
             'wallet_full_key': wallet_full_key,
             'is_commune': is_commune,
             'comm_rank': str(comm_rank),
             'comm_type': comm_type,
             'comm_size': str(comm_size),
             'comm_intra_key': comm_intra_key,
             'comm_full_key': comm_full_key
             }

outward_path = "./pdf_contents_a/address_text_" + request_id + ".txt"
with open(outward_path, 'w') as file:
     file.write(json.dumps(stats_dic)) # use `json.loads` to do the reverse
#######################


#######################
# 6) WALLET VISUALS
wallet_relevant = wallet_intra_key + wallet_full_key
wallet_relevant = list(set(wallet_relevant))

color_map = []
size_map = []
for node in S:
    if node == address:
        color_map.append('#Ff0000')
        size_map.append(50)
    elif node in wallet_relevant:
        color_map.append('#006AFB')
        size_map.append(50)
    else:
        color_map.append('#4F4F4F')
        size_map.append(15)

options = {"node_color": color_map, "edge_color": '#808080', "node_size": size_map, "linewidths": 0.5,
               "with_labels": False, "arrowsize": 4}
pos = nx.spring_layout(S)
nx.draw(S, pos, **options)
ax = plt.gca()
ax.collections[0].set_edgecolor("#000000")
wgraph_path = "./pdf_contents_a/wallet_graph_" + request_id + ".png"
plt.savefig(wgraph_path, format="png")
#plt.show()
plt.clf()
#######################

#######################
# 7) COMMUNITY VISUALS

if comm_size >= 5000:
    W = nx.Graph(H)
    # filter out all edges below threshold and grab id's
    threshold = 0.5 / 0.00000001
    long_edges = list(filter(lambda e: e[2] < threshold, (e for e in W.edges.data('weight'))))
    le_ids = list(e[:2] for e in long_edges)
    for link in le_ids:
        if link[0] == parent:
            le_ids.remove(link)
        elif link[1] == parent:
            le_ids.remove(link)
    # remove filtered edges from graph
    W.remove_edges_from(le_ids)
    W.remove_nodes_from(list(nx.isolates(W)))
    comm_relevant = comm_intra_key + comm_full_key
    comm_relevant = list(set(comm_relevant))

    color_map = []
    size_map = []
    for node in W:
        if node == parent:
            color_map.append('#Ff0000')
            size_map.append(50)
        elif node in comm_relevant:
            color_map.append('#006AFB')
            size_map.append(50)
        else:
            color_map.append('#4F4F4F')
            size_map.append(15)

    edges = W.edges()
    weights = [(W[u][v]['weight']) * 0.00000001 for u, v in edges]
    w_scale = 10 / np.log(max(weights))
    weights = [np.log(item) * w_scale for item in weights]

    # "width":0.1
    options = {"node_color": color_map, "edge_color": '#808080', "node_size": size_map, "linewidths": 0.5,
               "width": weights,
               "with_labels": False, "arrowsize": 4}

    pos = nx.spring_layout(W, iterations=50, k=7000 / math.sqrt(H.order()))
    nx.draw(W, pos, **options)
    ax = plt.gca()
    ax.collections[0].set_edgecolor("#000000")
    cgraph_path = "./pdf_contents_a/comm_graph_" + request_id + ".png"
    plt.savefig(cgraph_path, format="png", dpi=200)
    # plt.show()
    plt.clf()

else:
    # Set the node colours for relevant nodes.
    comm_relevant = comm_intra_key + comm_full_key
    comm_relevant = list(set(comm_relevant))
    color_map = []
    size_map = []
    for node in H:
        if node == parent:
            color_map.append('#Ff0000')
            size_map.append(50)
        elif node in comm_relevant:
            color_map.append('#006AFB')
            size_map.append(50)
        else:
            color_map.append('#4F4F4F')
            size_map.append(15)

    options = {"node_color": color_map, "edge_color": '#808080', "node_size": size_map, "linewidths": 0.5, "width": 0.1,
               "with_labels": False}

    pos = nx.spring_layout(H, iterations=70, k=2000 / math.sqrt(H.order()))
    nx.draw(H, pos, **options)
    cgraph_path = "./pdf_contents_a/comm_graph_" + request_id + ".png"
    plt.savefig(cgraph_path, format="png", dpi=200)
    # plt.show()
    plt.clf()
#######################

#######################
# 8) GLOBAL VISUALS
rawday_path = file_location + "fcl_txs/comm_tx_" + target_date + ".csv"
day_frame_g = pd.read_csv(rawday_path)
day_frame_g.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']
nodes_in = day_frame_g["txSender"].values.tolist()
nodes_in = [str(item) for item in nodes_in]
nodes_out = day_frame_g["txReceiver"].values.tolist()
nodes_out = [str(item) for item in nodes_out]
nodes_all = nodes_in + nodes_out
g_nodeList = np.unique(nodes_all)
g_edgeList = day_frame_g[["txSender", "txReceiver", "txValue"]].values.tolist()

G = nx.DiGraph()
G.add_nodes_from(g_nodeList)
G.add_weighted_edges_from(g_edgeList)

#{0:"Unknown", 1:"Miners", 2:"Exchanges", 3:"Black Market", 4:"Origin", 5:"State Backed Illicit", 6:"Scams and Ransomware"}
type_translate = {0:"#073B4C", 1:"#FFD166", 2:"#EF476F", 3:"#118AB2", 4:"#F5A623",
                  5:"#BD10E0", 6:"#06D6A0"}
comm_list = [str(i) for i in range(len(communities))]
color_map = []
size_map = []
for node in G:
    if node in comm_list:
        comm = int(node) - 1
        comm_info = communities[comm]
        c_type = comm_info["type"]
        c_type = type_translate[c_type]
        c_size = len(comm_info["members"])
        c_size = c_size/10
        if node == str(comm_rank):
            c_type = "#Ff0000"
        color_map.append(c_type)
        size_map.append(c_size)
    else:
        color_map.append('#4F4F4F')
        size_map.append(5)

# filter out all edges below threshold and grab id's
threshold = 0.5/0.00000001
long_edges = list(filter(lambda e: e[2] < threshold, (e for e in G.edges.data('weight'))))
le_ids = list(e[:2] for e in long_edges)
# remove filtered edges from graph
G.remove_edges_from(le_ids)

edges = G.edges()
weights = [(G[u][v]['weight'])*0.00000001 for u,v in edges]
w_scale = 10/np.log(max(weights))
weights = [np.log(item)*w_scale for item in weights]

options = {"node_color": color_map, "edge_color": '#808080', "node_size": size_map, "linewidths": 0.5, "width": weights,
           "with_labels": False, "arrowsize":4}

pos = nx.spring_layout(G, iterations=50, k=7000/math.sqrt(G.order()))
nx.draw(G, pos, **options)
ax = plt.gca()
ax.collections[0].set_edgecolor("#000000")

fgraph_path = "./pdf_contents_a/full_graph_" + request_id + ".png"
plt.savefig(fgraph_path, format="png", dpi=500)
#plt.show()
plt.clf()
#######################


#######################
# 9) REMOVE DATA
dir = "../fcl_data/btc_txs"
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = "../fcl_data/fcl_txs"
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))
#######################


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))