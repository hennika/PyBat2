import pandas as pd
import PlotSupport

########       Script for plotting data
# - Takes in specified pickles as pickle1, pickle2, etc., with optional specifications as cycles1, cycles2, colorscheme1, etc.
# - Sets specification for first pickle (default values are all cycles, blue color and/or 'Blues' color scheme (depending on x variable))
# - Plots first pickle with these specifications
# - Attempts to read next pickle,
#       - If so, sets next pickle specifications and add this to plot.
# - If no more pickles, add labels etc and show plot.

def plotter(**kwargs):
    x1, y1, xlabel, ylabel, xlim, ylim, xticks, yticks, legend_list, legend_loc, legend_color_list, custom_code, save_path = PlotSupport.SetPlotSpecs(**kwargs) # Sets specifications for plot
    pickle_name, df, cycles, color, color_list, legend_color_list = PlotSupport.SetPickleSpecs(legend_color_list,**kwargs) # Sets specifications for first pickle

    PlotSupport.AddPickleToPlot(df, cycles, x1, y1, color_list)       # Adds this pickle with specifications to plot

    for nr in range (2, 50):        # Does the same for rest of the wanted pickles (here up to 50).
        try:                        # Attempts to read next pickle. If found, will set specifications and add pickle to plot as above.
            next_pickle_name, next_y, next_cycles, next_color, next_color_scheme = PlotSupport.SetNextPickle(nr, **kwargs)
            pickle_name, df, cycles, color, color_list, legend_color_list = PlotSupport.SetPickleSpecs(legend_color_list, pickle1=next_pickle_name, cycles1=next_cycles, x1=x1, y1=next_y, color1=next_color, color_scheme1=next_color_scheme)
            PlotSupport.AddPickleToPlot(df, cycles, x1, next_y, color_list)
        except:
            continue # Script moves to next iteration, checking for yet another pickle.

    PlotSupport.PlotPlot(x1,y1, xlabel, ylabel, xlim, ylim, xticks, yticks, legend_list, legend_color_list, legend_loc, custom_code, save_path) # Add labels and legend, and shows plot

    return



#####    Script for testing function
pickle_name_1 = '/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\B1_combi_t02_01_APC-THF_2_4Vto0_2V_0_01C'
pickle_name_2 = '/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\B1_combi_t03_01_LiBH4_1_7to0_2V_0_01C_CE1'
pickle_name_3= '/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\TixC_10HF17a_S_T1_02_APC_002C'

custom = 'plt.text(50,1,\'Awesome\') \nplt.text(100,1,\'Awesomer\')'
plot1_path = '/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Graphs\Plot1'

#df = pd.read_pickle(pickle_name_1)  # Reads pickle
#print(df['cycle'])

##      Outputs
#plotter(pickle1=pickle_name_1, pickle2=pickle_name_2, x1='cycle_nr', y1='discharge_spec', legend=['Cell 1', 'Cell 2'])
#plotter(pickle1=pickle_name_2, pickle2=pickle_name_3, xlim=[0,150], ylim=[0.1,2.2], xticks=[0,50,100,150], yticks=[0.2, 1, 1.5, 2.1], xlabel='Capacity (mAh/g active material)',ylabel='Potential vs Mg/Mg$^{2+}$', x1='cap_incr_spec', y1='potential', cycles1=[0,1,5,10], color1='blue', color_scheme2='magma',legend=['Cell 1', 'Cell 2'], legend_loc=1, custom_code=custom, save_path=plot1_path)
#plotter(pickle1=pickle_name_3, x1='cap_incr_spec', y1='potential', legend=['Cell cycled on Lanhe!'], legend_loc=7)

# Todo:
# - Multiple y-axis (e.g. Coloumbic efficiency or both charge and discharge).
# - Add fontsize as user input and argument in labels, limits etc