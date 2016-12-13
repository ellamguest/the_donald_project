# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 10:53:23 2016

@author: emg
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

##### SCRAPE PAGE
url = 'https://web.archive.org/web/20161007131752/https://www.reddit.com/r/The_Donald/about/moderators/'
timestamp = url.split('/web/')[1].split('/https')[0]
#url = 'https://www.reddit.com/r/The_Donald/about/moderators/'
headers = {'user-agent': 'why_ask_reddit 1.0'}
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.text, "html5lib")

###### GET MOD INFO 
users = soup.find_all(href=re.compile("/user/"))
mods = users[10:] # skipping double entries on top 10 mods from sidebar 
    
name = []
href = []
datetime = []
date = []
permissions = []
postkarma = []
for mod in mods:
    info = mod.parent.parent.parent
    children = info.findChildren()
    name.append(children[9]['value'])
    href.append(children[2]['href'])
    datetime.append(children[5]['datetime'])
    date.append(children[5]['title'])
    permissions.append(children[8].findChildren()[2]['value'])
    postkarma.append(children[3])

columns = {'name': name, 'useraccount': href, 'permissions' : permissions, 'postkarma' : postkarma, 'datetime': datetime, 'date' : date}
df2 = pd.DataFrame(columns)
df2['timestamp'] = timestamp



    
##### GET MOD PROMOTION TIMES
times = soup.findAll(name='time')
# times[0] is time subreddit was created
    





###### found mod table
usertable = soup.findAll('div', {"class" : "moderator-table"})
usertable = usertable[0]

##### scratch

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
    


    

