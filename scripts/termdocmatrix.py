# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 17:36:06 2017

@author: emg
"""

import textmining

def termdocumentmatrix_example():
    # Create some very short sample documents
    doc1 = 'John and Bob are brothers.'
    doc2 = 'John went to the store. The store was closed.'
    doc3 = 'Bob went to the store too.'
    # Initialize class to create term-document matrix
    tdm = textmining.TermDocumentMatrix()
    # Add the documents
    tdm.add_doc(doc1)
    tdm.add_doc(doc2)
    tdm.add_doc(doc3)
    # Write out the matrix to a csv file. Note that setting cutoff=1 means
    # that words which appear in 1 or more documents will be included in
    # the output (i.e. every word will appear in the output). The default
    # for cutoff is 2, since we usually aren't interested in words which
    # appear in a single document. For this example we want to see all
    # words however, hence cutoff=1.
    tdm.write_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/tdm_ex.csv', cutoff=1)
    # Instead of writing out the matrix you can also access its rows directly.
    # Let's print them to the screen.
    for row in tdm.rows(cutoff=2):
            print row

termdocumentmatrix_example()



text1 = test['html'][0].get_text()
text2 = test['html'][1].get_text()
text3 = test['html'][2].get_text()

tdm = textmining.TermDocumentMatrix()
tdm.add_doc(text1)
tdm.add_doc(text2)
tdm.add_doc(text3)