###########################################
# written by: Mika Littor, Danny Ben-Zvi's Lab.
# This program creates a figure with multiple plots using module matplotlib in python 3.
# The figure represents the averaged values for all the of the mice recordred.
# The arguments needed in order for this program to run:
# 1) Path to the CSV directory that holds the data measured from the mice.
# THE NAME OF THE MOUSE SHOULD BE THE NAME OF THE FILE INSIDE THE DIRECTORY
# 2) Size of the sliding window in minutes.
# 3) The time between every two recordings of the mouse.
# IN ORDER TO USE PLEASE EDIT THE 'NAME MICE' ARGUMENT.
###########################################
from supplementary_file import *

BASIC_FILE_PATH = r"C:\Users\mikal\Documents\LAB2\mice_sugar_prj"
NAME_MICE = ["Naw2_M6", "Naw1_M4"]

# define limit of the y axis
Y_AXIS_MAX = 190
Y_AXIS_MIN = 100

# Location of the argument accepts by the user in the list received.
PATH_LOC_IN_ARGS = 0
WINDOW_SIZE_LOC_IN_ARGS = 1
RECORDING_SPACE_LOC_IN_ARGS = 2
ARGS_NUMBER = 3
ERR_WRONG_ARGS_NUM = "\nUsage: 3 arguments\n 1) Path to csv directory with mice data\n " \
                     "2) Sliding window size in minutes\n 3) Time in minutes between recordings\n"
ERR_PATH_NOT_EXISTS = "\nThe file does not exist on the path: "


def multiple_plots(dict_data, window_size, recording_space):
    """
    Method to plot multiple times in one figure.
    It receives a dictionary with the representation of the data in the csv file.
    Every key in the dictionary represent a different date that will have its own plot ont the graph.
    """
    fig, ax = plt.subplots()
    plt.rcParams['date.converter'] = 'concise'
    # change y axis
    plt.setp(plt.gca(), ylim=(Y_AXIS_MIN, Y_AXIS_MAX))
    first = True
    for mouse, coordinates in dict_data.items():
        # sorting the y coordinates
        y_coordinates = list(map(float, coordinates[1]))
        # plotting the current date
        if first:
            ax.plot(coordinates[0], y_coordinates, label="mouse 1", color="paleturquoise", linewidth=LINE_WIDTH)
            first = False
        else:
            ax.plot(coordinates[0], y_coordinates, label="mouse 2", color="royalblue", linewidth=LINE_WIDTH)
    create_plot(plt, window_size, recording_space)


def create_plot(plt, window_size, recording_space):
    """
    showing the plot created
    :param plt: the plot
    """
    plt.title("Avg Glucose Levels vs Time\nsliding window size " + str(window_size) + " minutes",
              fontdict=FONT_TITLE)
    plt.xlabel("Time (hour)", fontdict=FONT_LABEL)
    plt.ylabel("Glucose Levels (mg\\dl)", fontdict=FONT_LABEL)
    plt.legend(loc=0)
    locs, labels = plt.xticks()
    new_xticks = create_labels_for_x_axis(len(locs))
    plt.xticks(locs, new_xticks)
    # delete right and top grid
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # change width of the labels on the axis
    plt.tick_params(axis='both', labelsize=LABEL_SIZE)
    plt.show()


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
        avg_current_day = calc_per_day(window, dict_data, day)
        if avg_current_day != -10:
            avgs_lst.append(avg_current_day)
    # returning the avg calculation
    if avgs_lst != []:
        return sum(avgs_lst) / len(avgs_lst)
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
    return -10


def path_to_mouse(mouse, basic_path):
    """
    :param mouse: name of the current mouse
    :return: path to the current mouse's file
    """
    return basic_path + "\\" + mouse + "\\" + mouse.replace(" ", "_") + "_Hours.csv"


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
    dict_mouse = {}
    args_lst = sys.argv[1:]
    validation_of_args(args_lst)
    window_size_ele = int(int(args_lst[WINDOW_SIZE_LOC_IN_ARGS]) / int(args_lst[RECORDING_SPACE_LOC_IN_ARGS]) + 1)
    for mouse in sorted(NAME_MICE):
        path_file = path_to_mouse(mouse, args_lst[PATH_LOC_IN_ARGS])
        dict_data = create_dict_date_values(path_file)
        slided_data_dict = slide_data(dict_data, calc_avg, window_size_ele,
                                      int(args_lst[RECORDING_SPACE_LOC_IN_ARGS]))
        dict_mouse[mouse] = slided_data_dict
    multiple_plots(dict_mouse, int(args_lst[WINDOW_SIZE_LOC_IN_ARGS]), int(args_lst[RECORDING_SPACE_LOC_IN_ARGS]))


if __name__ == "__main__":
    main()
