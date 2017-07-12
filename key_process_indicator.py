#! /usr/bin/env python3

# Key process indicator
#
# This code will calculate the number of commits and plot a line graph of
# commits v. date.
#
# Import the required libraries and modules.
#
# Read the data file.
# The file format is csv utf-8. There are several columns of daily commits.
#
# Calculate a column of total daily commits.
#
# Calculate the median for the total number of commits. This will be used
# for the median line.
# Calculate the minimum for the total number of commits. This will be used
# for plotting the median line.
# Calculate the maxium for the total number of commits. This will be used
# for plotting themedian line.
#
# Define the graph title.
# Define the graph subtitle.
# Define the graph y axis label.
# Define the graph x axis label.
#
# Plot a graph of daily commits for each KPI v. the date.
# Save the graph as svg, png, and pdf.
#
# Plot a graph of total commits v. the date.
# Save the graph as svg, png, and pdf.
# Directory and OS commands
import os
# Check current working directory
current_working_directory = os.getcwd()
print (current_working_directory)
# Change directory
os.chdir("../../../")
current_working_directory = os.getcwd()
print (current_working_directory)

