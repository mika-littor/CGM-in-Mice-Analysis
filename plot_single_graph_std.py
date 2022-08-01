###########################################
# written by: Mika Littor, Danny Ben-Zvi's Lab.
# This program creates a figure with multiple plots using module matplotlib in python 3.
# The figure represents the median values for a single mouse using sliding window values
# The arguments needed in order for this program to run:
# 1) Name of the mouse.
# 2) Path to the CSV file that holds the data measured from a single mouse.
# 3) Size of the sliding window in minutes.
# 4) The time between every two recordings of the mouse
###########################################
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import statistics
import os.path

# Location of the argument accepts by the user in the list received.
MOUSE_NAME_LOC_IN_ARGS = 0
PATH_LOC_IN_ARGS = 1
WINDOW_SIZE_LOC_IN_ARGS = 2
RECORDING_SPACE_LOC_IN_ARGS = 3
ARGS_NUMBER = 4
ERR_WRONG_ARGS_NUM = "\nUsage: 3 arguments\n 1) Mouse's name\n 2) Path to csv file with single mouse's data\n " \
                     "3) Sliding window size in minutes\n 4) Time in minutes between recordings\n"
ERR_PATH_NOT_EXISTS = "\nThe file does not exist on the path: "

COL_DAY = 0
COL_MONTH = 1
COL_TIME = 2
COL_VALUE = 3
NUM_HOURS = 24  # number of hours for the plot

# GRAPH'S GUI
FONT_TITLE = {'family': 'Bookman Old Style', 'color': 'navy', 'size': 25}
FONT_LABEL = {'family': 'Bookman Old Style', 'color': 'black', 'size': 20}

# SLIDING WINDOW
FIRST_POINT_WIN = datetime(1900, 1, 1, 0, 0)
LAST_POINT_WIN = datetime(1900, 1, 1, 18, 0)

COLOR_HZ_SUBPLOT = "#33FFBE"
COLOR_HT_SUBPLOT = "#BE33FF"


def create_dict_date_values(args_lst):
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
    with open(args_lst[PATH_LOC_IN_ARGS]) as f:
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


def plot_data(slided_data_lst, args_lst):
    """
    Method to plot multiple times in one figure.
    It receives a list with the representation of the data in the csv file.
    """
    plt.rcParams['date.converter'] = 'concise'
    plt.yticks(range(0, 600, 10))
    y_coordinates = get_y_coordinates(slided_data_lst)
    y_coordinates_sorted = list(map(int, y_coordinates))
    plt.plot(slided_data_lst[0], y_coordinates_sorted, color=COLOR_HZ_SUBPLOT)
    # adding the error bars
    plt.fill_between(slided_data_lst[0], get_25_percentage(slided_data_lst), get_75_percentage(slided_data_lst))
    plt.title("Median glucose levels in a single mouse: " + args_lst[
        MOUSE_NAME_LOC_IN_ARGS] + "\n sliding window size " + args_lst[WINDOW_SIZE_LOC_IN_ARGS] +
              " minutes", fontdict=FONT_TITLE)
    plt.xlabel("Time\n", fontdict=FONT_LABEL)
    plt.ylabel("Glucose Levels\n", fontdict=FONT_LABEL)
    locs, labels = plt.xticks()
    new_xticks = create_labels_for_x_axis(len(locs))
    plt.xticks(locs, new_xticks)
    plt.show()

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


def get_y_coordinates(slided_data_lst):
    y_coordinates = []
    for lst in slided_data_lst[1]:
        y_coordinates.append(lst[1])
    return y_coordinates


def get_75_percentage(slided_data_lst):
    percentage_75_coordinates = []
    for lst in slided_data_lst[1]:
        percentage_75_coordinates.append(lst[2])
    return percentage_75_coordinates


def get_25_percentage(slided_data_lst):
    percentage_25_coordinates = []
    for lst in slided_data_lst[1]:
        percentage_25_coordinates.append(lst[0])
    return percentage_25_coordinates


def slide_data(dict_data, sliding_window_size, recording_space):
    """
    :param sliding_window_size: size of sliding window in minutes
    :param dict_data:
    :param recording_space - time between every two recordings of the mouse
    :return: list of 2 lists. the first hold datetime types in the sliding window, and the second contains the
    average value in every point using sliding window.
    """
    arr_times = arr_times_for_sliding_window(recording_space)
    i = 0
    # Initialize the list to return.
    moving_medians = [[], []]
    # Loop through the array to consider
    while i < len(arr_times) - sliding_window_size + 1:
        # Store elements from i to i+window_size in list to get the current window
        window = arr_times[i: i + sliding_window_size]
        #  returns a list that contains the percentage 25, median, and percentage 75 for every day
        window_median_lst = calc_median(window, dict_data)
        # Store the average of current window in moving average list
        moving_medians[0].append(arr_times[i])
        moving_medians[1].append(window_median_lst)
        # Shift window to right by one position
        i += 1
    return moving_medians


def calc_median(window, dict_data):
    """
    :param window: times in datetime for a specific window
    :param dict_data:
    :return: list that contains the percentage 25, median, and percentage 75 for every day
    """
    # need to figure out how to calculate the average in every window.
    # maybe calculate the average window for every day, and then calculate the average for the days.
    median_lst = []
    for day in dict_data.keys():
        avg_current_day = calc_median_per_day(window, dict_data, day)
        if avg_current_day != -10:
            median_lst.append(avg_current_day)
    # returning the avg calculation
    if median_lst != []:
        median = statistics.median(median_lst)
        percentile_75 = np.percentile(median_lst, 75)
        percentile_25 = np.percentile(median_lst, 25)
        return [percentile_25, median, percentile_75]
    else:
        return None


def calc_median_per_day(window, dict_data, day):
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
        if index_time != -10:
            # the time was in the list, therefore we insert it into
            lst_val_window.append(int(data_of_day[1][index_time]))
    if lst_val_window != []:
        return statistics.median(lst_val_window)
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


def arr_times_for_sliding_window(recording_space):
    """
    :param recording_space - time between every two recordings of the mouse
    creating an array of the times in the sliding window that is for 00:00 to 18:00. Every type is in datetime.
    :return:
    """
    return list(datetime_range(FIRST_POINT_WIN, LAST_POINT_WIN, timedelta(minutes=recording_space)))


def datetime_range(start, end, delta):
    current = start
    while current <= end:
        yield current
        current += delta


def validation_of_args(args_lst):
    """
    checks if the args are valid - meaning there are only two, and the second is a valid path.
    :param args_lst: list of arguments (not including the first argument as the path to this python file.
    """
    if len(args_lst) > ARGS_NUMBER:
        raise IndexError(ERR_WRONG_ARGS_NUM)
    path = args_lst[PATH_LOC_IN_ARGS]
    if not os.path.exists(path):
        raise IOError(ERR_PATH_NOT_EXISTS + path)


def main():
    # path_file = path_to_mouse(NAME_MOUSE)
    args_lst = sys.argv[1:]
    validation_of_args(args_lst)
    dict_data = create_dict_date_values(args_lst)
    window_size_ele = int(int(args_lst[WINDOW_SIZE_LOC_IN_ARGS]) / int(args_lst[RECORDING_SPACE_LOC_IN_ARGS]) + 1)
    slided_data_lst = slide_data(dict_data, window_size_ele, int(args_lst[RECORDING_SPACE_LOC_IN_ARGS]))
    plot_data(slided_data_lst, args_lst)


if __name__ == "__main__":
    main()
