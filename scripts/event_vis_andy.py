7# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:02:49 2016

@author: emg
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import scipy as sp

df = pd.read_csv('/Users/emg/Programming/GitHub/the_donald_project/raw_data/all_mods_merged.csv', index_col=1)

df = pd.read_csv('/Users/emg/Programming/GitHub/cmv/tidy_data/dated_mod_df.csv', index_col=0)
df['date'] = pd.to_datetime(df['date'])
df['pubdate'] = df['pubdate'].astype(str)
df['pubdate'] = df['pubdate'].apply(lambda t:'{}/{}/{}'.format(t[:4],t[4:6],t[6:8]))
df['pubdate'] = pd.to_datetime(df['pubdate'])

def weekly_mod_timeline(df):
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
                    .isnull())
    
    not_seen_old = (subset_old
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
    weeks = output.resample('W').last()
    return weeks

weeks = weekly_mod_timeline(df)
weeks.head()

output.to_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/day_mod_matrix.csv')

output = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/day_mod_matrix.csv', index_col=0)
output.index = pd.to_datetime(output.index)

#GET SUBSET OF MODS PRESENT FOR AT LEAST 1 WHOLE WEEK?
weeks = output.resample('W').last()
s = weeks.sum()
s = s[s>0]
weeks = weeks[s.index]

cg = sns.clustermap(weeks.T, col_cluster=False , figsize=(9,13))
plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
cg.ax_heatmap.set_title('Timeline of Moderator Presence', fontsize=20)
cg.ax_heatmap.set_ylabel('Moderator', fontsize=15)
cg.ax_heatmap.set_xlabel('Date (in weeks)', fontsize=15)


