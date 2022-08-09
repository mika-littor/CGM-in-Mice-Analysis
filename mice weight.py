import matplotlib.pyplot as plt
import numpy as np
from statistics import median
from scipy.stats import sem

# GRAPH'S GUI
FONT_TITLE = {'family': 'Arial Rounded MT Bold', 'color': 'black', 'size': 25, 'weight': 'bold'}
FONT_LABEL = {'family': 'Arial Rounded MT Bold', 'color': 'black', 'size': 20, 'weight': 'bold'}
LABEL_SIZE = 15

COL_DAY = 4
COL_WEIGHT = 5

def main():
    dict_day_weight = {}
    first_row = True
    file_path = r"C:\Users\mikal\Documents\LAB2\PROJECT_MICE_CGM\cgm weight long.csv"
    with open(file_path) as f:
        for row in f:
            if first_row:
                # the first row is a row of headers, therefore it shouldn't be added to the dictionary. s
                first_row = False
            else:
                row_data = list(row.split(","))
                day_num = int(row_data[COL_DAY])
                weight_num = float(row_data[COL_WEIGHT])
                if day_num in dict_day_weight:
                    dict_day_weight[day_num].append(weight_num)
                else:
                    dict_day_weight[day_num] = []
                    dict_day_weight[day_num].append(weight_num)

    lst_x_values = []
    lst_y_values = []
    for day, lst_weights in dict_day_weight.items():
        mean_weight = median(lst_weights)
        y_err = sem(lst_weights)
        plt.errorbar(x=day, y=mean_weight, yerr=y_err, ecolor="royalblue", fmt='.k', capthick=2, capsize=3)
        lst_x_values.append(day)
        lst_y_values.append(mean_weight)
    plt.plot(lst_x_values, lst_y_values, color="royalblue")



    plt.title("Mice Weight vs Time", fontdict=FONT_TITLE)
    plt.ylabel("Weight (gr)\n", fontdict=FONT_LABEL)
    plt.xlabel("\nTime (days)", fontdict=FONT_LABEL)
    plt.tick_params(axis='both', labelsize=LABEL_SIZE)
    # delete right and top grid
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.show()


if __name__ == "__main__":
    main()
