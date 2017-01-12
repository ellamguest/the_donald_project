# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 12:22:09 2017

@author: emg
"""

import pandas as pd
from bs4 import BeautifulSoup
from revisions_df_tools import *
from json_html_tools import json_to_html, tag_text

url = 'https://www.reddit.com/r/The_Donald/wiki/revisions/config/sidebar.json'
pages = after_pages(url)

dfs = []
for page in pages:
    df = get_revisions_df(page)
    dfs.append(df)
df = pd.concat(dfs)

df.to_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/sidebar_revisions.csv', index=False)

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/sidebar_revisions.csv', index_col=0)



# BREAKING TEXT DOWN BY TAG

content_df = df[['time','content']].head()
content_df['html'] = content_df['content'].apply(json_to_html)

d = {'headers':'h3', 'blockquotes':'blockquote','links':'a','lists':'ul'}

for key,value in d.iteritems():
    content_df[key] = content_df['html'].apply(lambda x: tag_text(x,value))





    