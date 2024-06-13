### THIS FILE CONTAINS THE CODE TO GENERATE THE CONTENT FOR A GENERAL REQUEST.


import networkx as nx
import pandas as pd
import numpy as np
import json
import csv
import sys
from datetime import datetime, timedelta

def get_day_txs(date):
    # get the file where the transactions for this day are stored
    day_path = "../fcl_data/btc_tx_" + date + ".csv"
    day_frame = pd.read_csv(day_path)
    day_frame.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']

    # generate a list of nodes
    nodes_in = day_frame["txSender"].values.tolist()
    nodes_in = [str(item) for item in nodes_in]
    nodes_out = day_frame["txReceiver"].values.tolist()
    nodes_out = [str(item) for item in nodes_out]
    nodes_all = nodes_in + nodes_out
    cd_nodelist = np.unique(nodes_all)

    # generate a list of edges
    cd_edgelist = day_frame[["txSender", "txReceiver"]].values.tolist()

    # generate the NetworkX graph
    day_graph = nx.Graph()
    day_graph.add_nodes_from(cd_nodelist)
    day_graph.add_edges_from(cd_edgelist)

    return day_graph

def get_comm_txs(date):
    # get the file where the transactions for this day are stored
    day_path = "../fcl_data/comm_tx_" + date + ".csv"
    day_frame = pd.read_csv(day_path)
    day_frame.columns = ['txTime', 'txHash', 'txFee', 'txSender', 'txReceiver', 'txValue']

    # generate a list of nodes
    nodes_in = day_frame["txSender"].values.tolist()
    nodes_in = [str(item) for item in nodes_in]
    nodes_out = day_frame["txReceiver"].values.tolist()
    nodes_out = [str(item) for item in nodes_out]
    nodes_all = nodes_in + nodes_out
    cd_nodelist = np.unique(nodes_all)

    # generate a list of edges
    cd_edgelist = day_frame[["txSender", "txReceiver"]].values.tolist()

    # generate the NetworkX graph
    day_graph = nx.Graph()
    day_graph.add_nodes_from(cd_nodelist)
    day_graph.add_edges_from(cd_edgelist)

    return day_graph


# ===================================
# 1) SET THE DATE TO GET
# ===================================

input_day = '2021-12-31' #sys.argv[1]
input_day = datetime.strptime(input_day, '%Y-%m-%d').strftime('%d_%m_%Y')
output_day = datetime.strptime(input_day, '%d_%m_%Y').strftime('%d/%m/%Y')

# ===================================
# 2) WORK WITH FULL TX GRAPH
# ===================================
big_graph = get_day_txs(input_day)
# Get number of nodes and links
big_nodes = big_graph.order()
big_edges = big_graph.size()

# Get the top 10 active addresses.
degrees = big_graph.degree
degrees = sorted(degrees, key=lambda x: x[1], reverse=True)
degrees_top = degrees[0:10]
degrees_top = pd.DataFrame(degrees_top)
degrees_top.columns = ['Address', 'Degree']


# ===================================
# 3) WORK WITH TOP CLUSTERS
# ===================================

comm_path = "../fcl_data/comm_" + input_day + ".txt"
with open(comm_path) as json_file:
    communities = json.load(json_file)

comm_number = len(communities)

comm_top = pd.DataFrame(columns=['Community_id', 'Type', 'Size',
                                 'Most Links 1', 'Links 1','Most Links 2', 'Links 2', 'Most Links 3', 'Links 3'])
for cluster in communities[0:10]:
    comm_id = cluster['id']
    comm_type = cluster['type']
    comm_size = len(cluster['members'])
    # Build the subgraph and get info
    comm_graph = big_graph.subgraph(cluster['members'])
    comm_degrees = comm_graph.degree
    comm_degrees = sorted(comm_degrees, key=lambda x: x[1], reverse=True)
    comm_top1, comm_link1 = comm_degrees[0]
    comm_top2, comm_link2 = comm_degrees[1]
    comm_top3, comm_link3 = comm_degrees[2]

    comm_top.loc[comm_top.shape[0]] = [comm_id, comm_type, comm_size,
                                       comm_top1, comm_link1, comm_top2, comm_link2,comm_top3, comm_link3]


# ===================================
# 4) GENERATE THE COMMUNITY GRAPH
# ===================================
#comm_list = list(range(1,(comm_number+1)))
#comm_list = map(str, comm_list)

#comm_graph = get_comm_txs(input_day)
# Set the node colours for communities.
#color_map = []
#for node in comm_graph:
#    if node in comm_list:
#        color_map.append('#2a9d8f')
#    else:
#        color_map.append('#4c28d7')

#pos = nx.spring_layout(comm_graph)
#nx.draw(comm_graph, pos, node_color=color_map, edge_color='#f75566', width=2, edge_cmap=plt.cm.Blues,
#        with_labels=False)
#plot_path = "./pdf_contents_g/community_network.png"
#plt.savefig(plot_path)

# ===================================
# 5) STORE THE INFO FOR THE PDF
# ===================================

top_path = "./pdf_contents_g/top_degree.csv"
degrees_top.to_csv(top_path, index=False)

with open("./pdf_contents_g/info_text.txt", "w") as text_file:
    text_file.write("Number of addresses: %i \nNumber of links: %i \nNumber of communities >= 100 addresses: %i" %
                    (big_nodes, big_edges, comm_number))

comm_top_path = "./pdf_contents_g/top_comm.csv"
comm_top.to_csv(comm_top_path, index=False)

with open("./pdf_contents_g/general_text.txt", "w") as text_file:
    text_file.write("This document gives a summary of the Bitcoin transaction network on the %s."
                    "It also provides a summary of the top 10 communities, with their most linked addresses.\n"
                    "In more genwral, it also reports the ten addresses with most links that day."
                    % (output_day))


print("SCRIPT FINISHED")
