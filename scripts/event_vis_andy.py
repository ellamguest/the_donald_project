# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:02:49 2016

@author: emg
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import scipy as sp
import numpy as np

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/all_mods_archive_it.csv')

subset = (df[['name', 'date', 'pubdate']].copy()
            .assign(
                date=lambda df: df['date'].pipe(pd.to_datetime).dt.normalize(),
                pubdate=lambda df: df['pubdate'].pipe(pd.to_datetime).dt.normalize()))
seen = (subset
                .groupby(['date', 'name']).first()['pubdate']
                .unstack()
                .isnull()
                .pipe(lambda x: ~x)
                .resample('D').mean()
                .fillna(0)
                .astype(bool))

not_seen = (subset
                .groupby(['pubdate', 'name']).first()['date']
                .unstack()
                .isnull()
                .resample('D').pad())
    

output = {}
current = pd.Series(False, seen.columns)    
for d in seen.index & not_seen.index:
    joined, left = seen.loc[d], not_seen.loc[d]
    current[joined] = True
    current[left] = False
    output[d] = current.copy()
output = pd.concat(output, 1).T

    
cg = sns.clustermap(output.resample('W').last().iloc[:, :100], row_cluster=False)
#plt.yticks(rotation=0)
plt.gcf().set_size_inches(24, 12)



##### trying to get cluster from seaborn
sns.clustermap(output, row_cluster=False)# simplifying for bit
cluster_data = cg.dendrogram_col.linkage #99 x 4
den = sp.cluster.hierarchy.dendrogram(cluster_data, labels = output.index, color_threshold=0.60)
ids = sp.cluster.hierarchy.fcluster(cluster_data, 3.9, criterion='distance')


### trying to get clusters from twomode net
aff = output.astype(int)
adj = aff.T.dot(aff)
mat = aff.T
#np.fill_diagonal(mat.values, 0)

#### iding very brief mods
sums = adj.sum()
x = sums[sums == 0]


# using scipy hierarchical clustering
link_mat = sp.cluster.hierarchy.linkage(mat)
den = sp.cluster.hierarchy.dendrogram(link_mat, labels=mat.index)
max_d = 7

clusters = pd.DataFrame(adj.index)
clusters['cluster'] = sp.cluster.hierarchy.fcluster(link_mat, 7, criterion='distance')
clusters.sort('cluster')



