#! /usr/bin/env python3

# Key Performance Indicators (KPIs)
#
# In brevi
#
# Office workers create, update, and publish documents. Whether it's
# creating presentations, responding to emails, or doing statistical analysis,
# they are creating documents. Unlike a manufacturing environment, their
# output appears invisible to an observer of their work process. If such a
# worker were to commit their documents to a Git repository, they could make
# their work visible . These commits could then be reported as a key
# performance indicator (KPI).
#
# Data
# The data file is available
# [here (kpis.csv)](https://drive.google.com/file/d/0BzrdQfHR2I5Dc0o5X3puNHUxdTQ/view?usp=sharing).
# It consists of a date column and six KPI data columns. Dates are entered
# using ISO 8601 date format (yyyy-mm-dd). The KPI columns are the number of
# commits per KPI.
#
# Methodology
# A Git "commit" is a recorded change to a repository. Each day an office
# worker determines the number of commits made for each repository, records
# the values in the kpis.csv file, and executes kpis.py or kpis.ipynb. A
# graph of individual commits v. date and a graph of total commits v. date are
# created and saved in svg and pdf formats.
#
# Import the required libraries and modules.
import pandas as pd
import matplotlib.pyplot as plt

# Read the csv data file. It is encoded in UTF-8.
# There are several columns of daily commits.
# Set "date" as the index.
commits = pd.read_csv('kpis.csv', parse_dates=True, index_col='Date')
# Calculate a column of total daily commits.
commits['Total']= commits['ForteF'] + commits['Private'] + \
        commits['Support'] + commits['Jupyter'] + commits['Tableau'] + \
        commits['KPI'] + commits['MSHA'] + commits['Anscombe'] + \
        commits['Cholera'] + commits['ImpactEffort'] + commits['PSA'] + \
        commits['HT1ST'] + commits['HT2ST'] + commits['HTPT'] + \
        commits['ControlCharts']
# Calculate a column of the median of the column of total daily commits.
# One day fix this so that it's not an additional column, but a number to plot.
commits['Median'] = commits['Total'].median()

# Define the graph title and subtitle, and the x and y axis labels.
title = 'Key Performance Indicator'
subtitle = 'Git Commits'
ylabel = 'Commits'
xlabel = 'Date'

# Create a graph of "individual commits v. date".
#
# Create a single subplot.
ax1 = plt.subplot(111)
# Plot "total commits v. date".
commits[['Private', 'Support']] \
         .plot.line(legend=True, ax=ax1, marker='o', markersize=3)\
         .axis('auto')
# Remove the top and right spines.
for spine in 'right', 'top':
    ax1.spines[spine].set_color('none')
ax1.set_title(title + '\n' + subtitle)
# Add the Y axis label.
ax1.set_ylabel(ylabel)
# Add the X axis label.
ax1.set_xlabel(xlabel)
# Remove the box around the legend.
ax1.legend(frameon=False)
# Save the graph as svg and pdf.
ax1.figure.savefig('kpi_commits.svg', format='svg')
ax1.figure.savefig('kpi_commits.pdf', format='pdf')

# Close the current figure window.
plt.close()

# Create a graph of "total commits v. date".

# Create a single subplot.
ax2 = plt.subplot(111)
# Plot "total commits v. date".
commits['Total'].plot.line(legend=True, ax=ax2, marker='o', \
        markersize=3).axis('auto')
commits['Median'].plot.line(legend=True, ax=ax2).axis('auto')
# Remove the top and right spines.
for spine in 'right', 'top':
    ax2.spines[spine].set_color('none')
# Place the ticks outside the axes.
ax2.tick_params(direction='out')
ax2.xaxis.set_ticks_position('bottom')
ax2.yaxis.set_ticks_position('left')
# Add the graph title and subtitle.
#ax2.set_title(r'\textbf{' + title + '}' + '\n' + subtitle)
ax2.set_title(title + '\n' + subtitle)
# Add the Y axis label.
ax2.set_ylabel(ylabel)
# Add the X axis label.
ax2.set_xlabel(xlabel)
# Remove the box around the legend.
ax2.legend(frameon=False)
# Save the graph as svg and pdf
ax2.figure.savefig('kpi_commits_total.svg', format='svg')
ax2.figure.savefig('kpi_commits_total.pdf', format='pdf')
