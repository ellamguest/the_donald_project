# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:54:24 2016

@author: emg
"""
import pandas as pd

def get_time_df(df):
    subset = (df[['name', 'date', 'pubdate']].copy()
            .assign(
                date = pd.to_datetime(df['date']).dt.normalize(),
                pubdate = pd.to_datetime(df['pubdate']).dt.normalize()))
    return subset

def get_start_days(df):
    subset = get_time_df(df)
    start = (subset
            .groupby(['date','name']).first()['pubdate']
            .unstack()
            .notnull())
    return start

starts = get_start_days(df)

def get_timeline(df):
    '''takes df w/ cols ['name', 'date', 'pubdate']
        returns df of days by names with boolean values
        for presence of mod at timepoint'''
    subset = (df[['name', 'date', 'pubdate']]  
            .assign(
                date = pd.to_datetime(df['date']).dt.normalize(),
                pubdate = pd.to_datetime(df['pubdate']).dt.normalize()))
                
    seen = (subset
                    .groupby(['date', 'name']).first()['pubdate']
                    .unstack()
                    .isnull()
                    .pipe(lambda x: ~x)
                    .resample('D').mean()
                    .fillna(0)
                    .astype(bool))
    
    
    not_seen = (subset
                    .groupby(['pubdate', 'name']).first()['date']
                    .unstack()
                    .isnull()
                    .resample('D').pad())
        
    
    output = {}
    current = pd.Series(False, seen.columns)    
    for d in seen.index & not_seen.index:
        joined, left = seen.loc[d], not_seen.loc[d]
        current[joined] = True
        current[left] = False
        output[d] = current.copy()
    output = pd.concat(output, 1).T
    return output
    
    
df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/all_mods_archive_it.csv', index_col=0)

seen = (subset
                    .groupby(['date', 'name']).first()['pubdate']
                    .unstack()
                    .isnull()
                    .pipe(lambda x: ~x)
                    .resample('D').mean()
                    .fillna(0)
                    .astype(bool))
