#! /usr/bin/env python3

'''
Calculate commits
Alternative version to improve labelling of X axis of the line plot
'''

import subprocess
from datetime import timezone
import pandas as pd
from matplotlib.dates import DateFormatter

author_dates = subprocess.check_output(['git', 'log', '--pretty=%aI'],
                                        universal_newlines=True) \
                         .splitlines()
s = pd.Series([pd.to_datetime(aI).astimezone(timezone.utc)
               for aI
               in author_dates])
print(s.head())
print(s.describe())
last_50 = s.nlargest(50).groupby(s.dt.date).agg('count')
ax = last_50.plot(style='.', rot=45, figsize=(9,2))
ax.get_xaxis().set_major_formatter(DateFormatter('%Y-%m-%d'))
