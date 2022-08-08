###########################################
# written by: Mika Littor, Danny Ben-Zvi's Lab.
# This program contains functions that are used by all of the programs in the directory.
# Download this file in order to run them.
###########################################
from datetime import datetime, timedelta
import sys
import matplotlib.pyplot as plt
import numpy as np
import os.path
import statistics
import pandas as pd

# The representation of the columns in the csv file
from scipy.signal import savgol_filter

COL_DAY = 0
COL_MONTH = 1
COL_TIME = 2
COL_VALUE = 3
NUM_HOURS = 24  # number of hours for the plot

# GRAPH'S GUI
FONT_TITLE = {'color': 'black', 'size': 25, 'weight': 'bold'}
FONT_LABEL = {'color': 'black', 'size': 20, 'weight': 'bold'}
LABEL_SIZE = 15
LINE_WIDTH = 2

# define limit of the y axis
Y_AXIS_MAX = 210
Y_AXIS_MIN = 100

# Timing between the sliding windows
SLIDING_WINDOW_DIFF = 2

# SLIDING WINDOW
FIRST_POINT_WIN = datetime(1900, 1, 1, 0, 0)
LAST_POINT_WIN = datetime(1900, 1, 1, 18, 00)


def create_dict_date_values(file_path):
    """
    This function creates a dictionary.
    Every key represents a certain date that will have its own plot, and the values are lists.
    Every list has two list - the first of time (X) coordinates, and the second of the value (Y) coordinates.
    :param args_lst: list of arguments received from the user.
    :return: the dictionary with the representation of the data.
    """
    dict_data = {}
    # the first row in the file is the headers of the table, and therefore should not be added to the dictionary.
    first_row = True
    with open(file_path) as f:
        for row in f:
            if first_row:
                # the first row is a row of headers, therefore it shouldn't be added to the dictionary. s
                first_row = False
            else:
                row_data = list(row.split(","))
                key_row = row_data[COL_DAY] + " " + row_data[COL_MONTH]
                # converting the time into the format "H:M"
                if row_data[COL_TIME] != "":
                    time_row = datetime.strptime(str(row_data[COL_TIME]), '%H:%M')
                    time_row.replace(month=1, day=1, year=2022)
                    value_row = row_data[COL_VALUE]
                    # adding the data of the row to the dictionary.
                    if key_row not in dict_data.keys():
                        dict_data[key_row] = [[time_row], [value_row]]
                    else:
                        values = dict_data[key_row]
                        values[0].append(time_row)
                        values[1].append(value_row)
    return dict_data


def create_labels_for_x_axis(num_labels):
    """
    creates labels for the x axis. Every label represents a hourly time.
    :param num_labels: number of labels to crete
    :return: list of strings that represent the labels.
    """
    time_between_hours = int(NUM_HOURS / (num_labels - 1))
    lst_labels = []
    current_time = 0
    for i in range(num_labels):
        converted_time = "%s:00" % current_time
        lst_labels.append(converted_time)
        current_time += time_between_hours
    return lst_labels


def calc_per_day(window, dict_data, day):
    """
    :param window: times in datetime for a specific window
    :param dict_data:
    :param day: name of the day to calculate the median for
    :return: the median value of the current day inside the window
    """
    # the data recorded that belongs to that specific day.
    data_of_day = dict_data[day]
    # list that holds the values of the recorded data in the current window.
    lst_val_window = []
    for t in window:
        # checking if the time was recorded that day. If so, adds its value to
        index_time = check_datetime_in_lst(t, data_of_day[0])
        if index_time != None:
            # the time was in the list, therefore we insert it into
            lst_val_window.append(float(data_of_day[1][index_time]))
    if lst_val_window != []:
        return statistics.median(lst_val_window)
    else:
        return None


def check_datetime_in_lst(t, lst):
    """
    method to check if the t time is in lst.
    :param t: datetime object
    :param lst: list of datetimes
    :return: true if t is in lst (also of t + 1 minute) is in lst , else retruns false.
    """
    index_time = 0
    for timing in lst:
        if (t == timing) or (t == (timing + timedelta(minutes=1))):
            return index_time
        else:
            index_time += 1
    return None


def slide_data(dict_data, func, window_size, recording_space, type_plot):
    """
    :param func: func_to_slide_data_on
    :param dict_data:
    :return: list of 2 lists. the first hold datetime types in the sliding wondow, and the second contains the
    average value in every point using sliding window.
    """
    arr_times = arr_times_for_sliding_window(recording_space)
    i = 0
    # Initialize the list to return.
    moving_lst = [[], []]
    # Loop through the array to consider
    while i < len(arr_times) - window_size + 1:
        # Store elements from i to i+window_size in list to get the current window
        window = arr_times[i: i + window_size]
        # Calculate the average of current window
        window_average = func(type_plot, dict_data, window)
        # Store the average of current window in moving average list
        moving_lst[0].append(arr_times[i])
        moving_lst[1].append(window_average)
        # Shift window to right by one position
        i += 1
    return moving_lst


def datetime_range(start, end, delta):
    current = start
    while current <= end:
        yield current
        current += delta


def arr_times_for_sliding_window(recording_space):
    """
    creating an array of the times in the sliding window that is for 00:00 to 18:00. Every type is in datetime.
    :return:
    """
    return list(datetime_range(FIRST_POINT_WIN, LAST_POINT_WIN, timedelta(minutes=recording_space)))




