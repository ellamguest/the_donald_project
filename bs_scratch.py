# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 10:53:23 2016

@author: emg
"""

import urllib2
from bs4 import BeautifulSoup
import re

url = 'http://web.archive.org/web/20161007131752/https://www.reddit.com/r/The_Donald/about/moderators/'
page = urllib2.urlopen(url)

soup = BeautifulSoup(page)

soup.prettify() # look at nested structure

all_tables = soup.find_all('table')

right_table=soup.find('table', class_='wikitable sortable plainrowheaders')

soup.contents[1]

for child in title_tag.children:
    print(child)
    
    
len(soup.findChildren()) # 1706 children
children = soup.findChildren()
len(set(children)) # 1176 unique children

for i in range(60,100):
    print children[i].attrs
    
ohsnap = soup.findAll(text='OhSnapYouGotServed') # two instances
obj = ohsnap[0]

len(obj.findParents()) # 9 parent tags

parents = obj.findParents()

for i in range(len(parents)):
    print parents[i].name

'''
parent names
a # a hyperlink
li # a list item
ul # An unordered list
div
div
div
body
html
[document]'''

# put is access backwards do not find!
x = soup.html.body.div.div.div
x.findAll(text='OhSnapYouGotServed')

#only find name if draw back of body level
c = soup.html.body

###  THERE ARE 6 'div' CHILDREN, FIND THE RIGHT ONE

name = 'PrinceCamelton'
obj.parent.parent.parent.findAll(text=name) # found at this level - ul

# ul (unordered list) includes the mod entries?
parent = obj.parent.parent.parent

parent.li # can get flair
mod_level = parent.li.a #indv
url = mod_level['href']
name = url.split('/user/')[1]

names = []

listings = obj.parent.parent.parent
children = listings.findChildren(name='li') # trying to select tags only

for child in children[:5]:
    tag = child.a
    url = tag['href']
    name = url.split('/user/')[1]
    names.append(name)
    

names = []
users = soup.find_all(href=re.compile("user"))
for x in users:
    url = x['href']
    print url
    name = url.split('/user/')[1]
    names.append(name.strip('/'))
    
# 10 names are repeats, first instance w/o '/' at end
# 41 modnames found
    

