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
import support

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
        cell_info = np.zeros(df.shape[0]) # Creates a list with equal length as the number of rows in the dataframe.
        cell_info[0] = float(char_mass)
        cell_info[1] =(float(char_mass)/2.0106) #Adds characteristic mass and loading to the dataframe cellInfo = [characterisstic mass, loading]
        df['cell_info'] = cell_info    #CellInfo is for some reason returned as a list of list. Fix this later.

    except:
        print('ERROR: Characteristic mass not availible from import document:'+CellKey +". "  'Neither characteristic mass or loading added to database')

    df.to_pickle((Database +"/"+CellKey))  # OBS! Removed .pkl to avoid error. For storing data as a Pickle

    return df

def vmp3 (data_url, CellKey, Database):
    Data, char_mass = id.importBiologic(data_url)     # use ID:importBiologic to import data and the characteristic mass from a biologic txt file.
    column_names = Data[0][0:(len(Data[0]))]           # Extracts the name of the colums from the txt file to place them in the dataframe
    df = pd.DataFrame(Data[1:], columns=column_names)  # Creates the dataframe
    # Fixing columns. Column names from CV-file:  ['mode', 'ox/red', 'error', 'control changes', 'counter inc.', 'time/s', 'control/V', 'Ewe/V', '<I>/mA', 'cycle number', '(Q-Qo)/C', '<Ece>/V', 'P/W', 'Ewe-Ece/V']
    del df['mode'], df['control changes'], df['counter inc.'], df['control/V']  # Deletes row that we do not want.
    df = df.rename(columns={'ox/red':'redox', 'time/s':'time','Ewe/V':'Ew','<I>/mA':'current', 'cycle number':'cycle', '(Q-Qo)/C':'(Q-Qo)/C', 'Ece/V': 'Ec', 'P/W': 'power', 'Ewe-Ece/V':'Ew-Ec'}) # Renaming.
    try:     # Seems like exported file can either contain <> or not
        df.rename(columns={'<Ece>/V': 'Ec'})
    except:
        print()
    try:        # If galvanostatic cycling from vmp3, will have additional columns and want to add specific capacity etc:
        # Fixing columns part 2. Column names from galvanostatic cycling are combination of regular biologic file and CV: ['mode', 'ox/red', 'error', 'control changes', 'Ns changes', 'counter inc.', 'Ns', 'time/s', 'dq/mA.h', '(Q-Qo)/mA.h', 'control/V/mA', 'Ewe/V', 'Q charge/discharge/mA.h', 'half cycle', 'Ece/V', 'Energy charge/W.h', 'Energy discharge/W.h', 'Capacitance charge/µF', 'Capacitance discharge/µF', '<I>/mA', 'x', 'Q discharge/mA.h', 'Q charge/mA.h', 'Capacity/mA.h', 'Efficiency/%', 'control/V', 'control/mA', 'cycle number', 'P/W', 'Ewe-Ece/V']
        # Should delete some, rename similar as regular biologic file and rename vmp3-specific columns (latter already done above).
        del df['Ns changes'], df['Ns'], df['(Q-Qo)/mA.h'], df['control/V/mA'], df['Q charge/discharge/mA.h'], df['x']  # Deletes row that we do not want.
        df = df.rename(columns={'ox/red':'redox','dq/mA.h':'dq','half cycle':'halfcycle','Energy charge/W.h':'energy_char','Energy discharge/W.h':'energy_dis','Capacitance charge/µF':'capacitance_char','Capacitance discharge/µF':'capacitance_dis', 'Q discharge/mA.h':'discharge_incr', 'Q charge/mA.h':'charge_incr','Capacity/mA.h' : 'cap_incr', 'Efficiency/%': 'QE', 'control/mA' : 'current_aim' ,'cycle number':'cycle'})
        df = AddSpecificCapacity.Incremental(df, char_mass)
        df = AddSpecificCapacity.Cyclebased(df, char_mass)
    except:
        print('Imported as \"CV\"-file, specific capacity not added.')

    df.to_pickle((Database +"/"+CellKey))  # Storing data as a Pickle

    return df

def lanhe(data_url, CellKey, Database):

    df = id.importLanhe(data_url)   # Imports excel file as dataframe.

    del df['Index'],df['Energy/mWh'], df['SEnergy/Wh/kg'],df['SysTime'], df['Unnamed: 10'] # Deletes row that we do not want/need.
    df = df.rename(columns={'TestTime/Sec.':'time', 'StepTime/Sec.':'step_time','Voltage/V':'potential','Current/mA':'current','Capacity/mAh':'cap_incr', 'SCapacity/mAh/g':'cap_incr_spec', 'State': 'mode'})

    # Tries to calculate characteristic mass and verifies with user / input from user:
    try:
        last_cap_incr = df['cap_incr'].iloc[-1]
        last_cap_incr_spec = df['cap_incr_spec'].iloc[-1]
        char_mass = last_cap_incr/last_cap_incr_spec*1000
        id.check_char_mass(char_mass)
        #support.print_cool('blue', 'Found this characteristic mass (mg): ', char_mass)
        #char_mass = support.input_cool('yellow', 'Please write desired mass (mg):   ')
    except:
        char_mass = support.input_cool('yellow', 'No characteristic mass found. Please input mass:   ')

    #Add additional variables to pandas
    # First, need incremental cycle, discharge_incr and charge_incr (have cap_incr) to use AddSpecificCapacity functions:
    df = addFromCurrents(df)
    # Then, can add specific incremental capacity (not really necessary, is in fact exported from Lanhe) and cyclebased:
    df = AddSpecificCapacity.Incremental(df, char_mass)
    df = AddSpecificCapacity.Cyclebased(df, char_mass)

    # Todo: Add cycle specific capacity
    # Todo: Add cell info as for biologic?

    df.to_pickle((Database +"/"+CellKey))  # Store data as a Pickle

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

    for i in range(0, len(df.index)):    # Read dataframe line for line
        if df['mode'][i] == 'D' or df['mode'][i]=='D_Rate':  # If mode is 'D' (Maccor) or 'D_Rate' (Lanhe), add capacity variable to discharge variable, and add zero to charge variable. Vice versa.
            discharge_incr.append(df['cap_incr'][i])
            charge_incr.append(0)
            continue                # Necesarry with continue to prevent extra 0 (it seems 'R' becomes true for 'C_Rate' or 'D_Rate')
        if df['mode'][i] == 'C' or df['mode'][i]=='C_Rate':  # If mode is 'C' (Maccor) or 'C_Rate' (Lanhe), add capacity variable to charge variable, and add zero to discharge variable.
            charge_incr.append(df['cap_incr'][i])
            discharge_incr.append(0)
            continue
        if df['mode'][i] == 'R':    # If mode is 'R', add zero to discharge and charge variables
            discharge_incr.append(0)
            charge_incr.append(0)

    df['discharge_incr'], df['charge_incr'] = [discharge_incr, charge_incr] # Add them as new columns to dataframe.

    return df

def AddCycleIncr(df):    # Was used on Lanhe-files, but replaced with addFromCurrents function.
    discharge_incr_float = StrToFloat.strToFloat(df['discharge_incr'].tolist())  # Extracting incremental discharge as float
    charge_incr_float = StrToFloat.strToFloat(df['charge_incr'].tolist())  # Extracting incremental charge as float
    #current_float = StrToFloat.strToFloat(df['current'].tolist())  # Extracting incremental charge as float
    cycle = []      # Initiates cycle variable (incremental cycle)
    cycle_nr = 0    # Cycle counter that will be written to cycle variable
    dis_char_cycle = False      # Used to define if cycling begins with discharge or charge, uses that to define if cycle starts with discharge or charge.
    char_dis_cycle = False      # Used to define if cycling begins with discharge or charge, uses that to define if cycle starts with discharge or charge.
    started = False             # Used to define if cycling has started

    for i in range(0, len(discharge_incr_float)):

        if discharge_incr_float[i]!=0 and discharge_incr_float[i-1] ==0 and started==False:    # New discharge and starting with discharge
            dis_char_cycle = True
            started = True
        if charge_incr_float[i] != 0 and charge_incr_float[i - 1] == 0 and started == False:   # New charge and starting with charge
            char_dis_cycle = True
            started = True
        if discharge_incr_float[i] != 0 and discharge_incr_float[i - 1] == 0 and dis_char_cycle == True:  # New discharge, which (might) define new cycle.
            cycle_nr = cycle_nr + 1     # New cycle
        if charge_incr_float[i] != 0 and charge_incr_float[i - 1] == 0 and char_dis_cycle == True:  # New charge, which (might) define new cycle.
            cycle_nr = cycle_nr + 1     # New cycle

        cycle.append(cycle_nr)

    df['cycle'] = cycle # Add cycle variable as new column in dataframe.

    return df

def addFromCurrents(df):    # Adds incremental cycle, charge and discharge from current signs.
    cycle = []           # Initiate variable
    cycle_nr = 0         # Cycle counter that will be written to cycle variable
    discharge_incr = []  # Initiate variable
    charge_incr = []     # Initiate variable
    dis_char_cycle = False  # Used to define if cycling begins with discharge or charge, uses that to define if cycle starts with discharge or charge.
    char_dis_cycle = False  # Used to define if cycling begins with discharge or charge, uses that to define if cycle starts with discharge or charge.
    started = False      # Used to define if cycling has started

    for i in range(0, len(df['current'])):    # Read dataframe line for line
        #---------------------------------
        #  Cycle variable:
        if df['current'][i] < 0 and df['current'][i-1] > 0 and started == False:  # New discharge, and current is turned on for first time
            started = True
            dis_char_cycle = True
        if df['current'][i] > 0 and df['current'][i-1] < 0 and started == False:  # New charge, and current is turned on for first time
            started = True
            char_dis_cycle = True
        if df['current'][i] < 0 and df['current'][i - 1] > 0 and started == True:  # New discharge, and new cycle
            cycle_nr = cycle_nr + 1
        if df['current'][i] > 0 and df['current'][i - 1] < 0 and started == True:  # New charge, and new cycle
            cycle_nr = cycle_nr + 1
        cycle.append(cycle_nr)
        # ---------------------------------
        # Discharge and charge variables:
        if df['current'][i]==0:     # If current is zero, capacity will be zero
            discharge_incr.append(0)
            charge_incr.append(0)
        if df['current'][i] < 0:  # Negative current means discharge
            discharge_incr.append(df['cap_incr'][i])
            charge_incr.append(0)
        if df['current'][i] > 0:
            discharge_incr.append(0)
            charge_incr.append(df['cap_incr'][i])
        # ---------------------------------

    df['cycle'], df['discharge_incr'], df['charge_incr'] = [cycle, discharge_incr, charge_incr] # Add them as new columns to dataframe.

    return df


#Script for testing functions.
CellKey = 'TixC_10HF17a_S_T1_02_APC_002C'
Database = 'C:/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Pickles'

# Biologic
#data_url = 'C:/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Raw_files\B1_combi\B1_combi_t02_01_APC-THF_2_4Vto0_2V_0_01C_CE3.mpt'
#df = biologic(data_url, CellKey, Database)

# Maccor
#data_url = 'C:/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Raw_files\B1_combi\B1_combi_multi_KOH_02.txt'
#df = maccor(data_url, CellKey, Database)

# Lanhe
#data_url = 'C:/Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Raw_files\TixC\_10HF17a\S\TixC_10HF17a_S_T1_02_APC_002C_008_4.xls'
#df = lanhe(data_url, CellKey, Database)

#print(df)

#Todo -Consider adding a new class of AddToPandas functions, which adds new columns to the dataframe. This to separat the initial formation of the dataframe and additions.

