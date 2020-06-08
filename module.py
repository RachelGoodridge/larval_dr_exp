import random as rnd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mp


class Worm():
    """ Creates a class called Worm with the following attributes.
    
    Class Attributes
    ----------------
    mean : fixed at 15
        This is the average number of hours that a worms takes to molt from one larval stage to the next.
    sd : fixed at 2
        Standard deviation. This is the normal amount of variation in molting times. (ie mean +/- 2 hours is normal)
        
    Instance Attributes
    -------------------
    molt_age : input a string from the list of food concentrations ["6 mg/mL", "4.8 mg/mL", "3.6 mg/mL", "2.4 mg/mL"]
        With less food concentration, the worm is expected to take longer to molt.
    spread : input an int or a float
        Used to controll the variance in starting age of the worm. If the spread is small, worms will be roughly the same age.
    diff : input an int or a float
        The difference in means between treatment groups. (UNKNOWN in real life)
    age : a random choice of float between zero and spread (no input required)
        This is controlled by spread. It determines how soon the worm will molt, depending on its age.
    """
    
    mean = 15
    sd = 2
    
    def __init__(self, molt_age, spread, diff):
        
        self.spread = spread
        self.diff = diff
        self.age = rnd.uniform(0, self.spread)
        
        # based on the input for molt_age, change the attribute to a float that determines when the worm will molt
        if molt_age == "6 mg/mL":
            # choose a random float based on the normal distribution, centered around the "mean" with "sd"
            self.molt_age = np.random.normal(self.mean, self.sd)
        
        elif molt_age == "4.8 mg/mL":
            # each treatment group's mean is increased in multiples of "diff"
            self.molt_age = np.random.normal(self.mean + self.diff, self.sd)
        
        elif molt_age == "3.6 mg/mL":
            self.molt_age = np.random.normal(self.mean + 2*self.diff, self.sd)
        
        elif molt_age == "2.4 mg/mL":
            self.molt_age = np.random.normal(self.mean + 3*self.diff, self.sd)


def create_groups(spread, diff, size):
    """ Create the 4 treatment groups using the Class Worm.
    
    Parameters
    ----------
    spread : an int or a float
        Used to controll the variance in starting age of the worm. If the spread is small, worms will be roughly the same age.
    diff : an int or a float
        The difference in means between treatment groups. (UNKNOWN in real life)
    size : an int
        The number of worms in each treatment group.
    
    Returns
    -------
    worms : a list of four lists of objects
        There are four lists (one for each treatment group) and within those lists, there are worm objects.
    """
    
    worms = []
    
    for i in ["6 mg/mL", "4.8 mg/mL", "3.6 mg/mL", "2.4 mg/mL"]:
        # the molt_age is a choice of food concentrations in the list above, one for each group
        worms.append([Worm(i, spread, diff) for j in range(size)])
    
    return worms


def find_molt(size, worms):
    """ Determine when each worm molts by molt_age minus current age.
    
    Parameters
    ----------
    size : an int
        The number of worms in each treatment group.
    worms : a list of four lists of objects
        There are four lists (one for each treatment group) and within those lists, there are worm objects.
    
    Returns
    -------
    molt : a list of four non-empty lists of floats
        There are four lists (one for each treatment group) and within those lists, the time required for a worm to molt.
    """
    
    molt = [[] for i in range(4)]
    
    for i in range(4):
        for j in range(size):
            # loop through each worm in every group to determine how many hours it will take to molt
            molt[i].append(worms[i][j].molt_age - worms[i][j].age)
    
    return molt


def find_small(molt, hour):
    """ Find the smallest of the molting times and round down to the nearest hour. 
    
    Parameters
    ----------
    molt : a list of four non-empty lists of floats
        There are four lists (one for each treatment group) and within those lists, the time required for a worm to molt.
    hour : an int or a float
        This represents the frequency that data are collected. (ie worms counted ____ times per hour)
    
    Returns
    -------
    small : an int or a float
        The bottom end of the smallest bin, a multiple of "hour"
    """
    
    # find the smallest molting time of all the groups
    small = min(min(molt[0]), min(molt[1]), min(molt[2]), min(molt[3]))
    
    if round(small/hour)*hour > small:
        # if rounding it to the nearest "hour" rounds up, then subtract "hour"
        small = round(small/hour)*hour - hour
    else:
        small = round(small/hour)*hour
    
    return small


def find_big(molt, hour):
    """ Find the largest of the molting times and round up to the nearest hour.
    
    Parameters
    ----------
    molt : a list of four non-empty lists of floats
        There are four lists (one for each treatment group) and within those lists, the time required for a worm to molt.
    hour : an int or a float
        This represents the frequency that data are collected. (ie worms counted ____ times per hour)
    
    Returns
    -------
    big : an int or a float
        The top end of the largest bin, a multiple of "hour"
    """
    
    # find the largest molting time of all the groups
    big = max(max(molt[0]), max(molt[1]), max(molt[2]), max(molt[3]))
    
    if round(big/hour)*hour < big:
        # if rounding it to the nearest "hour" rounds down, then add "hour"
        big = round(big/hour)*hour + hour
    else:
        big = round(big/hour)*hour
        
    return big


def find_mid_bin(small, big, hour):
    """ Determine when worms will be counted (ie the setup for creating the bins).
    
    Parameters
    ----------
    small : an int or a float
        The bottom end of the smallest bin, a multiple of "hour"
    big : an int or a float
        The top end of the largest bin, a multiple of "hour"
    hour : an int or a float
        This represents the frequency that data are collected. (ie worms counted ____ times per hour)
    
    Returns
    -------
    mid_bin : a list of integers or floats
        Worms will be counted at each hour indicated in this list.
    """
    
    # add hour to big to ensure that the mid_bin includes big
    mid_bin = np.arange(small, big + hour, hour)
    mid_bin = mid_bin.tolist()
    
    return mid_bin


def create_bin(mid_bin):
    """ Create bins that are 3 hours wide for each time counted.
    
    Parameters
    ----------
    mid_bin : a list of integers or floats
        Worms will be counted at each hour indicated in this list.
    
    Returns
    -------
    bins : a list of lists, each one contains two floats
        The two floats in each inner list represent the start time and end time for each bin.
    """
    
    bins = [0]*len(mid_bin)
    for i in range(len(mid_bin)):
        # each bin contains 1.5 hours before and after the time worms are counted
        bins[i] = [mid_bin[i]-1.5, mid_bin[i]+1.5]
    
    return bins


def sort_worm(group, bins, molt):
    """ Determine worms that fall into each bin based on when they molt.
    
    Parameters
    ----------
    group : an integer (0, 1, 2, or 3)
        This is used as an index into molt to determine which treatment group is being sorted.
    bins : a list of lists, each one contains two floats
        The two floats in each inner list represent the start time and end time for each bin.
    molt : a list of four non-empty lists of floats
        There are four lists (one for each treatment group) and within those lists, the time required for a worm to molt.
    
    Returns
    -------
    sorted_worms : a list of lists of floats
        There is a list for each bin, containing the molt times of all the worms that fall into that bin.
    """
    
    sorted_worms = [[] for i in range(len(bins))]
    for i in range(len(bins)):
        for j in molt[group]:
            # look at each molt time of a particular treatment group
            if j >= bins[i][0] and j < bins[i][1]:
                # if the molt time of a worm is between the start time and end time of a bin, append it
                sorted_worms[i].append(j)
    
    return sorted_worms


def fix_data(sorted_worms, mid_bin):
    """ Adjust groupings so they contain realistic data, ie mid_bin times not exact molting times.
    
    Parameters
    ----------
    sorted_worms : a list of lists of floats
        There is a list for each bin, containing the molt times of all the worms that fall into that bin.
    mid_bin : a list of integers or floats
        Worms will be counted at each hour indicated in this list.
    
    Returns
    -------
    flat_worm : a list of integers or floats
        The values are from mid_bin, but the frequency of each is dependent on how many worms are counted per bin.
    """
    
    flat_worm = []
    
    for sublist, i in zip(sorted_worms, range(len(sorted_worms))):
        # for each molt time in sorted_worms, add the corresponding mid_bin value to flat_worm
        flat_worm += [mid_bin[i] for j in range(len(sublist))]
    
    return flat_worm


def stats_test(flat_1, flat_2):
    """ Prints one-tailed p values and significance between flat_worm data from the treatment groups.
    
    Parameters
    ----------
    flat_1 : a list of integers or floats (treatment group A)
        The values are from mid_bin, but the frequency of each is dependent on how many worms are counted per bin.
    flat_2 : a list of integers or floats (treatment group B)
        The values are from mid_bin, but the frequency of each is dependent on how many worms are counted per bin.
    """
    
    # divide by 2 to make the p value for a one-sided t test
    test = stats.ttest_ind(flat_1, flat_2)[1]/2
    
    print("p value =", test, end=" ")
    # set the significance threshold to be 0.05
    if test < 0.05:
        print("significant")
    else:
        print("")


def find_density(sorted_worms, size):
    """ Determine the percentage of worms molting at each time.
    
    Parameters
    ----------
    sorted_worms : a list of lists of floats
        There is a list for each bin, containing the molt times of all the worms that fall into that bin.
    size : an int
        The number of worms in each treatment group.
    
    Returns
    -------
    sorted_worms : a list of floats
        Each list from the input sorted_worms will be replaced by a float that represents the fraction molting.
    """
    
    for i in range(len(sorted_worms)):
        # calculate the density of worms molting for each bin
        sorted_worms[i] = len(sorted_worms[i])/size
    
    return sorted_worms


def make_plot(mid_bin, worms0, worms1, worms2, worms3):
    """ Make a density plot that shows the fraction of worms glowing over time.
    
    Parameters
    ----------
    mid_bin : a list of integers or floats
        Worms will be counted at each hour indicated in this list.
    worms0 : a list of floats (first treatment group)
        Each list from the sort_worm function replaced by a float that represents the fraction molting.
    worms1 : a list of floats (second treatment group)
        Each list from the sort_worm function replaced by a float that represents the fraction molting.
    worms2 : a list of floats (third treatment group)
        Each list from the sort_worm function replaced by a float that represents the fraction molting.
    worms3 : a list of floats (fourth treatment group)
        Each list from the sort_worm function replaced by a float that represents the fraction molting.
    """
    
    # plot four lines on top of each other
    plt.plot(mid_bin, worms0, color="blue")
    plt.plot(mid_bin, worms1, color="orange")
    plt.plot(mid_bin, worms2, color="green")
    plt.plot(mid_bin, worms3, color="red")
    # add title and axes labels
    plt.suptitle("Unsynchronized Worms")
    plt.xlabel("Time in Hours")
    plt.ylabel("Fraction Glowing")
    # add a legend to identify treatment groups
    plt.legend([mp.Circle((0.5, 0.5), radius=0.25, facecolor="blue", edgecolor="none"),
                mp.Circle((0.5, 0.5), radius=0.25, facecolor="orange", edgecolor="none"),
                mp.Circle((0.5, 0.5), radius=0.25, facecolor="green", edgecolor="none"),
                mp.Circle((0.5, 0.5), radius=0.25, facecolor="red", edgecolor="none")],
               ["6 mg/mL", "4.8 mg/mL", "3.6 mg/mL", "2.4 mg/mL"])
    
    
def run(hour=1, spread=8, size=50, diff=1):
    """ String all the functions together to run the code with a single master function.
    
    Parameters
    ----------
    hour : an int or a float (default value = 1)
        This represents the frequency that data are collected. (ie worms counted ____ times per hour)
    spread : an int or a float (default value = 8)
        Used to controll the variance in starting age of the worm. If the spread is small, worms will be roughly the same age.
    size : an int (default value = 50)
        The number of worms in each treatment group.
    diff : an int or a float
        The difference in means between treatment groups. (UNKNOWN in real life)
    """
    
    # create the 4 treatment groups using the Class Worm
    worms = create_groups(spread, diff, size)    
    
    # determine when each worm molts by molt_age minus current age
    molt = find_molt(size, worms)
    
    # find the smallest of the molting times and round down to the nearest hour
    small = find_small(molt, hour)
    
    # find the largest of the molting times and round up to the nearest hour
    big = find_big(molt, hour)
    
    # determine when worms will be counted (ie the setup for creating the bins)
    mid_bin = find_mid_bin(small, big, hour)
    
    # create bins that are 3 hours wide for each time counted
    bins = create_bin(mid_bin)
    
    # determine worms that fall into each bin based on when they molt
    # repeat for each of the 4 treatment groups separately
    sorted_worms0 = sort_worm(0, bins, molt) 
    sorted_worms1 = sort_worm(1, bins, molt)
    sorted_worms2 = sort_worm(2, bins, molt)
    sorted_worms3 = sort_worm(3, bins, molt)
    
    # adjust groupings so they contain realistic data, ie mid_bin times not exact molting times
    # repeat for each of the 4 treatment groups separately
    flat_worm0 = fix_data(sorted_worms0, mid_bin)
    flat_worm1 = fix_data(sorted_worms1, mid_bin)
    flat_worm2 = fix_data(sorted_worms2, mid_bin)
    flat_worm3 = fix_data(sorted_worms3, mid_bin)
    
    # prints one-tailed p values and significance between flat_worm data from the treatment groups
    # repeat for each pairing of the closest treatment groups (ie 1&2, 2&3, 3&4)
    stats_test(flat_worm0, flat_worm1)
    stats_test(flat_worm1, flat_worm2)
    stats_test(flat_worm2, flat_worm3)
    
    # determine the percentage of worms molting at each time
    # repeat for each of the 4 treatment groups separately
    worms0 = find_density(sorted_worms0, size)
    worms1 = find_density(sorted_worms1, size)
    worms2 = find_density(sorted_worms2, size)
    worms3 = find_density(sorted_worms3, size)
    
    # make a density plot that shows the fraction of worms glowing over time
    make_plot(mid_bin, worms0, worms1, worms2, worms3)
    