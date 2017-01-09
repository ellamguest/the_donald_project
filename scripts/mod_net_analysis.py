# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 13:43:00 2017

@author: emg
"""

import pandas as pd
import numpy as np
import networkx as nx

data = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/all_mods_merged.csv', index_col=0)
df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/day_mod_matrix.csv',index_col=0)
df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/day_mod(10+days)_matrix.csv', index_col=0)
df = df.astype(int)
m = np.mat(df)
mat = m.T*m
x = pd.DataFrame(mat)
x.index, x.columns = df.columns, df.columns
x.to_csv('/Users/emg/Programmming/GitHub/the_donald_R/mod(10+days)_matrix_weighted.csv', index=False)



G=nx.from_numpy_matrix(mat)


# look at node attributes
cc = nx.connected_components(G)
sorted(nx.degree(G).values())
nx.clustering(G)
nx.degree(G,1)

nx.draw(G)
plt.savefig("basic_co-moderated_net.png")

# clustering coefficients:
cc = sorted(nx.clustering(G).values())
cc2 = sorted(nx.clustering(G2).values())


plt.plot(cc)
plt.ylabel('clustering coefficient')
plt.show()
