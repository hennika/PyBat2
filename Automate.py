import support
import ConvertToPandas
import MyPaths
from pathlib import Path
import matplotlib.pyplot as plt   # Plottepakke
import AccessData
import pandas as pd


def automatic_conversion(search_word,location, CellDatabase):                                             #Automatically converts search for mpt (biolofic) or txt (lanhe) files to pandas. Able to handle multiple files.

    all_files = support.search_file(search_word, location)                                                        #Search for cells with a spesific name in a given location.

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

def auto_import(search_word):
    raw_data = MyPaths.raw_data
    database = MyPaths.database
    all_files = support.search_file(search_word, raw_data)  # Search for cells with a specific name in the raw data folder.
    response = support.input_cool('yellow','Do you want to convert these files? yes/no:   ')

    if response.lower() == "yes":
        for line in all_files:                  #Loop through all input files.
            file_name = line.stem               #Saves the file name
            file_path = line.as_posix()         #Saves the file path

            support.print_cool('blue', '-'*80 + '\nConverting: ' + file_name + line.suffix)
            response = support.input_cool('yellow', 'Do you want to change cell key (what the cell will be saved as)? (yes/any button):   ')
            if response == 'yes':
                file_name = support.input_cool('yellow', 'Write cell key:   ')
            else:
                None

            if line.suffix == ".mpt":
                ConvertToPandas.biologic(file_path, file_name, database.as_posix())
                support.print_cool('green', 'Converted from Biologic: ' + file_name + line.suffix)
            elif line.suffix == ".xls":
                ConvertToPandas.lanhe(file_path, file_name, database.as_posix())
                support.print_cool('green', 'Converted from Lanhe: ' + file_name + line.suffix)
            else:
                try:
                    ConvertToPandas.maccor(file_path, file_name, database.as_posix())
                    support.print_cool('green', 'Converted from Maccor: ' + file_name + line.suffix)
                except:
                    support.print_cool('red', 'File not recognized: ' + file_path)

    elif response.lower() == 'no':
        support.print_cool('green','No files converted')
    else:
        support.print_cool('red', 'Input invalid')

    return

def merge_biologic(search_word, location):     #function takes a vector of dataframes an merged them into one dataframe based on the "cycle_nr, charge_spec, discharge_spec, QE" format.

    CellDatabase = Path(r'C:/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Database/CellDatabase/')   #Location where dataframes is stored.

    all_files = support.search_file(search_word, location)                                                        #Search for cells with the inputname in the given location

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