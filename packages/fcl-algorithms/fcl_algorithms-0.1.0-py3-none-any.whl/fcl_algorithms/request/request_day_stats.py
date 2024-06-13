# This script will take the desired date and produce all the necesary analysis and statistics to build the report.

# Outputs:
# 1) Global Level: date, total_transactions, total_active, total_links, total_wallets, total_communities
# 2) Splits: total_vol, vol_miners, vol_exchange, vol_black, vol_scams, vol_others
# 3) Wallets: wallet_name, wallet_volume, wallet_size
# 4) Community: community_name, community_volume, community_size, community_type
# 5) Graph: Community level graph with weighted edges/nodes?


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
import os
import sys


startTime = time.time()

# Decide what location we want to use
file_location = "../fcl_data/"
#file_location = "/Volumes/DingosDiner/fcl_data/"
#######################
#       INPUTS
#######################

date = sys.argv[1]                      # "yyyy-mm-dd"
request_id = sys.argv[2]                # "6"


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
    subprocess.call(['python', 'routine_data.py', date_target])

program_list = ['routine_wallet.py', 'routine_wallet_type.py',
                'routine_community.py', 'routine_community_type.py', 'routine_community_reduce.py']
for program in program_list:
    subprocess.call(['python', program, target_date])
    print("Finished: " + program)
#######################


#######################
#   2) GLOBAL LEVEL
# Load the complete transactions of networks
rawday_path = file_location + "btc_txs/btc_tx_" + target_date + ".csv"
day_frame = pd.read_csv(rawday_path)
day_frame.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']

total_tx = day_frame[["txHash"]].values.tolist()
total_tx = np.unique(total_tx)
total_transactions = len(total_tx)                              #Variable to extract

nodes_in = day_frame["txSender"].values.tolist()
nodes_in = [str(item) for item in nodes_in]
nodes_out = day_frame["txReceiver"].values.tolist()
nodes_out = [str(item) for item in nodes_out]
nodes_all = nodes_in + nodes_out
cd_nodeList = np.unique(nodes_all)
total_address = len(cd_nodeList)                                #Variable to extract
#######################

#######################
#   3) WALLET LEVEL
# Load the walllet level network
rawday_path = file_location + "fcl_txs/wallet_tx_" + target_date + ".csv"
day_frame_w = pd.read_csv(rawday_path)
day_frame_w.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']

nodes_in = day_frame_w["txSender"].values.tolist()
nodes_in = [str(item) for item in nodes_in]
nodes_out = day_frame_w["txReceiver"].values.tolist()
nodes_out = [str(item) for item in nodes_out]
nodes_all = nodes_in + nodes_out
wall_nodeList = np.unique(nodes_all)
total_wallet = len(wall_nodeList)                                #Variable to extract

total_vol = day_frame_w['txValue'].sum()                       #Variable to extract

wall_edgeList = day_frame_w[["txSender", "txReceiver", "txValue"]].values.tolist()
G = nx.DiGraph()
G.add_nodes_from(wall_nodeList)
G.add_weighted_edges_from(wall_edgeList)

wall_full_out = list(G.out_degree(weight="weight"))
wall_full_in = list(G.in_degree(weight="weight"))
wall_full_out.sort(key=lambda a: a[1], reverse=True)
wall_full_in.sort(key=lambda a: a[1], reverse=True)
wallet_full_out_stat = [x[0] for x in wall_full_out[:5]]
wallet_full_in_stat = [x[0] for x in wall_full_in[:5]]

wallets_key = wallet_full_out_stat + wallet_full_in_stat
wallets_key = list(set(wallets_key))
wallets_key = wallets_key[:5]

# Find out the volumes
wallets_in_v = [0]*len(wallets_key)
wallets_out_v = [0]*len(wallets_key)
i = 0
for wallet in wallets_key:
    wallets_in_v[i] = str(round((G.in_degree(wallet, weight="weight"))*0.00000001, 4))
    wallets_out_v[i] = str(round((G.out_degree(wallet, weight="weight"))*0.00000001, 4))
    i += 1

# Find out the size
wallet_path = file_location + "fcl_txs/wallets_" + target_date + ".json"
wallet_dict = json.load(open(wallet_path))
# Get the parent of the wallet.
wallets_size = [0]*len(wallets_key)
i = 0
for node in wallet_dict:
    if wallet_dict[node] in wallets_key:
        i = wallets_key.index(wallet_dict[node])
        wallets_size[i] += 1
#######################


#######################
#   4) COMMUNITY LEVEL
comm_path = file_location + "fcl_txs/comm_" + target_date + ".txt"
with open(comm_path) as json_file:
    communities = json.load(json_file)

comm_type = [0]*7
comm_size = [0]*7
comm_vol_in = [0]*7
comm_vol_out = [0]*7
comm_vol_with = [0]*7
splits = [0]*7
i = 0
for cluster in communities:
    id = cluster["id"][11:]
    commune = cluster["members"]
    type = cluster["type"]
    S = G.subgraph(commune)
    vol = S.size(weight="weight")
    if i <= 4:
        comm_vol_with[i] = str(round((vol)*0.00000001, 4))
        comm_size[i] = str(len(commune))
        comm_type[i] = str(type)
    i += 1

    # Add the volume to the type
    splits[type] += vol

total_coms = i



# Load the community level network
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

H = nx.DiGraph()
H.add_nodes_from(g_nodeList)
H.add_weighted_edges_from(g_edgeList)

for i in range(7):
    c = str(i+1)
    comm_vol_in[i] = str(round((H.in_degree(c, weight="weight"))*0.00000001, 4))
    comm_vol_out[i] = str(round((H.out_degree(c, weight="weight"))*0.00000001, 4))
#######################

################################
# 5) CLEAN AND EXPORT STATS
stats_dic = {'date': target_date,
             'total_transactions': str(total_transactions),
             'total_address': str(total_address),
             'total_wallet': str(total_wallet),
             'total_vol': str(round(total_vol*0.00000001, 4)),
             'total_coms': str(total_coms),
             'wallets_key': wallets_key,
             'wallets_in_v': wallets_in_v,
             'wallets_out_v': wallets_out_v,
             'wallets_size': wallets_size,
             'splits': splits,
             'comm_type': comm_type,
             'comm_size': comm_size,
             'comm_vol_with': comm_vol_with,
             'comm_vol_in': comm_vol_in,
             'comm_vol_out': comm_vol_out
             }

outward_path = "./pdf_contents_g/date_text_" + request_id + ".txt"
with open(outward_path, 'w') as file:
     file.write(json.dumps(stats_dic)) # use `json.loads` to do the reverse
#######################

#######################
# 6) GLOBAL VISUALS
#{0:"Unknown", 1:"Miners", 2:"Exchanges", 3:"Black Market", 4:"Origin", 5:"State Backed Illicit", 6:"Scams and Ransomware"}
type_translate = {0:"#073B4C", 1:"#FFD166", 2:"#EF476F", 3:"#118AB2", 4:"#F5A623",
                  5:"#BD10E0", 6:"#06D6A0"}
comm_list = [str(i) for i in range(len(communities))]
color_map = []
size_map = []
for node in H:
    if node in comm_list:
        comm = int(node) - 1
        comm_info = communities[comm]
        c_type = comm_info["type"]
        c_type = type_translate[c_type]
        c_size = len(comm_info["members"])
        c_size = c_size/10
        color_map.append(c_type)
        size_map.append(c_size)
    else:
        color_map.append('#4F4F4F')
        size_map.append(5)

# filter out all edges below threshold and grab id's
threshold = 0.5/0.00000001
long_edges = list(filter(lambda e: e[2] < threshold, (e for e in H.edges.data('weight'))))
le_ids = list(e[:2] for e in long_edges)
# remove filtered edges from graph
H.remove_edges_from(le_ids)

edges = H.edges()
weights = [(H[u][v]['weight'])*0.00000001 for u,v in edges]
w_scale = 10/np.log(max(weights))
weights = [np.log(item)*w_scale for item in weights]

#"width":0.1
options = {"node_color": color_map, "edge_color": '#808080', "node_size": size_map, "linewidths": 0.5, "width": weights,
           "with_labels": False, "arrowsize":4}

pos = nx.spring_layout(H, iterations=50, k=7000/math.sqrt(H.order()))
nx.draw(H, pos, **options)
ax = plt.gca()
ax.collections[0].set_edgecolor("#000000")

fgraph_path = "./pdf_contents_g/full_graph_" + request_id + ".png"
plt.savefig(fgraph_path, format="png", dpi=500)
#plt.show()
plt.clf()
#######################


#######################
# 7) REMOVE DATA
dir = "../fcl_data/btc_txs"
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = "../fcl_data/fcl_txs"
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))
#######################

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))