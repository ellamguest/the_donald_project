# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 16:40:43 2017

@author: emg
"""

import pandas as pd
import datetime

def load_sidebar_revisions():
    df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/sidebar_revisions.csv')
    return df

df = load_sidebar_revisions()
df.index = pd.to_datetime(df['time'].str[0:10])
del df.index.name


#mods = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/all_mods_merged.csv')

revs = mods[mods['name'].isin(authors)]

timeline = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/andy_output.csv', index_col=0)
timeline.index = timeline.index.to_datetime()


####RUN CLUSTER_ANALYSIS.PY TIME CLUSTERING TO GET CDF
first = cdf.groupby('cluster').first()['unit']
last = cdf.groupby('cluster').last()['unit']
clusters = cdf['cluster'].unique()
clusters.sort()
def revision_periods(row):
    return df[(df.index >= first[row]) & (df.index <= last[row])]
periods = pd.DataFrame({'cluster_num':clusters,'begin':first,'end':last})
del periods.index.name
periods['revisions'] = periods['cluster_num'].apply(revision_periods)


