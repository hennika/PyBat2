import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import GetLabels                  # For verifying correct x and y input
#import Error                      # For error handling
import matplotlib.pyplot as plt   # Plottepakke
import matplotlib.patches as mpatches # Legend in plot
import sys                        # For aborting scripts
import GetLabels                  # For labels to x and y variables


#-----------------------------------------------------------------------------------
########       Function for making list of color codes
## Takes optional color scheme as input
## Returns vector of colors to be used in plot

def GetColors(df, cycles=None, color=None, color_scheme=None):
    color_list = []     # This will be the return variable containing all colors to be plotted.

    if color!=None:     # If single color is specified, color list will be a list of the same color for every cycle.
        for i in range(0, len(cycles)):
            color_list.append(color)
        return color_list

    # If color is qualitative, will use tab10 as default: https://matplotlib.org/examples/color/colormaps_reference.html
    if color_scheme == 'Qualitative':
        color_list = plt.cm.tab10(np.linspace(0, 1, len(cycles)))
        return color_list

    if (cycles==None):        # If no cycles are defined, will plot all cycles
            last_cycle = df.astype(float).tail(1)['cycle'].as_matrix().astype(int)      # Reads df column "cycle" as float, returns last element as int.
            cycles = range(0, last_cycle[0], 1)   # Creates list from 0 to last cycle, increment 1

    color_min = 100  # Minimum color (if zero, first color is almost white).
    color_max = 300  # Maximum color, 300 looks nice.
    color_nr = color_min  # Color for each plot (used in loop below)
    try:
        color_iter = int(
            (color_max - color_min) / (len(cycles) - 1))  # If e.g. 3 cycles, want 300-100 = 200, 200/2=100 iteration.
    except:      # Need this exception to not divide by zero if plotting only one cycle.
        color_iter = 0  # If only one cycle is plotted, will not need to change color.
        color_nr = (color_min+color_max)/2      # Color is set to average of minimum and maximum.

    for i in range(0, len(cycles)):
        color_list.append(getattr(plt.cm, color_scheme)(color_nr))  # Setting color for given cycle
        color_nr = color_nr + color_iter  # Next color or color gradient

    return color_list

#-----------------------------------------------------------------------------------
def DefaultColorGradients (nr):
    return {
        1 : 'Blues',
        2 : 'Oranges',
        3 : 'Greens',
        4 : 'Reds',
        5 : 'Purples',
        6 : 'Greys',
        7 : 'YlOrBr',
        8 : 'GnBu',
        9 : 'spring',
        10: 'cool',
    }[nr]
#-----------------------------------------------------------------------------------
def SetPlotSpecs(**kwargs):
    try:
        x1 = kwargs['x1']
        GetLabels.GetLabels(x1)
    except:
        Error.Message('Not recognizable x variable')
    try:
        y1 = kwargs['y1']
        GetLabels.GetLabels(y1)
    except:
        Error.Message('Not recognizable y variable')
    try:
        xlim = kwargs['xlim']
    except:
        xlim = None
    try:
        ylim = kwargs['ylim']
    except:
        ylim = None
    try:
        legend = kwargs['legend']
    except:
        legend = None
    try:
        legend_loc = kwargs['legend_loc']
    except:
        legend_loc = 1

    legend_color_list = []      # list of colors for each legend entry.

    return (x1,y1, xlim, ylim, legend, legend_loc, legend_color_list)

#-----------------------------------------------------------------------------------

def SetPickleSpecs (legend_color_list, **kwargs):

    pickle_name = kwargs['pickle1']
    df = pd.read_pickle(pickle_name)  # Reads pickle as strings

    try:
        cycles = kwargs['cycles1']
    except:
        last_cycle = df.astype(float).tail(1)['cycle'].as_matrix().astype(int)
        cycles = range(0, last_cycle[0], 1)  # Creates list from 0 to last cycle, increment 1
    if cycles == None:                       # In the case that cycles1 = None from user.
        last_cycle = df.astype(float).tail(1)['cycle'].as_matrix().astype(int)
        cycles = range(0, last_cycle[0], 1)  # Creates list from 0 to last cycle, increment 1
    try:
        color_scheme = kwargs['color_scheme1']
    except:
        color_scheme = DefaultColorGradients(1)
    try:
        color = kwargs['color1']
    except:
        if kwargs['x1'] != 'cap_incr_spec':
            color = plt.get_cmap("tab10")(0)       # Default color is first color in tab10 colors (blue).
        else:
            color = None

    color_list = GetColors(df,cycles, color, color_scheme)     # Choose color maps from: https://matplotlib.org/examples/color/colormaps_reference.html

    legend_color_list.append(color_list[round(len(color_list) / 2)])  # Sets color for legend to be middle color if multiple cycles.

    return (pickle_name, df, cycles, color, color_list, legend_color_list)

#-----------------------------------------------------------------------------------
def AddLegend(legend, colorlist, legend_loc=1):       # Legend guide: https://matplotlib.org/users/legend_guide.html
    if legend == None:
        return
    patches=[]
    for i in range(0, len(legend)):     # Iterates through each legend entry
        patches.append(mpatches.Patch(color=colorlist[i], label=legend[i]))  #Sets legend color and text
    plt.legend(handles=patches, loc=legend_loc)     # Add all the specified legends to the plot.
    return

#-----------------------------------------------------------------------------------


def AddPickleToPlot (df, cycles, x1, y1, color_list):

    for i in range(0, len(cycles)):     # OBS: When plotting capacity vs cycle, it will only iterate once (different type of "cycle variable")
        df_cycle_x = df[df['cycle'].astype(float) == cycles[i]]   # Make new data frame for given cycle
        plt.scatter(df_cycle_x[x1].astype(float), df_cycle_x[y1].astype(float), s=2, c=color_list[i])  # s = size

    return

#-----------------------------------------------------------------------------------

def SetNextPickle (nr, **kwargs):

    try:
        kwargs['pickle'+str(nr-1)] = kwargs['pickle'+str(nr)]
    except:
          sys.exit(0)
    try:
        kwargs['cycles'+str(nr - 1)] = kwargs['cycles'+str(nr)]
    except:
        kwargs['cycles'+str(nr - 1)] = None
    try:
        kwargs['color_scheme'+str(nr - 1)] = kwargs['color_scheme'+str(nr)]
    except:
        kwargs['color_scheme'+str(nr - 1)] = DefaultColorGradients(nr)
    try:
        kwargs['color'+str(nr - 1)] = kwargs['color'+str(nr)]
    except:
        if kwargs['x1'] != 'cap_incr_spec':
            kwargs['color'+str(nr - 1)] = plt.get_cmap("tab10")(nr-1)
        else:
            kwargs['color'+str(nr - 1)] = None

    return (kwargs['pickle'+str(nr-1)],kwargs['cycles'+str(nr-1)],  kwargs['color'+str(nr-1)], kwargs['color_scheme'+str(nr-1)])

#-----------------------------------------------------------------------------------
def PlotPlot(x1, y1, xlim, ylim, legend_list, legend_color_list, legend_loc):

    plt.xlim(xlim)      # Specifies x limits (min, max)
    plt.ylim(ylim)      # Specifies y limits (min, max)

    plt.xlabel(GetLabels.GetLabels(x1))  # Gets label corresponding to variable
    plt.ylabel(GetLabels.GetLabels(y1))  # Gets label corresponding to variable

    AddLegend(legend_list, legend_color_list, legend_loc) # Adding legend(s) to plot.

    plt.show()

    return
#-----------------------------------------------------------------------------------
