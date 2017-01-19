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
    '''creates a json object from the url'''
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def get_after(url):
    '''find the id of the next page'''
    data = pull_page(url)
    after = data['data']['after']
    return after

def after_pages(url):
    '''gets the list of all historics pages'''
    urls = [url]
    after = get_after(url)
    while after != None:
        new = url + '?limit=100&after=' + after
        urls.append(new)
        after = get_after(new)    
    return urls

def get_revisions_df(url):
    '''compiles data on revisions across all pages'''
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
    return df


def json_to_html(json):
    '''must check json is in dict format, not string
     pandas converts to string when stored'''
    data = json['data']['content_html']
    soup = BeautifulSoup(data)
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    html = BeautifulSoup(text)
    return html


# BREAKING TEXT DOWN BY TAG

def tag_text(soup, tagname):
    '''input soup object, find all texts under that tag'''
    text = []
    for tag in soup.findAll(tagname):
        text.append(tag.text)
    return text
    

def tag_breakdown(df):
    '''df must have column ['html'] of soup objects
    creates additional columns for each tag component'''
    d = {'headers':'h3', 'blockquotes':'blockquote','links':'a','lists':'ul'}
    for key,value in d.iteritems():
        df[key] = df['html'].apply(lambda x: tag_text(x,value))
    return df






    