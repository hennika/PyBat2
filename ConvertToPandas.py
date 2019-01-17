# About script:
# -Takes a biologic/Lanhe/Maccor txt file and convert the data into a pandas dataframe. The name of the colums is changed to global standard.
# -Saves as pickle.

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

    colum_names = Data[0][0:(len(Data[0]))]                           # Extracts the name of the colums from the txt file to place them in the dataframe
    df = pd.DataFrame(Data[1:],columns=colum_names)                   # Creates the dataframe

    del df['mode'],df['control changes'], df['Ns changes'],df['counter inc.'],df['Ns'],df['(Q-Qo)/mA.h'],df['control/V/mA'],df['Q charge/discharge/mA.h'],df['x'],df['control/V']       # Deletes row that we do not want.

    #Replaces the name of the colums with standard names-
    # colum_names = ['redox', 'error', 'time', 'dq','potential','halfcycle','energy_char','energy dis','capacitance_char','capacitance dis', 'current','discharge incr', 'charge incr','cap incr','current aim',	'cycle'	,'power']
    df = df.rename(columns={'ox/red':'redox', 'time/s':'time','dq/mA.h':'dq','Ecell/V':'potential','Ewe/V':'potential','half cycle':'halfcycle','Energy charge/W.h':'energy_char','Energy discharge/W.h':'energy_dis','Capacitance charge/µF':'capacitance_char','Capacitance discharge/µF':'capacitance_dis','<I>/mA':'current', 'Q discharge/mA.h':'discharge_incr', 'Q charge/mA.h':'charge_incr','Capacity/mA.h' : 'cap_incr', 'Efficiency/%': 'QE', 'control/mA' : 'current_aim' ,'cycle number':'cycle','P/W': 'power'})
    # print(df.columns)

    ##Add additional variables to pandas
    df = AddSpecificCapacity.Incremental(df, char_mass)
    df = AddSpecificCapacity.Cyclebased(df, char_mass)

    try:
        cell_info = np.zeros(df.shape[0]) # Creats a list with equal length as the number of rows in the dataframe.
        cell_info[0] = float(char_mass)
        cell_info[1] =(float(char_mass)/2.0106) #Adds characteristic mass and loading to the dataframe cellInfo = [characterisstic mass, loading]
        df['cell_info'] = cell_info    #CellInfo is for some reason returned as a list of list. Fix this later.
    except:
        print('ERROR: Characteristic mass not availible from import document:'+CellKey +". "  'Neither characteristic mass or loading added to database')

    df.to_pickle((Database +"/"+CellKey))  # OBS! Removed .pkl to avoid error. For storing data as a Pickle

    return df

def lanhe(data_url, CellKey, Database):

    Data = id.importLanhe(data_url)

    df = pd.DataFrame(Data, columns=['cycle_nr', 'charge_spec', 'discharge_spec', 'QE'])  # Creates the dataframe

    # Todo: Add incremental specific capacity?
    # Todo: Add cell info as for biologic?

    df.to_pickle((Database +"/"+CellKey + '.pkl'))  # Store data as a Pickle

    return df

def maccor(data_url, CellKey, Database):
    Data, char_mass = id.importMaccor(data_url)  # use ID:importMaccor to import data and the characteristic mass from a Maccor txt file.

    column_names = Data[0][0:(len(Data[0]))]  # Extracts the name of the colums from the txt file to place them in the dataframe
    column_names.append('NA')                 # Some of the rows have a '\n' as 30th column.

    df = pd.DataFrame(Data[2:],  columns=column_names)  # Creates the dataframe
    # Now column names are: ['Rec', 'Cycle P', 'Cycle C', 'Step', 'TestTime', 'StepTime', 'Cap. [Ah]', 'Ener. [Wh]', 'Current [A]', 'Voltage [V]', 'Md', 'ES', 'DPT Time', 'AUX1 [V]', 'VAR1', 'VAR2', 'VAR3', 'VAR4', 'VAR5', 'VAR6', 'VAR7', 'VAR8', 'VAR9', 'VAR10', 'VAR11', 'VAR12', 'VAR13', 'VAR14', 'VAR15\n', 'NA']

    del df['ES'], df['AUX1 [V]'], df['VAR1'], df['VAR2'],df['VAR3'],df['VAR4'],df['VAR5'],df['VAR6'],df['VAR7'],df['VAR8'],df['VAR9'],df['VAR10'],df['VAR11'],df['VAR12'],df['VAR13'],df['VAR14'],df['VAR15\n'],df['NA']  # Deletes row that we do not want.
    # Now they are: ['Rec', 'Cycle P', 'Cycle C', 'Step', 'TestTime', 'StepTime', 'Cap. [Ah]', 'Ener. [Wh]', 'Current [A]', 'Voltage [V]', 'Md', 'DPT Time']
    # Replaces the name of the colums with standard names.
    df = df.rename(columns={'Rec': 'rec', 'Cycle P': 'cycle_p', 'Cycle C': 'cycle', 'Step': 'program_seq',
                            'TestTime': 'time', 'StepTime': 'program_seq_time',
                            'Cap. [Ah]': 'cap_incr', 'Ener. [Wh]': 'energy',
                            'Current [A]': 'current', 'Voltage [V]': 'potential',
                            'Md': 'mode', 'DPT Time': 'date'})
    # Now they are: ['rec', 'cycle_p', 'cycle', 'program_seq', 'time', 'program_seq_time', 'cap_incr', 'energy', 'current', 'potential', 'mode', 'date']

    df = AddDischargeAndChargeIncr(df)

    df = AddSpecificCapacity.Incremental(df, char_mass)
    df = AddSpecificCapacity.Cyclebased(df, char_mass)

    # Todo: Add cell info as for biologic?

    df.to_pickle((Database +"/"+CellKey))                                   #Store data as a Pickle

    return df

def AddDischargeAndChargeIncr(df):
    discharge_incr = []         # Initiate variables
    charge_incr = []            # Initiate variables

    for i in range(0, len(df['cycle'])):    # Read dataframe line for line
        if df['mode'][i] == 'R':    # If mode is 'R', add zero to discharge and charge variables
            discharge_incr.append(0)
            charge_incr.append(0)
        if df['mode'][i] == 'D':    # If mode is 'D', add capacity variable to discharge variable, and add zero to charge variable. Vice versa.
            discharge_incr.append(df['cap_incr'][i])
            charge_incr.append(0)
        if df['mode'][i] == 'C':  # If mode is 'C', add capacity variable to charge variable, and add zero to discharge variable.
            charge_incr.append(df['cap_incr'][i])
            discharge_incr.append(0)

    df['discharge_incr'], df['charge_incr'] = [discharge_incr, charge_incr] # Add them as new columns to dataframe.

    return df

#Script for testing functions.
#CellKey = 'B1_combi_multi_KOH_02'
#Database = 'C:/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles'

# Biologic
#data_url = 'C:/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Raw_files\B1_combi\B1_combi_t02_01_APC-THF_2_4Vto0_2V_0_01C_CE3.mpt'
#df = biologic(data_url, CellKey, Database)

# Maccor
#data_url = 'C:/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Raw_files\B1_combi\B1_combi_multi_KOH_02.txt'
#df = maccor(data_url, CellKey, Database)

#df = lanhe(data_url, CellKey)

#print(df)

#Todo -Consider adding a new class of AddToPandas functions, which adds new columns to the dataframe. This to separat the initial formation of the dataframe and additions.

