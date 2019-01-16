import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import StrToFloat
import ImportData as id
import ConvertToPandas

########       Script for returning labels for plot
# Takes in variable as input and returns the corresponding string

def GetLabels(x):
    return {
        'time': 'Time (s)',
        'potential': 'Potential (V)',
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
        'cycle_nr': 'Cycles',
        'discharge_spec': 'Discharge capacity (mAh/g)',
        'charge_spec': 'Charge capacity (mAh/g)',

    }[x]

#####    Script for testing function
#variable1 = 'potential'
#print (GetLabels(variable1))