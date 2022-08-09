<center>
# Simple Continuous Glucose Monitoring in Freely Moving Mice 
</center>

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
   matplotlib
   numpy
   os
   scipy
   statistics
   sys
   ```
2. CSV file for every mouse with the data measured using the CGM.

   The following format is best for creating neat plots 
(you can change the month column to contain month numbers if you wish to).

   | Day |  Month  | Time (HH:MM) | Value | 
   |:---:|:-------:|:------------:|:-----:|
   |  1  | January |    00:00     |  180  |
   |  2  | January |    00:02     |  182  |
   |  3  | January |    00:04     |  187  |

## Setup
1. Create a working directory
2. Add to the working directory the CSV files needed with the wanted data
3. Download from GitHub the file that creates the plot you are interested in 
4. Download from GitHub the supplementary file 
5. Add the files from 3+4 to the working directory
6. Run the file from 2 using a workbench for python
7. Enter the arguments needed for the program by the file according to the documentation below

#### Special Setup for the [plot_all_mice_avg](plot_all_mice.py) file:
1. Name each one of the CSV files inside the working directory 
after the name of the mouse it represents 
(e.g. the data of the mouse "Miki" should be stored inside "Miki.csv")
2. Edit the global variable ```NAME_MICE``` (list of strings) inside the [plot_all_mice_avg](plot_all_mice.py) 
file according to the mice's names 

## Files
### [FILE: supplementary_file](supplementary_file.py)
Add the supplementary file to your working directory (see Setup).
It contains code that is necessary for creating any of the plots.

### [FILE: multiple_plots_raw](multiple_plots_raw.py)
Creating a plot that shows the **"raw"** data recorded on a **single** mouse. 
Each day that was recorded appears as a single colored line on the plot.
The x-axis represents the time from 00:00 to 24:00, and the y-axis the glucose levels measured.

```
Arguments:
1) Mouse's name 
2) Path to the CSV file that holds the data measured from a single mouse, inside the working directory
```

![raw_image](graphs/raw%20data%20single%20mouse.png)

### [FILE: plot_single_mouse_per_day](plot_single_mouse_per_day.py)
Creating a plot that shows the **mean** glucose levels measured on a **single** mouse
during the time of recording. The x-axis represents the time from 00:00 to 24:00, 
and the y-axis the glucose levels measured. 

The mean line on the graph is calculated using "sliding window" technic. 
For (x, y) point on the line: y is the mean glucose levels 
measured from x to (x + window_size). When "window_size" is a parameter given by
the user (see below).

The graph also has "standard error bars", which show the 25 and 75 percentile calculated from the data.

Arguments:
```
1) Mouse's name
2) Path to the CSV file that holds the data measured from a single mouse, 
inside the working directory
3) Size of the sliding window in minutes
4) The time between every two recordings of the mouse (depends on the CGM sampling)
5) 
```

### [FILE: plot_single_mouse_std](plot_single_mouse_std.py)
Creating a plot similar to the one created by [plot_single_mouse_avg](plot_single_mouse_avg.py)
(see above), except for that the main line on the current plot represents the **median**.

Arguments:
```
1) Mouse's name
2) Path to the CSV file that holds the data measured from a single mouse, 
inside the working directory
3) Size of the sliding window in minutes
4) The time between every two recordings of the mouse (depends on the CGM sampling)
```

### [FILE: plot_all_mice_avg](plot_all_mice.py)
Creating a plot that shows the **mean** glucose levels measured on **all** mice during
the time of recording. The x-axis represents the time from 00:00 to 24:00, 
and the y-axis the glucose levels measured. 

_Each line on the graph represents the mean values of a single mouse._ It is calculated using "sliding window" technic. 
For (x, y) point on the line: y is the mean glucose levels 
measured from x to (x + window_size). When "window_size" is a parameter given by
the user (see below). 
In other words, this plot is a _combination of the plots_ created by the file 
[plot_single_mouse_avg](plot_single_mouse_avg.py) (see above) for all the mice. 

Arguments:
```
1) Path to the working directory
2) Size of the sliding window in minutes.
3) The time between every two recordings of the mouse (depends on the CGM sampling)
```
