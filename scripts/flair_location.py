# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 17:41:59 2017

@author: emg
"""
import pandas as pd
import us
import pycountry

# is it all just in 'author_flair_css_class'?

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/all_comments_top_posts.csv', index_col=0)

states = us.states.mapping('abbr','name')
d = {}
for x in set(df['author_flair_text']):
    if x in states:
        d[x] = [states[x]]
    else:
        d[x] =[]

for x in d.keys():
    try:
        country = pycountry.countries.lookup(x).name
        d[x].append(country)
    except LookupError:
        pass