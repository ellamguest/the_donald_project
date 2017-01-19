# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 12:22:09 2017

@author: emg
"""

import pandas as pd
from revisions_df_tools import *

def compile_sidebar_revisions():
    url = 'https://www.reddit.com/r/The_Donald/wiki/revisions/config/sidebar.json'
    pages = after_pages(url)
    
    dfs = []
    for page in pages:
        df = get_revisions_df(page)
        dfs.append(df)
    df = pd.concat(dfs)
    df.set_index('time', drop=True, inplace=True)
    del df.index.name
    
    return df

def load_sidebar_revisions():
    df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/sidebar_revisions.csv', index_col=0)
    return df






    






    