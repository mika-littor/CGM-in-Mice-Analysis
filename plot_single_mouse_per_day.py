###########################################
# written by: Mika Littor, Danny Ben-Zvi's Lab.
# This program creates a figure with multiple plots using module matplotlib in python 3.
# The figure represents the mean/median values for a single mouse using sliding window values, with 75% and 25% bars.
# The values are calculates using the data measured in all the days.
# The arguments needed in order for this program to run:
# 1) Name of the mouse.
# 2) Path to the CSV file that holds the data measured from a single mouse.
# 3) Size of the sliding window in minutes.
# 4) The time between every two recordings of the mouse
# 5) MODE: median or mean - mode for plotting the median or the mean plot
###########################################
from supplementary_file import *

# Location of the argument accepts by the user in the list received.
MOUSE_NAME_LOC_IN_ARGS = 0
PATH_LOC_IN_ARGS = 1
WINDOW_SIZE_LOC_IN_ARGS = 2
RECORDING_SPACE_LOC_IN_ARGS = 3
TYPE_PLOT_LOC_IN_ARGS = 4
ARGS_NUMBER = 5
ERR_WRONG_ARGS_NUM = "\nUsage: 3 arguments\n 1) Mouse's name\n 2) Path to csv file with single mouse's data\n " \
                     "3) Sliding window size in minutes\n 4) Time in minutes between recordings\n 5) Mode: mean / " \
                     "median\n"
ERR_PATH_NOT_EXISTS = "\nThe file does not exist on the path: "

COLOR_SINGLE_MOUSE_PLOT = "royalblue"
# for the standard error bars
SIZE_WINDOW_SMOOTH = 30
K_POLYNOMIAL = 3
COLOR_ERROR_BARS = "royalblue"
EDGE_COLOR_ERROR_BAR = "#8ed1fc80"


def create_lst_per_day(type_plot, dict_data, window):
    """
    :param type_plot: type of the plot - median or mean
    :param window: times in datetime for a specific window
    :param dict_data:
    :return: list that contains the percentage 25, median/mean, and percentage 75 for every day
    """
    lst = []
    for day in dict_data.keys():
        avg_current_day = calc_per_day(type_plot, dict_data, window, day)
        if avg_current_day != None:
            lst.append(avg_current_day)
    # returning the calculation
    if lst != []:
        if type_plot == TYPE_PLOT_MEDIAN:
            val = statistics.median(lst)
        else:
            val = statistics.mean(lst)
        percentile_75 = np.percentile(lst, 75)
        percentile_25 = np.percentile(lst, 25)
        return [percentile_25, val, percentile_75]
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


def define_plot_parameters(mouse_name, window_size, type):
    """
    Function that defines parameters for "plot_data"
    :param type: median or mean
    :param window_size:
    :param mouse_name:
    :param args_lst:
    :return:
    """
    plt.rcParams['date.converter'] = 'concise'
    # change y axis
    plt.setp(plt.gca(), ylim=(Y_AXIS_MIN, Y_AXIS_MAX))
    plt.title(type.capitalize() + " Glucose Levels of Mouse: " + "Mouse_X" + "\n Sliding Window Size " + window_size +
              " Minutes", fontdict=FONT_TITLE)
    plt.xlabel("\nTime (hour)", fontdict=FONT_LABEL)
    plt.ylabel("Glucose Levels (mg\\dL)\n", fontdict=FONT_LABEL)
    # delete right and top grid
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # change width of the labels on the axis
    plt.tick_params(axis='both', labelsize=LABEL_SIZE)


def get_percentile(slided_data_lst, percentile):
    """
    :param slided_data_lst:
    :return: list of values of the 25 percentile out of the data recorded
    """
    percentile_coordinates = []
    for lst in slided_data_lst[1]:
        if lst == None:
            continue
        if percentile == 25:
            percentile_coordinates.append(lst[0])
        else:
            percentile_coordinates.append(lst[2])
    return percentile_coordinates


def plot_data(slided_data_lst, mouse_name, window_size, type):
    """
    :param type: median or mean
    Method to plot multiple times in one figure.
    It receives a list with the representation of the data in the csv file.
    """
    define_plot_parameters(mouse_name, window_size, type)
    y_coordinates = np.array([x[1] for x in slided_data_lst[1] if x != None])
    lst_values = np.array(list(map(float, y_coordinates)))
    lst_time_in_int = np.array([(x.hour * 60 + x.minute) for x in slided_data_lst[0]])
    # make the error bars smoother
    y_smooth_25 = savgol_filter(get_percentile(slided_data_lst, 25), SIZE_WINDOW_SMOOTH, K_POLYNOMIAL)
    y_smooth_75 = savgol_filter(get_percentile(slided_data_lst, 75), SIZE_WINDOW_SMOOTH, K_POLYNOMIAL)
    plt.fill_between(slided_data_lst[0], y_smooth_25, y_smooth_75, color=COLOR_ERROR_BARS, alpha=0.1, edgecolor=None)
    plt.plot(slided_data_lst[0], lst_values, linewidth=LINE_WIDTH, color=COLOR_SINGLE_MOUSE_PLOT)
    locs, labels = plt.xticks()
    new_xticks = create_labels_for_x_axis(len(locs))
    plt.xticks(locs, new_xticks)
    plt.show()


def main():
    args_lst = sys.argv[1:]
    validation_of_args(args_lst)
    dict_data = create_dict_date_values(args_lst[PATH_LOC_IN_ARGS])
    # window_size_ele is a parameter used for calculation of the sliding window
    window_size_ele = int(int(args_lst[WINDOW_SIZE_LOC_IN_ARGS]) / int(args_lst[RECORDING_SPACE_LOC_IN_ARGS]) + 1)
    type_plot = args_lst[TYPE_PLOT_LOC_IN_ARGS].lower()
    slided_data_lst = slide_data(dict_data, create_lst_per_day, window_size_ele,
                                 int(args_lst[RECORDING_SPACE_LOC_IN_ARGS]), type_plot)
    plot_data(slided_data_lst, args_lst[MOUSE_NAME_LOC_IN_ARGS], args_lst[WINDOW_SIZE_LOC_IN_ARGS], type_plot)


if __name__ == "__main__":
    main()
