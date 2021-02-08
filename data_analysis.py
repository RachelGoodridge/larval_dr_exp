import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import pylab

def make_graph(exp):
    # change directory to folder location
    os.chdir("C://Users/Rachel/Documents/Rachel/BS MS Research/Larval_DR/experiments")
    
    try:
        # read in the data and setup information
        data = pd.read_excel(exp + "_data.xlsx")
        setup = pd.read_excel(exp + "_setup.xlsx")
    except:
        # reminder of the argument type allowed
        print("Function argument must be a string like this:")
        print("'exp_1'")
        print("'pilot_1'")
        return None
    
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
                     label=str(np.round(conc[col-1], decimals=3)))
    plt.xlabel("Hour of Data Collection")
    plt.ylabel("Fraction of Worms Molting")
    plt.title(main)
    plt.legend(title=chr(956) + "L E. coli / worm", bbox_to_anchor=(1,1))
