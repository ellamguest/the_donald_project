# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 15:42:42 2016

@author: emg
"""
import pandas as pd
import seaborn as sns
import scipy.cluster.hierarchy as hca

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/andy_output.csv', index_col=0)
df.index = pd.to_datetime(df.index)
df = df.astype('bool')

# GET TIME CLUSTERS

def get_den(data):
        link = hca.linkage(data)
        return hca.dendrogram(link)
    
get_den(df)

def get_fclusters(data, max_dist):
        fcluster = hca.fcluster(hca.linkage(data), max_d, criterion='distance')
        df = pd.DataFrame(columns = ['unit','cluster'])
        df['unit'], df['cluster'] = data.index, fcluster
        return df

max_d = 3.5
cdf = get_fclusters(df, max_d)
cdf.groupby('cluster')['cluster'].count()

cdf.plot(kind='bar')

# GET MOD CLUSTER
#mods = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/modxtime.csv', index_col=0)
mods = df.T
get_den(mods)

max_d = 5
cdf = get_fclusters(mods, max_d)
cdf.groupby('cluster')['cluster'].count()

sns.clustermap(mods, col_cluster=False)

cdf.set_index('unit', inplace=True)
mods['CLUSTER'] = cdf['cluster']

cdf.sort_values('cluster', inplace=True)
cdf.plot(kind='bar')

