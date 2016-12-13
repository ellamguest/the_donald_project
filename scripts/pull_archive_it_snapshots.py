# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 16:47:04 2016

@author: emg
"""
import requests
from bs4 import BeautifulSoup
import re
from scraping_functions import *

##### GET ALL ARCHIVED COPIES from archive.it
BEGIN_URL = 'https://archive.is/https://www.reddit.com/r/The_Donald/about/moderators'
headers = {'user-agent': 'why_ask_reddit 1.0'}
r = requests.get(BEGIN_URL, headers=headers)
soup = BeautifulSoup(r.text, "html5lib")


links = soup.findAll(href=re.compile("https://archive.is/")) # 75 links. ~ 67 snapshots
urls = []
for x in links:
    urls.append(x['href'])
users = urls[5:-3]
 
mod_info = compile_dfs(users)

df = pd.read_csv('all_mods_archive_it.csv')


 