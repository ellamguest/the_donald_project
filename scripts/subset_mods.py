# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:44:32 2016

@author: emg
"""

import pandas as pd

df = pd.read_csv('/Users/emg/Programmming/GitHub/the_donald_project/tidy_data/andy_output.csv', index_col=0)

# SELECTING MODS PRESENT OVER MANY DAYS
days = df.sum()
names = days[days>=10]
df = df[names.index]