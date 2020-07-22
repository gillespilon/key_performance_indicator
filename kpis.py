#! /usr/bin/env python3

'''
Calculate the number of daily commits for all git repositories.
Draw a line plot of daily commits versus date.
Must manually update the repository path list repositories.ods.

time -f '%e' ./kpis.py > kpis.txt
time -f '%e' ./kpis.py
./kpis.py > kpis.txt
./kpis.py
'''

from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
from itertools import groupby
from pathlib import Path
from os import chdir
import subprocess

from dateutil.parser import parse as parsedate
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.cm as cm
import pandas as pd


chdir(Path(__file__).parent.__str__())


c = cm.Paired.colors


def main():
    activity = recent_activity()
    plot_recent_activity(activity)
    activity.to_csv('activity.csv')


def commit_datetimes_since(repository: Path,
                           since: date,
                           until_inclusive: date = None) -> List[datetime]:
    '''
    Return all commit datetimes authored since given date
    '''

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
    '''
    List of repository paths
    '''
    return [
        Path.home() / 'documents' / 'websites' / repository_path
        for repository_path
        in pd.read_excel('repositories.ods',
                         index_col=False,
                         engine='odf',
                         usecols=['Repository path'])
           ['Repository path']
    ]


def repo_date_counts(repo: Path) -> Dict[date, int]:
    '''
    Dictionary of commits per day
    '''
    ago_31 = date.today() - timedelta(days=31)
    return {
        date: len(list(commits))
        for date, commits
        in groupby(sorted(commit_datetimes_since(repo, ago_31)),
                   key=lambda dt: dt.date())
    }


def recent_activity() -> pd.DataFrame:
    '''
    Dataframe of known commits
    '''
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

    There is only one x axis, on the bottom, and one y axis, on the left.
    '''
    for spine in 'right', 'top':
        ax.spines[spine].set_visible(False)


def plot_recent_activity(activity: Optional[pd.DataFrame] = None) -> None:
    '''
    Line plot of number commits versus date
    '''
    title = 'Daily commits'
    ylabel = 'Number of commits'
    xlabel = 'Date'
    if activity is None:
        activity = recent_activity()
    commits = activity.reset_index().groupby('date').agg('sum')
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    fig.autofmt_xdate()
    ax.plot(commits['commits'], color=c[0])
    print(f'Commits by date\n{commits}\n')
    print(f"Median commits: {commits['commits'].median().astype(int)}\n")
    print(f"Commits by ascending value\n{commits.sort_values(by='commits')}\n")
    print(f"Median commits: {commits['commits'].median().astype(int)}")
    commits['low'] = commits['commits'].where(commits['commits'].between(0, 0))
    ax.plot(commits['low'], marker='x', color=c[5])
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontweight='bold')
    ax.autoscale(tight=False)
    ax.axhline(y=commits['commits'].median(), color=c[1])
    despine(ax)
    ax.figure.savefig('commits_daily.svg', format='svg')


if __name__ == '__main__':
    main()


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
