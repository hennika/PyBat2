import MyPaths
from pathlib import Path
import Automate
import numpy as np                # Matrise pakke
import glob
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import StrToFloat
import ImportData as id
import AddSpecificCapacity
import FixUnevenLength            # Makes two list same length by removing or adding element
import sys                        # For exiting script among other
import ConvertToPandas
import Plotter
import AccessData
import support


# Initializing using MyPaths file (that will not generally be updated so you do not need to update folder locations).
raw_data = MyPaths.raw_data               # Location to raw data (text files).
database = MyPaths.database               # Location to where the imported cells will be (when saved as pickle)
exported_data = MyPaths.exported_data     # Location to where the exported data will be
plots = MyPaths.plots                     # Location to where plots are saved


print("hei")
"""
#########################################################################
#               NEW USER?
#
#               Start here! 
######################################################################### 
#
#       0) Fill in the locations of your folders in the "MyPaths" file!
#
#               Then proceed to section you want
#
#               1) Import new data
#               2) Plot data
#               3) Access and analyze data
#               4) Export data
#########################################################################

#########################################################################
#
#                       IMPORT NEW DATA
#
#########################################################################
"""
#------------------------------------------------------------------------
# Auto importing (remove # to run code)
#------------------------------------------------------------------------
# 1) Search for cell you want to import:
#search_word = 'TixC_10HF17a_S_T1_06_APC-THF_0_01Vto2_1V_002C_CG4'         # Regular biologic
#search_word = 'Gif_AQU_20_BMOC-DME_Mg-polished-outside_-09to21V_5mVs_C08' # Vmp3 file (CV)
#search_word = 'TixC-S31_T1_04_TFSI-Cl-DME_AQU_04to25V_100mAg_C09'         # Vmp3 file (galvanostatic cycling)
#search_word = 'TixC_10HF17a_S_T1_02_APC_002C_008_4'                       # Lanhe file
#search_word = 'B1_combi_multi_KOH_02'                                     # Maccor file
#search_word = 'B1_combi'                                                  # Multiple files plotting

# 2) Run code below and answer the pop-up questions:
#Automate.auto_import(search_word)

#------------------------------------------------------------------------
# Manual importing each file: (change to your folders and remove #)
#------------------------------------------------------------------------
# Example from Maccor:
#raw_data_path = (r'C:/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Raw_files\B1_combi\B1_combi_multi_KOH_02.txt')   # Location of data to be imported and converted
#cell_key = 'B1_combi_multi_KOH_02'   # What the cell will be saved as (after importing the file)
#database = 'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Pickles'   # Location to where the imported cells will be (when saved as pickle) (same as above)
# Run this:
#cell = ConvertToPandas.maccor(raw_data_path, cell_key, database)    # Imports and  converts to pickle and stores it.
# Now the data is stored in your database, and also in the "cell" variable above. You can test by e.g. printing out the 'potential' data by:
#print(cell['potential'])

# Example from Biologic:
#raw_data_path = (r'C:\Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Raw_files\TixC\_10HF14\S31\TixC-S31_T1_01_TFSI-Cl-DME_04to21V_25mAg_limit32h_CB1.mpt')   # Location of data to be imported and converted
#cell_key = 'TixC-S31_T1_01'   # What the cell will be saved as (after importing the file)
#database = 'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Pickles'   # Location to where the imported cells will be (when saved as pickle) (same as above)
# Run this:
#cell = ConvertToPandas.biologic(raw_data_path, cell_key, database)    # Imports and  converts to pickle and stores it.
# Now the data is stored in your database, and also in the "cell" variable above. You can test by e.g. printing out the 'potential' data by:
#print(cell['potential'])

"""
#########################################################################
#
#                           PLOT DATA
#
#########################################################################
"""
#------------------------------------------------------------------------
# Auto plotting (remove # to run code)
#------------------------------------------------------------------------
# 1) Search for cell(s) you want to plot:
#search_word = 'TixC_10HF17a'         # Example

# Specify x and y variables:
#x = 'cycle_nr'     # Cycle based capacities
#y = 'charge_spec'  # Cycle based capacities

#x = 'cap_incr_spec'    # Potential curves
#y = 'potential'        # Potential curves
#y = 'Ew'               # 3-electrode working electrode potential
#y2 = 'Ew-Ec'           # Plot same pickle twice ("0+0") to plot different y-variables for same cell.
#y3 = 'Ec'              # 3-electrode counter electrode potential

#x = 'Ew'               # CV
#y = 'current'          # CV

# Run this:
#Automate.auto_plot(search_word, x1=x, y1=y)

# You may supply specifications to plot if you like:
#xlabel = 'Capacity (mAh/g MXene-S composite)'                  # Override default x label
#ylabel = 'Potential vs Mg/Mg$^{2+}$'                           # Override default y label
#my_legend = ['Full cell','S-MXene half cell', 'Mg half cell']  # Override default legend (cell names)
#cycles = [10]                                                  # Specify which cycles to plot
#save_as = 'MXene-S 3-electrode cell'                           # Save plot as... (saved as png with 1000 dpi, in plots folder)
# Then you have to include specifications as arguments:
#Automate.auto_plot(search_word, x1=x, y1=y, xlabel=xlabel, ylabel=ylabel, cycles1=cycles, cycles2=cycles, y2=y2, cycles3=cycles, y3=y3, legend=my_legend, legend_loc=4, save_as=save_as)

#------------------------------------------------------------------------
# Manual plotting (remove #-> to run code)
#------------------------------------------------------------------------
# Set which cell from the database that you want to plot here (they are saved as "pickles" :D )
#cell_1 = Path(r'Insert location to cell you want to plot')      # Location to cell 1
#cell_1 = Path(r'/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\B1_combi_multi_KOH_02')     # Example 1

#cell_2 = Path(r'Insert location to cell you want to plot')      # Location to cell 2
#cell_2 = Path(r'/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\TixC-S31_T1_01')    # Example 2
# You can plot up to 50 cells :O

# Set variables to plot:
#x = 'cap_incr_spec'
#y = 'potential'
# Simple plotting, run this:
#Plotter.plotter(pickle1=cell_1, pickle2=cell_2, x1=x, y1=y)

# More advanced; you can specify and add stuff to plot:
#xlim = [0, 150]             # Specify x limits
#ylim = [0.1,2.2]            # Specify y limits
#xticks=[0,50,100,150]       # Specify x ticks (which x values to show on plot)
#yticks=[0.2, 1, 1.5, 2.1]   # Specify y ticks (which y values to show on plot)
#xlabel='Capacity (mAh/g active material)'   # Override default x label
#ylabel='Potential vs Mg/Mg$^{2+}$'          # Override default y label
#cycles1=[0,1,5,10]          # Only plot some specific cycles for cell_1 (can be done similar for cell 2 etc)
#color1='mediumblue'         # Specify if you want certain color for cell 1 (can be done similar for cell 2 etc). Choose among these: https://matplotlib.org/examples/color/named_colors.html
#color_scheme2='YlOrBr'      # Specify if you want certain color scheme, e.g. a gradient for different cycles. Choose among these: https://matplotlib.org/examples/color/colormaps_reference.html
#legend=['Cell 1', 'Cell 2'] # Specify legend. Remember to adjust for number of cells.
#legend_loc=1                # Specify where legend will be in plot (e.g. "2" is up left in plot)
#custom = 'plt.text(50,1,\'So science\') \nplt.text(90,1.75,\'Much wow\')'       # Code that will be executed to customize plot (add text, arrows etc).
#my_new_plot = '/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Plots\Plot1'  # Full path and name of plot that will be saved in high resolution (1000 dpi)

# Then run this: (you must remove variables that you don't specify)
# Plotter.plotter(pickle1=cell_1, pickle2=cell_2,x1=x, y1=y, xlim=xlim, ylim=ylim, xticks=xticks, yticks=yticks, xlabel=xlabel,ylabel=ylabel, cycles1=cycles1, color1=color1, color_scheme2=color_scheme2,legend=legend, legend_loc=legend_loc, custom_code=custom, save_path=my_new_plot)

"""
#########################################################################
#
#                    Export data
#
#########################################################################
"""
# Export data for e.g. plotting using other software.
# Location to cell:
cell_to_export = Path(r'Insert location to cell you want to export variables from')
# Ex: cell_to_export = Path(r'/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\TixC-S31_T1_01')

# Name of file that contains exported variables:
filename = 'your_filename_here'
# Choose which variables to export:
export_variables = ['cap_incr_spec', 'potential']       # As many as you like

# Run this:
# support.export_data(cell_to_export, filename, exported_data, export_variables)

"""
#########################################################################
#
#                    More to be added
#
#########################################################################
"""


""" More stuff below """
#Locations of folders: Can be imported by writing "from PyBat import Database"
# Andreas
#Database = 'C:/users/andnor/OneDrive - NTNU/Diatoma/Experimental/Database/'                         # Location where data frames are stored.
#CellDatabase = Path('C:/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Database/CellDatabase')   # Location where cell data frames are stored.
#Plots = 'C:/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Plots/'                               # Location wher plots are stored
#raw_data = Path(r"C:\Users\andnor\OneDrive - NTNU\Diatoma\Experimental\Experimental data\Galvanostatic Cycling")   # Location where raw data from experiments are located

# Henning
#Database = 'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/'                     # Location where data frames are stored.
#CellDatabase = Path('C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Pickles')    # Location (as path) where cell data frames are stored.
#CellDatabase_string = 'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Pickles'   # Location (as string) where cell data frames are stored.
#Plots = 'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Graphs'                  # Location where plots are stored
#raw_data = Path(r'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Raw_files')     # Location where raw data from experiments are located
#exported_data = 'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Exported'

#------------------------------General info-------------------------

#Input/Conversion of data

#search_word = 'TixC_10HF17a_S_T1_02_APC'
#Automate.auto_import(search_word)

#support.search_file(search_word, raw_data)    # search_word: Key word which will be search for. CellDatabase/raw_data: Location that will be searched in.

#Automate.automatic_conversion(search_word,raw_data,database)
#Automate.merge_biologic(search_word, CellDatabase)


# support.About(CellDatabase.as_posix(),'/F_SiO2MSC2_1_R0')


#---------------------Accessing Data-------------------

#Data = 'Cell_info'

#output = AccessData.AccessCellData(Cell)

#print(output)


