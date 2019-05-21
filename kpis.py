#! /usr/bin/env python3

'''
Calculate the number of daily commits for all git repositories.
Draw a scatter plot of daily commits versus date.
'''

# time -f '%e' ./kpis.py > kpis.txt
# ./kpis.py > kpis.txt


import subprocess
from os import chdir
from typing import Union, List, Dict, Optional
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
from itertools import groupby

from dateutil.parser import parse as parsedate
import pandas as pd
import matplotlib.cm as cm
import matplotlib.axes as axes
from matplotlib.dates import DateFormatter
import datasense as ds
from modelicares import util

chdir(Path(__file__).parent.__str__())

c = cm.Paired.colors
# c[0] c[1] ... c[11]
# See "paired" in "qualitative colormaps"
# https://matplotlib.org/tutorials/colors/colormaps.html

title = 'Daily commits'
ylabel = 'Number of commits'
xlabel = 'Date'




def commit_datetimes_since(repository: Path,
                           since: date,
                           until_inclusive: date = None) -> List[datetime]:
    'Return all commit datetimes authored since given date'

    if until_inclusive is None:
        until_inclusive = date.today()
    return [
        parsedate(author_date)
        for author_date
        in subprocess.check_output(
            ['git', 'log',
             '--pretty=%aI',
             '--author=Gilles',
             f'--since={since.isoformat()}',
             f'--until={until_inclusive.isoformat()}'],
            cwd=str(repository),
            universal_newlines=True
        ).splitlines()
    ]


def repository_paths() -> List[Path]:
    return [
        Path.home() / 'documents' / 'websites' / repository_path
        for repository_path
        in pd.read_csv('repositories.csv',
                       index_col=False,
                       usecols=['Repository path'])
              ['Repository path']
    ]


def repo_date_counts(repo: Path) -> Dict[date, int]:
    ago_30 = date.today() - timedelta(days=30)
    return {
        date: len(list(commits))
        for date, commits
        in groupby(sorted(commit_datetimes_since(repo, ago_30)),
                   key=lambda dt: dt.date())
    }


def recent_activity() -> pd.DataFrame:
    last_30_days = [
        date.today() - timedelta(days=i)
        for i
        in range(30)
    ]
    paths = repository_paths()
    known_commits = {
        repo: repo_date_counts(repo)
        for repo
        in paths
    }
    return pd.DataFrame(
        [(repo, date, known_commits[repo].get(date, 0))
         for repo in paths
         for date in last_30_days],
        columns=['repo', 'date', 'commits'],
    ).set_index(['repo', 'date'])


def despine(ax: axes.Axes) -> None:
    '''
    Remove the top and right spines of a graph.
    '''
    for spine in 'right', 'top':
        ax.spines[spine].set_color('none')


def plot_recent_activity(activity: Optional[pd.DataFrame] = None) -> None:
    if activity is None:
        activity = recent_activity()
    commits = activity.reset_index().groupby('date').agg('sum')
    ax = commits.plot.line(y='commits',
                           legend=False,
                           color=c[0],
                           rot=90,
                           figsize=(8,6))
    ax.get_xaxis().set_major_formatter(DateFormatter('%m-%d'))
    # ax.figure.subplots_adjust(bottom=0.2)
    ax.set_ylabel('commits')
    ax.set_xlabel('date')
    ax.set_title(title, fontweight='bold')
    ax.autoscale(tight=False)
    ax.axhline(y=commits['commits'].median(), color=c[1])
    # ax.annotate('median', xy=(0, commits['commits'].median()), xytext=(0, commits['commits'].median()))
    #util.add_hlines(ax=ax, positions=[min(y), max(y)], labels=["min", "max"], color='r', ls='--')
    despine(ax)
    ax.figure.savefig('commits_daily.svg', format='svg')
    # ax.figure.savefig('commits_daily.png', format='png')
    # ax.figure.savefig('commits_daily.pdf', format='pdf')


if __name__ == '__main__':
    activity = recent_activity()
    plot_recent_activity(activity)
    activity.to_csv('activity.csv')


# TODO: Do this with a cross join between a pd time series from -30, 0 and all
#       repos, not with a list comprehension.
#df = pd.DataFrame(
#    [(repo, date)
#     for repo in paths
#     for date in last_30_days],
#    columns=['repo', 'date'],
#).set_index(['repo', 'date']).join(
#    pd.DataFrame(
#        [(repo, date, commits)
#         for repo in paths
#         for date, commits in repo_date_counts(repo).items()],
#        columns=['repo', 'date', 'commits'],
#    ).set_index(['repo', 'date']),
#    how='left',
#).fillna(0).astype(int)
#df.to_csv('2.csv')
