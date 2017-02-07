# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 15:35:28 2017

@author: emg
"""

import praw
import pandas as pd

top_posts = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/period_top_posts.csv', thousands=',', index_col=0)
ids = list(top_posts['post_id'])

r = praw.Reddit(user_agent='why_ask_reddit 1.0')


def get_flat_comments(submission_id):
    submission = r.get_submission(submission_id=submission_id) #83 comments
    submission.replace_more_comments(limit=None)
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    return flat_comments

flat_comments = get_flat_comments('4ar1uc')

test = ids[:5]
all_comments = []
for submission_id in test:
    print submission_id
    print 'Fetching flat comments'
    flat_comments = get_flat_comments(submission_id)
    print '{} comments found'.format(len(flat_comments))
    all_comments.append(flat_comments)
print 'Pulled flat comments for {} submissions'.format(len(all_comments))