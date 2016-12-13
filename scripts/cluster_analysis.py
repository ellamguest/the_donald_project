# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 15:42:42 2016

@author: emg
"""
import pandas as pd
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hca

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/andy_output.csv', index_col=0)

# GET TIME CLUSTERS

def get_den(data):
        link = hca.linkage(data)
        return hca.dendrogram(link)

def get_fclusters(data, max_dist):
        fcluster = hca.fcluster(hca.linkage(data), max_d, criterion='distance')
        df = pd.DataFrame(columns = ['time','cluster'])
        df['time'], df['cluster'] = data.index, fcluster
        return df

max_d = 4
cdf = get_fclusters(df, max_d)
cdf.groupby('cluster')['cluster'].count()

cdf.plot(kind='bar')

# GET MOD CLUSTER
get_den(df.T)

max_d = 7
cdf = get_fclusters(df.T, max_d)
cdf.groupby('cluster')['cluster'].count()

cdf.plot(kind='bar')


# removing infrequent mods
mods = df.T.astype(int)
sums = mods.sum(axis=1)
nones = sums[sums == 0]
mods = mods[~mods.index.isin(nones.index)]