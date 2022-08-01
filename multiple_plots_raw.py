###########################################
# written by: Mika Littor, Danny Ben-Zvi's Lab.
# This program creates a figure with multiple plots using module matplotlib in python 3. Each figure represents the
# raw data taken from a single mouse. Every plot on the figure has its own color, and it demonstrates a single day in
# which data was measured.
# The arguments needed in order for this program to run:
# 1) Name of the mouse.
# 2) Path to the CSV file that holds the data measured from a single mouse.
###########################################
import sys
import matplotlib.pyplot as plt
from datetime import datetime
import os.path

# Location of the argument accepts by the user in the list received.
MOUSE_NAME_LOC_IN_ARGS = 0
PATH_LOC_IN_ARGS = 1
ARGS_NUMBER = 2
ERR_WRONG_ARGS_NUM = "\nUsage: 2 arguments. 1) Mouse's name 2) Path to csv file with single mouse's data\n"
ERR_PATH_NOT_EXISTS = "\nThe file does not exist on the path: "

# The representation of the columns in the csv file
COL_DAY = 0
COL_MONTH = 1
COL_TIME = 2
COL_VALUE = 3
NUM_HOURS = 24


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
                time_row = datetime.strptime(str(row_data[COL_TIME]), '%H:%M')
                value_row = row_data[COL_VALUE]
                # adding the data of the row to the dictionary.
                if key_row not in dict_data.keys():
                    dict_data[key_row] = [[time_row], [value_row]]
                else:
                    values = dict_data[key_row]
                    values[0].append(time_row)
                    values[1].append(value_row)
    return dict_data


def multiple_plots(dict_data, args_lst):
    """
    Method to plot multiple times in one figure.
    It receives a dictionary with the representation of the data in the csv file.
    Every key in the dictionary represent a different date that will have its own plot ont the graph.
    :param args_lst: list of arguments received from the user.
    """
    fig, ax = plt.subplots()
    plt.rcParams['date.converter'] = 'concise'
    plt.yticks(range(0, 600, 10))
    for date, coordinates in dict_data.items():
        # sorting the y coordinates
        y_coordinates = list(map(int, coordinates[1]))
        # plotting the current date
        ax.plot(coordinates[0], y_coordinates, label=date)
    create_plot(plt, args_lst[MOUSE_NAME_LOC_IN_ARGS])


def create_plot(plt, mouse_name):
    """
    showing the plot created
    :param plt: the plot
    :param mouse_name: name of the mouse
    """
    font1 = {'family': 'Arial', 'color': 'blue', 'size': 20}
    font2 = {'family': 'Arial', 'color': 'blue', 'size': 15}
    plt.title(mouse_name, fontdict=font1)
    plt.xlabel("values", fontdict=font2)
    plt.ylabel("Time", fontdict=font2)
    plt.legend(loc=0)
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
    args_lst = sys.argv[1:]
    validation_of_args(args_lst)
    dict_data = create_dict_date_values(args_lst)
    multiple_plots(dict_data, args_lst)


if __name__ == "__main__":
    main()
