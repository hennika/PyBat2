# About script:
# Takes in dataframe and add incremental specific capacity and/or cycle based specific capacity as new columns.

import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import sys                        # For exiting script among other
import support
import user_setup

def incremental_cycle_charge_discharge(df):    # Adds incremental cycle, charge and discharge from current signs.
    cycle = []           # Initiate variable
    cycle_nr = 0         # Cycle counter that will be written to cycle variable
    discharge_incr = []  # Initiate variable
    charge_incr = []     # Initiate variable
    dis_char_cycle = False  # Used to define if cycling begins with discharge or charge, uses that to define if cycle starts with discharge or charge.
    char_dis_cycle = False  # Used to define if cycling begins with discharge or charge, uses that to define if cycle starts with discharge or charge.
    started = False      # Used to define if cycling has started
    current_float = support.str_to_float(df['current'].tolist())  # Extracting incremental current as float

    for i in range(0, len(current_float)):    # Read dataframe line for line
        #---------------------------------
        #  Cycle variable:
        if current_float [i] < 0 and current_float[i-1] > 0 and started == False:  # New discharge, and current is turned on for first time
            started = True
            dis_char_cycle = True
        if current_float[i] > 0 and current_float [i-1] < 0 and started == False:  # New charge, and current is turned on for first time
            started = True
            char_dis_cycle = True
        if current_float[i] < 0 and current_float[i - 1] > 0 and started == True:  # New discharge, and new cycle
            cycle_nr = cycle_nr + 1
        if current_float[i] > 0 and current_float[i - 1] < 0 and started == True:  # New charge, and new cycle
            cycle_nr = cycle_nr + 1
        cycle.append(cycle_nr)
        # ---------------------------------
        # Discharge and charge variables:
        if not 'cap_incr' in df.columns:    # Used for e.g. linear sweep voltammetry, where there is no capacity values. Skip/add zero.
            discharge_incr.append(0)
            charge_incr.append(0)
            continue
        if current_float[i]==0:     # If current is zero, capacity will be zero
            discharge_incr.append(0)
            charge_incr.append(0)
        if current_float[i] < 0:  # Negative current means discharge
            discharge_incr.append(df['cap_incr'][i])
            charge_incr.append(0)
        if current_float[i] > 0:
            discharge_incr.append(0)
            charge_incr.append(df['cap_incr'][i])
        # ---------------------------------

    df['cycle'], df['discharge_incr'], df['charge_incr'] = [cycle, discharge_incr, charge_incr] # Add them as new columns to dataframe.

    return df

def specific_capacity_incremental(df, char_mass):

    discharge_incr_float = support.str_to_float(df['discharge_incr'].tolist())  # Extracting incremental discharge as float
    discharge_incr_spec = np.divide(discharge_incr_float,float(char_mass) / 1000)  # Divide by mass in grams to obtain specific capacity.
    discharge_incr_spec[discharge_incr_spec == 0] = 'nan'

    charge_incr_float = support.str_to_float(df['charge_incr'].tolist())  # Extracting incremental discharge as float
    charge_incr_spec = np.divide(charge_incr_float,float(char_mass) / 1000)  # Divide by mass in grams to obtain specific capacity.
    charge_incr_spec[charge_incr_spec == 0] = 'nan'

    cap_incr_float = support.str_to_float(df['cap_incr'].tolist())  # Extracting incremental discharge as float
    cap_incr_spec = np.divide(cap_incr_float,float(char_mass) / 1000)  # Divide by mass in grams to obtain specific capacity.
    cap_incr_spec[cap_incr_spec == 0] = 'nan'

    df['discharge_incr_spec'], df['charge_incr_spec'], df['cap_incr_spec'] = [discharge_incr_spec, charge_incr_spec, cap_incr_spec]  # Add them as new columns.

    return df


def specific_capacity_cycle(df, char_mass):
    cycle_incr_float = support.str_to_float(df['cycle'].tolist())  # Extracting incremental cycle number as float
    discharge_incr_float = support.str_to_float(
        df['discharge_incr'].tolist())  # Extracting incremental discharge as float
    charge_incr_float = support.str_to_float(df['charge_incr'].tolist())  # Extracting incremental discharge as float
    current_incr_float = support.str_to_float(df['current'].tolist())   # Extracting incremental current as float.
    # df = df.astype(float)  # Converts all dataframe values to float
    last_cycle = int(cycle_incr_float[-1])  # Extracts last element of cycle column (last cycle nr) and converts to int.
    cycles = list(range(last_cycle))  # Makes list of cycles, from 0 to last cycle nr.

    discharge_spec = []  # Initiates variable
    charge_spec = []  # Initiates variable
    current_spec = []
    for i in range(0, len(cycle_incr_float)):
        if cycle_incr_float[i] == 0 and discharge_incr_float[i] == 0 and charge_incr_float[i] == 0:  # Ignores rest step.
            continue
        if i == len(
                cycle_incr_float) - 1:  # If iteration has reached the second last row of df, add last value to charge and discharge.
            if not (discharge_incr_float[-1] == 0):  # Adding only if not zero.
                discharge_spec.append(discharge_incr_float[-1] / float(char_mass) * 1000)
            if not (charge_incr_float[-1] == 0):  # Adding only if not zero.
                charge_spec.append(charge_incr_float[-1] / float(char_mass) * 1000)
            current_spec.append(current_incr_float[-1] / float(char_mass)*1000)
            continue  # Iteration is finished, and should not go to if condition below.
        if discharge_incr_float[i] != 0 and discharge_incr_float[i + 1] == 0:  # Finds where the discharge ends.
            if discharge_incr_float[i] < discharge_incr_float[i-1]:     # Sometimes last value before changing to (dis)charge is transitioning to 0, use second last value instead.
                discharge_spec.append(discharge_incr_float[i-1] / float(char_mass) * 1000)  # Adding specific discharge/gram
                current_spec.append(current_incr_float[i-1] / float (char_mass)*1000)   # Adds current for discharge, assumes same on charge.
            else:
                discharge_spec.append(discharge_incr_float[i] / float(char_mass) * 1000)  # Adding specific discharge/gram
                current_spec.append(current_incr_float[i] / float(char_mass) * 1000)  # Adds current for discharge, assumes same on charge.
        if charge_incr_float[i] != 0 and charge_incr_float[i + 1] == 0:  # Finds where the charge ends.
            if charge_incr_float[i] < charge_incr_float[i-1]:  # Sometimes last value before changing to (dis)charge is transitioning to 0, use second last value instead.
                charge_spec.append(charge_incr_float[i-1] / float(char_mass) * 1000)  # Adding specific charge/gram
            else:
                charge_spec.append(charge_incr_float[i] / float(char_mass) * 1000)  # Adding specific charge/gram

    discharge_spec, charge_spec, cycles, current_spec = support.remove_last(discharge_spec, charge_spec, cycles, current_spec,
                                                              target=min(len(discharge_spec), len(charge_spec),
                                                                                len(cycles)))

    if (len(discharge_spec) != len(charge_spec) or len(discharge_spec) != len(cycles)):
        sys.exit("Error: Unequal lengths of discharge_spec/charge_spec/cycle_nr!")

    discharge_spec, charge_spec, cycles, current_spec = support.fill_none(discharge_spec, charge_spec, cycles, current_spec, target=len(
        cycle_incr_float))  # Fill rest of column with 'None'

    df['discharge_spec'], df['charge_spec'], df['cycle_nr'], df['current_spec'] = [discharge_spec, charge_spec, cycles, current_spec]  # Add them as new columns.

    return df

# ------------------------

# Takes in dataframe and add differential capacity as new column.


def diffcap (df):
    # Differential capacity = dQ/dE
    # Calculating differential capacity based on histograms:
    # Iterates through values, every time the potential difference reaches the histogram size (e.g. 10mV), it calculates the capacity difference in that interval
    #################################################
    hist_size = user_setup.hist_size  # VERY IMPORTANT #
    #################################################
    # histogram size for change in potential. *Should be significantly larger than the largest step in potential values!*
    # Can use this to find largest step in potential values:
    # max_volt_diff = max(np.diff(volt)) # Should give maximum voltage value difference.
    # print ('Maximum incremental voltage difference appears to be', max_volt_diff)

    volt = df['potential'].astype(float)  # Converts potential values to float.
    cap = df['cap_incr_spec']             # Copies cap_incr_spec to new variable for easier code reading.

    dQ = []         # Capacity difference between two measurements
    dE = []         # Voltage difference between two measurements
    diff_cap = []    # Differential capacity between two measurements

    dE_temp = 0         # temporary variable for cumulative dE
    dQ_temp = 0         # temporary variable for cumulative dQ
    volt_corr = []      # correlated voltage for diff_cap variable
    volt_corr_start = volt[0] # will be used to assign diffcap variable to "middle voltage" of histogram

    for it in range(0, (len(volt) - 2)): # Need to stop iterating before list is exceeded
        if (cap[it + 1] - cap[it]) < 0:  # If this is true, we are changing charging to discharge/vice versa
            diff_cap.append(None)         # Adds empty value in row instead of weird value, so the df['cycle'] can be used in plotting later
            volt_corr.append(None)
        else:
            dQ_temp = dQ_temp + (cap[it+1] - cap[it])
            dE_temp = dE_temp + (volt[it+1] - volt[it])
            if abs(dE_temp) > hist_size:
                diff_cap.append (support.safe_div(dQ_temp,dE_temp))    # Differential capacity for interval
                volt_corr.append ((volt_corr_start + volt[it])/2) #
                volt_corr_start=volt[it]
                #volt_corr.append(volt[it])                    # Relates this interval to last voltage value in the interval. Use middle instead.
                dE_temp = 0         # emptying temporary variable. Okay to do as long dE steps in data are much smaller than hist_size
                dQ_temp = 0         # emptying temporary variable
            else:
                diff_cap.append(None)   # adding empty value in row, so the df['cycle'] can be used in plotting later
                volt_corr.append(None)

    volt_corr, diff_cap = support.fill_none(volt_corr, diff_cap, target=len(df['potential'])) # This will add to "None" values to diff_cap variable, as it is two values shorter

    df['potential_diff_cap'], df['diff_cap'] = [volt_corr, diff_cap] # Add volt_corr and diff_cap as new columns.

    return df

def cell_info(df, char_mass, cell_key):
    try:
        cell_info = np.zeros(df.shape[0]) # Creates a list with equal length as the number of rows in the dataframe.
        cell_info[0] = float(char_mass)
        cell_info[1] =(float(char_mass)/2.0106) #Adds characteristic mass and loading to the dataframe cellInfo = [characterisstic mass, loading]
        df['cell_info'] = cell_info    #CellInfo is for some reason returned as a list of list. Fix this later.
    except:
        print('ERROR: Characteristic mass not availible from import document:' + cell_key + ". "  'Neither characteristic mass or loading added to database')

    return df

def add_cycle_incr(df):    # Was used on Lanhe-files, but replaced with add_from_currents function.
    discharge_incr_float = support.str_to_float(df['discharge_incr'].tolist())  # Extracting incremental discharge as float
    charge_incr_float = support.str_to_float(df['charge_incr'].tolist())  # Extracting incremental charge as float
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


def incremental_charge_discharge_from_cap(df):
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
        else:
            print('Not recognized Mode column variabel (', df['mode'][i],'), added zero for row: ', i)
            discharge_incr.append(0)
            charge_incr.append(0)

    df['discharge_incr'], df['charge_incr'] = [discharge_incr, charge_incr] # Add them as new columns to dataframe.

    return df

def inverted_potential (df):

    Ec_inv = []

    for i in range(0, len(df.index)):    # Read dataframe line for line
        Ec_inv.append(float(df['Ec'][i])*(-1))  # Inverting potential by multiplying with -1

    df['Ec_inv'] = Ec_inv

    return df