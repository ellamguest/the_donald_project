# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:02:49 2016

@author: emg
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

df = pd.read_csv('all_mods_archive_it.csv')

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