#! /usr/bin/env python3
'''
Calculate invoice preparation time

./kpi_invoice_preparation.py
time -f '%e' ./kpi_invoice_preparation.py
'''

from typing import List

import matplotlib.axes as axes
import datasense as ds
import pandas as pd
import numpy as np

title = 'Invoicing cycle time'
subtitle = 'Start of invoice to invoice sent'
ylabel = 'Time (min)'
xlabel = 'Date'
columns = ['Start invoice', 'Send invoice', 'Total time']


def main():
    invoicing = pd.read_csv(
        'invoice_preparation_time.csv',
        parse_dates=['Date']
    )
    print(invoicing.head())
    print(invoicing.dtypes)
    df = calculate_cycle_time(
        invoicing,
        columns
    )
    print(df.head())
    print(df.dtypes)
    plot_cycle_time(
        invoicing,
        column_x='Date',
        column_y='Total time'
    )


def despine(ax: axes.Axes) -> None:
    """
    Remove the top and right spines of a graph.

    Parameters
    ----------
    ax : axes.Axes

    Example
    -------
    >>> despine(ax)
    """
    for spine in 'right', 'top':
        ax.spines[spine].set_visible(False)


def calculate_cycle_time(
        df: pd.DataFrame,
        columns: List[str]
        ) -> pd.DataFrame:
    '''
    Calculate cycle time with two columns, store in third column
    columns[0] == start time
    columns[1] == end time
    columns[2] == total time
    '''
    df[columns[0]] = pd.to_datetime(
        df[columns[0]],
        format='%H:%M'
    )
    df[columns[1]] = pd.to_datetime(
        df[columns[1]],
        format='%H:%M'
    )
    df[columns[2]] = (df[columns[1]] - df[columns[0]])
    df[columns[2]] = df[columns[2]] / np.timedelta64(1, 'm')
    return df


def plot_cycle_time(
        df: pd.DataFrame,
        column_x: str,
        column_y: str
        ) -> None:
    fig, ax = ds.plot_line_x_y(
        X=df[column_x],
        y=df[column_y]
    )
    despine(ax)
    ax.set_title(title + '\n' + subtitle)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    fig.savefig('invoice_cycle_time.svg', format='svg')


if __name__ == '__main__':
    main()
