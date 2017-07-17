#! /usr/bin/env python3

# Key Process Indicators (KPIs)
#
# This code will calculate the number of commits and plot a line graph of
# commits v. date.
#
# Import the required libraries and modules.
#
# Read the csv data file. It is encoded in UTF-8.
# There are several columns of daily commits.
# Set "date" as the index.
#
# Calculate a column of total daily commits.
#
# Calculate a column of the median of the column of total daily commits.
# One day fix this so that it's not an additional column, but a number to plot.
#
# Define the graph title and subtitle, and the x and y axis labels.
#
# Create a grpah of "total commits v. date".
#
# Create a single subplot.
#
# Plot "total commits v. date".
#
# Remove the top and right spines.
#
# Place ticks outside the axes.
#
# Add the Y axis label.
#
# Add the X axis label.
#
# Remove the box around the legend.
#
# Save the graph as svg and pdf.
#
# Close the current figure window.
#
# Create a graph of "total commits v. date".
#
# Create a single subplot.
#
# Plot "total commits v. date".
#
# Remove the top and right spines.
#
# Place the ticks outside the axes.
#
# Add the graph title and subtitle.
#
# Add the Y axis label.
#
# Add the X axis label.
#
# Remove the box around the legend.
#
# Save the graph as svg and pdf.
#
# Directory and OS commands
import os
# Check current working directory
current_working_directory = os.getcwd()
print (current_working_directory)
# Change directory
os.chdir("../../../")
current_working_directory = os.getcwd()
print (current_working_directory)

