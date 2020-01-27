import pandas as pd
import export_data
import user_setup
import automate
import access_data
import support
# Initializing using user_setup file
raw_data = user_setup.raw_data               # Location to raw data (text files).
database = user_setup.database               # Location to where the imported cells will be (when saved as pickle)
exported_data = user_setup.exported_data     # Location to where the exported data will be
plots = user_setup.plots                     # Location to where plots are saved



"""
#########################################################################
#               Start here! 
######################################################################### 
           OBS: remove # to run code 
"""

# Search for cells to import or plot:
#search_word = 'Ti3C2'

# IMPORT:
#automate.auto_import(search_word)

# Merge:
#automate.merge_biologic2(search_word)

# Change cycle definition:
#automate.change_cycle_def(search_word)
# Add column from columns:
#automate.add_column(search_word, 'multiply_scalar', 'current_uA', 'current', 1000)
#automate.add_column(search_word, 'multiply_scalar', 'time_hour', 'time', 1/3600)
#automate.add_column(search_word, 'multiply_scalar', 'potential', 'Ew', 1)
#automate.add_column(search_word, 'CL+CCL')  # Capacity loss (discharge-charge) and cumulative capacity loss.

# PLOT:
#automate.auto_plot(search_word, x1 = 'cap_incr_spec', y1 = 'potential', cycles1=[1])
#automate.auto_plot(search_word, x1 = 'Re_Z', y1 = '-Im_Z', markersize=8, custom_code='plt.axis(\'equal\')')
#automate.auto_plot(search_word, x1 = 'Re_Z', y1 = '-Im_Z', y2='-Im_Zce', y3='-Im_Zwe-ce', markersize=8)

# More advanced plotting: include arguments as you wish. OBS! separate arguments by comma, but not comma after last argument!
# Ex:

"""automate.auto_plot(search_word,
                    x1 = 'cap_incr_spec',
                    y1 = 'potential',
                   #x1 = 'potential_diff_cap',
                   #y1 = 'diff_cap',
                   #y2 = 'charge_spec',
                   #y1 = 'current',
                   #y1 = 'Ew',
                  # y1 = 'Ew-Ec',
                   #y2 = 'Ew-Ec',
                   #y3 = 'Ec_inv',
                   cycles1 = [1,10],
                   cycles2 = [1,10],
                   #cycles1=[0,1,5,10,50,100],
                   #cycles1=[0,1,2,3,4],
                   # cycles2=[0,5,8,10],
                   # cycles3=[0,5,8,10],
                   #cycles2=[0,1,2,3,4],
                   #cycles3=[0,1,2,3,4],
                   #color_scheme1 = 'Qualitative',
                   #color_scheme1= 'Oranges',
                   #color1='blue',
                   #color2='orange',
                   #legend_color_type='individual_cycles',
                   #legend=['Cycle 1', 'Cycle 2'],
                   #legend = ['Full cell', 'Cathode', 'Anode'],
                  #legend = ['Mg(TFSI)$_{2}$-2MgCl$_{2}$ in DME'],
                   #legend = ['Cycle 1-15'],
                   legend_loc = 5,
                    xlabel='Capacity (mAh/g PMTT)',
                    ylabel='Potential (V vs Mg/Mg$^{2+}$)',
                    #ylabel='Current (mA)',
                   #ylabel = 'Capacity (mAh/g PMTT)',
                   custom_code_first = 'plt.rcParams.update({\'font.size\': 14})',
                   custom_code = 'plt.tick_params(direction=\'in\')\n'
                                'plt.tight_layout()',  # For fixing labels outside chart.
                   #custom_code = 'plt.axhline(color=\'black\',linewidth=1,y=0) \nplt.axvline(color=\'black\',linewidth=1, x=0)',
                    #ylabel='Current (mA)',
                   #xlim = [0, 350],
                   ylim = [-0.03, 2.7],
                   #markersize=10,
                   #xticks = [0, 5, 10, 15],
                   yticks = [0, 0.5, 1, 1.5, 2, 2.5],
                    #cycles1 = [0, 1, 10],                 # Plot only certain cycles for cell 1
                    #cycles2 = [0, 1, 10],                 # Plot only certain cycles for cell 2
                    legend = ['50 mA/g', '100 mA/g'],       # OBS: nr of legend strings must match nr of cells
                    #save_as='MP1H\MP1H_D1_03_and_06_50-and-100mA_1_and10cycles'              # Save plot in plots folder as png file (1000 dpi)
                   )"""



""" Plotting multiple y-axes manually"""
"""
import matplotlib.pyplot as plt   # Plottepakke
cell_1 = pd.read_pickle('C:\\Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\PMTT_D2_03_Cel_01to3V')  # Reads pickle as strings
cell_1_cycles = support.str_to_float(cell_1['cycle_nr'].tolist())  # Extracting cycle number as float
cell_1_disch= support.str_to_float(cell_1['discharge_spec'].tolist())  # Extracting discharge capacities as float
cell_1_char = support.str_to_float(cell_1['charge_spec'].tolist())  # Extracting charge capacitiies as float
cell_1_eff = [float(ai)/bi*100 for ai,bi in zip(cell_1_disch,cell_1_char)]  # Obtaining Coulombic efficiencies

# Plotting charge and discharge on first y-axis, and Coulombic effiiency on secondary y-axis. Both vs same x-axis (cycle number)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(cell_1_cycles, cell_1_disch, 'g-')
ax1.plot(cell_1_cycles, cell_1_char, 'g--')
ax2.plot(cell_1_cycles, cell_1_eff, 'b-')

ax1.set_xlabel('Cycle number')
ax1.set_ylabel('Capacity (mAh/g active material)', color='g')
ax2.set_ylabel('Coulombic efficiency (%)', color='b')

ax2.set_ylim(0, 100)

fig.tight_layout()  # Makes sure everything is within figure
ax1.legend(['Discharge','Charge'], loc=1, prop={'size': 12})
plt.show()
"""


# EXPORT:
#export_cell = 'TixC-S31_T1_01'                      # Cell to export (pickle name)
#export_file = 'your_filename_here'                  # Filename of exported file
#export_variables = ['cap_incr_spec', 'potential']   # Variables to export (as many as you like)
# Run this:
#export_data.export_data(export_cell, export_file, export_variables)





"""
More stuff below
"""
# Additional plotting arguments:
#
#xlim = [0, 150]             # Specify x limits
#ylim = [0.1,2.2]            # Specify y limits
#xticks=[0,50,100,150]       # Specify x ticks (which x values to show on plot)
#yticks=[0.2, 1, 1.5, 2.1]   # Specify y ticks (which y values to show on plot)
#xlabel='Capacity (mAh/g active material)'   # Override default x label
#ylabel='Potential vs Mg/Mg$^{2+}$'          # Override default y label
#cycles1=[0,1,5,10]          # Only plot some specific cycles for cell 1 (can be done similar for cell 2 etc)
#color1='mediumblue'         # Specify if you want certain color for cell 1 (can be done similar for cell 2 etc). Choose among these: https://matplotlib.org/examples/color/named_colors.html
#color_scheme2='YlOrBr'      # Specify if you want certain color scheme, e.g. a gradient for different cycles. Choose among these: https://matplotlib.org/examples/color/colormaps_reference.html
#legend=['Cell 1', 'Cell 2'] # Specify legend. Remember to adjust for number of cells.
#legend_loc=1                # Specify where legend will be in plot (e.g. "2" is up left in plot)
#custom_code = 'plt.text(50,1,\'So science\') \nplt.text(90,1.75,\'Much wow\')'       # Code that will be executed to customize plot (add text, arrows etc).
#save_as = 'my_new_plot'  # Name of plot that will be saved in high resolution (1000 dpi) in plots folder