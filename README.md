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
1. Create a working directory
2. Add to the working directory the CSV files needed with the wanted data
3. Download from GitHub the file that creates the plot you are interested in 
4. Download from GitHub the supplementary file 
5. Add the files from 3+4 to the working directory
6. Run the file from 2 using Python workbench 
7. Enter the arguments needed by the file according to the documentation below

NOTE: If you wish to run the [FILE: plot_all_mice_avg](plot_all_mice_avg.py) then 
each one of the CSV files inside the working directory should be named after the mouse its holds
the data for. 

## Files
### [FILE: supplementary_file](supplementary_file.py)
Add the supplementary file to your working directory (see Setup).
It contains code that is necessary for creating any of the plots.

### [FILE: multiple_plots_raw](multiple_plots_raw.py)
Creating a plot that shows the **"raw"** data recorded on a **single** mouse. 
Each day that was recorded appears as a single colored line on the plot.
The x-axis represents the time from 00:00 to 24:00, and the y-axis the glucose levels measured.

Arguments:
```
1. mouse's name 
2. Path to the CSV file that holds the data measured from a single mouse
```

### [FILE: plot_single_mouse_avg](plot_single_mouse_avg.py)
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

```

### [FILE: plot_single_mouse_std](plot_single_mouse_std.py)
Creating a plot similar to the one created by [plot_single_mouse_avg](plot_single_mouse_avg.py)
(see above), except for that the main line on the current plot represents the **median**.

Arguments:
```

```

### [FILE: plot_all_mice_avg](plot_all_mice_avg.py)
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

```
