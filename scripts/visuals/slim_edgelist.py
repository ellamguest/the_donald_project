 #!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 12:14:07 2017

@author: emg
"""

import pandas as pd

# INIT t_d or cmv
sub = 't_d'
fullname = 'r/The_Donald'
#version = 3

#sub = 't_d'
#fullname = 'r/The_Donald'
version = 2

#sub = 'cmv'
#fullname = 'r/changemyview'
#version = 2

df =  pd.read_csv('/Users/emg/Programmming/GitHub/R-mod-nets/{}/data/edgelist.csv'.format(sub))
count = df.groupby('sub')['sub'].count()
shared = list(count[count>(version-1)].index)
df = df[df['sub'].isin(shared)]
df = df[df['sub']!=fullname]
df.to_csv('/Users/emg/Programmming/GitHub/R-mod-nets/{}/data/edgelist_shared{}.csv'.format(sub, version), index=False)


nodes = pd.read_csv('/Users/emg/Programmming/GitHub/R-mod-nets/{}/data/nodelist.csv'.format(sub))
names = list(set(df['mod'])) + list(set(df['sub']))
#names.remove(fullname)
shared = nodes[nodes['name'].isin(names)]
shared.to_csv('/Users/emg/Programmming/GitHub/R-mod-nets/{}/data/nodelist_shared{}.csv'.format(sub, version), index=False)

df.to_csv('/Users/emg/Programmming/GitHub/R-mod-nets/{}/data/edgelist_shared{}-test.csv'.format(sub, version), index=False, header=False)
