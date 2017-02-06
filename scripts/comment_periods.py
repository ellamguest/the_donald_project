# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 14:37:53 2017

@author: emg
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re

# use cluster_analysis.py to produce clustering df (cdf)

############## GET DATA
# use cluster_analysis.py to produce updated clustering df (cdf)
df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/all_mods_merged.csv', index_col=1)
cdf = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/time_clusters.csv', index_col=0)
cdf.index = pd.to_datetime(cdf.index)
cdf.plot(kind='bar', x=cdf.index.date)

begins = cdf.groupby('cluster').head(1).reset_index()
begins.columns = ['begins','cluster']
ends = cdf.groupby('cluster').tail(1).reset_index()
ends.columns = ['ends','cluster']

# getting exact time periods
periods = pd.merge(begins,ends)
periods['lower'] = [str(x.value)[:-9] for x in periods['begins']]
periods['upper'] = [str(x.value)[:-9] for x in periods['ends']]
periods['range'] = periods['lower'] + '..' + periods['upper']

# getting week window around beginning of time period
l_frame = periods['begins'].map(lambda x: x - timedelta(days=7))
periods['l_frame'] = [str(x.value)[:-9] for x in l_frame]
r_frame = periods['begins'].map(lambda x: x + timedelta(days=7))
periods['r_frame'] = [str(x.value)[:-9] for x in r_frame]
periods['window'] = periods['l_frame'] + '..' + periods['r_frame']
periods['url'] = periods['window'].map(lambda x:'https://www.reddit.com/r/the_donald/search?q=timestamp:{}&sort=top&restrict_sr=on&syntax=cloudsearch'.format(x))

################# PULL COMMENTS



from scraping_functions import *

##### GET ALL ARCHIVED COPIES from archive.it

def make_soup(url):
    headers = {'user-agent': 'why_ask_reddit 1.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html5lib")
    return soup

def get_top_posts(soup, i):
    '''soup is a BeautifulSoup object'''
    headers = soup.findAll("header", { "class" : "search-result-header" })
    titles = [x.a.text for x in headers]
    tags = soup.findAll("div", { "class" : "search-result-meta" })
    urls = [x.a['href'] for x in tags]
    dt = [x.time['datetime'] for x in tags]
    author = [x.find_all('span', {'class':'search-author'})[0].a['href'] for x in tags]
    score = [x.find('span', {'class':'search-score'}).text[:-7] for x in tags]
    start = periods['begins'][i]    
    top_posts = pd.DataFrame(data = {'title':titles,'date':dt,'url':urls,'author':author,'score':score, 'start':start})
    return top_posts
    
dfs = []
for i in periods.index:
    soup = make_soup(periods['url'][i])
    df = get_top_posts(soup, i)
    dfs.append(df)
    
top_posts = pd.concat(dfs)
top_posts.columns = ['rank', u'author', u'date', u'score', u'start', u'title', u'url']
top_posts['post_id'] = top_posts['url'].map(lambda x: x.split('/')[6])
top_posts.to_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/period_top_posts.csv', encoding='utf-8')

top_posts = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/period_top_posts.csv', thousands=',', index_col=0)


x = top_posts[['score','start','title']].sort_values('score', ascending= False)
    

