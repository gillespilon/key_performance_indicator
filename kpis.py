#! /usr/bin/env python3

'''
Calculate the number of daily commits for all git repositories.
Draw a scatter plot of daily commits versus date.

    time -f '%e' ./kpis.py > kpis.txt
    ./kpis.py > kpis.txt
    ./kpis.py | tee kpis.txt
'''

# time -f '%e' ./kpis.py > kpis.txt
# ./kpis.py > kpis.txt


import subprocess
from os import chdir
from typing import List, Dict, Optional
from pathlib import Path
from datetime import date, datetime, timedelta
from itertools import groupby

from dateutil.parser import parse as parsedate
import pandas as pd
import matplotlib.cm as cm
import matplotlib.axes as axes
from matplotlib.dates import DateFormatter, DayLocator
from matplotlib.ticker import NullFormatter
from matplotlib.ticker import NullLocator
from matplotlib.ticker import MaxNLocator


chdir(Path(__file__).parent.__str__())


c = cm.Paired.colors  # c[0] c[1] ... c[11]
# https://matplotlib.org/tutorials/colors/colormaps.html


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
    ago_31 = date.today() - timedelta(days=31)
    return {
        date: len(list(commits))
        for date, commits
        in groupby(sorted(commit_datetimes_since(repo, ago_31)),
                   key=lambda dt: dt.date())
    }


def recent_activity() -> pd.DataFrame:
    last_31_days = [
        date.today() - timedelta(days=i)
        for i
        in range(31)
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
         for date in last_31_days],
        columns=['repo', 'date', 'commits'],
    ).set_index(['repo', 'date'])


def despine(ax: axes.Axes) -> None:
    '''
    Remove the top and right spines of a graph.

    Used to enforce standard and *correct* style. There is only one x, and one
    y axis, left and bottom, therefore there should only be these axes.
    '''
    for spine in 'right', 'top':
        ax.spines[spine].set_visible(False)


def plot_recent_activity(activity: Optional[pd.DataFrame] = None) -> None:
    title = 'Daily commits'
    ylabel = 'Number of commits'
    xlabel = 'Date'
    if activity is None:
        activity = recent_activity()
    commits = activity.reset_index().groupby('date').agg('sum')
    ax = commits.plot(y='commits',
                      legend=False,
                      style='.-',
                      color=c[0],
                      rot=90,
                      figsize=(12, 6),
                      x_compat=True)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    print(f'Commits by date\n{commits}\n')
    print(f"Median commits: {commits['commits'].median().astype(int)}\n")
    print(f"Commits by ascending value\n{commits.sort_values(by='commits')}\n")
    print(f"Median commits: {commits['commits'].median().astype(int)}")
    commits['low'] = commits['commits'].where(commits['commits'].between(0, 0))
    ax.plot(commits['low'], marker='x', color=c[5])
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(DateFormatter('%d'))
    ax.set_title(title, fontweight='bold')
    ax.autoscale(tight=False)
    ax.axhline(y=commits['commits'].median(), color=c[1])
    despine(ax)
    ax.figure.savefig('commits_daily.svg', format='svg')


if __name__ == '__main__':
    activity = recent_activity()
    plot_recent_activity(activity)
    activity.to_csv('activity.csv')


# TODO: Do this with a cross join between a pd time series from -31, 0 and all
#       repos, not with a list comprehension.
# df = pd.DataFrame(
#     [(repo, date)
#     for repo in paths
#     for date in last_31_days],
#    columns=['repo', 'date'],
# ).set_index(['repo', 'date']).join(
#    pd.DataFrame(
#        [(repo, date, commits)
#         for repo in paths
#         for date, commits in repo_date_counts(repo).items()],
#        columns=['repo', 'date', 'commits'],
#    ).set_index(['repo', 'date']),
#    how='left',
# ).fillna(0).astype(int)
# df.to_csv('2.csv')
