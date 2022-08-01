#####
# written by Mika Littor.
#####

from csv import reader
import sys

import matplotlib.dates
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from datetime import datetime, timedelta
import numpy as np
import random

BASIC_FILE_PATH = r"C:\Users\mikal\Documents\LAB2\mice_sugar_prj"
NAME_MICE = {"Naw1_M3": "HZ", "Naw1_M4": "HZ", "Naw2_M6": "HT", "Naw2_M8": "HZ", "Naw2_M10": "HT",
             "Naw2_M11": "HT", "Naw3_M2": "HT", "Naw3_M3": "HZ"}
COL_DAY = 0
COL_MONTH = 1
COL_TIME = 2
COL_VALUE = 3

# GRAPH'S GUI
FONT_TITLE = {'family': 'Bookman Old Style', 'color': 'navy', 'size': 25}
FONT_LABEL = {'family': 'Bookman Old Style', 'color': 'black', 'size': 20}

# SLIDING WINDOW
WINDOW_SIZE = 11
RECORDING_SPACE = 2  # 2 mins between each recording
FIRST_POINT_WIN = datetime(1900, 1, 1, 0, 0)
LAST_POINT_WIN = datetime(1900, 1, 1, 18, 0)

COLOR_HZ_SUBPLOT = "#33FFBE"
COLOR_HT_SUBPLOT = "#BE33FF"


def create_dict_date_values(file_path):
    """
    This function creates a dictionary.
    Every key represents a certain date that will have its own plot, and the values are lists.
    Every list has two list - the first of time (X) coordinates, and the second of the value (Y) coordinates.
    :return: the dictionary with the representation of the data.
    """
    dict_data = {}
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


def multiple_plots(dict_data):
    """
    Method to plot multiple times in one figure.
    It receives a dictionary with the representation of the data in the csv file.
    Every key in the dictionary represent a different date that will have its own plot ont the graph.
    """
    fig, ax = plt.subplots()
    plt.rcParams['date.converter'] = 'concise'
    plt.yticks(range(0, 600, 10))

    # setting the color for the
    # cm = plt.get_cmap('tab20b')  # in order to set the color for the graphs
    # num_colors = len(dict_data.keys())
    # picking color for the plot
    # ax.set_prop_cycle('color', [cm(1. * i / num_colors) for i in range(num_colors)])

    for mouse, coordinates in dict_data.items():
        # sorting the y coordinates
        y_coordinates = list(map(int, coordinates[1]))
        # plotting the current date
        if NAME_MICE[mouse] == "HZ":
            ax.plot(coordinates[0], y_coordinates, label=(mouse + ":" + NAME_MICE[mouse]), color=COLOR_HZ_SUBPLOT)
        else:
            ax.plot(coordinates[0], y_coordinates, label=(mouse + ":" + NAME_MICE[mouse]), color=COLOR_HT_SUBPLOT)
    plt.legend(prop={'size': 20})
    create_plot(plt)


def create_plot(plt):
    """
    showing the plot created
    :param plt: the plot
    """
    sliding_window = str(int((WINDOW_SIZE - 1) * RECORDING_SPACE))
    plt.title("Avg Glucose Levels vs Time\n(sliding window size " + sliding_window + " minutes)\n", fontdict=FONT_TITLE)
    plt.xlabel("Time\n", fontdict=FONT_LABEL)
    plt.ylabel("Glucose Levels\n", fontdict=FONT_LABEL)
    plt.legend(loc=0)
    locs, labels = plt.xticks()
    new_xticks = ["00:00", "02:00", "04:00", "06:00", "8:00", "10:00", "12:00", "14:00", "16:00", "18:00"]
    plt.xticks(locs, new_xticks)
    plt.show()


def slide_data(dict_data):
    """
    :param dict_data:
    :return: list of 2 lists. the first hold datetime types in the sliding wondow, and the second contains the
    average value in every point using sliding window.
    """
    arr_times = arr_times_for_sliding_window()

    i = 0
    # Initialize the list to return.
    moving_averages = [[], []]

    # Loop through the array to consider
    while i < len(arr_times) - WINDOW_SIZE + 1:
        # Store elements from i to i+window_size in list to get the current window
        window = arr_times[i: i + WINDOW_SIZE]

        # Calculate the average of current window
        window_average = calc_avg(window, dict_data)

        # Store the average of current window in moving average list
        moving_averages[0].append(arr_times[i])
        moving_averages[1].append(window_average)

        # Shift window to right by one position
        i += 1

    return moving_averages


def calc_avg(window, dict_data):
    """
    :param window: times in datetime for a specific window
    :param dict_data:
    :return: the average value in the window to be plotted
    """
    # need to figure out how to calculate the average in every window.
    # maybe calculate the average window for every day, and then calculate the average for the days.
    avgs_lst = []
    for day in dict_data.keys():
        avg_current_day = calc_avg_per_day(window, dict_data, day)
        if avg_current_day != -10:
            avgs_lst.append(avg_current_day)
    # returning the avg calculation
    if avgs_lst != []:
        return sum(avgs_lst) / len(avgs_lst)
    else:
        return None


def calc_avg_per_day(window, dict_data, day):
    """
    :param window: times in datetime for a specific window
    :param dict_data:
    :param day: name of the day to calculate the average for
    :return: the average value of the current day inside the window
    """
    # the data recorded that belongs to that specific day.
    data_of_day = dict_data[day]
    # list that holds the values of the recorded data in the current window.
    lst_val_window = []
    for t in window:
        # checking if the time was recorded that day. If so, adds its value to
        index_time = check_datetime_in_lst(t, data_of_day[0])
        if index_time != -10:
            # the time was in the list, therefore we insert it into
            lst_val_window.append(int(data_of_day[1][index_time]))

    if lst_val_window != []:
        return sum(lst_val_window) / len(lst_val_window)
    else:
        return -10


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
    return -10


def arr_times_for_sliding_window():
    """
    creating an array of the times in the sliding window that is for 00:00 to 18:00. Every type is in datetime.
    :return:
    """
    return list(datetime_range(FIRST_POINT_WIN, LAST_POINT_WIN, timedelta(minutes=RECORDING_SPACE)))


def datetime_range(start, end, delta):
    current = start
    while current <= end:
        yield current
        current += delta


def path_to_mouse(mouse):
    """
    :param mouse: name of the current mouse
    :return: path to the current mouse's file
    """
    return BASIC_FILE_PATH + "\\" + mouse + "\\" + mouse.replace(" ", "_") + "_Hours.csv"


def main():
    dict_mouse = {}
    for mouse in sorted(NAME_MICE.keys()):
        path_file = path_to_mouse(mouse)
        dict_data = create_dict_date_values(path_file)
        slided_data_dict = slide_data(dict_data)
        dict_mouse[mouse] = slided_data_dict
    print(dict_mouse)
    multiple_plots(dict_mouse)


if __name__ == "__main__":
    main()




