# Library for all suporting functions to Pybat
#import numpy as np                # Matrise pakke
import os
import sys          # For aborting scripts
from glob import glob
from pathlib import Path
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
#import strToFloat
import ConvertToPandas
import AccessData
import pickle as pkl



def search_file(search_word, location):                                                                    #Function for searching in a file system for a given file name.
    #Location: The folder from which all subfolders are searched in.
    #Search_word: The word that will be search for in the subfolders of "location"

    all_files = []

    if search_word.lower() == 'all':
        print("\nFiles found:")
        for file in location.rglob('**/*'):
            all_files.append(file)          #Vector with the path of all files with corresponds with the search word.

    else:
        print("\nFiles found:")
        for file in location.rglob('**/' + search_word + '*'):
            all_files.append(file)          #Vector with the path of all files with corresponds with the search word.

    for line in all_files:
        print(line)

    return all_files

def automatic_conversion(search_word,location, CellDatabase):                                             #Automatically converts search for mpt (biolofic) or txt (lanhe) files to pandas. Able to handle multiple files.

    all_files = search_file(search_word, location)                                                        #Search for cells with a spesific name in a given location.


    response = input("\n Do you want to convert these files? yes/no:   ")


    if response.lower() == "yes":
        for line in all_files:                                                                            #Loop through all input files.
            file_name = line.stem                                                                         #Saves the file name
            file_path = line.as_posix()                                                                   #Saves the file path

            if line.suffix == ".txt":
                ConvertToPandas.lanhe(file_path, file_name, CellDatabase.as_posix())
            elif line.suffix == ".mpt":
                ConvertToPandas.biologic(file_path,file_name, CellDatabase.as_posix())
            else:
                print("File format not recognized")

        print("\n Files converted")

    elif response.lower() == 'no':

        print("\n No files converted")

    else:
        print("\n Input invalide")

    return


def clean_data_lanhe(df):                                                                                  #This function removes the first cycle from lanhe data, making the cycling start at Cycle 1 not Cycle 0.
    df.drop(df.index[0], inplace=True)
    df['cycle'] = range(1, (len(df['cycle'].tolist()) + 1))
    return df








def merge_biologic(search_word, location):     #function takes a vector of dataframes an merged them into one dataframe based on the "cycle_nr, charge_spec, discharge_spec, QE" format.

    CellDatabase = Path(r'C:/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Database/CellDatabase/')   #Location where dataframes is stored.

    all_files = search_file(search_word, location)                                                        #Search for cells with the inputname in the given location

    response = input("\n Do you want to merge these files? yes/no:   ")                                 #Response from user


    if response.lower() == "yes":                                                                         #Starts mergning

        df_list = []                                                                                      #List of dataframes to be merged.

        for line in all_files:                                                                            #Creates a list of all dataframes to be merged.
            df_list.append(AccessData.AccessCellData(line.stem))

        df_merged = pd.concat(df_list, axis=0)                                                            #Actuall merging of dataframes.
        df_merged = df_merged.ix[:,['cycle_nr', "charge_spec", "discharge_spec", 'QE']]                   #Desides which colums are to be merged.
        df_merged = df_merged.dropna()                                                                    #Drop rows without input.

        df_merged['cycle_nr'] = range(1, df_merged.shape[0] + 1)                                          #Renumber the cycling_nr column to go from 1--> x.
        df_merged.set_index([list(range(df_merged.shape[0]))], inplace=True)                              #Renumber the index of the dataframe to go from 1 --> x.


        plt.scatter(df_merged['cycle_nr'], df_merged['discharge_spec'], s=10, color='deepskyblue')        #Plots result, so that the user can see if it is satisfying.
        plt.show()

        response = input("\n Would you like to store the new file? yes/no:   ")

        if response.lower() == "yes":
            response = input("\n Please write file name:  ")
            df_merged.to_pickle(CellDatabase.as_posix() + "/" + response + '.pkl')

            print("\n Database saved as: ",  response + '.pkl')

        else:
            print("\n New dataframe not saved")

        return df_merged

    else:
        print("\n Input invalid")

    return print("\n No merge conducted")


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




# Takes string as input and print it as error message, then aborts script.
def error_message(string):

    print ('\x1b[0;31;0m' + string + '\x1b[0m') # Red color. Colors from https://stackoverflow.com/questions/287871/print-in-terminal-with-colors

    sys.exit(1)             # Will make this function return false value

    return

# Export data for e.g. plotting using other software.
def export_data(pickle_path, pickle_name, destination, *argv):
    df = pd.read_pickle(pickle_path+'\\'+pickle_name)  # Reads pickle
    if not os.path.exists(destination):     # Making destination folder if it does not exists already.
        os.makedirs(destination)
    #writer = pd.ExcelWriter(destination+'\\'+pickle_name+'.xlsx', engine='xlsxwriter')
    #counter = 0         # Counter needed for ExcelWriter to add next variable in next column (and not overwrite it).
    for arg in argv:     # Iterate through all variables specified
        try:
            # If Excel:
            #df[arg].to_excel(writer, startcol=counter, index=False, freeze_panes=[1,0])     # Freezes top row, for easy reading.
            #counter = counter + 1      # Counter needed to add next variable in next column (and not overwrite it).

            # If csv-file:
            df[arg].to_csv(destination + '\\' + pickle_name + '.csv', sep='\t', float_format='%f', encoding='utf-8', index=False)

        except:
            error_message('Error in reading/writing the variable to export')

    # Add some cell formats for prettier values in Excel:
    # OBS! Comma and scientific writing may cause some problems.
    #workbook = writer.book
    #worksheet = writer.sheets['Sheet1']
    #format1 = workbook.add_format({'num_format': '0.00'})
    #worksheet.set_column('A:AA', None, format1) # None argument refers to column width.
    #writer.save()

    print (pickle_name + '.xlsx \n \t exported to \n' + destination)

    return

