#! /usr/bin/env python3
"""
Calculate the number of daily commits for all git repositories.

- Create a web page of dates, commits.
- Draw a line plot of daily commits versus date.
- Must manually update the repository path list repositories.ods.
"""

from datetime import date, datetime, timedelta
from typing import Dict, List, NoReturn
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
    path_activity_group_sort = Path("activity_grouped_sorted.ods")
    path_repositories_file = Path("repositories.ods")
    path_activity_raw = Path("activity_raw.ods")
    df_columns = ["repo", "date", "commits"]
    repositories_column = "Repository path"
    output_url = "commits.html"
    header_title = "Commits"
    header_id = "commits"
    original_stdout = ds.html_begin(
        output_url=output_url, header_title=header_title, header_id=header_id
    )
    activity = recent_activity(
        column=repositories_column, repositories=path_repositories_file,
        df_columns=df_columns,
    )
    ds.save_file(df=activity, file_name=path_activity_raw)
    plot_recent_activity(
        activity=activity, df_columns=df_columns,
        path_activity_group_sort=path_activity_group_sort,
    )
    ds.html_end(original_stdout=original_stdout, output_url=output_url)


def commit_datetimes_since(
    *, repository: Path, since: date, until_inclusive: date = None
) -> List[datetime]:
    """
    Return all commit datetimes authored since given date.

    Parameters
    ----------
    repository : Path
        Path of repository.
    since : date
        Start date of commits.
    until_inclusive : date
        End date of commits.

    Returns
    -------
    author_date : List[datetime]:
    """
    if until_inclusive is None:
        until_inclusive = date.today()
    return [
        parsedate(timestr=author_date)
        for author_date in subprocess.check_output(
            args=[
                "git", "log", "--pretty=%aI", "--author=Gilles",
                f"--since={since.isoformat()}",
                f"--until={until_inclusive.isoformat()}",
            ],
            cwd=str(repository),
            universal_newlines=True,
        ).splitlines()
    ]


def repository_paths(*, column: str, repositories: Path) -> List[Path]:
    """
    List of repository paths.

    Parameters
    ---------
    column : str
        Column name.
    repositories : str
        Path of the repositories.

    Returns
    -------
    List[Path]
    """
    return [
        Path.home() / repository_path
        for repository_path in ds.read_file(
            file_name=repositories,
            usecols=[column],
        )[column]
    ]


def repo_date_counts(*, repo: Path) -> Dict[date, int]:
    """
    Dictionary of commits per day.

    Parameters
    ----------
    repo : Path
        Path of repository.

    Returns
    -------
    date : Dict[date, int]
    """
    ago_31 = date.today() - timedelta(days=31)
    return {
        date: len(list(commits))
        for date, commits in groupby(
            sorted(
                commit_datetimes_since(
                    repository=repo, since=ago_31, until_inclusive=None
                )
            ),
            key=lambda dt: dt.date(),
        )
    }


def recent_activity(
    *, column: str, repositories: Path, df_columns: List[str]
) -> pd.DataFrame:
    """
    Dataframe of known commits

    Parameters
    ----------
    column : str
        Column label in .ods file.
    repositories : Path
        Path of .ods file.
    df_columns : List[str]
        List of column labels to create.

    Returns
    -------
    pd.DataFrame
    """
    last_31_days = [date.today() - timedelta(days=i) for i in range(31)]
    paths = repository_paths(column=column, repositories=repositories)
    known_commits = {repo: repo_date_counts(repo=repo) for repo in paths}
    df = pd.DataFrame(
        [
            (repo, date, known_commits[repo].get(date, 0))
            for repo in paths
            for date in last_31_days
        ],
        columns=df_columns,
    ).astype(
        dtype={
            df_columns[0]: "str", df_columns[1]: "datetime64[ns]",
            df_columns[2]: "int64",
        }
    )
    return df


def plot_recent_activity(
    *, activity: pd.DataFrame,
    df_columns: List[str],
    path_activity_group_sort: Path
) -> NoReturn:
    """
    Line plot of number commits versus date.

    Parameters
    ----------
    activity : pd.DataFrame
        DataFrame of commit activity.
    df_columns : List[str]
        List of column labels to create.
    """
    y_label = "Number of commits"
    title = "Daily commits"
    figsize = (12, 6)
    x_label = "Date"
    if activity is None:
        # added next line instead of second line down
        pass
        # activity = recent_activity()
    commits = activity.groupby(df_columns[1]).agg("sum").reset_index()
    fig, ax = ds.plot_line_x_y(
        # X=commits.index,
        X=commits[df_columns[1]],
        y=commits[df_columns[2]],
        figsize=figsize,
    )
    ax.set_ylim(bottom=-1)
    ax.xaxis.set_major_formatter(formatter=mdates.DateFormatter("%m-%d"))
    ax.set_ylabel(ylabel=y_label)
    ax.set_xlabel(xlabel=x_label)
    ax.set_title(label=title)
    median_value = commits[df_columns[2]].median()
    ax.axhline(y=median_value, color="#33bbee", label=int(median_value))
    ax.legend(frameon=False)
    ds.despine(ax=ax)
    fig.savefig(fname="commits_daily.svg", format="svg")
    ds.html_figure(file_name="commits_daily.svg")
    print(f"Commits by date\n{commits}\n")
    print(f"Median commits: {median_value.astype(dtype='int')}\n")
    commits_grouped_sorted = commits.sort_values(by="commits")
    commits_grouped_sorted["order"] = range(1, 32, 1)
    print(f"Commits by ascending value\n{commits_grouped_sorted}\n")
    print(f"Median commits: {median_value.astype(dtype='int')}")
    ds.save_file(df=commits_grouped_sorted, file_name=path_activity_group_sort)


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
