# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 10:11:46 2016

@author: emg
"""

import pandas as pd
import requests


url = 'https://www.reddit.com/r/The_Donald/about/moderators.json'
headers={'User-agent':'why_ask_reddit bot 0.1'}

response = requests.get(url, headers=headers)
data = response.json()

cols = data['data']['children'][0]['data'].keys()
df = pd.DataFrame(columns=cols)

for i in range(len(data['data']['children'])):
    x = data['data']['children'][i]['data']
    info = []
    for key in x.keys():
        info.append(x[str(key)])
    df.loc[i] = info
df['datetime'] = pd.to_datetime(df.created, unit='s')