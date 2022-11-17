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
    # we obtain an iterator to extract the csv data
    reader = csv.DictReader(csvfile)
    # initialising the data lists
    data_NOCom = []
    data_NCLOC = []
    data_DCP = []
    for row in reader:
        # We have to convert and cast to float the str corresponding to each 
        # value since the boxplot takes a list of numbers 
        data_NOCom.append(float(row[reader.fieldnames[1]]))
        data_NCLOC.append(float(row[reader.fieldnames[2]]))
        data_DCP.append(float(row[reader.fieldnames[3]]))

# Conversion of data lists to numpy array in order to compute the pearson and spearman coeffs
data_NOCom = np.array(data_NOCom)
data_NCLOC = np.array(data_NCLOC)
data_DCP = np.array(data_DCP)


# Draw box plots
# We will need a special marker to display the extremes values
little_dot = dict(markerfacecolor='r', marker='.', markersize=5)

# NOCom
# We create a new figure to draw the box plot inside
fig_NOCOM = plt.figure(1, figsize =(10, 7))
# We define an horizontal box plot that is also using the custom marker we defined earlier
bp_dict_NOCOM = plt.boxplot(data_NOCom, vert=False, flierprops=little_dot)
# We add values corresponding to the metrics as text on top of the plot
draw_text(bp_dict_NOCOM)
plt.title("Boîte à moustache NOCOM")
plt.draw()

# NCLOC
fig_NCLOC = plt.figure(2, figsize =(10, 7))
bp_dict_NCLOC= plt.boxplot(data_NCLOC, vert=False, flierprops=little_dot)
draw_text(bp_dict_NCLOC)
plt.title("Boîte à moustache NCLOC")
plt.draw()

# DCP
fig_DCP = plt.figure(3, figsize =(10, 7))
bp_dict_DCP = plt.boxplot(data_DCP, vert=False, flierprops=little_dot)
draw_text(bp_dict_DCP)
plt.title("Boîte à moustache DCP")
plt.draw()


# Draw data visualisation
# NOCom
fig_NOCOM_scatter = plt.figure(4, figsize =(10, 7))
# We define a scatter plot using the data set element numbers as x and the data set values as y
plt.scatter(np.arange(1, data_NOCom.size+1), data_NOCom)
plt.title("Nuage de points NOCOM")
plt.ylabel("NOCOM")
plt.draw()

# NCLOC
fig_NCLOC_scatter = plt.figure(5, figsize =(10, 7))
plt.scatter(np.arange(1, data_NCLOC.size+1), data_NCLOC)
plt.title("Nuage de points NCLOC")
plt.ylabel("NCLOC")
plt.draw()

# DCP
fig_DCP_scatter = plt.figure(6, figsize =(10, 7))
plt.scatter(np.arange(1, data_DCP.size+1), data_DCP)
plt.title("Nuage de points DCP")
plt.ylabel("DCP")
plt.draw()


# Correlation and regression compute
# pearson
pearson_NOCom_NCLOC = stats.pearsonr(data_NOCom, data_NCLOC)
pearson_NOCom_DCP = stats.pearsonr(data_NOCom, data_DCP)

# spearman
spearman_NOCom_NCLOC = stats.spearmanr(data_NOCom, data_NCLOC)
spearman_NOCom_DCP = stats.spearmanr(data_NOCom, data_DCP)

# linear regression compute
lreg_NOCom_NCLOC = stats.linregress(data_NOCom, data_NCLOC)
# We extract the coefficient and the y-intercept
a_NCLOC = lreg_NOCom_NCLOC[0]
b_NCLOC = lreg_NOCom_NCLOC[1]
lreg_NOCom_DCP = stats.linregress(data_NOCom, data_DCP)
a_DCP = lreg_NOCom_DCP[0]
b_DCP = lreg_NOCom_DCP[1]


# Draw data relation
# NCLOC/NOCom
fig_NOCOM_NCLOC_scatter = plt.figure(7, figsize =(10, 7))
# We define a scatter plot using values for NOCom as x and values for NCLOC as y
plt.scatter(data_NOCom, data_NCLOC)
# We plot the line corresponding to the linear regression
plt.plot(data_NOCom,a_NCLOC*data_NOCom+b_NCLOC, 
        label="Régression linéaire : y = "+str(a_NCLOC)+"x + "+str(b_NCLOC), 
        color="red")
plt.legend()
plt.title("Nuage de points NCLOC en fonction de NOCom")
plt.xlabel("NOCom")
plt.ylabel("NCLOC")
# We add text to the bottom of the plot to display the correlation coeffs
plt.gcf().text(0.125, 0.045, "pearson = " + str(pearson_NOCom_NCLOC[0]), fontsize=12)
plt.gcf().text(0.125, 0.02, "spearman = " + str(spearman_NOCom_NCLOC[0]), fontsize=12)
plt.subplots_adjust(bottom=0.15)
plt.draw()

# DCP/NOCom
fig_NOCOM_DCP_scatter = plt.figure(8, figsize =(10, 7))
plt.scatter(data_NOCom, data_DCP)
#y2 = a_DCP*data_NOCom+b_DCP
plt.plot(data_NOCom,a_DCP*data_NOCom+b_DCP, 
        label="Régression linéaire : y = "+str(a_DCP)+"x + "+str(b_DCP), 
        color="red")
plt.legend()
plt.title("Nuage de points DCP en fonction de NOCom")
plt.xlabel("NOCom")
plt.ylabel("DCP")
plt.gcf().text(0.125, 0.045, "pearson = " + str(pearson_NOCom_DCP[0]), fontsize=12)
plt.gcf().text(0.125, 0.02, "spearman = " + str(spearman_NOCom_DCP[0]), fontsize=12)
plt.subplots_adjust(bottom=0.15)
plt.draw()


# We show all the figures we created
plt.show()