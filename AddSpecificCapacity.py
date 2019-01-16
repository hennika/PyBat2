# About scrip:
# Takes in dataframe and add incremental specific capacity and/or cycle based specific capacity as new columns.

import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import StrToFloat                 # Converts strings to float
import FixUnevenLength            # Makes two list same length by removing or adding element
import sys                        # For exiting script among other
import FindMinLength              # Returning minimum length of inputs


def Incremental(df, char_mass):


    discharge_incr_float = df['discharge_incr'].astype(float)   # Extracting incremental discharge as float
    discharge_incr_spec = np.divide(discharge_incr_float,float(char_mass)/1000)  # Divide by mass in grams to obtain specific capacity.

    charge_incr_float   = df['charge_incr'].astype(float)     # Extracting incremental discharge as float
    charge_incr_spec    = np.divide(charge_incr_float,float(char_mass)/1000)     # Divide by mass in grams to obtain specific capacity.

    cap_incr_float   = df['cap_incr'].astype(float)             # Extracting incremental discharge as float
    cap_incr_spec    = np.divide(cap_incr_float,float(char_mass)/1000)           # Divide by mass in grams to obtain specific capacity.

    df['discharge_incr_spec'], df['charge_incr_spec'], df['cap_incr_spec'] = [discharge_incr_spec, charge_incr_spec, cap_incr_spec] # Add them as new columns.

    return df


def Cyclebased(df, char_mass):

    df = df.astype(float)  # Converts all dataframe values to float
    last_cycle = df.tail(1)['cycle'].as_matrix().astype(int)  # Finds last cycle nr. (last row in cycle coloumn)
    cycles = list(range(last_cycle[0]))  # Makes list of cycles, from 0 to last cycle nr.

    discharge_spec = []     # Initiates variable
    charge_spec = []        # Initiates variable



    for i in range(0, len(df['cycle'])):
        #Change histroy
            #-Change if statements to elif

        #for j in range(0, len(df.shapep[1])):
        
        if df['cycle'][i] == 0 and df['discharge_incr'][i]==0 and df['charge_incr'][i]==0:    # Ignores rest step.
            continue
        if df['discharge_incr'][i]==0 or df['charge_incr'][i]==0: #************OBSOBSOBSOBS************* Hadde masse 0er i charge_incr og discharge_incr som ble med over til discharg_incr_spec. Satt defor inn denne if setningen for å ikke ta med disse. Men det fungerte ikke....
            continue
        if i == len(df['cycle'])-1: # If iteration has reached the second last row of df, add last value to charge and discharge.
            if not (df.tail(1)['discharge_incr'].as_matrix().astype(float) == 0):     # Adding only if not zero.
                discharge_spec.append(df.tail(1)['discharge_incr'].as_matrix().astype(float))
            if not (df.tail(1)['charge_incr'].as_matrix().astype(float) == 0):        # Adding only if not zero.
                charge_spec.append(df.tail(1)['charge_incr'].as_matrix().astype(float))
            continue        # Iteration is finished, and should not go to if condition below.
        if df['discharge_incr'][i] !=0 and df['discharge_incr'][i+1] == 0:       # Finds where the discharge ends.
            discharge_spec.append(df['discharge_incr'][i]/float(char_mass)*1000) # Adding specific discharge/gram
        if df['charge_incr'][i] != 0 and df['charge_incr'][i + 1] == 0:          # Finds where the charge ends.
            charge_spec.append(df['charge_incr'][i]/float(char_mass)*1000)     # Adding specific charge/gram

    discharge_spec, charge_spec, cycles = FixUnevenLength.RemoveLast(discharge_spec,charge_spec,cycles, target=min(len(discharge_spec),len(charge_spec),len(cycles)))

    if (len(discharge_spec)!= len(charge_spec) or len(discharge_spec) != len(cycles)):
        sys.exit("Error: Unequal lengths of discharge_spec/charge_spec/cycle_nr!")

    discharge_spec, charge_spec, cycles = FixUnevenLength.FillNone(discharge_spec,charge_spec, cycles, target=len(df['cycle']))   # Fill rest of column with 'None'

    df['discharge_spec'], df['charge_spec'], df['cycle_nr'] = [discharge_spec, charge_spec, cycles] # Add them as new columns.
    #plt.scatter(df['cycle_nr'], df['charge_spec'])
    #plt.show()


    return df

#Script for testing functions.
# This function is used in ConvertToPandas, use that function to test this function.
# Alternatively, you can uncomment the two last sentences in the script (plots the variables) and run ConvertToPandas.
