# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 12:04:25 2016

@author: emg
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

headers = {'user-agent': 'why_ask_reddit 1.0'}

##### GET ALL ARCHIVED COPIES
# all 2016 entries, weren't any in 2015, will need to update for 2017
BEGIN_URL = 'http://web.archive.org/web/20160101000000*/https://www.reddit.com/r/The_Donald/about/moderators/'
headers = {'user-agent': 'why_ask_reddit 1.0'}
r = requests.get(BEGIN_URL, headers=headers)
soup = BeautifulSoup(r.text, "html5lib")

date_captures = soup.findAll('div', {'class' : 'date captures'})
snapshots = []
for date in date_captures:
    for snapshot in date.findAll(name='li'):
        snapshots.append(snapshot)

unique_urls = []
for snapshot in snapshots:
    unique_url = str(snapshot).split('href="')[1].split('">')[0]
    unique_urls.append(unique_url)

BASE_URL = 'http://web.archive.org'
urls, timestamps = [], []
for item in unique_urls:
    url = BASE_URL + item
    urls.append(url)
    timestamp = item.split('/web/')[1].split('/')[0]
    timestamps.append(timestamp)
    
columns = {'snapshot' : urls, 'timestamp' : timestamps}
snapshot_df = pd.DataFrame()
snapshot_df.to_csv('the_donald_snapshots_list_2dec.csv')

##### CHECK PAGES ARCHIVED SUCCESSFULLY
#df = pd.read_csv('the_donald_snapshots_list_2dec.csv', index_col=0)
#urls = df.snapshot

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

df['success'] = mark_unsuccessful(urls) # 11 false
df.to_csv('the_donald_snapshots_list_2dec.csv')

##### SCRAPE  + COMPILE MOD INFO
df = pd.read_csv('the_donald_snapshots_list_2dec.csv', index_col=0)
possibles = df[df['success'] != False]
urls = possibles.snapshot


def scrape_mod_table(url): 
    '''pulls mod info from soup object of /about/moderators snapshot
       dumps info into a dataframe '''
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
    
dfs = []
for url in urls:
    scrape_mod_table(url)
   
mod_hist = pd.concat(dfs)
mod_hist['archived'] = mod_hist.useraccount.str[5:19]
mod_hist['postkarma'] = mod_hist.postkarma.str[3:-4]
mod_hist = mod_hist[['name', 'useraccount', 'permissions', 'postkarma', 'datetime', 'date', 'archived']]
mod_hist.to_csv('t_d_mod_hist.csv')
mods = pd.read_csv('t_d_mod_hist.csv')
mods.rename(columns={'Unnamed: 0':'rank'}, inplace=True)


# fixing karma string until rescrape not as tag!!!
k = []
for tag in mod_hist.postkarma:
    k.append(str(tag)[3:-4])
mod_hist['postkarma'] = k













    
