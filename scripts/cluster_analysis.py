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
weeks = df.resample('W').mean()


# GET TIME PERIOD CLUSTERS
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
cdf.set_index('unit', drop=True, inplace=True)
del cdf.index.name

cdf.groupby('cluster')['cluster'].count()

cdf.plot(kind='bar', x=weeks.index.date)

cdf.to_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/time_clusters.csv')



#CLUSTERMAP OF TIMES W/ MODS ORGANISED BY CLUSTER
df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/day_mod(10+days)_matrix.csv', index_col=0)
df.index = pd.to_datetime(df.index)
mods = df.resample('W').mean().T
mods.columns = mods.columns.date

cg = sns.clustermap(mods, col_cluster=False , figsize=(9,13))
plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
cg.ax_heatmap.set_title('Timeline of Moderator Presence', fontsize=20)
cg.ax_heatmap.set_ylabel('Moderator', fontsize=15)
cg.ax_heatmap.set_xlabel('Date (in weeks)', fontsize=15)



