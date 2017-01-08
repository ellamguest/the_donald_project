# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 15:56:41 2017

@author: emg
"""

import pandas as pd
import requests

headers={'User-agent':'wednesdaysguest bot 0.1'}

def pull_page(url):
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

#sidebar = pull_page('https://www.reddit.com/r/The_Donald/wiki/config/sidebar.json')
#about = pull_page('https://www.reddit.com/r/The_Donald/about.json')
#submit_text = about['data']['submit_text']
#public_desc = about['data']['public_description']
#desc = about['data']['description']
# wiki_pages = 'https://www.reddit.com/r/The_Donald/wiki/pages'
revisions = pull_page('https://www.reddit.com/r/The_Donald/wiki/revisions/index.json?limit=100')

columns=['time','reason','page','author','created_utc','hidden','l_karma','c_karma','gold','mod','email']
df = pd.DataFrame(columns=columns)

for i in range(len(revisions['data']['children'])):
    print i
    x = revisions['data']['children'][i]
    time = x['timestamp']
    reason = x['reason']
    page = x['page']
    if x['author'] == None:
        info = [time,reason,page,None,None,None,None,None,None,None,None]
    else:
        author = x['author']['data']['name']
        created_utc = x['author']['data']['created_utc']
        hidden = x['author']['data']['hide_from_robots']
        l_karma = x['author']['data']['link_karma']
        c_karma = x['author']['data']['comment_karma']
        gold = x['author']['data']['is_gold']
        mod = x['author']['data']['is_mod']
        email = x['author']['data']['has_verified_email']
        info = [time,reason,page,author,created_utc,hidden,l_karma,c_karma,gold,mod,email]
    df.loc[i] = info

df['time'] = pd.to_datetime(df['time'], unit='s')
df = df.fillna(False)

df.to_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/wiki_revisions.csv')

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/wiki_revisions.csv', index_col=0)
