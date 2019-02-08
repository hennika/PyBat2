# About script:
# Takes in dataframe and add incremental specific capacity and/or cycle based specific capacity as new columns.

import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import StrToFloat                 # Converts strings to float
import FixUnevenLength            # Makes two list same length by removing or adding element
import sys                        # For exiting script among other
import FindMinLength              # Returning minimum length of inputs

def Incremental(df, char_mass):

    discharge_incr_float = StrToFloat.strToFloat(df['discharge_incr'].tolist())  # Extracting incremental discharge as float
    discharge_incr_spec = np.divide(discharge_incr_float,float(char_mass) / 1000)  # Divide by mass in grams to obtain specific capacity.

    charge_incr_float = StrToFloat.strToFloat(df['charge_incr'].tolist())  # Extracting incremental discharge as float
    charge_incr_spec = np.divide(charge_incr_float,float(char_mass) / 1000)  # Divide by mass in grams to obtain specific capacity.

    cap_incr_float = StrToFloat.strToFloat(df['cap_incr'].tolist())  # Extracting incremental discharge as float
    cap_incr_spec = np.divide(cap_incr_float,float(char_mass) / 1000)  # Divide by mass in grams to obtain specific capacity.

    df['discharge_incr_spec'], df['charge_incr_spec'], df['cap_incr_spec'] = [discharge_incr_spec, charge_incr_spec, cap_incr_spec]  # Add them as new columns.

    return df


def Cyclebased(df, char_mass):
    cycle_incr_float = StrToFloat.strToFloat(df['cycle'].tolist())  # Extracting incremental cycle number as float
    discharge_incr_float = StrToFloat.strToFloat(
        df['discharge_incr'].tolist())  # Extracting incremental discharge as float
    charge_incr_float = StrToFloat.strToFloat(df['charge_incr'].tolist())  # Extracting incremental discharge as float

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

    discharge_spec, charge_spec, cycles = FixUnevenLength.RemoveLast(discharge_spec, charge_spec, cycles,
                                                                     target=min(len(discharge_spec), len(charge_spec),
                                                                                len(cycles)))

    if (len(discharge_spec) != len(charge_spec) or len(discharge_spec) != len(cycles)):
        sys.exit("Error: Unequal lengths of discharge_spec/charge_spec/cycle_nr!")

    discharge_spec, charge_spec, cycles = FixUnevenLength.FillNone(discharge_spec, charge_spec, cycles, target=len(
        cycle_incr_float))  # Fill rest of column with 'None'

    df['discharge_spec'], df['charge_spec'], df['cycle_nr'] = [discharge_spec, charge_spec, cycles]  # Add them as new columns.

    return df

#Script for testing functions.
# This function is used in ConvertToPandas, use that function to test this function.
# Alternatively, you can uncomment the two last sentences in the script (plots the variables) and run ConvertToPandas.
