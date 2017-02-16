# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:20:22 2017

@author: emg
"""

import pandas as pd
import re
#import string

# IMPORT AND PREP DATA FRAMES
posts = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/period_top_posts.csv', thousands=',', index_col=0)
posts.index = posts['post_id']
posts['title'] = posts['title'].str.decode(encoding='utf-8')

attrs = ['author','body','created','score', 'link_id', 'distinguished', 'gilded'] #only selecting limited attributes for now
comments = pd.read_pickle('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/ALL_comments_top_100_posts')
comments = comments[attrs]
comments['date'] = pd.to_datetime(comments['created'], unit='s')
comments['post_id']=comments['link_id'].str[3:]


# TIDY DATA INTO DOCUMENTS
docs = []
for post_id in posts.index:
    body = list(comments[comments['post_id']==post_id]['body'])
    body.insert(0, posts['title'].loc[post_id])
    doc = ' '.join(body)
    docs.append(re.sub(r'[^\w\s]','',doc))


####### GENSIM
# VECTORISE
from gensim import corpora
from gensim.parsing.preprocessing import STOPWORDS

def tokenize(text):
    return [token for token in text.lower().split() if token not in STOPWORDS]

texts = [tokenize(text) for text in docs]

dictionary = corpora.Dictionary(texts)
dict_map = dictionary.token2id

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/corpus.mm', corpus)

#TRANSFORMATION INTERFACE
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities

corpus = corpora.MmCorpus('/tmp/corpus.mm')

tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

doc = 'Hillary Clinton is crooked'
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print(vec_lsi)

lsi.print_topics(20, 4)

for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
    print(doc)


index = similarities.MatrixSimilarity(lsi[corpus])
sims = index[vec_lsi]
print(list(enumerate(sims)))


#### SCIKIT-LEARN
import numpy as np  # a conventional alias
import sklearn.feature_extraction.text as text

vectorizer = text.CountVectorizer(input='content', stop_words='english', min_df=20)

dtm = vectorizer.fit_transform(docs).toarray()
vocab = np.array(vectorizer.get_feature_names())

from sklearn import decomposition
num_topics = 20
num_top_words = 20
clf = decomposition.LatentDirichletAllocation(n_components=num_topics, random_state=1)


   
###### NLTK OLD CODE
# PERFORM CLUSTERING ANALYSIS
raw = docs[0]
tokens = nltk.word_tokenize(raw.lower())

stopwords = nltk.corpus.stopwords.words('english')
filtered_tokens = [token for token in tokens if token not in stopwords]
filtered_words = [word for word in filtered_tokens if word not in string.punctuation]

text = nltk.Text(filtered_words)
text.collocations()

nltk_df = pd.DataFrame(data={'post':d.keys(), 'body':d.values()})
#nltk_df['body'] = nltk_df['body'].str.decode('utf-8')
nltk_df['tokens'] = nltk_df['body'].map(lambda x: nltk.word_tokenize(x))
nltk_df['filtered_tokens'] = nltk_df['tokens'].map(lambda x: [t for t in x if t not in stopwords])

wnl = nltk.WordNetLemmatizer()
nltk_df['lemma_words'] = nltk_df['filtered_tokens'].map(lambda x: [wnl.lemmatize(t) for t in x])
nltk_df['filtered_words'] = nltk_df['lemma_words'].map(lambda x: ' '.join([w for w in x if w not in string.punctuation]))

texts = list(nltk_df['filtered_words'])

tfidf_vectorizer = feature_extraction.text.TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
terms = tfidf_vectorizer.get_feature_names()

dist = 1 - metrics.pairwise.cosine_similarity(tfidf_matrix)

km = cluster.KMeans(n_clusters=4)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist() # list of clusters

nltk_df['clusters'] = clusters
nltk_df['date'] = posts['date']
nltk_df.index = nltk_df['post']

c = nltk_df[['clusters','date', 'filtered_words']].sort(['clusters','date'])
zero = c[c['clusters']==0]
one = c[c['clusters']==1]
two = c[c['clusters']==2]
three = c[c['clusters']==3]