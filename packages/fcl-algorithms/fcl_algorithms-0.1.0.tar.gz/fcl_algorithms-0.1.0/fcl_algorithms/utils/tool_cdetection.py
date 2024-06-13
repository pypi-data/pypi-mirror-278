# This script will take the day's transaction graph and generate the communities.

import networkx as nx
from cdlib import algorithms
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class Community:
    def __init__(self, id, c_type, members):
        self.id = id
        self.type = c_type
        self.members = members


# ===================================
# 1) SET THE DATE TO GET
# ===================================

current_day = datetime.today() - timedelta(days=1)
curr_day_mill = current_day.timestamp() * 1000
curr_day_mill = str(curr_day_mill).split('.')[0]
date_curr = current_day.strftime('%d_%m_%Y')

#input_day = '2022-01-20'  #sys.argv[1] #
#date_curr = datetime.strptime(input_day, '%Y-%m-%d').strftime('%d_%m_%Y')

# ===================================
# 2) BUILD THE TX GRAPH
# ===================================
print("==================================================")
print("==================================================")
print(" STARTING TO BUILD THE TX GRAPH")
print("==================================================")
print("==================================================")

rawday_path = "../fcl_data/btc_tx_" + date_curr + ".csv"
day_frame = pd.read_csv(rawday_path)
day_frame.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']
# generate a list of nodes
nodes_in = day_frame["txSender"].values.tolist()
nodes_in = [str(item) for item in nodes_in]
nodes_out = day_frame["txReceiver"].values.tolist()
nodes_out = [str(item) for item in nodes_out]
nodes_all = nodes_in + nodes_out
cd_nodeList = np.unique(nodes_all)
nodeDict = {v: v for v in cd_nodeList}
# generate a list of edges
cd_edgeList = day_frame[["txSender", "txReceiver"]].values.tolist()
# generate the NetworkX graph with all transactions.
print("======> GOT THE DATA, BUILDING THE GRAPH")
G = nx.Graph()
G.add_nodes_from(cd_nodeList)
G.add_edges_from(cd_edgeList)
# Generate a small fake graph for testing
#G = nx.erdos_renyi_graph(500, 0.5, seed=123, directed=False)

# ===================================
# 3) FIND AND STORE COMMUNITIES
# ===================================
print("==================================================")
print("==================================================")
print(" FINDING AND STORING COMMUNITIES")
print("==================================================")
print("==================================================")
cd_communities = algorithms.louvain(G)

print("======> GOT THE PARTITION, STORING THE COMMUNITIES")

communities = {}
commune_num = 0
for commune in cd_communities.communities:
    if len(commune) >= 10:
        commune_num += 1
        commune_id = date_curr + "_" + str(commune_num)
        new_community = Community(commune_id, 0, commune)
        communities[commune_num] = new_community
        for node in commune:
            nodeDict[node] = commune_id

communitiesJ = [{'id': com.id, "type": com.type, "members": com.members} for key, com in communities.items()]

comm_path = "../fcl_data/comm_" + date_curr + ".txt"
with open(comm_path, "w") as write_file:
    json.dump(communitiesJ, write_file, indent=1)

# ===================================
# 4) REDUCE THE TX NETWORK
# ===================================
print("==================================================")
print("==================================================")
print(" REDUCING THE TRANSACTION NETWORK")
print("==================================================")
print("==================================================")

day_frame['sender_com'] = day_frame['txSender'].map(nodeDict)
day_frame['receiver_com'] = day_frame['txReceiver'].map(nodeDict)
day_frame = day_frame[['txTime', 'txHash', 'txFee', 'sender_com', 'receiver_com', 'txValue']]
comm_frame = day_frame[day_frame.sender_com != day_frame.receiver_com]
comNet_Path = "../fcl_data/comm_tx_" + date_curr + ".csv"
comm_frame.to_csv(comNet_Path, header=False, index=False)

# Opening JSON file
# with open(comm_path) as json_file:
#   load_data = json.load(json_file)
# print(load_data[1]["members"])

print("***************** SCRIPT COMPLETE ****************")


