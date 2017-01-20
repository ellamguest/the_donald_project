# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 18:01:01 2017

@author: emg
"""
# using code from http://brandonrose.org/clustering
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3
from revisions_df_tools import pull_page, json_to_html

'''working w/ 2 lists:
times = for labelling (aka titles)
texts = for content (aka synopses)
'''

#### PREPPING MY DATA
df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/sidebar_revisions.csv', index_col=0)
df.index = pd.to_datetime(df.index)

sample = df[['author','url']].head(50)
sample['json'] = sample['url'].map(pull_page)
sample['html'] = sample['json'].map(json_to_html)

times = sample.index
texts = []
for text in sample['html']:
    texts.append(text.get_text())

#### Stopwords, stemming, and tokenizing

stopwords = nltk.corpus.stopwords.words('english')

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

# here I define a tokenizer and stemmer which returns the set of stems in the text that it is passed
def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens
    

# create two lists: 1) all words tokenized + stemmed, 2) all words tokenized only
totalvocab_stemmed = []
totalvocab_tokenized = []
for i in texts:
    allwords_stemmed = tokenize_and_stem(i) #for each item in 'synopses', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
    
    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

# create a vocab df with index = stems and columns = all matching tokens
vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

### !UNIQUE VOCAB MEANS APPEAR TO BE FEW TOKENS WITH SHARED STEMS ###


#### Tf-idf and document similarity ####

''' step 1) count word occurrences by document.
    step 2) create a document-term matrix (dtm) aka term frequency matrix
    step 3) apply the term frequency-inverse document frequency weighting
    
    parameter notes:
    max_df: if the term is in greater than 80% of the documents it probably cares little meanining , play with
    min_idf: this could be an integer (e.g. 5) and the term would have to be in at least 5 of the documents to be considered, play with 
    ngram_range: set length on n-grams considered
'''

from sklearn.feature_extraction.text import TfidfVectorizer

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(texts) #fit the vectorizer to synopses

print(tfidf_matrix.shape)

# terms is just a list of the features used in the tf-idf matrix. This is a vocabulary
terms = tfidf_vectorizer.get_feature_names()

'''dist is defined as 1 - the cosine similarity of each document.
Cosine similarity is measured against the tf-idf matrix and can be used to
generate a measure of similarity between each document and the other documents 
in the corpus. Subtracting it from 1 provides cosine distance which I will use 
for plotting on a euclidean (2-dimensional) plane.
Note that with dist it is possible to evaluate the similarity of any two or more texts
'''
from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)

#### K-means clustering ####

from sklearn.cluster import KMeans

num_clusters = len(sample['author'].unique())
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)

clusters = km.labels_.tolist()
clusters

### pickling model
from sklearn.externals import joblib

#joblib.dump(km,  'doc_cluster.pkl')
km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

# create doc attribute df including cluster assignment
authors = sample['author']
revs = { 'time': times, 'author': sample['author'].tolist(), 'text': texts, 'cluster': clusters}

frame = pd.DataFrame(revs, index = [clusters] , columns = ['time', 'author', 'cluster', 'text'])

frame['cluster'].value_counts()

### original has some code on group mean rank not applicable here ###

#### identify n words most identified with each cluster, gives sense of cluster topic

from __future__ import print_function

print("Top terms per cluster:")
print()
#sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')
    
    for ind in order_centroids[i, :3]: #replace 6 with n words per cluster
        print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    print() #add whitespace
    print() #add whitespace
    
    print("Cluster %d authors:" % i, end='')
    if type(frame.ix[i]['author']) == str:
        print(frame.ix[1]['author'])
    else:
        for author in frame.ix[i]['author']:
            print(' %s,' % author, end='')
    print() #add whitespace
    print() #add whitespace
    
print()
print()


#### Multidimensional scaling ####
# convert the dist matrix into a 2-dimensional array using multidimensional scaling
# Another option would be to use principal component analysis.

import os  # for os.path.basename

import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.manifold import MDS

MDS()

# convert two components as we're plotting points in a two-dimensional plane
# "precomputed" because we provide a distance matrix
# we will also specify `random_state` so the plot is reproducible.
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

xs, ys = pos[:, 0], pos[:, 1]
print()
print()

####Visualizing document clusters####
# using matplotlib and mpld3 (a matplotlib wrapper for D3.js)
# step 1 define some dictionaries for going from cluster number to color and to cluster name

#set up colors per clusters using a dict
cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#66a61e'}
              
cluster_names = {}
# cannibalizing code above to get list of highest ranking words per cluster
for i in range(num_clusters):
    names = []
    for ind in order_centroids[i, :3]: 
        names.append(vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'))
    cluster_names[i] = names


#some ipython magic to show the matplotlib plots inline
%matplotlib inline 

#create data frame that has the result of the MDS plus the cluster numbers and titles
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=times)) 

#group by cluster
groups = df.groupby('label')


# set up plot
fig, ax = plt.subplots(figsize=(17, 9)) # set size
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

#iterate through groups to layer the plot
#note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
            label=cluster_names[name], color=cluster_colors[name], 
            mec='none')
    ax.set_aspect('auto')
    ax.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params(\
        axis= 'y',         # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelleft='off')
    
ax.legend(numpoints=1)  #show legend with only 1 point

#add label in x,y position with the label as the film title
for i in range(len(df)):
    ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)  

    
    
plt.show() #show the plot

#uncomment the below to save the plot if need be
#plt.savefig('clusters_small_noaxes.png', dpi=200)