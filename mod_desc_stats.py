# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 14:01:12 2016

@author: emg
"""

import pandas as pd
import numpy as np

df = pd.read_csv('all_mods_archive_it.csv')

# mod consistency

counts = df.groupby('name')['name'].count()
counts.sort_values(ascending=False, inplace=True)

singles = counts[counts==1] #4
counts.plot(kind='hist', cumulative=True)

# mod list sizes

list_sizes = df.groupby('pubdate')['pubdate'].count().sort_values(ascending=False)

perm_freq = df.groupby('permissions')['permissions'].count().sort_values(ascending=False)

# attempting gantt chart like timeline of mod instances by mod

samp = df.sample(100)
names = samp.name.unique()
timepoints = pd.to_datetime(samp.pubdate).unique()
timepoints.sort()

import matplotlib.pyplot as pl
xticks = timepoints
x = [i for i in range(len(timepoints))]
y = x = [i for i in range(len(names))]
pl.plot(x,y)
pl.xticks(x,xticks, rotation=90)
pl.show()

def create_index_dictionary(array):
    d = {}
    for item in array:
        d[item] = np.where(array==item)[0][0]
    return d

times = df.pubdate.unique()
times.sort()
time_dict = create_index_dictionary(times)
df['timepoint'] = df['pubdate'].map(time_dict)

# to order mods alphabetically
names = df.name.unique()
names.sort()
name_dict = create_index_dictionary(names)
df['mod_alpha'] = df['name'].map(name_dict)

df.plot(x='timepoint',y='mod_alpha', kind='scatter', title='mod presence at timepoint')


# to order mods by most frequent, in ascending order (0 = least freq)
df['count'] = df.groupby(['name'])['name'].transform('count')
rank = counts.rank(method='first')
df['freq_rank'] = df['name'].map(rank)
df.plot(x='timepoint',y='freq_rank', kind='scatter', title='mod presence at timepoint')

# looking at two-mode mods by timepoints
df['value']=1
mxt = df.pivot(index='rank',columns='timepoint', values='value').fillna(0)



# looking at karma variation
min_karma = df.groupby('name')['postkarma'].min()
max_karma = df.groupby('name')['postkarma'].max()
mean_karma = df.groupby('name')['postkarma'].mean()
karma_diff = max_karma - min_karma
counts = df.groupby('name')['name'].count()