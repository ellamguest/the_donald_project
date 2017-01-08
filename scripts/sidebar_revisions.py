# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 12:22:09 2017

@author: emg
"""

import pandas as pd
import requests
from revisions_df_tools import *

url = 'https://www.reddit.com/r/The_Donald/wiki/revisions/config/sidebar.json'
pages = after_pages(url)


sidebar_revs = get_revisions_df('https://www.reddit.com/r/The_Donald/wiki/revisions/config/sidebar.json?limit=100')
sidebar_revs2 = get_revisions_df(pages[1])

dfs = []
for page in pages:
    df = get_revisions_df(page)
    dfs.append(df)
df = pd.concat(dfs)
