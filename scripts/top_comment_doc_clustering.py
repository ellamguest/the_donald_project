# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:20:22 2017

@author: emg
"""

import pandas as pd
import nltk
import re
from doc_clustering import tokenize_and_stem
import string
from sklearn import feature_extraction, externals, cluster, metrics, manifold
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hca

# IMPORT AND PREP DATA FRAMES
posts = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/period_top_posts.csv', thousands=',', index_col=0)
posts.index = posts['post_id']
posts['title'] = posts['title'].str.decode(encoding='utf-8')

attrs = ['author','body','created','score', 'link_id', 'distinguished', 'gilded'] #only selecting limited attributes for now
comments = pd.read_pickle('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/ALL_comments_top_100_posts')
comments = comments[attrs]
comments['date'] = pd.to_datetime(comments['created'], unit='s')
comments['post_id']=comments['link_id'].str[3:]
comments['body'] = comments['body'].str.encode('utf-8')

# TIDY DATA INTO DOCUMENTS
d = {}
for post in posts.index:
    d[post] = [posts['title'].loc[post]]

for comment in comments.index:
    d[comments['post_id'].loc[comment]].append(comments['body'].loc[comment])

for key, value in d.iteritems():
    d[key] = ''.join(value).decode('utf-8')

docs_key = []
for key,value in d.iteritems():
    text = ''.join(value).decode('utf-8')
    t = key, text
    docs_key.append(t)
    
docs = []
for doc in docs_key:
    docs.append(doc[1])

    

# PERFORM CLUSTERING ANALYSIS
stopwords = nltk.corpus.stopwords.words('english')
stemmer = nltk.stem.snowball.SnowballStemmer("english")

raw = docs[0]
raw = raw.encode('utf-8').lower()
tokens = nltk.word_tokenize(raw.decode('utf-8'))
filtered_tokens = [token for token in tokens if token not in stopwords]
filtered_words = [word for word in filtered_tokens if word not in string.punctuation]

text = nltk.Text(filtered_words)
text.collocations()

nltk_df = pd.DataFrame(data={'post':d.keys(), 'body':d.values()})
nltk_df['body'] = nltk_df['body'].str.decode('utf-8')
nltk_df['tokens'] = nltk_df['body'].map(lambda x: nltk.word_tokenize(x))
nltk_df['filtered_tokens'] = nltk_df['tokens'].map(lambda x: [token for token in x if token not in stopwords])
nltk_df['filtered_words'] = nltk_df['filtered_tokens'].map(lambda x: ' '.join([word for word in x if word not in string.punctuation]))

texts = list(nltk_df['filtered_words'])

tfidf_vectorizer = feature_extraction.text.TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
terms = tfidf_vectorizer.get_feature_names()

dist = 1 - metrics.pairwise.cosine_similarity(tfidf_matrix)

def plot_dendrogram(dist):
    '''dist is a distance matrix created from the tf-idf'''
    linkage_matrix = hca.linkage(dist, method='ward') #using distance matrix fro tfidf
    
    fig, ax = plt.subplots(figsize=(6, 25)) # set size
    ax = hca.dendrogram(linkage_matrix, orientation='right', labels=posts['date'])
    plt.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    
    plt.tight_layout() #show plot with tight layout

plot_dendrogram(dist)
