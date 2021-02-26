import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import os
import numpy as np
import pylab
from scipy import stats

# change directory to folder location
os.chdir("C://Users/Rachel/Documents/Rachel/BS MS Research/Larval_DR/experiments")

def make_graph(exp):
    # read in the data and setup information
    data = pd.read_excel(exp + "_data.xlsx")
    setup = pd.read_excel(exp + "_setup.xlsx")    
    
    # data manipulation
    conc = []
    for col in data.columns:
        if col != "time":
            # find the total number of worms per well
            total = max([int(setup[setup["well_num"]==col]["worm_num"]), max(data[col])])
            if total != 0:
                # divide glowing worms by total number of worms
                data[col] = data[col]/total
                # find the amount of E. coli per worm
                conc.append(int(setup[setup["well_num"]==col]["e_coli"])/total)
            else:
                conc.append(0)
    
    # convert time to hours and subtract the first value
    times = [i.hour + (i.minute/60) for i in data["time"]]
    times = np.array(times) - times[0]
    
    # create the title of the plot based on the file name
    main = exp.split("_")
    if main[0] == "exp":
        main = "Experiment " + main[1]
    if main[0] == "pilot":
        main = "Pilot Experiment " + main[1]
    
    # determine the color of each line using a colormap theme
    cm = pylab.get_cmap("winter")
    colors = np.array(conc)/max(conc)
    colors = [cm(1.*i) for i in colors]
    
    # plot the lines on top of the same figure
    for col in data.columns:
        if col != "time" and not np.all(data[col]==0):
            plt.plot(times, data[col], marker=".", ms=8, color=colors[col-1], mfc="0.0", mec="0.0",
                     label=str(col) + " \u2192 " + str(np.round(conc[col-1], decimals=3)))
    plt.xlabel("Hour of Data Collection")
    plt.ylabel("Fraction of Worms Molting")
    plt.title(main)
    plt.legend(title=chr(956) + "L E. coli / worm", bbox_to_anchor=(1,1))
    
def stats_test(exp_list=["exp_1", "exp_4"]):
    # keep track of how many points are in each quadrant
    green_count = 0
    red_count = 0
    orange_count = 0
    # loop through all the valid experiments
    for exp in exp_list:
        # read in the data
        data = pd.read_excel(exp + "_data.xlsx")
        setup = pd.read_excel(exp + "_setup.xlsx")
        
        # create distribution of times based on data
        times = [i.hour + (i.minute/60) for i in data["time"]]
        times = np.array(times) - times[0]
        groups = [col for col in data.columns if col != "time"and not np.all(data[col]==0)]
        time_dist = [np.repeat(times,data[i]) for i in groups]    
    
        # data manipulation
        conc = []
        for i in groups:
            # find the total number of worms per well
            total = max([int(setup[setup["well_num"]==i]["worm_num"]), max(data[i])])
            # find the amount of E. coli per worm
            conc.append(int(setup[setup["well_num"]==i]["e_coli"])/total)    
    
        # run a pairwise t-test between all groups
        pairs = np.array([[x,y] for i,x in enumerate(groups) for j,y in enumerate(groups) if i < j])
        for pair in pairs:
            # find the correct index
            a = np.where(groups==pair[0])[0][0]
            b = np.where(groups==pair[1])[0][0]
            if len(time_dist[a]) > 1 and len(time_dist[b]) > 1:
                test = stats.ttest_ind(time_dist[a], time_dist[b])[1]
                # plot the differences in groups if significant
                if test < 0.05:
                    # find the slope
                    x = conc[b] - conc[a]
                    y = np.mean(time_dist[b]) - np.mean(time_dist[a])
                    # choose colors based on which quadrant the point is in
                    if x > 0 and y < 0:
                        plt.plot(x, y, "o", color="green")
                        green_count += 1
                    elif x < 0 and y > 0:
                        plt.plot(x, y, "o", color="green")
                        green_count += 1
                    elif x > 0 and y > 0:
                        plt.plot(x, y, "o", color="red")
                        red_count += 1
                    elif x < 0 and y < 0:
                        plt.plot(x, y, "o", color="red")
                        red_count += 1
                    else:
                        plt.plot(x, y, "o", color="orange")
                        orange_count += 1
    
    # configurations for the rest of the plot
    plt.axvline(x=0, color="black")
    plt.axhline(y=0, color="black")
    plt.xlabel("Difference in Concentrations per Worm")
    plt.ylabel("Difference in Average Molting Times")
    plt.title("Statistically Significant Groups")
    green_points = mlines.Line2D([], [], color="green", marker="o", linestyle="None",
                                 markersize=10, label="green - " + str(green_count))
    red_points = mlines.Line2D([], [], color="red", marker="o", linestyle="None",
                               markersize=10, label="red - " + str(red_count))
    orange_points = mlines.Line2D([], [], color="orange", marker="o", linestyle="None",
                                  markersize=10, label="orange - " + str(orange_count))
    plt.legend(handles=[green_points, red_points, orange_points], loc="best")
    