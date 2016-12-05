# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 16:47:04 2016

@author: emg
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from scraping_functions import make_soup, check_archiving_success, mark_unsuccessful, scrape_mod_table 

##### GET ALL ARCHIVED COPIES from archive.it
BEGIN_URL = 'https://archive.is/https://www.reddit.com/r/The_Donald/about/moderators'
headers = {'user-agent': 'why_ask_reddit 1.0'}
r = requests.get(BEGIN_URL, headers=headers)
soup = BeautifulSoup(r.text, "html5lib")


links = soup.findAll(href=re.compile("https://archive.is/")) # 75 links. ~ 67 snapshots
urls = []
for x in links:
    urls.append(x['href'])

urls = urls[5:-3] # 67!
 
   
mod_hist = pd.concat(dfs)
mod_hist['archived'] = mod_hist.useraccount.str[5:19]
mod_hist['postkarma'] = mod_hist.postkarma.str[3:-4]
mod_hist = mod_hist[['name', 'useraccount', 'permissions', 'postkarma', 'datetime', 'date', 'archived']]
mod_hist.to_csv('t_d_mod_hist.csv')
mods = pd.read_csv('t_d_mod_hist.csv')
mods.rename(columns={'Unnamed: 0':'rank'}, inplace=True)

##### GET MOD LIST FROM EACH ARCHIVE.IT SNAPSHOT
# 67 snapshots
sample = urls[:5]

x = compile_dfs(urls)


 