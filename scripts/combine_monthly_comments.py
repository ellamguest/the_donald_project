#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 12:04:09 2017

@author: emg
"""
import pandas as pd
#import re
import pickle

# TRAINING DATASET

months = ['15_07', '15_08', '15_09', '15_10', '15_11', '15_12', 
          '16_01', '16_02', '16_03', '16_04', '16_05', '16_06', 
          '16_07', '16_08', '16_09', '16_10', '16_11', '16_12', 
          '17_01']

month_dict = {}
for i, item in enumerate(months):
    month_dict[i] = item

base_filename = '/Users/emg/Programmming/GitHub/the_donald_project/raw_data/bigquery/td_comments_20{}.csv'
docs = []

for month in months:
    df = pd.read_csv(base_filename.format(month))
    df['body'].replace(regex=True,inplace=True,to_replace=r'[^\w\s]',value=r'')
    comments = [x for x in list(df['body'].str.lower()) if str(x) != 'nan']
    doc = ' '.join(comments)
    docs.append(doc)

pickle.dump(docs, open('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/monthly_comments.p','wb'))    
    
dfs = [pd.read_csv(base_filename.format(month)) for month in months]

for month in months:
    df = pd.read_csv(base_filename.format(month))

all_comments = pd.concat(dfs)
pd.to_pickle(all_comments, '/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/all_td_comments')

all_comments = pd.read_pickle('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/all_td_comments')
all_comments = all_comments[['body','created_utc']]
all_comments['date'] = pd.to_datetime(all_comments['created_utc'], unit='s')
all_comments.sort_values('date', inplace=True)
grouped_comments = all_comments.groupby(all_comments.date.dt.week)


##### CREATE CORPUS, TFIDF, AND LSI
# re-run top_comment_doc_clustering.py if needed
from gensim import corpora, models, similarities
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = corpora.Dictionary.load('/tmp/td_dictionary.dict')
dict_map = dictionary.id2token

corpus = corpora.MmCorpus('/tmp/td_corpus.mm') # should be n months in length
tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=200) # initialize an LSI transformation
lsi.save('/Users/emg/Programmming/GitHub/the_donald_project/analysis_results/td_lsi')

lsi = models.LsiModel.load('/Users/emg/Programmming/GitHub/the_donald_project/analysis_results/td_lsi', mmap='r')
                   
lsi.print_topics(10, 4)

corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
    print(doc)      


## TEST DATASETS
periods = pickle.load( open( "/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/comment_periods.p", "rb" ) )

doc = periods[1]

def most_freq_tokens(doc, num_tokens):
    '''gets the most frequent num_tokens in the doc,
        using the existing corpora dictionary'''
    vec_bow = dictionary.doc2bow(doc.lower().split())
    id_freq = sorted(vec_bow, key=lambda x: x[1], reverse=True)
    token_freq = []
    for x in id_freq:
        token_freq.append('{} : {}'.format(dict_map[x[0]], x[1]))
    return token_freq[:num_tokens]

most_freq_tokens(periods[1],15)





vec_lsi = lsi[vec_bow] # convert the query to LSI space
doc_sim = sorted(vec_lsi, key=lambda x: x[1], reverse=True)    

month_sim = []
for x in doc_sim:
    month_sim.append('{} : {}'.format(month_dict[x[0]], x[1]))
month_sim        
                         
                         


