# Simple Continuous Glucose Monitoring in Freely Moving Mice 

Doron Kleiman, Mika Littor, Mahmoud Nawas, Rachel Ben-Haroush Schyr, Danny Ben-Zvi 

## Introduction
Welcome to the homepage of the CGM (continuous glucose monitoring) analysis code!

This folder contains 5 code files written in Python 3.
The files produce plots out of data recorded from mice, using CGM.

You can reach us at [Ben-Zvi Lab](https://www.benzvilab.com/).

## Requirements 
1. Installation of Python 3 with the following packages:
    ```
   datetime
   matplotlib.pyplot
   numpy
   os.path
   statistics
   sys
   ```
2. CSV file with the columns... recorded as...
   adding an example...

## Setup
1. Download the file that creates the plot you are interested in 
2. Download the supplementary file 
3. Add the files to your working directory
4. Run the file from 1 using Python workbench 

## Files
### [FILE: supplementary_file](supplementary_file.py)
Add the supplementary file to your working directory (see Setup).
It contains code that is necessary for creating any of the plots.
### [FILE: multiple_plots_raw](multiple_plots_raw.py)
Creating a plot that shows the "raw" data recorded on a **single** mouse. 
Each day that was recorded appears as a single colored line on the plot.
The x-axis represents the time from 00:00 to 24:00, and the y-axis the glucose levels measured.
### [FILE: plot_single_mouse_avg](plot_single_mouse_avg.py)
Creating a plot that shows the mean glucose levels measured on a **single** mouse
during the time of recording. The x-axis represents the time from 00:00 to 24:00, 
and the y-axis the glucose levels measured. 

The mean line on the graph is calculated using "sliding window" technic. 
For (x, y) point on the line: y is the mean glucose levels 
measured from x to (x + window_size). When "window_size" is a parameter given by
the user (see below).

The graph also has "standard error bars", which show the 25% and the 75% mean values 
calculated from the data.
### [FILE: plot_single_mouse_std](plot_single_mouse_std.py)
Creating a plot
### [FILE: plot_all_mice_avg](plot_all_mice_avg.py)
Creating a plot
