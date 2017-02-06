# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 16:09:14 2017

@author: emg
"""

import pandas as pd
import requests
import json

top_posts = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/period_top_posts.csv', thousands=',', index_col=0)

fullnames = { 't1':'comment',
             't2':'account',
             't3':'link',
             't4':'message',
             't5':'subreddit',
             't6':'award',
             't8':'promoCampaign'}
        
columns = [u'subreddit_id',
 u'banned_by',
 u'removal_reason',
 u'link_id',
 u'likes',
 u'replies',
 u'user_reports',
 u'saved',
 u'id',
 u'gilded',
 u'archived',
 u'report_reasons',
 u'author',
 u'parent_id',
 u'score',
 u'approved_by',
 u'controversiality',
 u'body',
 u'edited',
 u'author_flair_css_class',
 u'downs',
 u'body_html',
 u'subreddit',
 u'name',
 u'score_hidden',
 u'stickied',
 u'created',
 u'author_flair_text',
 u'created_utc',
 u'distinguished',
 u'mod_reports',
 u'num_reports',
 u'ups']

headers = {'user-agent': 'why_ask_reddit 1.0'}
 
sample = top_posts.sample(5)
top_posts['url'] = top_posts['url'].map(lambda x: x.split('?')[0] + '.json')


def get_comments(urls):
    dfs = []
    for url in urls:
        r = requests.get(url, headers=headers)
        data = r.json()
        
        comments = data[1]['data']['children'][:-1]
        df = pd.DataFrame(columns=columns)
    
        for i in range(len(comments)):
            info = []
            for x in columns:
                info.append(comments[i]['data'][x])
            df.loc[i] = info
        dfs.append(df)
    return dfs

dfs = get_comments(top_posts['url'])

all_comments = pd.concat(dfs)
all_comments['date'] = pd.to_datetime(all_comments['created'], unit='s')

all_comments.to_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/all_comments_top_posts.csv', encoding='utf-8')

