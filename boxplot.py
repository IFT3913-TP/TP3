# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import stats

# function to add labels on box plot elements 
def draw_text(bp_dict):
    for line in bp_dict['medians']:
        # get position data for median line
        x, y = line.get_xydata()[1] # top of median line
        # overlay median value
        plt.text(x, y, '%.2f' % x,
            horizontalalignment='center') # draw above, centered

    for line in bp_dict['boxes']:
        x, y = line.get_xydata()[0] # bottom of left line
        plt.text(x,y, '%.2f' % x,
            horizontalalignment='center', # centered
            verticalalignment='top')      # below
        x, y = line.get_xydata()[3] # bottom of right line
        plt.text(x,y, '%.2f' % x,
            horizontalalignment='center', # centered
                verticalalignment='top')      # below

    for line in bp_dict['caps']:
        x, y = line.get_xydata()[0] # bottom of left line
        plt.text(x,y, '%.2f' % x,
            horizontalalignment='center', # centered
            verticalalignment='top')      # below

    for line in bp_dict['fliers']:
        for point in line.get_xydata():
            x, y = point # bottom of left line
            plt.text(x,y*0.975, '%.2f' % x,
                horizontalalignment='center', # centered
                verticalalignment='bottom')      # below



# Extracting data from the csv dataset
with open('jfreechart-stats.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    data_1 = []
    data_2 = []
    data_3 = []
    for row in reader:
        # We have to convert and cast to float the str corresponding to each 
        # value since the boxplot takes a list of numbers 
        data_1.append(float(row[reader.fieldnames[1]]))
        data_2.append(float(row[reader.fieldnames[2]]))
        data_3.append(float(row[reader.fieldnames[3]]))

# Conversion to numpy array in order to compute the pearson coeff
data_1 = np.array(data_1)
data_2 = np.array(data_2)
data_3 = np.array(data_3)

little_dot = dict(markerfacecolor='r', marker='.', markersize=5)

fig_1 = plt.figure(1, figsize =(10, 7))
bp_dict_1 = plt.boxplot(data_1, vert=False, flierprops=little_dot)
draw_text(bp_dict_1)

fig_2 = plt.figure(2, figsize =(10, 7))
bp_dict_2= plt.boxplot(data_2, vert=False, flierprops=little_dot)
draw_text(bp_dict_2)


fig_3 = plt.figure(3, figsize =(10, 7))
bp_dict_3 = plt.boxplot(data_3, vert=False, flierprops=little_dot)
draw_text(bp_dict_3)
plt.show()

# Correlation compute
i = 0
for dataname in reader.fieldnames[1:]:
    print("d" + str(i) + "=" +dataname)
    i+=1
# pearson
pearson_d1_d2 = stats.pearsonr(data_1, data_2)
print("pearson_d1_d2 : ", end="")
print(pearson_d1_d2)

pearson_d1_d3 = stats.pearsonr(data_1, data_3)
print("pearson_d1_d3 : ", end="")
print(pearson_d1_d3)

pearson_d2_d3 = stats.pearsonr(data_2, data_3)
print("pearson_d2_d3 : ", end="")
print(pearson_d2_d3)

# spearman

spearman_d1_d2 = stats.spearmanr(data_1, data_2)
print("spearman_d1_d2 : ", end="")
print(spearman_d1_d2)

spearman_d1_d3 = stats.spearmanr(data_1, data_3)
print("spearman_d1_d3 : ", end="")
print(spearman_d1_d3)

spearman_d2_d3 = stats.spearmanr(data_2, data_3)
print("spearman_d2_d3 : ", end="")
print(spearman_d2_d3)