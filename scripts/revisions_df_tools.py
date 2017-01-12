# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 12:25:07 2017

@author: emg
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

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
    df['url'] = 'https://www.reddit.com/r/The_Donald/wiki/' + df['page'] + '.json?v=' + df['url_id']
    df['content'] = df['url'].map(pull_page)
    df['json'] = df.url.map(get_json)    
    return df
    
def get_json(url):
    return url.split('?')[0] + '.json?' + url.split('?')[1]
    
def pull_page(url):
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def json_to_html(json):
    data = json['data']['content_html']
    soup = BeautifulSoup(data)
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    html = BeautifulSoup(text)
    return html

def tag_text(html, tagname):
    text = []
    for tag in html.findAll(tagname):
        text.append(tag.text)
    return text






    