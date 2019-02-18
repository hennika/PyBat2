########       Script for accessing data
## - Takes data_url (location of datafile) and variable (wanted data) as input
## - Returns a list with the data in float format.


import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import StrToFloat
#from PyBat import Database
#from PyBat import CellDatabase
CellDatabase = 'C:/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Database/CellDatabase/'



def AccessData(CellKey,variable):

    df = pd.read_pickle((CellDatabase + CellKey + '.pkl'))

    output = StrToFloat.strToFloat(df[variable].tolist())    #Extracts the wanted variable "variable" from the dataframe, converts it to a string and returns it.

    return output


def AccessCellData(CellKey):

    df = pd.read_pickle(CellDatabase + CellKey + '.pkl')
    df = df.astype(float)
    return df







#####    Script for testing function
# ##      Innputs:
# #Location of data
# #data_url = '/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Experimental data/Data Transfers/180226, DataTransfer/Diatoma, Biologic/180214/180214_SiO2MSC1_35CB_ECDEC_17_Hold120_2mV_CE5.mpt'
# CellKey = 'SiO2'
#
# ##      Desired variable
# variable1 = 'cap_incr_spec'
# variable2 = 'potential'
#
# ##      Outputs
# #output1 = accessingData(data_url,variable1)
# #output2 = accessingData(data_url,variable2)
# output1 = accessingData(CellKey,variable1)
# output2 = accessingData(CellKey,variable2)
#
# #print(variable1,':', output1,'\n', variable2,'    :', output2)
#
#
# x = output1
#
# y = output2
#
#
# #plt.plot(x, y, ls='None')
# plt.plot(x, y)
# #plt.scatter(x,y,s=0.01)
# plt.xlabel(variable1)
# plt.ylabel(variable2)
# plt.title('About as simple as it gets, folks')
# plt.grid(False)
# plt.locator_params(axis='both', nbins=6)
# #plt.ylim(ymax=2.4)
# plt.show()


