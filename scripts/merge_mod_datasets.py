# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 18:30:21 2017

@author: emg
"""
import pandas as pd
import datetime

df1 = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/all_mods_archive_it.csv', index_col=0)
df2 = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/all_mods_web_archive.csv', index_col=0)
df2.columns = ['rank','name','useraccount','permissions', 'postkarma', 'datetime', 'date', 'pubdate']

def get_datetime(string):
    string = ''.join(ch for ch in str(string) if ch.isalnum())
    date = datetime.datetime.strptime(string,'%Y%m%d%H%M%S')
    return date

df1.pubdate = df1.pubdate.apply(get_datetime)
df2.pubdate = df2.pubdate.apply(get_datetime)

df1['day'] = pd.DatetimeIndex(df1.pubdate).normalize()
df2['day'] = pd.DatetimeIndex(df2.pubdate).normalize()

overlap = []
for day in df1.day.unique():
    if day in df2.day.unique():
        overlap.append(day)
        

cols = ['rank','name','useraccount','permissions', 'postkarma', 'date', 'pubdate', 'day']
df1, df2 = df1[cols], df2[cols]

df = pd.concat([df1,df2], keys=['it', 'web'])
df = df.sort(['pubdate', 'rank']) #4403

uni = df.drop_duplicates() #4197

df.to_csv('/Users/emg/Programmming/GitHub/the_donald_project/raw_data/all_mods_merged.csv')