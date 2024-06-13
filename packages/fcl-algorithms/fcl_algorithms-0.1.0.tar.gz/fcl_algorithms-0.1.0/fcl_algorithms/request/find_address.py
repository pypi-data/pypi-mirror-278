### THIS FILE CONTAINS THE CODE TO RUN WHEN A REQUEST IS MADE ON A SPECIFIC ADDRESS

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

def get_user_txs(graph,address):

    #get all the neighbours
    nb_1 = list(graph.neighbors(address))

    nb_2 = []
    for i in nb_1:
        nb_2 = nb_2 + list(graph.neighbors(i))

    #nb_3 = []
    #for j in nb_2:
    #    nb_3 = nb_3 + list(graph.neighbors(j))

    nb_total = nb_1 + nb_2

    # get the user's subgraph
    user_graph = graph.subgraph(nb_total)

    return user_graph

def get_user_info(input_day,address, request_id):
    # get today's graph
    today_graph = get_day_txs(input_day)
    #print("got the full tx graph")

    #obtain the user info
    user_degree = today_graph.degree[address]
    nb_1 = list(today_graph.neighbors(address))
    user_num = len(nb_1)

    # get user graph
    user_graph = get_user_txs(today_graph, address)

    # Set the node colours for all nodes.
    color_map = []
    for node in user_graph:
        if node == address:
            color_map.append('#2a9d8f')
        else:
            color_map.append('#4c28d7')

    print("Starting the plot")

    n = len(color_map)
    pos = nx.spring_layout(user_graph, iterations=100, scale=3, weight=0.2)
    #pos = nx.nx_agraph.pygraphviz_layout(user_graph, prog="sfdp")

    nx.draw(user_graph, pos, node_size=2, node_color=color_map, edge_color='#f75566', width=0.1, edge_cmap=plt.cm.Blues,
            with_labels=False)
    plot_path = "./pdf_contents_a/address_network_" + request_id + ".png"
    plt.savefig(plot_path, dpi=1000)
    print("Ended the plot")

    user_info = [user_degree, user_num, nb_1]

    return user_info


########################
#      USER INPUTS
########################

input_day = '2022-01-20'  #sys.argv[1] #
input_day = datetime.strptime(input_day, '%Y-%m-%d').strftime('%d_%m_%Y')
output_day = datetime.strptime(input_day, '%d_%m_%Y').strftime('%d/%m/%Y')
address = '000000000000000000000000' #sys.argv[2]
request_id = "6" #sys.argv[3]

user_data = get_user_info(input_day, address, request_id)

#Store the user info in the .txt file

info_path = "./pdf_contents_a/info_text_" + request_id + ".txt"
with open(info_path, "w") as text_file:
    text_file.write("Number of links: %i \nNumber of direct neighbours: %i" % (int(user_data[0]), user_data[1]))

text_path = "./pdf_contents_a/address_text_" + request_id + ".txt"
with open(text_path, "w") as text_file:
    text_file.write("This document gives a summary of the address, %s, on the %s."
                    " It also provides a snapshot of its closest links, to show its closest structure.\n"
                    "In the future some features we will add would be community and wallet participation."
                    % (address, output_day))

