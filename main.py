# Import libraries
import matplotlib.pyplot as plt
import numpy as np
from csv import DictReader
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
    reader = DictReader(csvfile)
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

# NOCom box plot
# We use this numpy function to obtain the quantiles
[vmin,l,m,u,vmax] = np.quantile(data_NOCom, [0,0.25,0.5,0.75,1])

# We then compute the box plot parameters
d = u - l
s = u + 1.5*d
i = max(u - 1.5*d, vmin)

# We create a new figure to display the box plot
fig, ax = plt.subplots(figsize=(15,3), label="Boîte à moustache NOCom")

# We define the data structure that will be used to draw the box plot
boxes = [
    {
        'label' : "NOCom",
        'whislo': i,    # Bottom whisker position
        'q1'    : l,    # First quartile (25th percentile)
        'med'   : m,    # Median         (50th percentile)
        'q3'    : u,    # Third quartile (75th percentile)
        'whishi': s,    # Top whisker position
        'fliers': data_NOCom[data_NOCom>s]        # Outliers
    }
]

# We declare the box plot, passing the values we computed earlier
bp_dict = ax.bxp(boxes, showfliers=True, vert=False, flierprops=little_dot)

# We add labels to the box plot elements
draw_text(bp_dict)

# We add to the right of the plot the values used to draw the box plot 
plt.gcf().text(0.835, 0.75, "quartile supérieur = " + str(u), fontsize=10)
plt.gcf().text(0.835, 0.7, "quartile inférieur = " + str(l), fontsize=10)
plt.gcf().text(0.835, 0.65, "longueur de la boîte = " + str(d), fontsize=10)
plt.gcf().text(0.835, 0.6, "limite supérieure = " + str(s), fontsize=10)
plt.gcf().text(0.835, 0.55, "limite inférieure = " + str(i), fontsize=10)

# We must adjust the size of the plot in order to make room for the text on the right
plt.subplots_adjust(bottom=0.17, right=0.825)

plt.title("Boîte à moustache NOCom")
# This is required to draw the plot
plt.draw()
# We save the plot to a pdf file
plt.savefig('exports/moustache_NOCom.pdf', bbox_inches='tight')


# We do the same thing for NCLOC box plot
[vmin,l,m,u,vmax] = np.quantile(data_NCLOC, [0,0.25,0.5,0.75,1])
d = u - l
s = u + 1.5*d
i = max(u - 1.5*d, vmin)
fig, ax = plt.subplots(figsize=(15,3), label="Boîte à moustache NCLOC")
boxes = [
    {
        'label' : "NCLOC",
        'whislo': i,    # Bottom whisker position
        'q1'    : l,    # First quartile (25th percentile)
        'med'   : m,    # Median         (50th percentile)
        'q3'    : u,    # Third quartile (75th percentile)
        'whishi': s,    # Top whisker position
        'fliers': data_NCLOC[data_NCLOC>s]        # Outliers
    }
]
bp_dict = ax.bxp(boxes, showfliers=True, vert=False, flierprops=little_dot)
draw_text(bp_dict)
plt.title("Boîte à moustache NCLOC")
plt.gcf().text(0.835, 0.75, "quartile supérieur = " + str(u), fontsize=10)
plt.gcf().text(0.835, 0.7, "quartile inférieur = " + str(l), fontsize=10)
plt.gcf().text(0.835, 0.65, "longueur de la boîte = " + str(d), fontsize=10)
plt.gcf().text(0.835, 0.6, "limite supérieure = " + str(s), fontsize=10)
plt.gcf().text(0.835, 0.55, "limite inférieure = " + str(i), fontsize=10)
plt.subplots_adjust(bottom=0.17, right=0.825)
plt.draw()
plt.savefig('exports/moustache_NCLOC.pdf', bbox_inches='tight')

# We do the same thing for DCP box plot
[vmin,l,m,u,vmax] = np.quantile(data_DCP, [0,0.25,0.5,0.75,1])
d = u - l
s = u + 1.5*d
i = max(u - 1.5*d, vmin)
fig, ax = plt.subplots(figsize=(15,3), label="Boîte à moustache DCP")
boxes = [
    {
        'label' : "DCP",
        'whislo': i,    # Bottom whisker position
        'q1'    : l,    # First quartile (25th percentile)
        'med'   : m,    # Median         (50th percentile)
        'q3'    : u,    # Third quartile (75th percentile)
        'whishi': s,    # Top whisker position
        'fliers': data_DCP[data_DCP>s]         # Outliers
    }
]
bp_dict = ax.bxp(boxes, showfliers=True, vert=False, flierprops=little_dot)
draw_text(bp_dict)
plt.title("Boîte à moustache DCP")
plt.gcf().text(0.835, 0.75, "quartile supérieur = " + str(u), fontsize=10)
plt.gcf().text(0.835, 0.7, "quartile inférieur = " + str(l), fontsize=10)
plt.gcf().text(0.835, 0.65, "longueur de la boîte = " + str(d), fontsize=10)
plt.gcf().text(0.835, 0.6, "limite supérieure = " + str(s), fontsize=10)
plt.gcf().text(0.835, 0.55, "limite inférieure = " + str(i), fontsize=10)
plt.subplots_adjust(bottom=0.17, right=0.825)
plt.draw()
plt.savefig('exports/moustache_DCP.pdf', bbox_inches='tight')


# Draw data visualisation
# NOCom
fig, ax = plt.subplots(figsize=(15,7), label="Nuage de points NOCom")
# We define a scatter plot using the data set element numbers as x and the data set values as y
plt.scatter(np.arange(1, data_NOCom.size+1), data_NOCom)
plt.title("Nuage de points NOCom")
plt.ylabel("NOCom")
plt.draw()
plt.savefig('exports/nuage_NOCom.pdf', bbox_inches='tight')

# NCLOC
fig, ax = plt.subplots(figsize=(15,7), label="Nuage de points NCLOC")
plt.scatter(np.arange(1, data_NCLOC.size+1), data_NCLOC)
plt.title("Nuage de points NCLOC")
plt.ylabel("NCLOC")
plt.draw()
plt.savefig('exports/nuage_NCLOC.pdf', bbox_inches='tight')

# DCP
fig, ax = plt.subplots(figsize=(15,7), label="Nuage de points DCP")
plt.scatter(np.arange(1, data_DCP.size+1), data_DCP)
plt.title("Nuage de points DCP")
plt.ylabel("DCP")
plt.draw()
plt.savefig('exports/nuage_DCP.pdf', bbox_inches='tight')


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
fig, ax = plt.subplots(figsize=(15,7), label="Nuage de points NCLOC en fonction de NOCom")
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
plt.savefig('exports/relation_NCLOC_NOCom.pdf', bbox_inches='tight')

# DCP/NOCom
fig, ax = plt.subplots(figsize=(15,7), label="Nuage de points DCP en fonction de NOCom")
plt.scatter(data_NOCom, data_DCP)
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
plt.savefig('exports/relation_DCP_NOCom.pdf', bbox_inches='tight')

# We show all the figures we created
plt.show()