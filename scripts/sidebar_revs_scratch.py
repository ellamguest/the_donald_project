# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 16:40:43 2017

@author: emg
"""

import pandas as pd
import datetime
from sidebar_revisions import content_df


df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/sidebar_revisions.csv', index_col=0)
df.index = pd.to_datetime(df.index)

#mods = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/all_mods_merged.csv')
#revs = mods[mods['name'].isin(authors)]

#timeline = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/andy_output.csv', index_col=0)
#timeline.index = timeline.index.to_datetime()


####RUN CLUSTER_ANALYSIS.PY TIME CLUSTERING TO GET CDF
first = cdf.groupby('cluster').first()['unit']
last = cdf.groupby('cluster').last()['unit']
#clusters = cdf['cluster'].unique()
#clusters.sort()
#def revision_periods(row):
#    return df[(df.index >= first[row]) & (df.index <= last[row])]
#periods = pd.DataFrame({'cluster_num':clusters,'begin':first,'end':last})
#del periods.index.name
#periods['revisions'] = periods['cluster_num'].apply(revision_periods)
#
#cluster1text = periods['revisions'][1]
#
#contentdf = content_df()

subset1 = df[(df.index >= first[1]) & (df.index <= last[1])]


