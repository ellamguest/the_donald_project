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

# looking at instances per mod
dates = df.groupby('name')['date'].unique()
instances = pd.DataFrame(dates)
n = []
for x in dates:
    n.append(len(x))

instances['instances'] = n
instances['count'] = counts
instances['perm_types'] = df.groupby('name')['permissions'].unique()

n = []
for x in instances['perm_types']:
    n.append(len(x))

instances['perm_#'] = n

# looking at permission types
all_perm = df[df['permissions'] == '+all']
top_mods = all_perm['name'].unique()

def andy():
    import seaborn as sns
    import matplotlib.pyplot as plt    
    
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
    
    sns.clustermap(output.resample('W').last().iloc[:, :100], row_cluster=False)
    plt.gcf().set_size_inches(24, 12)