# About scrip:
#-Takes a biologic txt file and convert the data into a pandas dataframe. The name of the colums is changed to global standard.

import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import StrToFloat
import ImportData as id
import AddSpecificCapacity
import FixUnevenLength            # Makes two list same length by removing or adding element
import sys                        # For exiting script among other

def biologic(data_url, CellKey, Database):

    Data, char_mass = id.importBiologic(data_url)                     # use ID:importBiologic to import data and the characteristic mass from a bilogic txt file.



    colum_names = Data[0][0:(len(Data[0]))]                         # Extracts the name of the colums from the txt file to place them in the dataframe

    df = pd.DataFrame(Data[1:],columns=colum_names)                   # Creates the dataframe




    del df['mode'],df['control changes'], df['Ns changes'],df['counter inc.'],df['Ns'],df['(Q-Qo)/mA.h'],df['control/V/mA'],df['Q charge/discharge/mA.h'],df['x'],df['control/V']       # Deletes row that we do not want.

    #colum_names = ['redox', 'error', 'time', 'dq','potential','halfcycle','energy_char','energy dis','capacitance_char','capacitance dis', 'current','discharge incr', 'charge incr','cap incr','current aim',	'cycle'	,'power']

    #Replaces the name of the colums with standard names-
    df = df.rename(columns={'ox/red':'redox', 'time/s':'time','dq/mA.h':'dq','Ecell/V':'potential','Ewe/V':'potential','half cycle':'halfcycle','Energy charge/W.h':'energy_char','Energy discharge/W.h':'energy_dis','Capacitance charge/µF':'capacitance_char','Capacitance discharge/µF':'capacitance_dis','<I>/mA':'current', 'Q discharge/mA.h':'discharge_incr', 'Q charge/mA.h':'charge_incr','Capacity/mA.h' : 'cap_incr', 'Efficiency/%': 'QE', 'control/mA' : 'current_aim' ,'cycle number':'cycle','P/W': 'power'})

    print(df.columns)
    ##Add additional variables to pandas


    #try:

    df = AddSpecificCapacity.Incremental(df, char_mass)
    df = AddSpecificCapacity.Cyclebased(df, char_mass)


    #except:

        #print("Calculations of cycle based capacity failed. ")

    try:

        cell_info = np.zeros(df.shape[0]) # Creats a list with equal length as the number of rows in the dataframe.

        cell_info[0] = float(char_mass)
        cell_info[1] =(float(char_mass)/2.0106) #Adds characteristic mass and loading to the dataframe cellInfo = [characterisstic mass, loading]

        df['cell_info'] = cell_info    #CellInfo is for some reason returned as a list of list. Fix this later.



    except:
        print('ERROR: Characteristic mass not availible from import document:'+CellKey +". "  'Neither characteristic mass or loading added to database')

    df.to_pickle((Database +"/"+CellKey + '.pkl'))                                   #Store data as a Pickle

    return df

def lanhe(data_url, CellKey, Database):

    Data = id.importLanhe(data_url)

    df = pd.DataFrame(Data, columns=['cycle_nr', 'charge_spec', 'discharge_spec', 'QE'])  # Creates the dataframe

    df.to_pickle((Database +"/"+CellKey + '.pkl'))  # Store data as a Pickle

    return df




#Script for testing functions.
#
#
#CellKey = 'NMC'
#
#data_url = '/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Experimental data/Data Transfers/180226/Diatoma, Biologic/180214/180214_SiO2MSC1_35CB_ECDEC_17_Hold120_2mV_CE5.mpt'

#data_url = 'C:/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Experimental data/Data Transfers/180424/180126_NMC_std1_08_ECDEC_005_3.txt'
#df = lanhe(data_url, CellKey)
#
#
#
#print(df)


#Todo -Consider adding a new class of AddToPandas functions, which adds new columns to the dataframe. This to separat the initial formation of the dataframe and additions.

