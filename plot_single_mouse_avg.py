###########################################
# written by: Mika Littor, Danny Ben-Zvi's Lab.
# This program creates a figure with multiple plots using module matplotlib in python 3.
# The figure represents the mean values for a single mouse using sliding window values, with 75% and 25% bars.
# The values are calculates using the data measured in all the days.
# The arguments needed in order for this program to run:
# 1) Name of the mouse.
# 2) Path to the CSV file that holds the data measured from a single mouse.
# 3) Size of the sliding window in minutes.
# 4) The time between every two recordings of the mouse
###########################################
from supplementary_file import *

# Location of the argument accepts by the user in the list received.
MOUSE_NAME_LOC_IN_ARGS = 0
PATH_LOC_IN_ARGS = 1
WINDOW_SIZE_LOC_IN_ARGS = 2
RECORDING_SPACE_LOC_IN_ARGS = 3
ARGS_NUMBER = 4
ERR_WRONG_ARGS_NUM = "\nUsage: 3 arguments\n 1) Mouse's name\n 2) Path to csv file with single mouse's data\n " \
                     "3) Sliding window size in minutes\n 4) Time in minutes between recordings\n"
ERR_PATH_NOT_EXISTS = "\nThe file does not exist on the path: "


def plot_data(slided_data_lst, args_lst):
    """
    Method to plot multiple times in one figure.
    It receives a list with the representation of the data in the csv file.
    """
    plt.rcParams['date.converter'] = 'concise'
    plt.yticks(range(0, 600, 10))
    y_coordinates = get_y_coordinates(slided_data_lst)
    y_coordinates_sorted = list(map(float, y_coordinates))
    plt.plot(slided_data_lst[0], y_coordinates_sorted, color=COLOR_HZ_SUBPLOT)
    # adding the error bars
    plt.fill_between(slided_data_lst[0], get_25_percentile(slided_data_lst), get_75_percentile(slided_data_lst))
    plt.title("Mean glucose levels in a single mouse: " + args_lst[
        MOUSE_NAME_LOC_IN_ARGS] + "\n sliding window size " + args_lst[WINDOW_SIZE_LOC_IN_ARGS] +
              " minutes", fontdict=FONT_TITLE)
    plt.xlabel("Time\n", fontdict=FONT_LABEL)
    plt.ylabel("Glucose Levels\n", fontdict=FONT_LABEL)
    locs, labels = plt.xticks()
    new_xticks = create_labels_for_x_axis(len(locs))
    plt.xticks(locs, new_xticks)
    plt.show()


def calc_avg(window, dict_data):
    """
    :param window: times in datetime for a specific window
    :param dict_data:
    :return: list that contains the percentage 25, median, and percentage 75 for every day
    """
    # need to figure out how to calculate the average in every window.
    # maybe calculate the average window for every day, and then calculate the average for the days.
    mean_lst = []
    for day in dict_data.keys():
        avg_current_day = calc_per_day(window, dict_data, day)
        if avg_current_day != -10:
            mean_lst.append(avg_current_day)
    # returning the avg calculation
    if mean_lst != []:
        mean = statistics.mean(mean_lst)
        percentile_75 = np.percentile(mean_lst, 75)
        percentile_25 = np.percentile(mean_lst, 25)
        return [percentile_25, mean, percentile_75]
    else:
        return None


def validation_of_args(args_lst):
    """
    checks if the args are valid - meaning there are only two, and the second is a valid path.
    :param args_lst: list of arguments (not including the first argument as the path to this python file.
    """
    if len(args_lst) != ARGS_NUMBER:
        raise IndexError(ERR_WRONG_ARGS_NUM)
    path = args_lst[PATH_LOC_IN_ARGS]
    if not os.path.exists(path):
        raise IOError(ERR_PATH_NOT_EXISTS + path)


def main():
    args_lst = sys.argv[1:]
    validation_of_args(args_lst)
    dict_data = create_dict_date_values(args_lst[PATH_LOC_IN_ARGS])
    # window_size_ele is a parameter used for calculation of the sliding window
    window_size_ele = int(int(args_lst[WINDOW_SIZE_LOC_IN_ARGS]) / int(args_lst[RECORDING_SPACE_LOC_IN_ARGS]) + 1)
    slided_data_lst = slide_data(dict_data, calc_avg, window_size_ele, int(args_lst[RECORDING_SPACE_LOC_IN_ARGS]))
    plot_data(slided_data_lst, args_lst)


if __name__ == "__main__":
    main()
