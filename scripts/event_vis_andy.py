7# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:02:49 2016

@author: emg
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import scipy as sp

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/all_mods_merged.csv', index_col=1)
#df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/all_mods_archive_it.csv', index_col=0)
#ap = df[df['permissions']=='+all']



subset = (df[['name', 'date', 'pubdate']].copy()
            .assign(
                date=lambda df: df['date'].pipe(pd.to_datetime).dt.normalize(),
                pubdate=lambda df: df['pubdate'].pipe(pd.to_datetime).dt.normalize()))

subset = subset.sort_values(['name','date'])

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

output.to_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/day_mod_matrix.csv')

output = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/day_mod_matrix.csv', index_col=0)
output.index = pd.to_datetime(output.index)

#GET SUBSET OF MODS PRESENT FOR AT LEAST 1 WHOLE WEEK?
weeks = output.resample('W').last()
s = weeks.sum()
s = s[s>0]
weeks = weeks[s.index]

  
cg = sns.clustermap(weeks.T, row_cluster=True)
#plt.yticks(rotation=0)
plt.gcf().set_size_inches(12, 24)



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



