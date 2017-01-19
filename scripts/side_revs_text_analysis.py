# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 16:21:04 2017

@author: emg
"""

import pandas as pd
import nltk
from bs4 import BeautifulSoup
from revisions_df_tools import *

revs = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/sidebar_revisions.csv', index_col=0)
revs.index = pd.to_datetime(revs.index)

periods = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/example_periods.csv', index_col=0)
periods['begin'] = pd.to_datetime(periods['begin'])
periods['end'] = pd.to_datetime(periods['end'])


subset = revs[(revs.index >= periods['begin'][1]) & (revs.index <= periods['end'][1])]
test = subset.head()
test['json'] = test['url'].map(pull_page)
test['html'] = test['json'].map(json_to_html)
#test = tag_breakdown(test)



text = test['html'][0].get_text()
tokens = nltk.word_tokenize(text)
tagged = nltk.pos_tag(tokens)
nltk.download()
entities = nltk.chunk.ne_chunk(tagged)