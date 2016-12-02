# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 16:26:02 2016

@author: emg
"""

import pandas as pd

mods = pd.read_csv('t_d_mod_hist.csv')
mods.rename(columns={'Unnamed: 0':'rank'}, inplace=True)

counts = mods.groupby('name')['name'].count()