import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import glob

class TaggedAddress:
    def __init__(self, id, c_type, description):
        self.id = id
        self.type = c_type
        self.description = description

########################################
# 1) Load the existing tags
########################################

comm_path = "../fcl_data/tags/tagged_db_3.txt"
with open(comm_path) as json_file:
    old_tags = json.load(json_file)

tags_dic = {}
for tag in old_tags:
    new_tag = TaggedAddress(tag["id"], tag["type"], tag["description"])
    tags_dic[tag["id"]] = new_tag

########################################
# 2) Load  and add the new tags
########################################

# USING A CSV WITH ALL THE DATA

this_path = "../fcl_data/reported_origin.csv"

data = pd.read_csv(this_path, sep= ";")
df = pd.DataFrame(data)
df = df.reset_index()  # make sure indexes pair with number of rows
for index, row in df.iterrows():
    tag_id = row['Address']
    new_tag = TaggedAddress(tag_id, row['Type'], row['Description'])
    tags_dic[tag_id] = new_tag


# USING A CSV WITH ONLY ADDRESSES FOR A GIVEN AGENT.

#this_path = "/Users/diegolara/devel/project_fcl/fcl_data/reported_illicit.csv"
#this_desc = "AgoraMarket. A darknet marketplace."
#this_type = 3


#db_known = pd.concat(
#    [pd.read_csv(f, header=None) for f in glob.glob(this_path)],
#    ignore_index=True)
#db_known = set(db_known[0])
#
#for tag in db_known:
#    new_tag = TaggedAddress(tag, this_type, this_desc)
#    tags_dic[tag] = new_tag
#
########################################
# 3) Store the modified version.
########################################

tagsJ = [{'id': tg.id, "type": tg.type, "description": tg.description} for key, tg in tags_dic.items()]
comm_path = "../fcl_data/tags/tagged_db_3.txt"
with open(comm_path, "w") as write_file:
    json.dump(tagsJ, write_file, indent=1)

print("Completed the update.")
