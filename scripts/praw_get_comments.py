# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 15:35:28 2017

@author: emg
"""

import praw
import pandas as pd
import configparser
from prawini import get_params

# OPEN PRAW SESSION
params = get_params()
r = praw.Reddit(client_id=params['client_id'],
                client_secret=params['client_secret'],
                user_agent=params['user_agent'])

top_posts = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/period_top_posts.csv', thousands=',', index_col=0)
ids = list(top_posts['post_id'])

# GET POST COMMENTS
def get_flat_comments(submission_id):
    submission = r.submission(id=submission_id) #83 comments
    submission.comments.replace_more(limit=None)
    flat_comments = submission.comments.list()
    print '{} out of {} comments found for {}'.format(len(flat_comments),
                                                submission.num_comments,
                                                submission_id)
    return flat_comments

def compile_flat_comments(ids):
    data = []    
    for post in ids:
        flat_comments = get_flat_comments(post)
        data.append(flat_comments)
    return data


all_flat_comments = compile_flat_comments(ids)

# DUMP COMMENT INFO IN DATAFRAME

def comment_df(attrs):
    dfs = []
    for flat_comments in all_flat_comments:
        df = pd.DataFrame(columns=attrs)
        for comment in flat_comments:
            df.loc[comment.id] = [None]*(len(attrs)) 
            for attr, value in comment.__dict__.iteritems():
                if attr in attrs:
                  df[attr][comment.id] = value
        
        dfs.append(df)
    return pd.concat(dfs)

# UNPICKLE ENTIRE AND SELECT COLUMNS

attrs = ['author','body','created','score', 'link_id', 'distinguished', 'gilded'] #only selecting limited attributes for now
df = pd.read_pickle('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/ALL_comments_top_100_posts')
df = df[attrs]
df['date'] = pd.to_datetime(df['created'], unit='s')

###### PICKLE ENTIRE COMMENT DATA DUMP

#df = comment_df(all_attrs)
#df.to_pickle('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/ALL_comments_top_100_posts')


all_attrs = ['approved_by',
'archived',
'author',
'author_flair_css_class',
'author_flair_text',
'banned_by',
'block',
'body',
'body_html',
'clear_vote',
'controversiality',
'created',
'created_utc',
'delete',
'distinguished',
'downs',
'downvote',
'edit',
'edited',
'fullname',
'gild',
'gilded',
'id',
'is_root',
'likes',
'link_id',
'mark_read',
'mark_unread',
'mod',
'mod_reports',
'name',
'num_reports',
'parent',
'parent_id',
'parse',
'permalink',
'refresh',
'removal_reason',
'replies',
'reply',
'report',
'report_reasons',
'save',
'saved',
'score',
'score_hidden',
'stickied',
'submission',
'subreddit',
'subreddit_id',
'unsave',
'ups',
'upvote',
'user_reports']


