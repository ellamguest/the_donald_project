# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:44:49 2016

"""
"""NOT PULLING FROM WBM BUT CURRENT""""
import pandas as pd
import requests

url = 'http://web.archive.org/web/20161130144405/https://www.reddit.com/r/The_Donald/.json'
headers={'User-agent':'why_ask_reddit bot 0.1'}
url2 = 'https://www.reddit.com/r/The_Donald/.json'

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
    

mods = 'https://www.reddit.com/r/The_Donald/about/moderators/.json'
response2 = requests.get(mods, headers=headers)
data2 = response2.json()

# currently 5 mods, non more than 1 month old

cols2 = data2['data']['children'][0].keys()
df2 = pd.DataFrame(columns=cols2)

for i in range(len(data2['data']['children'])):
    x = data2['data']['children'][i]
    info = []
    for key in x.keys():
        info.append(x[str(key)])
    df2.loc[i] = info
df2['datetime'] = pd.to_datetime(df2.date, unit='s')


