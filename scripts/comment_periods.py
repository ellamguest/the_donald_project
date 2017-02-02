# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 14:37:53 2017

@author: emg
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# use cluster_analysis.py to produce clustering df (cdf)

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/all_mods_merged.csv', index_col=1)
cdf = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/time_clusters.csv', index_col=0)
cdf.index = pd.to_datetime(cdf.index)
cdf.plot(kind='bar', x=cdf.index.date)

begins = cdf.groupby('cluster').head(1).reset_index()
begins.columns = ['begins','cluster']
ends = cdf.groupby('cluster').tail(1).reset_index()
ends.columns = ['ends','cluster']

periods = pd.merge(begins,ends)
periods = periods[['begins','ends','cluster']]

url = 'https://www.reddit.com/r/help/search?q=timestamp:1458432000..1461456000&sort=top&restrict_sr=on&syntax=cloudsearch'

lowers = []
for x in periods['begins']:
    lowers.append(str(x.value)[:-9])
periods['lower'] = lowers

uppers = []
for x in periods['ends']:
    uppers.append(str(x.value)[:-9])
periods['upper'] = uppers

periods['range'] = periods['lower'] + '..' + periods['upper']

periods['url'] = periods['range'].map(lambda x:"""https://www.reddit.com/r/the_donald/
                search?q=timestamp:{}&sort=top&restrict_sr=on&syntax=cloudsearch""".format(x))

