#! /usr/bin/env python3


'''
Calculate invoice preparation time

./kpi_invoice_preparation.py
python kpi_invoice_preparatio.py
time -f '%e' ./kpi_invoice_preparation.py
'''


import pandas as pd
import numpy as np
import matplotlib.axes as axes

def despine(ax: axes.Axes) -> None:
    '''
    Remove the top and right spines of a graph.
    '''
    for spine in 'right', 'top':
        ax.spines[spine].set_color('none')


invoicing = pd.read_csv('invoice_preparation_time.csv',
                        parse_dates=True,
                        index_col='Date')
invoicing['Start invoice'] = pd.to_datetime(invoicing['Start invoice'],
                                            format='%H:%M')
invoicing['Send invoice'] = pd.to_datetime(invoicing['Send invoice'],
                                           format='%H:%M')
invoicing['total_time'] = (invoicing['Send invoice'] -
                           invoicing['Start invoice'])
invoicing['Total time'] = invoicing['total_time'] / np.timedelta64(1, 'm')
invoicing = invoicing.drop(['total_time'], axis=1)
title = 'Invoicing cycle time'
subtitle = 'Start of invoice to invoice sent'
ylabel = 'Time (min)'
xlabel = 'Date'
ax = invoicing['Total time'].plot.line(legend=False, marker='o', markersize=3)
ax.axis('auto')
despine(ax)
ax.set_title(title + '\n' + subtitle)
ax.set_ylabel(ylabel)
ax.set_xlabel(xlabel)
ax.figure.savefig('invoice_cycle_time.svg', format='svg')
ax.figure.savefig('invoice_cycle_time.pdf', format='pdf')
