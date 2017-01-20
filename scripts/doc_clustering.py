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
times or authors = for labelling (aka titles)
texts = for content (aka synopses)
'''

#### PREPPING MY DATA
df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/sidebar_revisions.csv', index_col=0)
df.index = pd.to_datetime(df.index)

sample = df[['author','url']].head(50)
sample['json'] = sample['url'].map(pull_page)
sample['html'] = sample['json'].map(json_to_html)

times = sample.index
titles = sample['author']
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
cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#3364FF'}
              
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
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=sample['author'])) 
  
df['shapes'] = df['title'].map({1:'o',11:'^',12:'s'}) # want to make shape correspond to month of revision, come back to
#group by cluster
groups = df.groupby('label')


# set up plot
def plot():
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

plot()
plt.close()

#plt.savefig('clusters_small_noaxes.png', dpi=200)


''' INTERACTIVE VISUALISATION W/ MPLD3 - beyond me atm
using mpld3 for D3.js interactive graphic capabilites
!! need to go over toolbar bit !!
might want to change is the x and y attr for the position of the toolbar

#define custom toolbar location
class TopToolbar(mpld3.plugins.PluginBase):
    """Plugin for moving toolbar to top of figure"""

    JAVASCRIPT = """
    mpld3.register_plugin("toptoolbar", TopToolbar);
    TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
    TopToolbar.prototype.constructor = TopToolbar;
    function TopToolbar(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    TopToolbar.prototype.draw = function(){
      // the toolbar svg doesn't exist
      // yet, so first draw it
      this.fig.toolbar.draw();

      // then change the y position to be
      // at the top of the figure
      this.fig.toolbar.toolbar.attr("x", 150);
      this.fig.toolbar.toolbar.attr("y", 400);

      // then remove the draw function,
      // so that it is not called again
      this.fig.toolbar.draw = function() {}
    }
    """
    def __init__(self):
        self.dict_ = {"type": "toptoolbar"}

#create data frame that has the result of the MDS plus the cluster numbers and titles
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles)) 

#group by cluster
groups = df.groupby('label')

#define custom css to format the font and to remove the axis labeling
css = """
text.mpld3-text, div.mpld3-tooltip {
  font-family:Arial, Helvetica, sans-serif;
}

g.mpld3-xaxis, g.mpld3-yaxis {
display: none; }

svg.mpld3-figure {
margin-left: -200px;}
"""

# Plot 
fig, ax = plt.subplots(figsize=(14,6)) #set plot size
ax.margins(0.03) # Optional, just adds 5% padding to the autoscaling

#iterate through groups to layer the plot
for name, group in groups:
    points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=18, 
                     label=cluster_names[name], mec='none', 
                     color=cluster_colors[name])
    ax.set_aspect('auto')
    labels = [i for i in group.title]
    
    #set tooltip using points, labels and the already defined 'css'
    tooltip = mpld3.plugins.PointHTMLTooltip(points[0], labels,
                                       voffset=10, hoffset=10, css=css)
    #connect tooltip to fig
    mpld3.plugins.connect(fig, tooltip, TopToolbar())    
    
    #set tick marks as blank
    ax.axes.get_xaxis().set_ticks([])
    ax.axes.get_yaxis().set_ticks([])
    
    #set axis as blank
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    
ax.legend(numpoints=1) #show legend with only one dot

mpld3.display() #show the plot

#uncomment the below to export to html
html = mpld3.fig_to_html(fig)
print(html)

'''

'''
Hierarchical document clustering
Ward clustering algorithm - agglomerative clustering method
step 1) used the precomputed cosine distance matrix (dist) to calclate a linkage_matrix
step 2) then plot as a dendrogram.
'''

from scipy.cluster.hierarchy import ward, dendrogram

linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances

fig, ax = plt.subplots(figsize=(5, 7)) # set size
ax = dendrogram(linkage_matrix, orientation="right", labels=titles);

plt.tick_params(\
    axis= 'x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

plt.tight_layout() #show plot with tight layout

#uncomment below to save figure
#plt.savefig('ward_clusters.png', dpi=200) #save figure as ward_clusters
plt.close()

'''
Latent Dirichlet Allocation - topic modelling
LDA is a probabilistic topic model that assumes documents are a mixture of topics and that each word in the document is attributable to the document's topics
For my implementaiton of LDA, I use the Gensim pacakage.
preprocess the synopses a bit differently here - HE REMOVED PROPPER NOUNS, I WILL NOT
'''

from gensim import corpora, models, similarities 

#tokenize
tokenized_text = [tokenize_and_stem(text) for text in texts]

#remove stop words
texts = [[word for word in text if word not in stopwords] for text in tokenized_text]

#create a Gensim dictionary from the texts
dictionary = corpora.Dictionary(texts)

#remove extremes (similar to the min/max df step used when creating the tf-idf matrix)
dictionary.filter_extremes(no_below=1, no_above=0.8)

#convert the dictionary to a bag of words corpus for reference
corpus = [dictionary.doc2bow(text) for text in texts]

# run the model
%time lda = models.LdaModel(corpus, num_topics=5, 
                            id2word=dictionary, 
                            update_every=5, 
                            chunksize=10000, 
                            passes=100)