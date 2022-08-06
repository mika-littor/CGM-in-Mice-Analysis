###########################################
# written by: Mika Littor, Danny Ben-Zvi's Lab.
# This program creates a figure with multiple plots using module matplotlib in python 3. Each figure represents the
# raw data taken from a single mouse. Every plot on the figure has its own color, and it demonstrates a single day in
# which data was measured.
# The arguments needed in order for this program to run:
# 1) Name of the mouse.
# 2) Path to the CSV file that holds the data measured from a single mouse.
###########################################
from supplementary_file import *

# Location of the argument accepts by the user in the list received.
MOUSE_NAME_LOC_IN_ARGS = 0
PATH_LOC_IN_ARGS = 1
ARGS_NUMBER = 2
ERR_WRONG_ARGS_NUM = "\nUsage: 2 arguments. 1) Mouse's name 2) Path to csv file with single mouse's data\n"
ERR_PATH_NOT_EXISTS = "\nThe file does not exist on the path: "

NUM_HOURS = 24 # number of hours for the plot
DICT_WANTED_DATES = {"17 April": "#6C7FA5", "15 April": "#7CA3DB", "12 April": "#9BD4FF"}


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
        if date in DICT_WANTED_DATES.keys():
            # sorting the y coordinates
            x_coordinates = [x for x in coordinates[0] if x < LAST_POINT_WIN]
            y_coordinates = list(map(float, coordinates[1]))[:len(x_coordinates)]
            # plotting the current date
            ax.plot(x_coordinates, y_coordinates, label=date, linewidth=LINE_WIDTH, color=DICT_WANTED_DATES[date])
    create_plot(plt, args_lst[MOUSE_NAME_LOC_IN_ARGS])


def create_plot(plt, mouse_name):
    """
    showing the plot created
    :param plt: the plot
    :param mouse_name: name of the mouse
    """
    plt.title("Raw Data of Mouse: Mouse 1", fontdict=FONT_TITLE)
    plt.xlabel("Time (hour)", fontdict=FONT_LABEL)
    plt.ylabel("Glucose Levels (mg\\dl)", fontdict=FONT_LABEL)
    plt.legend(loc=0, prop={'size': 20})
    locs, labels = plt.xticks()
    new_xticks = create_labels_for_x_axis(len(locs))
    plt.xticks(locs, new_xticks)
    # change y axis
    plt.setp(plt.gca(), ylim=(Y_AXIS_MIN, Y_AXIS_MAX))
    # change width of the labels on the axis
    plt.tick_params(axis='both', labelsize=LABEL_SIZE)
    # delete right and top grid
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.locator_params(axis='y', nbins=51)
    plt.show()


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
    multiple_plots(dict_data, args_lst)


if __name__ == "__main__":
    main()
