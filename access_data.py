########       Script for accessing data
## - Takes data_url (location of datafile) and variable (wanted data) as input
## - Returns a list with the data in float format.


import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import support
from user_setup import database as database


def access_data(cell_key, variable):

    df = pd.read_pickle((database.as_posix() +"/" + cell_key))

    output = support.str_to_float(df[variable].tolist())    #Extracts the wanted variable "variable" from the dataframe, converts it to a string and returns it.

    return output


def access_cell_data(cell_key):

    df = pd.read_pickle(database.as_posix() + "/" + cell_key )
    df = df.astype(float)
    return df

def access_cell_as_string(cell_key):

    df = pd.read_pickle(database.as_posix() + "/" + cell_key )

    return df

def columns (data_url, list_of_variables):
    df = pd.read_pickle(data_url)  # Reads pickle as strings
    out_list = [[] for i in range(len(list_of_variables))]  # Initiate list of lists, with as many lists as variables.
    counter = 0
    for i in list_of_variables:
        out_list[counter].append (support.str_to_float(df[i].tolist()))
        counter = counter + 1
    return out_list