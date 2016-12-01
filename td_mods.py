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

cols = data['data']['children'][0].keys()
df = pd.DataFrame(columns=cols)

for i in range(len(data['data']['children'])):
    x = data['data']['children'][i]
    info = []
    for key in x.keys():
        info.append(x[str(key)])
    df.loc[i] = info
df['datetime'] = pd.to_datetime(df.date, unit='s')
df.to_csv('1decmods.csv', index=True)


https://www.reddit.com/user/OhSnapYouGotServed.json



# trying to use memento api for archived data
http://timetravel.mementoweb.org/api/json/20161010/https://www.reddit.com/r/The_Donald/about/moderators