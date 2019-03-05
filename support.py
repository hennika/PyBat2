# Library for all supporting functions to Pybat
#import numpy as np                # Matrise pakke
import os
import sys                         # For aborting scripts
from glob import glob
from pathlib import Path
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import pickle as pkl

def search_file(search_word, location):                                                                    #Function for searching in a file system for a given file name.
    # Location: The folder from which all subfolders are searched in.
    #Search_word: The word that will be search for in the subfolders of "location"

    all_files = find_files(search_word, location)   # Finds and returns files as list

    print('\033[94m')   # Starts printing in blue until '\x1b[0m' stops it (at definition end)
    for line in all_files:
        print(line)
    print('\x1b[0m')  # Stops color printing

    return all_files

def print_files_nr (files): # Prints files with nr first (starting at 0)
    counter = 0
    print('\033[94m')   # Starts printing in blue until '\x1b[0m' stops it (at definition end)
    for line in files:
        print(counter, ':  ', line)
        counter = counter + 1
    print('\x1b[0m')  # Stops color printing

    return

def find_files(search_word, location):
    #Location: The folder from which all subfolders are searched in.
    #Search_word: The word that will be search for in the subfolders of "location"
    all_files = []

    if search_word.lower() == 'all':
        print("Files found:")
        for file in location.rglob('**/*'):
            all_files.append(file)          #Vector with the path of all files with corresponds with the search word.

    else:
        print("Files found:")
        for file in location.rglob('**/' + search_word + '*'):
            all_files.append(file)          #Vector with the path of all files with corresponds with the search word.

    return all_files

def save_figure(fig_handle, location):

    response = input("\n Would you like to save figure? (yes/no)  ")

    if response.lower() == 'yes':
        response_filename = input("Please write filename: ")

        if not search_file(response_filename, location):
            plt.savefig(location.as_posix() + '/'+ response_filename + '.png', dpi=500)
            with open(location.as_posix()+ '/' + response_filename + '.pkl', 'wb') as file:
                pkl.dump(fig_handle, file)

        else:
            response = input("\n File already exists, do you want to overwrite the file?: (yes/no) ")
            print(response)

            if response.lower() == 'yes':
                plt.savefig(location.as_posix() + '/'+ response_filename, dpi=500)
                with open(location.as_posix() + '/'+ response_filename + '.pkl', 'wb') as file:
                    pkl.dump(fig_handle, file)

            else:
                print("\n File not saved, program exited")


def open_figure(name,location):
   return pkl.load(open(location.as_posix() + '/' + name + ".pkl", 'rb'))


def about(data_storage, CellKey):
    df = pd.read_pickle((data_storage + CellKey + '.pkl'))
    print(df.columns)
    return


# Takes string as input and print it as error message, then aborts script.
def error_message(string):

    print ('\x1b[0;31;0m' + string + '\x1b[0m') # Red color. Colors from https://stackoverflow.com/questions/287871/print-in-terminal-with-colors

    sys.exit(1)             # Will make this function return false value

    return

# Export data for e.g. plotting using other software.
def export_data(pickle, pickle_name, *argv):
    from user_setup import database as database
    from user_setup import exported_data as exported_data

    df = pd.read_pickle(database.as_posix() + '/' + pickle)  # Reads pickle

    #writer = pd.ExcelWriter(destination+'\\'+pickle_name+'.xlsx', engine='xlsxwriter')
    #counter = 0         # Counter needed for ExcelWriter to add next variable in next column (and not overwrite it).
    for arg in argv:     # Iterate through all variables specified
        try:
            # If Excel:
            #df[arg].to_excel(writer, startcol=counter, index=False, freeze_panes=[1,0])     # Freezes top row, for easy reading.
            #counter = counter + 1      # Counter needed to add next variable in next column (and not overwrite it).

            # If csv-file:
            df[arg].to_csv(str(exported_data) + '\\' + pickle_name + '.csv', sep='\t', float_format='%f', encoding='utf-8', index=False)
        except:
            error_message('Error in reading/writing the variable to export')

    # Add some cell formats for prettier values in Excel:
    # OBS! Comma and scientific writing may cause some problems.
    #workbook = writer.book
    #worksheet = writer.sheets['Sheet1']
    #format1 = workbook.add_format({'num_format': '0.00'})
    #worksheet.set_column('A:AA', None, format1) # None argument refers to column width.
    #writer.save()

    print (pickle_name + '.xlsx \n \t exported to \n' + str(exported_data))
    return

def print_cool (color, *argv):      # Prints arguments (as strings) with colors/bold/underline. Should handle strings and numbers.
    color_choice = choose_color(color)  # Collects corresponding color code

    print(color_choice) # Starts color printing
    for arg in argv:
        try:
            print(arg)
        except:
            print(str(arg))
    print('\x1b[0m')    # Stops color printing before next print
    return

def input_cool(color, question):

    color_choice = choose_color(color) # Collects corresponding color code
    print(color_choice)     # Starts color printing before input
    response = input(question)
    print('\x1b[0m')    # Stops color printing before next print

    if response == 'abort':
        sys.exit(1)

    return response

def choose_color (color):           # Dictionary with color alternatives.
    return {
        'green': '\033[92m',  # Colors: https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
        'red': '\033[91m',
        'blue': '\033[94m',
        'yellow': '\033[93m',
        'purple': '\033[95m',
        'bold': '\033[1m',
        'underline': '\033[4m'
    }[color]

def safe_div(x, y):     # Function for avoiding division by zero error, instead return zero.
    if y == 0:
        return 0
    return x / y