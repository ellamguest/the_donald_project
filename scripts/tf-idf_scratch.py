# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 17:39:36 2017

@author: emg
"""

import pandas as pd
import math
import nltk
import re
#from textblob import TextBlob as tb
from __future__ import division, unicode_literals, print_function
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_pickle('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/sidebar_revisions.pkl')
sample = df.sample(10)
texts = [text.get_text() for text in sample['html']]
#bloblist = [tb(text) for text in texts]
#
#def tf(word, blob):
#    return blob.words.count(word) / len(blob.words)
#
#def n_containing(word, bloblist):
#    '''find the n of documents containing the word'''
#    return sum(1 for blob in bloblist if word in blob.words)
#
#def idf(word, bloblist):
#    return math.log(len(bloblist)) / (1 + n_containing(word, bloblist))
#    
#def tfidf(word, blob, bloblist):
#    return tf(word, blob) * idf(word, bloblist)
#
#
#for i, blob in enumerate(bloblist):
#    print("Top words in document {}".format(i+1))
#    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
#    sorted_words = sorted(scores.items(), key=lambda x : x[1], reverse=True)
#    for word, score in sorted_words[:3]:
#        print ("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
#    

def tokenize_and_stem(text):
    # tokenize then stem each work in text
    stemmer = nltk.stem.snowball.SnowballStemmer("english")
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(re.sub(r'[^\w]', '', token))
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english', tokenizer=tokenize_and_stem, ngram_range=(1,2))
tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
terms = tfidf_vectorizer.get_feature_names()
tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=terms)
tfidf = tfidf.T

def get_top(doc_num, num_terms):
    top = tfidf[doc_num].order(ascending=False)[:num_terms]
    df = pd.DataFrame({'terms':top.index,'score':top.tolist(), 'document':doc_num}, index=range(1,num_terms+1))
    return df

dfs = []
for i in tfidf.columns:
    df = get_top(i, 10)
    dfs.append(df)

top = pd.concat(dfs)

for i in tfidf.columns:
    print("Top ngrams in document {}:".format(i+1))
    print()
    for word in tfidf[i].order(ascending=False)[:5].index:
        print(word)
    print()


