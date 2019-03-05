import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import get_labels                  # For verifying correct x and y input
import support                    # For error handling
import matplotlib.pyplot as plt   # Plottepakke
import matplotlib.patches as mpatches # Legend in plot
import sys                        # For aborting scripts
import get_labels                  # For labels to x and y variables
import math                       # For floor
import user_setup

#-----------------------------------------------------------------------------------
########       Function for making list of color codes
## Takes optional color scheme as input
## Returns vector of colors to be used in plot

def get_colors(df, cycles=None, color=None, color_scheme=None):
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
        last_cycle = df['cycle'].as_matrix().astype(int)[-1]  # Converts cycle column to int, and get last element (last cycle nr).
        cycles = range(0, last_cycle, 1)   # Creates list from 0 to last cycle, increment 1

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
def default_color_gradients (nr):
    return {
        1 : 'Blues',
        2 : 'Oranges',
        3 : 'Greens',
        4 : 'Greys',
        5 : 'Purples',
        6 : 'Reds',
        7 : 'YlOrBr',
        8 : 'GnBu',
        9 : 'spring',
        10: 'cool',
    }[nr]
#-----------------------------------------------------------------------------------
def set_plot_specs(**kwargs):
    try:
        x1 = kwargs['x1']
        get_labels.get_labels(x1)
    except:
        support.error_message('Not recognizable x variable (error in set_plot_specs - get_labels)')
    try:
        y1 = kwargs['y1']
        get_labels.get_labels(y1)
    except:
        support.error_message('Not recognizable y variable (error in set_plot_specs - get_labels)')
    try:
        xlabel = kwargs['xlabel']
    except:
        xlabel = None
    try:
        ylabel = kwargs['ylabel']
    except:
        ylabel = None
    try:
        xlim = kwargs['xlim']
    except:
        xlim = None
    try:
        ylim = kwargs['ylim']
    except:
        ylim = None
    try:
        xticks = kwargs['xticks']
    except:
        xticks = None
    try:
        yticks = kwargs['yticks']
    except:
        yticks = None
    try:
        legend = kwargs['legend']
    except:
        try:
            legend = kwargs['autolegend']   # autolegend variable used by auto_plot if no legend is specified.
        except:
            legend = None
    try:
        legend_loc = kwargs['legend_loc']
    except:
        legend_loc = 1

    legend_color_list = []      # list of colors for each legend entry.

    try:
        custom_code = kwargs['custom_code']
    except:
        custom_code = None
    try:
        save_path = kwargs['save_path']
    except:
        try:
            save_name = kwargs['save_as']
            save_path = str(user_setup.plots) + '\\' + save_name
        except:
            save_path = None

    return (x1,y1, xlabel, ylabel, xlim, ylim, xticks, yticks, legend, legend_loc, legend_color_list, custom_code, save_path)

#-----------------------------------------------------------------------------------

def set_pickle_specs (legend_color_list, **kwargs):

    pickle_name = kwargs['pickle1']
    df = pd.read_pickle(pickle_name)  # Reads pickle as strings

    try:
        cycles = kwargs['cycles1']
    except:
        last_cycle = math.floor(df['cycle'].as_matrix().astype(float)[-1])    # Converts cycle column to float, then rounds last element (last cycle) down using floor function to convert to int.
        cycles = range(0, last_cycle+1, 1)  # Creates list from 0 to last cycle, increment 1. Need +1 after last cycle to get actual last cycle. Look up range function.
    if cycles == None:                       # In the case that cycles1 = None from user.
        last_cycle = math.floor(df['cycle'].as_matrix().astype(float)[-1])    # Converts cycle column to float, then rounds last element (last cycle) down using floor function to convert to int.
        cycles = range(0, last_cycle+1, 1)  # Creates list from 0 to last cycle, increment 1. Need +1 after last cycle to get actual last cycle. Look up range function.
    try:
        color_scheme = kwargs['color_scheme1']
    except:
        color_scheme = default_color_gradients(1)
    try:
        color = kwargs['color1']
    except:
        if kwargs['x1'] != 'cap_incr_spec':
            color = plt.get_cmap("tab10")(0)       # Default color is first color in tab10 colors (blue).
        else:
            color = None

    color_list = get_colors(df, cycles, color, color_scheme)     # Choose color maps from: https://matplotlib.org/examples/color/colormaps_reference.html

    legend_color_list.append(color_list[round(len(color_list) / 2)])  # Sets color for legend to be middle color if multiple cycles.

    return (pickle_name, df, cycles, color, color_list, legend_color_list)

#-----------------------------------------------------------------------------------
def add_limits(xlim, ylim):  # Specifies x and y limits
    if xlim != None:    # If not specified, will plot default
        try:
            plt.xlim(xlim)  # Specifies x limits (min, max) from user
        except:
            print ('Not recognisable x limits. \n Format: xlim = [min, max] \n Example: xlim = [0, 50]')
    if ylim != None:
        try:
            plt.ylim(ylim)  # Specifies y limits (min, max) from user
        except:
            print ('Not recognisable y limits. \n Format: ylim = [min, max] \n Example: ylim = [0.1, 2.2]')
    return
#-----------------------------------------------------------------------------------
def add_ticks(xticks, yticks):  # Specifies x and y ticks
    if xticks != None:    # If not specified, will plot default
        try:
            plt.xticks(xticks)   # Specifies x ticks from user
        except:
            print ('Not recognisable x ticks. \n Format: xticks = [value1,value2,...] \n Example: xticks=[25,50,75,100]')
    if yticks != None:
        try:
            plt.yticks(yticks)   # Specifies y ticks from user
        except:
            print ('Not recognisable y ticks. \n Format: yticks = [value1, value2, value3, ...] \n Example: yticks = [0, 0.5, 1, 1.5]')
    return
#-----------------------------------------------------------------------------------
def add_labels(x1, y1, xlabel, ylabel):  # Add label to plot
    if xlabel == None:
        plt.xlabel(get_labels.get_labels(x1))  # Adds default label corresponding to variable
    else:
        plt.xlabel(xlabel)
    if ylabel == None:
        plt.ylabel(get_labels.get_labels(y1))  # Adds default label corresponding to variable
    else:
        plt.ylabel(ylabel)

    return
#-----------------------------------------------------------------------------------
def add_legend(legend, colorlist, legend_loc=1):       # Legend guide: https://matplotlib.org/users/legend_guide.html
    if legend == None:
        return
    patches=[]
    for i in range(0, len(legend)):     # Iterates through each legend entry
        patches.append(mpatches.Patch(color=colorlist[i], label=legend[i]))  #Sets legend color and text
    plt.legend(handles=patches, loc=legend_loc)     # Add all the specified legends to the plot.
    return
#-----------------------------------------------------------------------------------
def add_custom (custom_code):    # Executes string in custom_code as code. Multiple lines separated by \n. Ex: custom_code='plt.text(50,1,\'Awesome\') \nplt.text(100,1,\'Awesomer\')'
    if custom_code!= None:
        try:
            exec(custom_code)
        except:
            print('Not recognisable custom code. Needs to be one string, where multiple lines are separated by \\n.')
    return
#-----------------------------------------------------------------------------------
def SavePlot(save_path): # Save high resolution by saving displayed plot as .eps and use that in latex, or as png by using save_path variable
    if save_path!=None:  # Saves plot as png, if save_path variable is used.
        plt.savefig((save_path+'.png'), format='png', dpi=1000)     # > 300 DPI is recommended by NTNU in master theses.
    return
#-----------------------------------------------------------------------------------


def AddPickleToPlot (df, cycles, x1, y1, color_list):

    for i in range(0, len(cycles)):     # OBS: When plotting capacity vs cycle, it will only iterate once (different type of "cycle variable")
        df_cycle_x = df[df['cycle'].astype(float) == cycles[i]]   # Make new data frame for given cycle
        plt.scatter(df_cycle_x[x1].astype(float), df_cycle_x[y1].astype(float), s=2, c=color_list[i])  # s = size
    return

#-----------------------------------------------------------------------------------

def set_next_pickle (nr, **kwargs):

    try:
        kwargs['pickle'+str(nr-1)] = kwargs['pickle'+str(nr)]
    except:
        try:
            kwargs['pickle' + str(nr - 1)] = kwargs['override']
        except:
          sys.exit(0)
    try:
        kwargs['y' + str(nr - 1)] = kwargs['y' + str(nr)]   # Looks for y2 etc, will be plotted on same axis as before.
    except:
        kwargs['y' + str(nr - 1)] = kwargs['y1']
    try:
        kwargs['cycles'+str(nr - 1)] = kwargs['cycles'+str(nr)]
    except:
        kwargs['cycles'+str(nr - 1)] = None
    try:
        kwargs['color_scheme'+str(nr - 1)] = kwargs['color_scheme'+str(nr)]
    except:
        kwargs['color_scheme'+str(nr - 1)] = default_color_gradients(nr)
    try:
        kwargs['color'+str(nr - 1)] = kwargs['color'+str(nr)]
    except:
        if kwargs['x1'] != 'cap_incr_spec':
            kwargs['color'+str(nr - 1)] = plt.get_cmap("tab10")(nr-1)
        else:
            kwargs['color'+str(nr - 1)] = None

    return (kwargs['pickle'+str(nr-1)],kwargs['y' + str(nr - 1)],kwargs['cycles'+str(nr-1)],  kwargs['color'+str(nr-1)], kwargs['color_scheme'+str(nr-1)])

#-----------------------------------------------------------------------------------
def plot_plot(x1, y1, xlabel, ylabel, xlim, ylim, xticks, yticks, legend_list, legend_color_list, legend_loc, custom_code, save_path):

    add_limits(xlim, ylim) # Changes x and y limits (min, max), if specified.
    add_ticks(xticks, yticks) # Changes x and y ticks (min, max), if specified.
    add_labels(x1, y1, xlabel, ylabel) # Adds label, either default to variable or specified
    add_legend(legend_list, legend_color_list, legend_loc) # Adding legend(s) to plot.
    add_custom(custom_code) # Executes string in custom_code as code. Multiple lines separated by \n. Ex: custom_code='plt.text(50,1,\'Awesome\') \nplt.text(100,1,\'Awesomer\')'

    SavePlot(save_path) # Save high resolution by saving displayed plot as .eps and use that in latex, or as png by using save_path variable

    plt.show()

    return
#-----------------------------------------------------------------------------------
