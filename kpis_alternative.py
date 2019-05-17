#! /usr/bin/env python3

'''
Calculate commits
Alternative version to improve labelling of X axis of the line plot
'''

import subprocess
from datetime import timezone
import pandas as pd
from matplotlib.dates import DateFormatter
import matplotlib.axes as axes

def despine(ax: axes.Axes) -> None:
    '''
    Remove the top and right spines of a graph.
    '''
    for spine in 'right', 'top':
        ax.spines[spine].set_color('none')


author_dates = subprocess.check_output(['git', 'log', '--pretty=%aI'],
                                        universal_newlines=True) \
                         .splitlines()
s = pd.Series([pd.to_datetime(aI).astimezone(timezone.utc)
               for aI
               in author_dates])
print(s.head())
print(s.describe())
last_50 = s.nlargest(50).groupby(s.dt.date).agg('count')
ax = last_50.plot.line(rot=45, figsize=(8,6))
ax.get_xaxis().set_major_formatter(DateFormatter('%Y-%m-%d'))
despine(ax)
ax.figure.savefig('commits_alternative.svg', format='svg')
