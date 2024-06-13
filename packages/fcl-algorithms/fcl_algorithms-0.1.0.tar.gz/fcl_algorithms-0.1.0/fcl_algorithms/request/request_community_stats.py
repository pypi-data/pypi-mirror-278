# This script will take the desired date and community rank.
# Then produce all the necessary analysis and statistics to build the report.

# Outputs:
# Summary: Take the summary statistics of the community.
# Wallets: Take note of wallets that are known using the type and other key ones, take their stats.
# Graphs: Community and global level graphs with different colours for type.

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

comm_name = sys.argv[2]                    # "1"
date = sys.argv[1]                          # "yyyy-mm-dd"
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
    subprocess.call(['python', 'routine_data.py', date_target])

program_list = ['routine_wallet.py', 'routine_wallet_type.py',
                'routine_community.py', 'routine_community_type.py', 'routine_community_reduce.py']
for program in program_list:
    subprocess.call(['python', program, target_date])
    print("Finished: " + program)
#######################


#######################
#   2) COMMUNITY STATS
# Load the walllet level network
rawday_path = file_location + "fcl_txs/wallet_tx_" + target_date + ".csv"
day_frame_w = pd.read_csv(rawday_path)
day_frame_w.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']

try:
  this = int(comm_name)
except:
  quit()

nodes_in = day_frame_w["txSender"].values.tolist()
nodes_in = [str(item) for item in nodes_in]
nodes_out = day_frame_w["txReceiver"].values.tolist()
nodes_out = [str(item) for item in nodes_out]
nodes_all = nodes_in + nodes_out
wall_nodeList = np.unique(nodes_all)
wall_edgeList = day_frame_w[["txSender", "txReceiver", "txValue"]].values.tolist()

G = nx.DiGraph()
G.add_nodes_from(wall_nodeList)
G.add_weighted_edges_from(wall_edgeList)

comm_path = file_location + "fcl_txs/comm_" + target_date + ".txt"
with open(comm_path) as json_file:
    communities = json.load(json_file)

####### Check that the community requested is here, otherwise change it.
maxim = len(communities)
this = int(comm_name)
if this > maxim:
    comm_name = str(maxim-1)



i = 0
for cluster in communities:
    i += 1
    id = cluster["id"][11:]
    if id == comm_name:
        commune = cluster["members"]
        comm_type = cluster["type"]
        comm_rank = str(i)

        S = G.subgraph(commune)
        comm_size = S.order()
        comm_vol_with = str(round(S.size(weight="weight")*0.00000001, 4))
        comm_link_with = S.size()

#######################


#######################
#   3) KEY WALLETS
# Reading the data from the file
types_path = file_location + "fcl_txs/types_" + target_date + ".json"
types_dict = json.load(open(types_path))

wallet_path = file_location + "fcl_txs/wallets_" + target_date + ".json"
wallet_dict = json.load(open(wallet_path))

key_wallets = []
key_types = []
key_size = []
key_vol_in = []
key_vol_out = []

for node in S:
    wallet_type = types_dict[node]
    if wallet_type != 0:
        key_wallets.append(node)
        key_types.append(str(wallet_type))
        key_vol_in.append(str(round((S.in_degree(node, weight="weight"))*0.00000001, 4)))
        key_vol_out.append(str(round((S.out_degree(node, weight="weight"))*0.00000001, 4)))
        # Find how many other addresses have the same parent
        parent = wallet_dict[node]
        wallet_size = 0
        for address in wallet_dict:
            if wallet_dict[address] == parent:
                wallet_size += 1
        key_size.append(str(wallet_size))

if len(key_wallets) < 12:
    needed = 12 - len(key_wallets)
    wall_full_out = list(S.out_degree(weight="weight"))
    wall_full_in = list(S.in_degree(weight="weight"))
    wall_full_out.sort(key=lambda a: a[1], reverse=True)
    wall_full_in.sort(key=lambda a: a[1], reverse=True)
    wallet_full_out_stat = [x[0] for x in wall_full_out[:10]]
    wallet_full_in_stat = [x[0] for x in wall_full_in[:10]]

    wallets_key = wallet_full_out_stat + wallet_full_in_stat
    wallets_key = list(set(wallets_key))
    wallets_key = wallets_key[:needed]
    for key in wallets_key:
        key_wallets.append(key)
        key_types.append(str(types_dict[key]))
        key_vol_in.append(str(round((S.in_degree(key, weight="weight"))*0.00000001, 4)))
        key_vol_out.append(str(round((S.out_degree(key, weight="weight"))*0.00000001, 4)))
        # Find how many other addresses have the same parent
        parent = wallet_dict[key]
        wallet_size = 0
        for address in wallet_dict:
            if wallet_dict[address] == parent:
                wallet_size += 1
        key_size.append(str(wallet_size))

key_wallets = key_wallets[:11]
key_types = key_types[:11]
key_size = key_size[:11]
key_vol_in = key_vol_in[:11]
key_vol_out = key_vol_out[:11]
#######################


#######################
#   4) FULL LEVEL
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

comm_vol_in = str(round((H.in_degree(comm_rank, weight="weight"))*0.00000001, 4))
comm_vol_out = str(round((H.out_degree(comm_rank, weight="weight"))*0.00000001, 4))
comm_link_in = str(H.in_degree(comm_rank))
comm_link_out = str(H.out_degree(comm_rank))
#######################

################################
# 5) CLEAN AND EXPORT STATS
stats_dic = {'date': target_date,
             'comm_name': comm_name,
             'comm_rank': comm_rank,
             'comm_type': comm_type,
             'comm_size': comm_size,
             'comm_link_with': comm_link_with,
             'comm_vol_with': comm_vol_with,
             'comm_vol_in': comm_vol_in,
             'comm_vol_out': comm_vol_out,
             'comm_link_in': comm_link_in,
             'comm_link_out': comm_link_out,
             'key_wallets': key_wallets,
             'key_types': key_types,
             'key_size': key_size,
             'key_vol_in': key_vol_in,
             'key_vol_out': key_vol_out
             }

outward_path = "./pdf_contents_c/comm_text_" + request_id + ".txt"
with open(outward_path, 'w') as file:
     file.write(json.dumps(stats_dic)) # use `json.loads` to do the reverse
#######################

#######################
# 6) COMMUNITY VISUALS
#{0:"Unknown", 1:"Miners", 2:"Exchanges", 3:"Black Market", 4:"Origin", 5:"State Backed Illicit", 6:"Scams and Ransomware"}
type_translate = {0:"#4F4F4F", 1:"#FFD166", 2:"#EF476F", 3:"#118AB2", 4:"#F5A623",
                  5:"#BD10E0", 6:"#06D6A0"}
W = nx.Graph(S)
# filter out all edges below threshold and grab id's
threshold = 0.5 / 0.00000001
long_edges = list(filter(lambda e: e[2] < threshold, (e for e in W.edges.data('weight'))))
le_ids = list(e[:2] for e in long_edges)
for link in le_ids:
    if link[0] in key_wallets:
        le_ids.remove(link)
    elif link[1] in key_wallets:
        le_ids.remove(link)

# remove filtered edges from graph
W.remove_edges_from(le_ids)
W.remove_nodes_from(list(nx.isolates(W)))

color_map = []
size_map = []
i = 0
for node in W:
    c_type = type_translate[types_dict[node]]
    color_map.append(c_type)
    if node in key_wallets:
        size_map.append(50)
    else:
        size_map.append(15)
    i += 1

edges = W.edges()
weights = [(W[u][v]['weight'])*0.00000001 for u,v in edges]
w_scale = 10/np.log(max(weights))
weights = [np.log(item)*w_scale for item in weights]

# "width":0.1
options = {"node_color": color_map, "edge_color": '#808080', "node_size": size_map, "linewidths": 0.5,
           "width": weights,
           "with_labels": False, "arrowsize": 4}

pos = nx.spring_layout(W, iterations=50, k=7000 / math.sqrt(H.order()))
nx.draw(W, pos, **options)
ax = plt.gca()
ax.collections[0].set_edgecolor("#000000")
cgraph_path = "./pdf_contents_c/comm_graph_" + request_id + ".png"
plt.savefig(cgraph_path, format="png", dpi=200)
# plt.show()
plt.clf()
#######################


#######################
# 7) GLOBAL VISUALS
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
        if node == str(comm_rank):
            c_type = "#Ff0000"
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

options = {"node_color": color_map, "edge_color": '#808080', "node_size": size_map, "linewidths": 0.5, "width": weights,
           "with_labels": False, "arrowsize":4}

pos = nx.spring_layout(H, iterations=50, k=7000/math.sqrt(H.order()))
nx.draw(H, pos, **options)
ax = plt.gca()
ax.collections[0].set_edgecolor("#000000")

fgraph_path = "./pdf_contents_c/full_graph_" + request_id + ".png"
plt.savefig(fgraph_path, format="png", dpi=500)
#plt.show()
plt.clf()
#######################

#######################
# 8) REMOVE DATA
dir = "../fcl_data/btc_txs"
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = "../fcl_data/fcl_txs"
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))
#######################


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))