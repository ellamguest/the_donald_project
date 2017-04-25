# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 16:47:04 2016

@author: emg
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

def make_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_ais_snapshots():
    source = 'https://archive.is/https://www.reddit.com/r/The_Donald/about/moderators'
    r = requests.get(source)
    soup = BeautifulSoup(r.text, "html5lib")
    snaps = soup.findAll('img', {'alt':"screenshot of https://www.reddit.com/r/The_Donald/about/moderators"})
    
    urls = []
    for snap in snaps:
        url = snap.parent['href']
        urls.append(url)
    return urls  

def ais_snapshot_df(url):
    soup = make_soup(url)
    mods = soup.findAll('input', {'value':'moderator'})
    
    d = {}
    for mod in mods:
        name = mod.parent.findAll('input', {'name':'name'})[0]['value']
        date = mod.parent.parent.parent.parent.time['title']
        permissions = mod.parent.findAll('input', {'name':'permissions'})[0]['value']
        karma = mod.parent.parent.parent.parent.b.text
        d[name] = [date, permissions, karma]  
    
    df = pd.DataFrame.from_dict(d, orient="index")
    df['pubdate'] = soup.findAll('time')[0].text
    return df 

def compile_ais_snapshots(urls):
    dfs = []
    for url in urls:
        dfs.append(ais_snapshot_df(url))
    
    df = pd.concat(dfs)
    df.reset_index(inplace=True)
    df.columns = ['name', 'date','permissions','karma','pubdate']   
    df['date'] = pd.to_datetime(df['date'])
    df['pubdate'] = pd.to_datetime(df['pubdate'])
    return df

urls = get_ais_snapshots()
df = compile_ais_snapshots(urls)
   
df.to_csv('/Users/emg/Programming/GitHub/the_donald_project/raw_data/td-is-snaps-100417.csv')


wbm = pd.read_csv('/Users/emg/Programming/GitHub/the_donald_project/raw_data/td-wbm-snaps-100417.csv', index_col=0)
ais = pd.read_csv('/Users/emg/Programming/GitHub/the_donald_project/raw_data/td-is-snaps-100417.csv', index_col=0)

df = pd.concat([wbm,ais])
df.sort_values('date', inplace=True)
df.reset_index(drop=True, inplace=True)

df.to_csv('/Users/emg/Programming/GitHub/subreddit-visuals/tidy_data/mods/td-mod-hist.csv')
