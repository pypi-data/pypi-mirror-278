# This is step 4 (of 4) in the operation.
# It runs when called and stores all the relevant data for the website.

import json
import csv
from datetime import datetime, timedelta


templateJustNodes = '{address}'
templateJustLinks = '{source},{target},{value}'



class Transx:
    def __init__(self, source, target, value):
        self.source = source
        self.target = target
        self.value = value

class Node:
    def __init__(self, address, community):
        self.address = address
        self.community = community


# Get the last day we have reduced.
last_day = datetime.strptime('01_01_2021', '%d_%m_%Y')  # This is the last day that is complete.
today = datetime.today() - timedelta(days=1)
lim_day = datetime.strptime('04_01_2021', '%d_%m_%Y')  # This is the last day missing.
current_day = last_day

while current_day < lim_day:
    current_day = current_day + timedelta(days=1)
    curr_day_mill = current_day.timestamp() * 1000
    curr_day_mill = str(curr_day_mill).split('.')[0]
    date_curr = current_day.strftime('%d_%m_%Y')
    print("The current day I am working on is: " + date_curr)

    day_path = "/Users/diegolara/PycharmProjects/play-btc-comsite/web_txs/comm_tx_" + date_curr + ".csv"
    with open(day_path, newline='') as f:
        reader = csv.reader(f)
        day_txs = list(reader)

    line_id = 0
    links = {}

    for link in day_txs:
        source = link[3]
        target = link[4]
        value = link[5]
        line = Transx(source, target, value)
        links[line_id] = line
        line_id += 1

    edges = [{'source': link.source, "target": link.target, "value": link.value} for key, link in links.items()]

    edge_path = "/Users/diegolara/PycharmProjects/play-btc-comsite/web_txs/edges_" + date_curr + ".json"
    with open(edge_path, "w") as write_file:
        json.dump(edges, write_file, indent=1)

    nodes = {}

    for key, link in links.items():
        try:
            comnum = link.source
            comnum = comnum.split(".", 1)
            comnum = int(comnum[0])
        except:
            comnum = 0
        new_node = Node(link.source, comnum)
        nodes[new_node.address] = new_node

    for key, link in links.items():
        try:
            comnum = link.target
            comnum = comnum.split(".", 1)
            comnum = int(comnum[0])
        except:
            comnum = 0
        new_node = Node(link.target, comnum)
        nodes[new_node.address] = new_node


    nodesJ = [{'id': node.address, "group": node.community} for key, node in nodes.items()]

    node_path = "/Users/diegolara/PycharmProjects/play-btc-comsite/web_txs/nodes_" + date_curr + ".json"
    with open(node_path, "w") as write_file:
        json.dump(nodesJ, write_file, indent=1)