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

##############################################################################
##############################################################################

''' PREPPING DATA '''
def prep_sample(filename):
    '''filename is a csv file of sidebar revisions'''
    sidebar_revisions = pd.read_csv(filename, index_col=0)
    sidebar_revisions.index = pd.to_datetime(sidebar_revisions.index)
    sidebar_revisions = sidebar_revisions[sidebar_revisions['author'] != 'False']
    
    sample = sidebar_revisions[['author','url']].sample(50)
    sample['json'] = sample['url'].map(pull_page)
    sample['html'] = sample['json'].map(json_to_html)
    return sample

##############################################################################
##############################################################################

''' CLEANING DATA (Stopwords, stemming, and tokenizing) '''

stopwords = nltk.corpus.stopwords.words('english')
stemmer = nltk.stem.snowball.SnowballStemmer("english")

def tokenize_and_stem(text):
    # tokenize then stem each work in text
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
#print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

##############################################################################
##############################################################################

''' TF-IDF DOCUMENT SIMILARITY

 step 1) count word occurrences by document.
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

##############################################################################
##############################################################################

#### K-means clustering ####

from sklearn.cluster import KMeans
from sklearn.externals import joblib

def pickle_dump_kmeans():
    num_clusters = len(sample['author'].unique()) # set number of clusters to number of unique authors
    km = KMeans(n_clusters=num_clusters)
    km.fit(tfidf_matrix)
    joblib.dump(km,  'doc_cluster.pkl')

#km = joblib.load('doc_cluster.pkl')
#clusters = km.labels_.tolist()

# create doc attribute df including cluster assignment
revs = { 'time': times, 'author': sample['author'].tolist(), 'text': texts, 'cluster': clusters, 'month' : sample.index.month}

frame = pd.DataFrame(revs, index = [clusters] , columns = ['time', 'author', 'cluster', 'text', 'month'])

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


##############################################################################
##############################################################################
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

##############################################################################
##############################################################################

'''VISUALISING DOCUMENT CLUSTERS - K-MEANS'''



def kmeans_plot():
    cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#3364FF'}
              
    cluster_names = {}
    # cannibalizing code above to get list of highest ranking words per cluster
    for i in range(num_clusters):
        names = []
        for ind in order_centroids[i, :3]: 
            names.append(vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'))
        cluster_names[i] = names
        
    #create data frame that has the result of the MDS plus the cluster numbers and titles
    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=sample['author'])) 
      
    df['shapes'] = df['title'].map({1:'o',11:'^',12:'s'}) # want to make shape correspond to month of revision, come back to
    #group by cluster
    groups = df.groupby('label')

    fig, ax = plt.subplots(figsize=(11, 6)) # set size
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
        
    ax.legend(numpoints=1, loc=0)  #show legend with only 1 point
    
    #add label in x,y position with the label as the author name
    for i in range(len(df)):
        ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)  
    
        
        
    plt.show() #show the plot

kmeans_plot()


#plt.savefig('clusters_small_noaxes.png', dpi=200)



##############################################################################
##############################################################################


''' HIERARCHICAL (DOCUMENT) CLUSTERING ANALYSIS
Ward clustering algorithm - agglomerative clustering method
step 1) used the precomputed cosine distance matrix (dist) to calclate a linkage_matrix
step 2) then plot as a dendrogram.
'''

from scipy.cluster.hierarchy import ward, dendrogram

def hca_plot(dist):
    # dist is a numpy.ndarray created for k-means testing
    linkage_matrix = ward(dist)
    
    fig, ax = plt.subplots(figsize=(5, 7)) # set size
    ax = dendrogram(linkage_matrix, orientation="right", labels=titles);
    
    plt.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    
    plt.tight_layout() #show plot with tight layout
    #plt.savefig('ward_clusters.png', dpi=200) #save figure as ward_clusters



##############################################################################
##############################################################################

''' TOPIC MODELLING - Latent Dirichlet Allocation
LDA is a probabilistic topic model that assumes documents are a mixture of
topics and that each word in the document is attributable to the document's topics
EXAMPLE REMOVED PROPER NOUNS, I HAVE NOT
'''

from gensim import corpora, models, similarities 

def lda(texts):
    '''text is a list of sidebar revisions returns from prep_texts'''
    tokenized_text = [tokenize_and_stem(text) for text in texts] #tokenize
    stopless_texts = [[word for word in text if word not in stopwords] for text in tokenized_text] #remove stop words
    dictionary = corpora.Dictionary(stopless_texts) #create a Gensim dictionary from the texts
    dictionary.filter_extremes(no_below=1, no_above=0.8) #remove extremes (similar to the min/max df step used when creating the tf-idf matrix)
    corpus = [dictionary.doc2bow(text) for text in stopless_texts] #convert the dictionary to a bag of words corpus for reference
    
    # run the model
    %time lda = models.LdaModel(corpus, num_topics=5, id2word=dictionary, update_every=5, chunksize=10000, passes=100)
    return lda

def lda_topic_list(lda):
    # convert the topics into just a list of the top 20 words in each topic
    topics_matrix = lda.show_topics(formatted=False, num_words=20)
    
    for n in range(len(topics_matrix)):
        topic_words = topics_matrix[n][1]
        print('TOPIC {}'.format(n))
        print()
        print([str(word[0]) for word in topic_words])
        print()


##############################################################################
##############################################################################
'''RUN SECTIONS'''

sample = prep_sample('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/sidebar_revisions.csv')
times = sample.index
names = sample['author']
texts = [text.get_text() for text in sample['html']]


pickle_dump_kmeans()

km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

kmeans_plot() # must have called order_centroids from?



hca_plot(dist)

lda = lda(texts)
lda.show_topics()
lda_topic_list.lda()