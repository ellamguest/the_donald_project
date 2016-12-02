# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 12:04:25 2016

@author: emg
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

##### SCRAPE PAGE
url = 'https://web.archive.org/web/20161007131752/https://www.reddit.com/r/The_Donald/about/moderators/'
timestamp = url.split('/web/')[1].split('/https')[0]
#url = 'https://www.reddit.com/r/The_Donald/about/moderators/'
headers = {'user-agent': 'why_ask_reddit 1.0'}
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.text, "html5lib")

###### GET MOD INFO 
users = soup.find_all(href=re.compile("/user/"))
mods = users[10:] # skipping double entries on top 10 mods from sidebar 
    
name = []
href = []
datetime = []
date = []
permissions = []
postkarma = []
for mod in mods:
    info = mod.parent.parent.parent
    children = info.findChildren()
    name.append(children[9]['value'])
    href.append(children[2]['href'])
    datetime.append(children[5]['datetime'])
    date.append(children[5]['title'])
    permissions.append(children[8].findChildren()[2]['value'])
    postkarma.append(children[3])

columns = {'name': name, 'useraccount': href, 'permissions' : permissions, 'postkarma' : postkarma, 'datetime': datetime, 'date' : date}
df2 = pd.DataFrame(columns)
df2['timestamp'] = timestamp



##### GET ALL ARCHIVED COPIES
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

##### TEST URL GENERATION
