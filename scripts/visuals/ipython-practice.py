think#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 11:01:16 2017

@author: emg
"""

import csv
from igraph import *
import pandas as pd
import matplotlib.pyplot as plt

#run slim_edgelist to get df
df = pd.read_csv('/Users/emg/Programmming/GitHub/R-mod-nets/cmv/data/edgelist_shared2.csv')
edges = zip(df['mod'],df['sub'])
g = Graph.TupleList(edges)

df = pd.read_csv('/Users/emg/Programmming/GitHub/R-mod-nets/cmv/data/nodelist_shared2.csv', index_col=0)
order = g.vs['name']
df = df.reindex(order)
g.vs['type']=df['mode']


net <- graph_from_data_frame(d=edges, vertices=nodes)
net <- simplify(net, remove.loops = T)



plt(g)
communities = igraph.community_edge_betweenness()

dendrogram = graph.community_edge_betweenness()
# convert it into a flat clustering
clusters = dendrogram.as_clustering()
# get the membership vector
membership = clusters.membership