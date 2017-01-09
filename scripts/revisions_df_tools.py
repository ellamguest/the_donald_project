# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 12:25:07 2017

@author: emg
"""
import pandas as pd
import requests

headers={'User-agent':'whyaskreddit bot 0.1'}

def pull_page(url):
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def get_after(url):
    data = pull_page(url)
    after = data['data']['after']
    return after

def after_pages(url):
    urls = [url]
    after = get_after(url)
    while after != None:
        new = url + '?limit=100&after=' + after
        urls.append(new)
        after = get_after(new)    
    return urls

def get_revisions_df(url):
    revisions = pull_page(url)
    columns=['time','reason','page','url_id','author','created_utc','hidden','l_karma','c_karma','gold','mod','email']
    df = pd.DataFrame(columns=columns)
    for i in range(len(revisions['data']['children'])):
        print i
        x = revisions['data']['children'][i]
        time = x['timestamp']
        reason = x['reason']
        page = x['page']
        url_id = x['id']
        if x['author'] == None:
            info = [time,reason,page,url_id,None,None,None,None,None,None,None,None]
        else:
            author = x['author']['data']['name']
            created_utc = x['author']['data']['created_utc']
            hidden = x['author']['data']['hide_from_robots']
            l_karma = x['author']['data']['link_karma']
            c_karma = x['author']['data']['comment_karma']
            gold = x['author']['data']['is_gold']
            mod = x['author']['data']['is_mod']
            email = x['author']['data']['has_verified_email']
            info = [time,reason,page, url_id,author,created_utc,hidden,l_karma,c_karma,gold,mod,email]
        df.loc[i] = info
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df.fillna(False)
    df['url'] = 'https://www.reddit.com/r/The_Donald/wiki/' + df['page'] + '?v' + df['url_id']
    return df



    