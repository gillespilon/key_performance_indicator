#! /usr/bin/env python3
"""
Calculate the number of daily commits for all git repositories.

- Create a web page of dates, commits.
- Draw a line plot of daily commits versus date.
- Must manually update the repository path list repositories.ods.

time -f '%e' ./kpis.py
./kpis.py
"""

from datetime import date, datetime, timedelta
from typing import Dict, List
from itertools import groupby
from pathlib import Path
from os import chdir
import subprocess

from dateutil.parser import parse as parsedate
import matplotlib.dates as mdates
import datasense as ds
import pandas as pd


def main():
    chdir(Path(__file__).parent.resolve())  # required for cron
    df_columns = ["repo", "date", "commits"]
    path_repositories_file = Path("repositories.ods")
    repositories_column = "Repository path"
    output_url = "commits.html"
    header_title = "Commits"
    header_id = "commits"
    original_stdout = ds.html_begin(
        output_url=output_url, header_title=header_title, header_id=header_id
    )
    activity = recent_activity(
        column=repositories_column,
        repositories=path_repositories_file,
        df_columns=df_columns
    )
    plot_recent_activity(
        activity=activity,
        df_columns=df_columns
    )
    ds.html_end(original_stdout=original_stdout, output_url=output_url)


def commit_datetimes_since(
    repository: Path, since: date, until_inclusive: date = None
) -> List[datetime]:
    """
    Return all commit datetimes authored since given date.

    Parameters
    ----------
    repository : Path
    since : date
    until_inclusive : List[datetime]

    Returns
    -------
    author_date : List[datetime]:
    """
    if until_inclusive is None:
        until_inclusive = date.today()
    return [
        parsedate(author_date)
        for author_date in subprocess.check_output(
            [
                "git",
                "log",
                "--pretty=%aI",
                "--author=Gilles",
                f"--since={since.isoformat()}",
                f"--until={until_inclusive.isoformat()}",
            ],
            cwd=str(repository),
            universal_newlines=True,
        ).splitlines()
    ]


def repository_paths(
    column: str,
    repositories: str
) -> List[Path]:
    """
    List of repository paths.

    Returns
    -------
    List[Path]
    """
    return [
        Path.home() / "documents" / "websites" / repository_path
        for repository_path in pd.read_excel(
            repositories,
            index_col=False,
            engine="odf",
            usecols=[column],
        )[column]
    ]


def repo_date_counts(repo: Path) -> Dict[date, int]:
    """
    Dictionary of commits per day.

    Parameters
    ----------
    repo : Path

    Returns
    -------
    date : Dict[date, int]
    """
    ago_31 = date.today() - timedelta(days=31)
    return {
        date: len(list(commits))
        for date, commits in groupby(
            sorted(commit_datetimes_since(repo, ago_31)),
            key=lambda dt: dt.date()
        )
    }


def recent_activity(
    column: 'str',
    repositories: 'str',
    df_columns: List[str]
) -> pd.DataFrame:
    """
    Dataframe of known commits

    Returns
    -------
    pd.DataFrame
    """
    last_31_days = [date.today() - timedelta(days=i) for i in range(31)]
    paths = repository_paths(
        column=column,
        repositories=repositories
    )
    known_commits = {repo: repo_date_counts(repo) for repo in paths}
    df = pd.DataFrame(
        [
            (repo, date, known_commits[repo].get(date, 0))
            for repo in paths
            for date in last_31_days
        ],
        columns=df_columns,
    ).astype(
        dtype={
            df_columns[0]: "str",
            df_columns[1]: "datetime64[ns]",
            df_columns[2]: "int64"
        }
    )
    return df


def plot_recent_activity(
    activity: pd.DataFrame,
    df_columns: List[str]
) -> None:
    """
    Line plot of number commits versus date.

    Parameters
    ----------
    activity    : pd.DataFrame
    """
    figsize = (12, 6)
    title = "Daily commits"
    y_label = "Number of commits"
    x_label = "Date"
    if activity is None:
        activity = recent_activity()
    commits = activity.groupby(df_columns[1]).agg("sum").reset_index()
    fig, ax = ds.plot_line_x_y(
        # X=commits.index,
        X=commits[df_columns[1]],
        y=commits[df_columns[2]],
        figsize=figsize,
    )
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.set_ylabel(ylabel=y_label, fontweight="bold")
    ax.set_xlabel(xlabel=x_label, fontweight="bold")
    ax.set_title(label=title, fontweight="bold")
    median_value = commits[df_columns[2]].median()
    ax.axhline(y=median_value, color="#33bbee", label=int(median_value))
    ax.legend(frameon=False)
    ds.despine(ax)
    fig.savefig(fname="commits_daily.svg", format="svg")
    ds.html_figure(file_name="commits_daily.svg")
    print(f"Commits by date\n{commits}\n")
    print(f"Median commits: {median_value.astype(dtype='int')}\n")
    print(f"Commits by ascending value\n{commits.sort_values(by='commits')}\n")
    print(f"Median commits: {median_value.astype(dtype='int')}")


if __name__ == "__main__":
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
# ).fillna(0).astype(dtype='int')
# df.to_csv('2.csvactivity
