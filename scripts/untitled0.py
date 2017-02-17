#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 12:04:09 2017

@author: emg
"""

import pandas as pd

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/bigquery/td_comments_2016_05.csv')
df['body'].replace(regex=True,inplace=True,to_replace=r'[^\w\s]',value=r'')
#df = df[df['body']!='']

docs = [x for x in list(df['body'].str.lower()) if str(x) != 'nan']

months = ['15_07', '15_08', '15_09', '15_10', '15_11', '15_12', 
          '16_01', '16_02', '16_03', '16_04', '16_05', '16_06', 
          '16_07', '16_08', '16_09', '16_10', '16_11', '16_12', 
          '17_01']

base_filename = '/Users/emg/Programmming/GitHub/the_donald_project/raw_data/bigquery/td_comments_20{}.csv'
docs = []

for month in months:
    df = pd.read_csv(base_filename.format(months[0]))
    df['body'].replace(regex=True,inplace=True,to_replace=r'[^\w\s]',value=r'')
    comments = [x for x in list(df['body'].str.lower()) if str(x) != 'nan']
    doc = ' '.join(comments)
    docs.append(doc)