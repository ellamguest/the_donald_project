# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 15:42:42 2016

@author: emg
"""
import pandas as pd
import seaborn as sns
import scipy.cluster.hierarchy as hca
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/day_mod(10+days)_matrix.csv', index_col=0)
df.index = pd.to_datetime(df.index)
#df = df.T


# GET TIME CLUSTERS
def get_den(data):
        link = hca.linkage(data)
        return hca.dendrogram(link)

def get_fclusters(data, max_dist):
        fcluster = hca.fcluster(hca.linkage(data), max_d, criterion='distance')
        df = pd.DataFrame(columns = ['unit','cluster'])
        df['unit'], df['cluster'] = data.index, fcluster
        return df

get_den(weeks)
max_d = 3
cdf = get_fclusters(weeks, max_d)
cdf.groupby('cluster')['cluster'].count()

cdf.plot(kind='bar')

weeks = df.resample('W').mean()
months = df.resample('m').sum()


# GET MOD CLUSTER
#mods = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/modxtime.csv', index_col=0)
mods = df.resample('W').mean().T
get_den(mods)

max_d = 2.3
cdf = get_fclusters(mods, max_d)
cdf.groupby('cluster')['cluster'].count()

cdf.sort_values('cluster', inplace=True)
cdf.plot(kind='bar')

cdf.set_index('unit', inplace=True)
mods['CLUSTER'] = cdf['cluster']
mods.sort_values('CLUSTER',inplace=True)

sns.clustermap(mods, col_cluster=False) #dates
sns.clustermap(mods, row_cluster=False) #mods

#CLUSTERMAP OF TIMES W/ MODS ORGANISED BY CLUSTER
cg = sns.clustermap(mods, col_cluster=False)
cg.ax
plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
plt.gcf().set_size_inches(10, 15)


