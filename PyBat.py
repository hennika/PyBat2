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
exported_data = 'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Exported'

#------------------------------General info-------------------------

#Input/Conversion of data

# Manual importing:
# Maccor
data_url = 'C:/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Raw_files\B1_combi\B1_combi_multi_KOH_02.txt'   # Location of data to be imported and converted
CellKey = 'B1_combi_multi_KOH_02'   # What the "pickle" will be saved as (after importing the file)
Database = 'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Pickles'   # Location where the pickles are stored.

df = ConvertToPandas.maccor(data_url, CellKey, Database)    # Imports and  converts to pickle and stores it.

print(df['potential'])
#search_word = 'CB'
#support.search_file(search_word, raw_data)    # search_word: Key word which will be search for. CellDatabase/raw_data: Location that will be searched in.

#support.search_file(search_word, raw_data)    # search_word: Key word which will be search for. CellDatabase/raw_data: Location that will be searched in.

#support.automatic_conversion(search_word,raw_data,CellDatabase)
#support.merge_biologic(search_word, CellDatabase)

#------------------------------Plotting------------------------------
#
# About(CellDatabase.as_posix(),'/F_SiO2MSC2_1_R0')
#
#
#
pickle_name_1 = '/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\B1_combi_t02_01_APC-THF_2_4Vto0_2V_0_01C'
pickle_name_2 = '/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles\B1_combi_t03_01_LiBH4_1_7to0_2V_0_01C_CE1'

# Simple plotting:
#Plotter.plotter(pickle1=pickle_name_1, pickle2=pickle_name_2, x1='cap_incr_spec', y1='potential', legend=['Cell 1', 'Cell 2'])
# Advanced:
#custom = 'plt.text(50,1,\'So science\') \nplt.text(90,1.75,\'Much wow\')'       # Code that will be executed to customize plot (add text, arrows etc).
#plot1_path = '/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Graphs\Plot1'  # Name of plot including full path
# Plotter.plotter(pickle1=pickle_name_1, pickle2=pickle_name_2, xlim=[0,150], ylim=[0.1,2.2], xticks=[0,50,100,150], yticks=[0.2, 1, 1.5, 2.1], xlabel='Capacity (mAh/g active material)',ylabel='Potential vs Mg/Mg$^{2+}$', x1='cap_incr_spec', y1='potential', cycles1=[0,1,5,10], color1='blue', color_scheme2='magma',legend=['Cell 1', 'Cell 2'], legend_loc=1, custom_code=custom, save_path=plot1_path)



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
