import numpy as np                # Matrise pakke
import glob
from pathlib import Path
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
#Hidden functions in next line
## Functions
### Div


def About(data_storage, CellKey):
    df = pd.read_pickle((data_storage + CellKey + '.pkl'))
    print(df.columns)
    return

"""
#########################################################################
#               NEW USER?
#
#               Start here! 
######################################################################### 
# -------------------------------------------------------------------------------------
# Fill in the locations of your folders using the variables below (see examples below)
# -------------------------------------------------------------------------------------"""
raw_data = Path(r'Insert your path to raw data (text files) here')                           # Location to raw data (text files).
# Ex: raw_data = Path(r'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Raw_files')     # Location to raw data (text files).
cell_database = Path(r'Insert your path to your folder where the imported cells will be')    # Location to where the imported cells will be (when saved as pickle)
# Ex: cell_database = Path(r'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Pickles')  # Location to where the imported cells will be (when saved as pickle)
exported_data = Path(r'Insert your path to your folder where the exported data will be')     # Location to where the exported data will be
# Ex: exported_data = Path(r'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Exported') # Location to where the exported data will be

"""
#########################################################################
#               Proceed to section you want
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
# Manual importing each file: (change to your specifications and remove "->")
# Example from Maccor:
# -> raw_data_path = (r'C:/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Raw_files\B1_combi\B1_combi_multi_KOH_02.txt')   # Location of data to be imported and converted
# -> cell_key = 'B1_combi_multi_KOH_02'   # What the cell will be saved as (after importing the file)
# -> database = 'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Pickles'   # Location to where the imported cells will be (when saved as pickle) (same as above)
# Run this:
# -> cell = ConvertToPandas.maccor(raw_data_path, cell_key, database)    # Imports and  converts to pickle and stores it.
# Now the data is stored in your database, and also in the "cell" variable above. You can test by e.g. printing out the 'potential' data by:
# -> print(cell['potential'])

# Example from Biologic:
#-> raw_data_path = (r'C:\Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Raw_files\TixC\_10HF14\S31\TixC-S31_T1_01_TFSI-Cl-DME_04to21V_25mAg_limit32h_CB1.mpt')   # Location of data to be imported and converted
#-> cell_key = 'TixC-S31_T1_01'   # What the cell will be saved as (after importing the file)
#-> database = 'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Pickles'   # Location to where the imported cells will be (when saved as pickle) (same as above)
# Run this:
# -> cell = ConvertToPandas.biologic(raw_data_path, cell_key, database)    # Imports and  converts to pickle and stores it.
# Now the data is stored in your database, and also in the "cell" variable above. You can test by e.g. printing out the 'potential' data by:
# -> print(cell['potential'])

"""
#########################################################################
#
#                           PLOT DATA
#
#########################################################################
"""
# Set which cell from the database that you want to plot here (they are saved as "pickles" :D )
cell_1 = Path(r'Insert location to cell you want to plot')      # Location to cell 1
# Ex: cell_1 = Path(r'/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\B1_combi_multi_KOH_02')
#cell_1 = Path(r'/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\B1_combi_multi_KOH_02')

cell_2 = Path(r'Insert location to cell you want to plot')      # Location to cell 2
# Ex: cell_2 = Path(r'/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\TixC-S31_T1_01')
#cell_2 = Path(r'/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\TixC-S31_T1_01')
# You can plot up to 50 cells, that should be enough, shouldn't it?

# Set variables to plot:
x = 'cap_incr_spec'
y = 'potential'
# Simple plotting, run this:
# -> Plotter.plotter(pickle1=cell_1, pickle2=cell_2, x1=x, y1=y)

# More advanced; you can specify and add stuff to plot:
xlim = [0, 150]             # Specify x limits
ylim = [0.1,2.2]            # Specify y limits
xticks=[0,50,100,150]       # Specify x ticks (which x values to show on plot)
yticks=[0.2, 1, 1.5, 2.1]   # Specify y ticks (which y values to show on plot)
xlabel='Capacity (mAh/g active material)'   # Override default x label
ylabel='Potential vs Mg/Mg$^{2+}$'          # Override default y label
cycles1=[0,1,5,10]          # Only plot some specific cycles for cell_1 (can be done similar for cell 2 etc)
color1='mediumblue'         # Specify if you want certain color for cell 1 (can be done similar for cell 2 etc). Choose among these: https://matplotlib.org/examples/color/named_colors.html
color_scheme2='YlOrBr'      # Specify if you want certain color scheme, e.g. a gradient for different cycles. Choose among these: https://matplotlib.org/examples/color/colormaps_reference.html
legend=['Cell 1', 'Cell 2'] # Specify legend. Remember to adjust for number of cells.
legend_loc=1                # Specify where legend will be in plot (e.g. "2" is up left in plot)
custom = 'plt.text(50,1,\'So science\') \nplt.text(90,1.75,\'Much wow\')'       # Code that will be executed to customize plot (add text, arrows etc).
my_new_plot = '/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Graphs\Plot1'  # Full path and name of plot that will be saved in high resolution (1000 dpi)

# Run this:
# -> Plotter.plotter(pickle1=cell_1, pickle2=cell_2,x1=x, y1=y, xlim=xlim, ylim=ylim, xticks=xticks, yticks=yticks, xlabel=xlabel,ylabel=ylabel, cycles1=cycles1, color1=color1, color_scheme2=color_scheme2,legend=legend, legend_loc=legend_loc, custom_code=custom, save_path=my_new_plot)


"""
#########################################################################
#
#                    More to be added
#
#########################################################################
"""


""" Older stuff below """
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

#search_word = 'CB'
#support.search_file(search_word, raw_data)    # search_word: Key word which will be search for. CellDatabase/raw_data: Location that will be searched in.

#support.search_file(search_word, raw_data)    # search_word: Key word which will be search for. CellDatabase/raw_data: Location that will be searched in.

#support.automatic_conversion(search_word,raw_data,CellDatabase)
#support.merge_biologic(search_word, CellDatabase)


# About(CellDatabase.as_posix(),'/F_SiO2MSC2_1_R0')


#---------------------Accessing Data-------------------

#Data = 'Cell_info'

#output = AccessData.AccessCellData(Cell)

#print(output)

#---------------------Exporting Data-------------------

# Export data for e.g. plotting using other software:
# Uses CellDatabase_string to find pickle and exported_data as destination
#pickle = 'B1_combi_t02_01_APC-THF_2_4Vto0_2V_0_01C'     # Pickle to be exported.
#export_variables = ['cap_incr_spec', 'potential']       # As many as you like

#support.export_data(CellDatabase_string, pickle, exported_data, export_variables)

#df = pd.read_pickle(pickle_name_1)  # Reads pickle
#print(df['cap_incr_spec'])
