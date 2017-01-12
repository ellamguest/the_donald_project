# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 12:22:09 2017

@author: emg
"""

import pandas as pd
import nltk
from revisions_df_tools import *

def compile_sidebar_revisions():
    url = 'https://www.reddit.com/r/The_Donald/wiki/revisions/config/sidebar.json'
    pages = after_pages(url)
    
    dfs = []
    for page in pages:
        df = get_revisions_df(page)
        dfs.append(df)
    df = pd.concat(dfs)
    
    return df

#df.to_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/sidebar_revisions.csv', index=False)

def load_sidebar_revisions():
    df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/sidebar_revisions.csv', index_col=0)
    return df


# BREAKING TEXT DOWN BY TAG

def content_df():
    load_sidebar_revisions()
    content_df = df[['time','content']].head()
    content_df['html'] = content_df['content'].apply(json_to_html)
    return content_df

cdf = content_df()

def tag_breakdown(df):
    d = {'headers':'h3', 'blockquotes':'blockquote','links':'a','lists':'ul'}
    for key,value in d.iteritems():
        df[key] = df['html'].apply(lambda x: tag_text(x,value))
    return df

tag_breakdown(cdf)

# tokenizing text
nltk.download()
text = cdf['html'].iloc[0].get_text()
tokens = nltk.word_tokenize(text)
tagged = nltk.pos_tag(tokens)
entities = nltk.chunk.ne_chunk(tagged)



    