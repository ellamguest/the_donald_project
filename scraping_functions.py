# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 17:28:14 2016

@author: emg
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime

headers = {'user-agent': 'why_ask_reddit 1.0'}

def make_soup(url):
    '''makes soup object from url using requests module '''
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html5lib")
    return soup

def get_pubdate(url):
    soup = make_soup(url)
    pubdate = soup.find('time', {'itemprop':'pubdate'})['datetime']
    return pubdate

def get_mods_list(url):
    soup = make_soup(url)
    users = soup.find_all(href=re.compile("/user/"))
    mods = users[10:]
    return mods

def get_mod_info(mod):
    children = mod.parent.parent.parent.findChildren()
    name = children[9]['value']
    href = children[2]['href']
    date = children[5]['title']
    permissions = children[8].findChildren()[2]['value']
    postkarma = str(children[3]).split('">')[1].split('</')[0]
    return [name, href, date, permissions, postkarma]

def create_mod_df(url):
    mods = get_mods_list(url)
    columns = ['name', 'useraccount', 'date', 'permissions', 'postkarma']
    df = pd.DataFrame(columns = columns)
    for i in range(len(mods)):
        print i
        info = get_mod_info(mods[i])
        df.loc[i] = info
    df['source'] = url
    df['pubdate'] = datetime.strptime(get_pubdate(url), '%Y-%m-%dT%H:%M:%SZ')
    return df


def compile_dfs(urls):
    dfs = []
    n = 0
    for url in urls:
        print n
        df = create_mod_df(url)
        dfs.append(df)
        n+=1
    return pd.concat(dfs)







def scrape_mod_table(url, dfs): 
    '''pulls mod info from soup object of /about/moderators snapshot
       dumps info into an empty dataframe (dfs) '''
    soup = make_soup(url)
    users = soup.find_all(href=re.compile("/user/"))
    mods = users[10:] # skipping double entries on top 10 mods from sidebar 
    name, href, date, permissions, postkarma = [], [], [], [], []
    pubdate = soup.find('time', {'itemprop':'pubdate'})['datetime']
    for mod in mods:
        children = mod.parent.parent.parent.findChildren()
        name.append(children[9]['value'])
        href.append(children[2]['href'])
        # datetime.append(children[5]['datetime']) archive.it doesn't have so skip for now
        date.append(children[5]['title'])
        permissions.append(children[8].findChildren()[2]['value'])
        postkarma.append(str(children[3]).split('">')[1].split('</')[0])
    columns = {'name': name, 'useraccount': href, 'permissions' : permissions, 'postkarma' : postkarma, 'date' : date, 'source' : url, 'pubdate' : pubdate}
    df = pd.DataFrame(columns)
    dfs.append(df)






    
##### IF ARCHIVE DOES DOES ALWAYS CAPUTRE SUCCESSFUL SNAPSHOTS

def check_archiving_success(soup):
    '''check if snapshot archived successfully or received bot notice '''
    if soup.body.findAll(text=re.compile('whoa there, pardner!')) == []:
        return True
    else:
        return False
        
def mark_unsuccessful(urls):
    success = []
    for url in urls:
        if check_archiving_success(make_soup(url)) == False:
            answer = 'False'
        else:
            answer = ''
        success.append(answer)
    return success
    
#####