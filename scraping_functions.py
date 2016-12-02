# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 17:28:14 2016

@author: emg
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

headers = {'user-agent': 'why_ask_reddit 1.0'}

def make_soup(url):
    '''makes soup object from url using requests module '''
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html5lib")
    return soup
    
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

def scrape_mod_table(url, dfs): 
    '''pulls mod info from soup object of /about/moderators snapshot
       dumps info into an empty dataframe (dfs) '''
    soup = make_soup(url)
    users = soup.find_all(href=re.compile("/user/"))
    mods = users[10:] # skipping double entries on top 10 mods from sidebar 
    name, href, datetime, date, permissions, postkarma = [], [], [], [], [], []
    for mod in mods:
        #info = mod.parent.parent.parent
        #children = info.findChildren()
        children = mod.parent.parent.parent.findChildren()
        name.append(children[9]['value'])
        href.append(children[2]['href'])
        datetime.append(children[5]['datetime'])
        date.append(children[5]['title'])
        permissions.append(children[8].findChildren()[2]['value'])
        postkarma.append(str(children[3]))
    columns = {'name': name, 'useraccount': href, 'permissions' : permissions, 'postkarma' : postkarma, 'datetime': datetime, 'date' : date}
    df = pd.DataFrame(columns)
    dfs.append(df)