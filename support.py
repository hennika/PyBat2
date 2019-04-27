# Library for all supporting functions to Pybat
#import numpy as np                # Matrise pakke
import sys                         # For aborting scripts
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import pickle as pkl

def search_file(search_word, location):                                                                    #Function for searching in a file system for a given file name.
    # Location: The folder from which all subfolders are searched in.
    #Search_word: The word that will be search for in the subfolders of "location"

    all_files = find_files(search_word, location)   # Finds and returns files as list
    all_files = remove_files(all_files)     # Removes specific types of files from list

    print('\033[94m')   # Starts printing in blue until '\x1b[0m' stops it (at definition end)
    for line in all_files:
        print(line)
    print('\x1b[0m')  # Stops color printing

    return all_files

def remove_files (files):   # Keeps only supported files for importing.
    supported = ['.mpt', '.txt', '.TXT', '.xls', '.xlsx']
    files_filtered = []
    for line in files:
        if any(x in line.suffix for x in supported):
            files_filtered.append(line)
    return files_filtered

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


def fill_none(*args, **kwargs):     # Takes in lists and make them even by filling them with 'None' values to target length
    try:
        target = kwargs['target']
    except:
        print('Unrecognizable target length')
    new_args = []
    for arg in args:
        while len(arg) < target:
            arg.append(None)
        new_args.append(arg)
    return new_args


def remove_last(*args, **kwargs):   # Takes in lists and make them even by removing the last elements until target length is reached.

    try:
        target = kwargs['target']
    except:
        print('Unrecognizable target length')
    new_args = []
    for arg in args:
        while len(arg) > target:
            arg.pop()
        new_args.append(arg)
    return new_args


def str_to_float(string):   # Takes a string as a variable and returns it as a float
    if type(string) == list:
        for index in range(0, len(string)):
            try:
                string[index] = float(string[index])
            except:
                None
    else:
        string = float(string)

    return string