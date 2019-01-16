import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import GetLabels
import PlotSupport

########       Script for plotting data
# - Takes in specified pickles as pickle1, pickle2, etc., with optional specifications as cycles1, cycles2, colorscheme1, etc.
# - Sets specification for first pickle (default values are all cycles, blue color and/or 'Blues' color scheme (depending on x variable))
# - Plots first pickle with these specifications
# - Attempts to read next pickle,
#       - If so, sets next pickle specifications and add this to plot.
# - If no more pickles, add labels etc and show plot.

def plotter(**kwargs):
    x1, y1, xlim, ylim, legend_list, legend_loc, legend_color_list = PlotSupport.SetPlotSpecs(**kwargs) # Sets specifications for plot
    pickle_name, df, cycles, color, color_list, legend_color_list = PlotSupport.SetPickleSpecs(legend_color_list,**kwargs) # Sets specifications for first pickle

    PlotSupport.AddPickleToPlot(df, cycles, x1, y1, color_list)       # Adds this pickle with specifications to plot

    for nr in range (2, 50):        # Does the same for rest of the wanted pickles (here up to 50).
        try:                        # Attempts to read next pickle. If found, will set specifications and add pickle to plot as above.
            next_pickle_name, next_cycles, next_color, next_color_scheme = PlotSupport.SetNextPickle(nr, **kwargs)
            pickle_name, df, cycles, color, color_list, legend_color_list = PlotSupport.SetPickleSpecs(legend_color_list, pickle1=next_pickle_name, cycles1=next_cycles, x1=x1, y1=y1, color1=next_color, color_scheme1=next_color_scheme)
            PlotSupport.AddPickleToPlot(df, cycles, x1, y1, color_list)
        except:
            continue # Script moves to next iteration, checking for yet another pickle.

    PlotSupport.PlotPlot(x1,y1, xlim, ylim, legend_list, legend_color_list, legend_loc) # Add labels and legend, and shows plot

    return



#####    Script for testing function
# pickle_name_1 = '/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\B1_combi_t01_02_APC-THF_2_1Vto0_2V_0_01C'
# pickle_name_2 = '/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\B1_combi_t03_01_LiBH4_1_7to0_2V_0_01C_CE1'
#
# #      Outputs
# plotter(pickle1=pickle_name_1, pickle2=pickle_name_2, x1='cycle_nr', y1='discharge_spec',legend=['Cell 1', 'Cell 2'])
# plotter(pickle1=pickle_name_1, pickle2=pickle_name_2, x1='cap_incr_spec', y1='potential', cycles1=[0,1,5,10], color1='blue', color_scheme2='magma',legend=['Cell 1', 'Cell 2'], legend_loc=1)

# Todo:
# - Multiple y-axis (e.g. Coloumbic efficiency or both charge and discharge).
# - Specify x and y ticks.
# - Specify x and y labels.