########       Script for accessing data
## - Takes data_url (location of datafile) and variable (wanted data) as input
## - Returns a list with the data in float format.


import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke

import string_to_float
from user_setup import database as database


def access_data(cell_key, variable):

    df = pd.read_pickle((database.as_posix() +"/" + cell_key))

    output = string_to_float.str_to_float(df[variable].tolist())    #Extracts the wanted variable "variable" from the dataframe, converts it to a string and returns it.

    return output


def access_cell_data(cell_key):

    df = pd.read_pickle(database.as_posix() + "/" + cell_key )
    df = df.astype(float)
    return df







