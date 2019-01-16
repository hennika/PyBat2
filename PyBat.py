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
Database = 'C:/users/andnor/OneDrive - NTNU/Diatoma/Experimental/Database/'                         #Location where data frames are stored.
CellDatabase = Path('C:/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Database/CellDatabase')            # Location where cell data frames are stored.

Plots = 'C:/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Plots/'                                 # Location wher plots are stored
raw_data = Path(r"C:\Users\andnor\OneDrive - NTNU\Diatoma\Experimental\Experimental data\Galvanostatic Cycling")   # Location where raw data from experiments are located



#------------------------------General info-------------------------


#Innput/Conversion of data



search_word = "SiO2MSC2_16_LongP1"


#support.search_file(search_word, raw_data)    # search_word: Key word which will be search for. CellDatabase/raw_data: Location that will be searched in.

support.automatic_conversion(search_word,raw_data,CellDatabase)
#support.merge_biologic(search_word, CellDatabase)

#------------------------------Plotting------------------------------
#
# About(CellDatabase.as_posix(),'/F_SiO2MSC2_1_R0')
#
#
#
# # #


# #






#Plotter.plotter(pickle1=pickle_name_1, pickle2=pickle_name_2, x1='cap_incr_spec', y1='potential', cycles1=[0,1,5,10], color1='blue', color_scheme2='magma',legend=['Cell 1', 'Cell 2'], legend_loc=1)




#---------------------Accessing Data-------------------

#Data = 'Cell_info'

#output = AccessData.AccessCellData(Cell)

#print(output)



