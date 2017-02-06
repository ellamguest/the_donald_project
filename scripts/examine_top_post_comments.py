# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 18:17:21 2017

@author: emg
"""
import pandas as pd

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/all_comments_top_posts.csv', index_col=0)

useful = ['subreddit_id', 'link_id', 'replies', 'id', 'gilded', 'archived', 
'author', 'parent_id', 'score', 'controversiality', 'body', 'edited',
'author_flair_css_class', 'body_html', 'name', 'score_hidden','stickied',
'created', 'author_flair_text', 'distinguished', 'mod_reports', 'ups', 'date'] 

df = df[useful]

stickies = df[df['stickied']==True]
stickies[['body', 'score','date','author']]