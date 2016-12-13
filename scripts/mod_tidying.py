# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 16:32:19 2016

@author: emg
"""
import pandas as pd

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/andy_output.csv', index_col=0)

# removing infrequent mods, out by daily average presence
mods = df.T.astype(int)
sums = mods.sum(axis=1)
nones = sums[sums == 0]
mods = mods[~mods.index.isin(nones.index)]