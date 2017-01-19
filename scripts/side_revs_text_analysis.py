# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 16:21:04 2017

@author: emg
"""

import pandas as pd
import nltk
import re
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
test = tag_breakdown(test)


# BASIC TEXT PARSING

text = test['html'][0].get_text()
tokens = nltk.word_tokenize(text)
words = [word.encode('utf-8') for word in tokens]
words = filter(None,[re.sub(r'\W+', '', word) for word in words])
tagged = nltk.pos_tag(words)


# PLAYING W/ TEXT PARSING
from nltk.stem.porter import *
stemmer = PorterStemmer()

plurals = ['caresses', 'flies', 'dies', 'mules', 'denied',
            'died', 'agreed', 'owned', 'humbled', 'sized',
           'meeting', 'stating', 'siezing', 'itemization',
           'sensational', 'traditional', 'reference', 'colonizer',
           'plotted']
singles = [stemmer.stem(plural) for plural in plurals]
print(' '.join(singles))  # doctest: +NORMALIZE_WHITESPACE