# This script will take an address or list of addresses and produce a json for website exaple graph

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
from datetime import datetime, timedelta
import json
import time

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

class Transx:
    def __init__(self, source, target):
        self.source = source
        self.target = target

class Node:
    def __init__(self, address, group):
        self.address = address
        self.group = group


########################
#      USER INPUTS
########################
input_day = '2022-01-17'  # sys.argv[1]
input_day = datetime.strptime(input_day, '%Y-%m-%d').strftime('%d_%m_%Y')
output_day = datetime.strptime(input_day, '%d_%m_%Y').strftime('%d/%m/%Y')
address_path = "../fcl_data/address_list.json" # sys.argv[2]
with open(address_path, 'r') as f:
  address_list = json.load(f)

request_id = 2  # sys.argv[3]

########################
#      USER INPUTS
########################

day_full = get_day_txs(input_day)

if len(address_list) == 1:
    ########################
    #   ONLY ONE ADDRESS
    ########################

    # get user and neighbour's graph.
    user_data = get_user_txs(day_full, address_list[0])

    # build the node list with type
    nodes = {}
    node_list = list(user_data.nodes)

    for address in node_list:
        node_group = 1
        if address in address_list:
            node_group = 2
        new_node = Node(address, node_group)
        nodes[new_node.address] = new_node

    # get the nodes list and save it.
    nodesJ = [{'id': node.address, "group": node.group} for key, node in nodes.items()]
    nodesJ_path = "../fcl_data/nodes_address.json"
    with open(nodesJ_path, "w") as write_file:
        json.dump(nodesJ, write_file, indent=1)

    # build the edge list
    edges = {}
    i = 0
    for e in user_data.edges:
        i += 1
        new_edge = Transx(e[0], e[1])
        edges[i] = new_edge

    # get the edge list and save it.
    edgesJ = [{'source': edge.source, "target": edge.target} for key, edge in edges.items()]
    edgesJ_path = "../fcl_data/edges_address.json"
    with open(edgesJ_path, "w") as write_file:
        json.dump(edgesJ, write_file, indent=1)

if len(address_list) > 1:

    # get community's graph.
    comm_graph = day_full.subgraph(address_list)

    # build the node list with type
    nodes = {}
    node_list = list(comm_graph.nodes)

    for address in node_list:
        node_group = 1
        if address in address_list:
            node_group = 2
        new_node = Node(address, node_group)
        nodes[new_node.address] = new_node

    # get the nodes list and save it.
    nodesJ = [{'id': node.address, "group": node.group} for key, node in nodes.items()]
    nodesJ_path = "../fcl_data/nodes_comm.json"
    with open(nodesJ_path, "w") as write_file:
        json.dump(nodesJ, write_file, indent=1)

    # build the edge list
    edges = {}
    i = 0
    for e in comm_graph.edges:
        i += 1
        new_edge = Transx(e[0], e[1])
        edges[i] = new_edge

    # get the edge list and save it.
    edgesJ = [{'source': edge.source, "target": edge.target} for key, edge in edges.items()]
    edgesJ_path = "../fcl_data/edges_comm.json"
    with open(edgesJ_path, "w") as write_file:
        json.dump(edgesJ, write_file, indent=1)