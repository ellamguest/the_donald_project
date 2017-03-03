#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 10:59:57 2017

@author: emg
"""
import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

edgelist = pd.read_csv('/Users/emg/Programmming/GitHub/R-mod-nets/t_d/data/edgelist.csv')
edgelist = edgelist[edgelist.groupby('sub').sub.transform(len) > 1] #limiting to subs co-modded by at least 2 t_d mods
edges = zip(edgelist['mod'],edgelist['sub'])



# get only subs shared by atleast two mods
counts = edgelist.groupby('sub')['sub'].count()
shared_subs = list(counts[counts>1].index)


G = nx.from_edgelist(edges)

nodelist = pd.read_csv('/Users/emg/Programmming/GitHub/R-mod-nets/t_d/data/nodelist.csv', index_col=0)
kept = G.nodes()
nodelist = nodelist[nodelist.index.isin(kept)]
node_modes = {} # 0 = mod, 1 = sub
for node in nodelist.index:
    node_modes[node] = nodelist.loc[node]['mode']
modes = nodelist['mode']

nx.set_node_attributes(G, 'mode', node_modes)

pos = nx.fruchterman_reingold_layout_layout(G)

nx.draw_networkx(G, pos=pos, arrows=False, with_labels=False,
                 node_size=30, node_color=modes, alpha=0.5)





B = nx.Graph()
B.add_nodes_from(list(set(edgelist['mod'])), bipartite=0)
B.add_nodes_from(list(set(edgelist['sub'])), bipartite=1)
B.add_edges_from(edges)

pos = nx.fruchterman_reingold_layout_layout(B)

nx.draw_networkx(B, pos=pos, arrows=False, with_labels=False,
                 node_size=30, node_color=modes, alpha=0.5)



