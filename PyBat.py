
import user_setup
from pathlib import Path
import automate
import numpy as np                # Matrise pakke
import glob
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import string_to_float
import import_data as id
import add_specific_capacity
import fix_uneven_length            # Makes two list same length by removing or adding element
import sys                        # For exiting script among other
import convert_to_pandas
import plotter
import access_data
import support
# Initializing using user_setup file
raw_data = user_setup.raw_data               # Location to raw data (text files).
database = user_setup.database               # Location to where the imported cells will be (when saved as pickle)
#exported_data = user_setup.exported_data     # Location to where the exported data will be
#plots = user_setup.plots                     # Location to where plots are saved



"""
#########################################################################
#               Start here! 
######################################################################### 
           OBS: remove # to run code 
"""


#search_word = 'Random'
automate.auto_plot(search_word,
                   x1 = 'cap_incr_spec',
                   y1 = 'potential',
                   #x1 = 'potential_diff_cap',
                   #y1 = 'diff_cap'
                   #cycles1=[0, 1, 10]
                   #      cycles2=[0, 1, 10],
                   #     cycles3=[0, 1, 10],
                   #    legend=['Cell 1', 'Cell 2', 'Cell 3'],
                   #   xlabel='Capacity (mAh/g MXene)',
                   #  ylabel='Potential (V vs Mg/Mg$^{2+}$)',
                   # save_as='Cells on all three testers'
                   )





# Search for cells to import or plot:
search_word = 'Random'



# IMPORT:
#automate.auto_import(search_word)


# PLOT:
automate.auto_plot(search_word, x1 = 'cap_incr_spec', y1 = 'potential')

# More advanced plotting: include arguments as you wish. OBS! separate arguments by comma, but not comma after last argument!
# Ex:
#automate.auto_plot(search_word,
                    #x1 = 'cap_incr_spec',
                    #y1 = 'potential',
                    #xlabel='Capacity (mAh/g active material)',
                    #ylabel='Potential (V vs Mg/Mg$^{2+}$)',
                    #cycles1 = [0, 1, 10],                 # Plot only certain cycles for cell 1
                    #cycles2 = [0, 1, 10],                 # Plot only certain cycles for cell 2
                    #legend = ['Cell 1', 'Cell 2'],       # OBS: nr of legend strings must match nr of cells
                    #save_as='My first plot'              # Save plot in plots folder as png file (1000 dpi)
                   #)

# EXPORT:
#export_cell = 'TixC-S31_T1_01'                      # Cell to export (pickle name)
#export_file = 'your_filename_here'                  # Filename of exported file
#export_variables = ['cap_incr_spec', 'potential']   # Variables to export (as many as you like)
# Run this:
#support.export_data(export_cell, export_file, export_variables)






















































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

# !! OBS: functions below not tested !!
#Input/Conversion of data:
# --------------------------------------------
#support.search_file(search_word, raw_data)    # search_word: Key word which will be search for. CellDatabase/raw_data: Location that will be searched in.


#Automate.automatic_conversion(search_word,raw_data,database)
#Automate.merge_biologic(search_word, CellDatabase)


# support.about(CellDatabase.as_posix(),'/F_SiO2MSC2_1_R0')


#---------------------Accessing Data-------------------


#automate.automatic_conversion(search_word,raw_data,database)
#automate.merge_biologic(search_word, CellDatabase)
# Accessing Data:
# --------------------------------------------
#support.About(CellDatabase.as_posix(),'/F_SiO2MSC2_1_R0')

#Data = 'Cell_info'
#output = access_data.access_cell_data(Cell)
#print(output)
=======
import user_setup
from pathlib import Path
import automate
import numpy as np                # Matrise pakke
import glob
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import string_to_float
import import_data as id
import add_specific_capacity
import fix_uneven_length            # Makes two list same length by removing or adding element
import sys                        # For exiting script among other
import convert_to_pandas
import plotter
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
search_word = 'Random'


# IMPORT:
#automate.auto_import(search_word)


# PLOT:
automate.auto_plot(search_word, x1 = 'cap_incr_spec', y1 = 'potential')

# More advanced plotting: include arguments as you wish. OBS! separate arguments by comma, but not comma after last argument!
# Ex:
#automate.auto_plot(search_word,
                    #x1 = 'cap_incr_spec',
                    #y1 = 'potential',
                    #xlabel='Capacity (mAh/g active material)',
                    #ylabel='Potential (V vs Mg/Mg$^{2+}$)',
                    #cycles1 = [0, 1, 10],                 # Plot only certain cycles for cell 1
                    #cycles2 = [0, 1, 10],                 # Plot only certain cycles for cell 2
                    #legend = ['Cell 1', 'Cell 2'],       # OBS: nr of legend strings must match nr of cells
                    #save_as='My first plot'              # Save plot in plots folder as png file (1000 dpi)
                   #)

# EXPORT:
#export_cell = 'TixC-S31_T1_01'                      # Cell to export (pickle name)
#export_file = 'your_filename_here'                  # Filename of exported file
#export_variables = ['cap_incr_spec', 'potential']   # Variables to export (as many as you like)
# Run this:
#support.export_data(export_cell, export_file, export_variables)
















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

# !! OBS: functions below not tested !!
#Input/Conversion of data:
# --------------------------------------------
#support.search_file(search_word, raw_data)    # search_word: Key word which will be search for. CellDatabase/raw_data: Location that will be searched in.
#automate.automatic_conversion(search_word,raw_data,database)
#automate.merge_biologic(search_word, CellDatabase)
# Accessing Data:
# --------------------------------------------
#support.About(CellDatabase.as_posix(),'/F_SiO2MSC2_1_R0')
#Data = 'Cell_info'
#output = access_data.access_cell_data(Cell)
#print(output)
