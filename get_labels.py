import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import string_to_float
import import_data as id
import convert_to_pandas

########       Script for returning labels for plot
# Takes in variable as input and returns the corresponding string

def GetLabels(x):
    return {
        'time': 'Time (s)',
        'potential': 'Potential (V)',
        'potential_diff_cap': 'Potential (V)',
        'energy_char': 'Charge energy (Wh)',
        'energy_dis': 'Discharge energy (Wh)',
        'capacitance_char': 'Charge capacitance (F)',
        'capacitance_dis': 'Discharge capacitance (F)',
        'current': 'Current (mA)',
        'charge_incr': 'Charge capacity (mAh)',
        'discharge_incr': 'Discharge capacity (mAh)',
        'cap_incr': 'Capacity (mAh)',
        'discharge_incr_spec': 'Discharge capacity (mAh/g)',
        'charge_incr_spec': 'Charge capacity (mAh/g)',
        'cap_incr_spec': 'Capacity (mAh/g)',
        'diff_cap': 'Differential capacity (mAh/g/V)',
        'cycle_nr': 'Cycles',
        'discharge_spec': 'Discharge capacity (mAh/g)',
        'charge_spec': 'Charge capacity (mAh/g)',
        'Ew' : 'Ew (V)',
        'Ec' : 'Ec (V)',
        'Ew-Ec' : 'Ew-Ec (V)',

    }[x]

#####    Script for testing function
#variable1 = 'potential'
#print (GetLabels(variable1))