# About script:
# Takes in dataframe and add incremental specific capacity and/or cycle based specific capacity as new columns.

import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import string_to_float                 # Converts strings to float
import fix_uneven_length            # Makes two list same length by removing or adding element
import sys                        # For exiting script among other
import find_min_length              # Returning minimum length of inputs
import support
import user_setup

def Incremental(df, char_mass):

    discharge_incr_float = string_to_float.strToFloat(df['discharge_incr'].tolist())  # Extracting incremental discharge as float
    discharge_incr_spec = np.divide(discharge_incr_float,float(char_mass) / 1000)  # Divide by mass in grams to obtain specific capacity.

    charge_incr_float = string_to_float.strToFloat(df['charge_incr'].tolist())  # Extracting incremental discharge as float
    charge_incr_spec = np.divide(charge_incr_float,float(char_mass) / 1000)  # Divide by mass in grams to obtain specific capacity.

    cap_incr_float = string_to_float.strToFloat(df['cap_incr'].tolist())  # Extracting incremental discharge as float
    cap_incr_spec = np.divide(cap_incr_float,float(char_mass) / 1000)  # Divide by mass in grams to obtain specific capacity.

    df['discharge_incr_spec'], df['charge_incr_spec'], df['cap_incr_spec'] = [discharge_incr_spec, charge_incr_spec, cap_incr_spec]  # Add them as new columns.

    return df


def Cyclebased(df, char_mass):
    cycle_incr_float = string_to_float.strToFloat(df['cycle'].tolist())  # Extracting incremental cycle number as float
    discharge_incr_float = string_to_float.strToFloat(
        df['discharge_incr'].tolist())  # Extracting incremental discharge as float
    charge_incr_float = string_to_float.strToFloat(df['charge_incr'].tolist())  # Extracting incremental discharge as float

    # df = df.astype(float)  # Converts all dataframe values to float
    last_cycle = int(cycle_incr_float[-1])  # Extracts last element of cycle column (last cycle nr) and converts to int.
    cycles = list(range(last_cycle))  # Makes list of cycles, from 0 to last cycle nr.

    discharge_spec = []  # Initiates variable
    charge_spec = []  # Initiates variable
    for i in range(0, len(cycle_incr_float)):
        if cycle_incr_float[i] == 0 and discharge_incr_float[i] == 0 and charge_incr_float[
            i] == 0:  # Ignores rest step.
            continue
        if i == len(
                cycle_incr_float) - 1:  # If iteration has reached the second last row of df, add last value to charge and discharge.
            if not (discharge_incr_float[-1] == 0):  # Adding only if not zero.
                discharge_spec.append(discharge_incr_float[-1] / float(char_mass) * 1000)
            if not (charge_incr_float[-1] == 0):  # Adding only if not zero.
                charge_spec.append(charge_incr_float[-1] / float(char_mass) * 1000)
            continue  # Iteration is finished, and should not go to if condition below.
        if discharge_incr_float[i] != 0 and discharge_incr_float[i + 1] == 0:  # Finds where the discharge ends.
            if discharge_incr_float[i] < discharge_incr_float[i-1]:     # Sometimes last value before changing to (dis)charge is transitioning to 0, use second last value instead.
                discharge_spec.append(discharge_incr_float[i-1] / float(char_mass) * 1000)  # Adding specific discharge/gram
            else:
                discharge_spec.append(discharge_incr_float[i] / float(char_mass) * 1000)  # Adding specific discharge/gram
        if charge_incr_float[i] != 0 and charge_incr_float[i + 1] == 0:  # Finds where the charge ends.
            if charge_incr_float[i] < charge_incr_float[i-1]:  # Sometimes last value before changing to (dis)charge is transitioning to 0, use second last value instead.
                charge_spec.append(charge_incr_float[i-1] / float(char_mass) * 1000)  # Adding specific charge/gram
            else:
                charge_spec.append(charge_incr_float[i] / float(char_mass) * 1000)  # Adding specific charge/gram

    discharge_spec, charge_spec, cycles = fix_uneven_length.RemoveLast(discharge_spec, charge_spec, cycles,
                                                                       target=min(len(discharge_spec), len(charge_spec),
                                                                                len(cycles)))

    if (len(discharge_spec) != len(charge_spec) or len(discharge_spec) != len(cycles)):
        sys.exit("Error: Unequal lengths of discharge_spec/charge_spec/cycle_nr!")

    discharge_spec, charge_spec, cycles = fix_uneven_length.FillNone(discharge_spec, charge_spec, cycles, target=len(
        cycle_incr_float))  # Fill rest of column with 'None'

    df['discharge_spec'], df['charge_spec'], df['cycle_nr'] = [discharge_spec, charge_spec, cycles]  # Add them as new columns.

    return df

# ------------------------

# Takes in dataframe and add differential capacity as new column.


def add_diffcap (df):
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

    volt=df['potential'].astype(float)  # Converts potential values to float.
    cap=df['cap_incr_spec']             # Copies cap_incr_spec to new variable for easier code reading.

    dQ = []         # Capacity difference between two measurements
    dE = []         # Voltage difference between two measurements
    diffCap = []    # Differential capacity between two measurements

    dE_temp = 0         # temporary variable for cumulative dE
    dQ_temp = 0         # temporary variable for cumulative dQ
    volt_corr = []      # correlated voltage for diffCap variable
    volt_corr_start = volt[0] # will be used to assign diffcap variable to "middle voltage" of histogram

    for it in range(0, (len(volt) - 2)): # Need to stop iterating before list is exceeded
        if (cap[it + 1] - cap[it]) < 0:  # If this is true, we are changing charging to discharge/vice versa
            diffCap.append(None)         # Adds empty value in row instead of weird value, so the df['cycle'] can be used in plotting later
            volt_corr.append(None)
        else:
            dQ_temp = dQ_temp + (cap[it+1] - cap[it])
            dE_temp = dE_temp + (volt[it+1] - volt[it])
            if abs(dE_temp) > hist_size:
                diffCap.append (support.safe_div(dQ_temp,dE_temp))    # Differential capacity for interval
                volt_corr.append ((volt_corr_start + volt[it])/2) #
                volt_corr_start=volt[it]
                #volt_corr.append(volt[it])                    # Relates this interval to last voltage value in the interval. Use middle instead.
                dE_temp = 0         # emptying temporary variable. Okay to do as long dE steps in data are much smaller than hist_size
                dQ_temp = 0         # emptying temporary variable
            else:
                diffCap.append(None)   # adding empty value in row, so the df['cycle'] can be used in plotting later
                volt_corr.append(None)

    volt_corr, diffCap = fix_uneven_length.FillNone(volt_corr, diffCap, target=len(df['potential'])) # This will add to "None" values to diffCap variable, as it is two values shorter

    df['potential_diff_cap'], df['diff_cap'] = [volt_corr, diffCap] # Add volt_corr and diffCap as new columns.

    return df
