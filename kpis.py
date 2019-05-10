#! /usr/bin/env python3

'''
Calculate the number of daily commits for all git repositories.
Draw a scatter plot of daily commits versus date.
'''

# time -f '%e' ./kpis.py > kpis.txt
# ./kpis.py > kpis.txt


import subprocess
from os import path
from dateutil.parser import parse as parsedate


import pandas as pd
import matplotlib.cm as cm
import matplotlib.axes as axes


c = cm.Paired.colors
# c[0] c[1] ... c[11]
# See "paired" in "qualitative colormaps"
# https://matplotlib.org/tutorials/colors/colormaps.html


title = 'Daily commits'
ylabel = 'Number of commits'
xlabel = 'Date'


def dataframes(repository_path):
    '''
    Create a dataframe with count column for each repository.
    '''
    history = subprocess.check_output(
        ['git', 'log', '--pretty=%aI', '--author=Gilles'],
        cwd=path.expanduser(f'~/documents/websites/{repository_path}'),
        universal_newlines=True).splitlines()
    dates = list(map(parsedate, history))
    df = pd.DataFrame.from_dict({'Date': dates}, dtype='datetime64[ns]')\
                     .set_index('Date')
    df['count'] = 1
    df = df.groupby(df.index.date).count()
    df = df.reset_index().rename(columns={'index':'date'})
    return df


def despine(ax: axes.Axes) -> None:
    '''
    Remove the top and right spines of a graph.
    '''
    for spine in 'right', 'top':
        ax.spines[spine].set_color('none')


def plot_scatter(df, column_name):
    '''
    Scatter plot of column_name versus index.
    '''
    ax = df.plot.line(y=column_name,
                      legend=False,
                      style='.',
                      color=c[0],
                      rot=45)
    ax.set_ylabel(column_name)
    ax.set_xlabel('date')
    ax.set_title(f'{title}', fontweight='bold')
    ax.autoscale(tight=False)
    ax.axhline(int(df[column_name].median()), color=c[1])
    despine(ax)
    ax.figure.savefig(f'commits_daily.svg', format='svg')


parameters = pd.read_csv('repositories.csv',index_col=False)
repository_path = parameters['Repository path']


commits = pd.DataFrame(columns=['date', 'count'])
for item in repository_path:
    commits_item = dataframes(item)
    commits = pd.merge(commits, commits_item,
                       how='outer', on='date')\
                .sort_values(by=['date'])
    commits['count'] = commits['count_x'].fillna(0) + \
                       commits['count_y'].fillna(0)
    commits = commits.drop(columns=['count_x', 'count_y'])
commits['date'] = pd.to_datetime(commits['date'])
commits = commits[-30:].set_index('date')
print(f'Last 30 days:\n{commits}')

plot_scatter(commits, 'count')
