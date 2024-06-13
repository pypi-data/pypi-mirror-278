# This python file will take the entire transaction network for a day and generate the communities.
# It will then store the resulting split in a seperate file.

import networkx as nx
from cdlib import algorithms
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import csv
import sys
import matplotlib.pyplot as plt


class Community:
    def __init__(self, id, c_type, members):
        self.id = id
        self.type = c_type
        self.members = members


# Decide what location we want to use
file_location = "../fcl_data/"
#file_location = "/Volumes/DingosDiner/fcl_data/"
# ===================================
# 1) SET THE DATE TO GET AND ITER
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

#input_day = '2022-01-20'  #sys.argv[1] #
#date_curr = datetime.strptime(input_day, '%Y-%m-%d').strftime('%d_%m_%Y')

while current_day < lim_day:
    curr_day_mill = current_day.timestamp() * 1000
    curr_day_mill = str(curr_day_mill).split('.')[0]
    date_curr = current_day.strftime('%d_%m_%Y')
    print(date_curr)

    # ===================================
    # 2) BUILD THE TX GRAPH
    # ===================================
    print("==================================================")
    print("==================================================")
    print(" STARTING TO BUILD THE TX GRAPH FOR " + date_curr)
    print("==================================================")
    print("==================================================")

    rawday_path = file_location + "fcl_txs/wallet_tx_" + date_curr + ".csv"
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

    # ===================================
    # 3) GETTING THE SUMMARY STATS
    # ===================================
    print("==================================================")
    print("==================================================")
    print(" GETTING THE DAILY STATS")
    print("==================================================")
    print("==================================================")

    # Number of transactions
    transactions = day_frame["txHash"].values.tolist()
    number_tx = len(np.unique(transactions))
    print("1) The total number of transactions: " + str(number_tx))
    # Number of links
    number_links = G.size()
    print("3) The total number of links: " + str(number_links))
    # Number of nodes
    number_nodes = G.order()
    print("4) The total number of nodes: " + str(number_nodes))
    # Number of components
    number_comp = nx.number_connected_components(G)
    print("5) The total number of connected components: " + str(number_comp))
    # Density
    number_dense = (2*number_links)/(number_nodes*(number_nodes-1))
    print("6) The graph density: " + str(number_dense))
    # Degree histogram
    hist_deg = nx.degree_histogram(G)
    hist_deg = hist_deg[:500]

    # ===================================
    # 4) FIND AND ANALYSING COMMUNITIES
    # ===================================
    print("==================================================")
    print("==================================================")
    print(" FINDING AND ANALYSING COMMUNITIES")
    print("==================================================")
    print("==================================================")
    cd_communities = algorithms.louvain(G)

    print("======> GOT THE PARTITION, STORING THE COMMUNITIES")

    communities = {}
    commune_num = 0
    comms_data = []
    for commune in cd_communities.communities:
        if len(commune) >= 100:
            commune_num += 1
            commune_id = date_curr + "_" + str(commune_num)
            new_community = Community(commune_id, 0, commune)
            communities[commune_num] = new_community
            for node in commune:
                nodeDict[node] = commune_id
            # COMMUNITY STATS
            S = G.subgraph(commune)     # Build the subgraph
            sub_links = S.size()  # Number of links
            sub_nodes = len(commune)  # Number of nodes
            #sub_tris = sum(nx.triangles(S).values()) / 3  # Number of triangles
            sub_deg = nx.degree_histogram(S)
            sub_deg = sub_deg[:500]  # Histogram for Degree distribution
            if nx.is_connected(S):
                sub_con = 1
            else:
                sub_con = 0
            sub_cent = nx.eigenvector_centrality_numpy(S)
            sub_cv = list(sub_cent.values())
            bins = np.linspace(0, 1, num=101)
            sub_chist = np.histogram(sub_cv, bins=bins)
            sub_chist = sub_chist[0]
            com_stats = [commune_id, sub_nodes, sub_links, sub_con, sub_deg, sub_chist]
            comms_data.append(com_stats)

    com_df = pd.DataFrame(comms_data, columns=["i", "sub_nodes", "sub_links", "sub_con", "sub_deg", "sub_chist"])
    comstats_path = file_location + "fcl_txs/comstats_" + date_curr + ".txt"
    com_df.to_csv(comstats_path, index=False)

    # ===================================
    # 5) STORING THE COMMUNITIES
    # ===================================
    print("==================================================")
    print("==================================================")
    print("STORING THE COMMUNITIES")
    print("==================================================")
    print("==================================================")

    communitiesJ = [{'id': com.id, "type": com.type, "members": com.members} for key, com in communities.items()]

    comm_path = file_location + "fcl_txs/comm_" + date_curr + ".txt"
    with open(comm_path, "w") as write_file:
        json.dump(communitiesJ, write_file, indent=1)


    # ===================================
    # 5) STORING THE SUMMARY STATS
    # ===================================
    print("==================================================")
    print("==================================================")
    print("STORING THE SUMMARY STATS")
    print("==================================================")
    print("==================================================")

    # List to store data
    day_stats = [date_curr, number_tx, number_links, number_nodes, number_comp, number_dense, commune_num, hist_deg]
    day_stats_path = file_location + "summary_stats/day_stats.csv"
    with open(day_stats_path, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(day_stats)

    print(" COMPLETED ANALYSIS FOR " + date_curr)
    current_day = current_day + timedelta(days=1)


print("***************** SCRIPT COMPLETE ****************")