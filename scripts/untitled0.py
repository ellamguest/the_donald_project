#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 12:30:25 2017

@author: emg
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
#import os

cdx = 'http://web.archive.org/cdx/search/cdx?url=https://www.reddit.com/r/The_Donald/about/moderators'
response = requests.get(cdx)
text = response.text
lines = text.splitlines()

times = []
for line in lines:
    time = line.split(' ')[1]
    times.append(time)
    
def save_snapshot(time):
    #save wbm td snapshot at time to file
    test = 'http://web.archive.org/web/{}/https://www.reddit.com/r/The_Donald/about/moderators'.format(time)
    response = requests.get(test)
    
    filename = "/Users/emg/Google Drive/PhD/data/the_donald/td-wbm-snapshots/td-wbm-{}.html".format(time)
    with open(filename, "wb") as file:
        file.write(response.content)

for time in times:
    save_snapshot(time)


def load_snapshot(time):
    f = open("/Users/emg/Google Drive/PhD/data/the_donald/td-wbm-snapshots/td-wbm-{}.html".format(time), 'r')
    return f.read() 

    
def snapshot_df(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        table = soup.findAll("div", {"class":"moderator-table"})[0]
    except IndexError:
        print "whoa there, pardner! This snapshot is empty :("
    else:
        rows = table.find_all('tr')           
        
        d = {}
        for row in rows:          
            name_karma = row.findAll('span', {'class':'user'})[0].text
            name = name_karma.split(u'\xa0')[0]
            karma = name_karma.split(u'\xa0')[1]
            date = row.findAll('time')[0]['datetime']
            permissions = row.findAll('input', {'name':'permissions'})[0]['value']
            d[name] = [date, permissions, karma]   
        d.keys()
        
        df = pd.DataFrame.from_dict(d, orient="index")
        df['pubdate'] = times[-1]
        return df
    
dfs = []
for time in times[:5]:
    html = load_snapshot(times[-1])
    df = snapshot_df(html)
    dfs.append(df)






