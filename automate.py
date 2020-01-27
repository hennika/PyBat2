import support
import import_cell
import user_setup
from pathlib import Path
import matplotlib.pyplot as plt   # Plottepakke
import access_data
import pandas as pd

def automatic_conversion(search_word, location, cell_database):                                             #Automatically converts search for mpt (biolofic) or txt (lanhe) files to pandas. Able to handle multiple files.

    all_files = support.search_file(search_word, location)                                                        #Search for cells with a spesific name in a given location.

    response = input("\n Do you want to convert these files? yes/no:   ")

    if response.lower() == "yes":
        for line in all_files:                                                                            #Loop through all input files.
            file_name = line.stem                                                                         #Saves the file name
            file_path = line.as_posix()                                                                   #Saves the file path

            if line.suffix == ".txt":
                import_cell.lanhe(file_path, file_name, cell_database.as_posix())
            elif line.suffix == ".mpt":
                import_cell.biologic(file_path, file_name, cell_database.as_posix())
            else:
                print("File format not recognized")

        print("\n Files converted")

    elif response.lower() == 'no':

        print("\n No files converted")

    else:
        print("\n Input invalid")

    return

def auto_import(search_word, **kwargs):

    try:
        if kwargs['testing']==True:
            raw_data = Path(r'..\PyBat2-master\testing')
            database = Path(r'..\PyBat2-master\testing\database')
        else:
            raw_data = user_setup.raw_data
    except:
        raw_data = user_setup.raw_data
        database = user_setup.database

    all_files = support.search_file(search_word, raw_data)  # Search for cells with a specific name in the raw data folder.
    response = support.input_cool('yellow','Do you want to convert these files? yes/no:   \n(.mpr and .mgr files will be skipped)   ')

    if response.lower() == "yes":
        for line in all_files:                  #Loop through all input files.
            file_name = line.stem               #Saves the file name
            file_path = line.as_posix()         #Saves the file path

            if line.suffix == '.mpr' or line.suffix=='.mgr':
                continue

            support.print_cool('blue', '-'*80 + '\nConverting: ' + file_name + line.suffix)
            response = support.input_cool('yellow', 'Do you want to change cell key (what the cell will be saved as)? (yes/any button):   ')
            if response == 'yes':
                file_name = support.input_cool('yellow', 'Write cell key:   ')
            else:
                None

            identifier = identify_file(line.suffix, file_path)

            if identifier == 'biologic':
                import_cell.biologic(file_path, file_name, database.as_posix())
                support.print_cool('green', 'Converted from Biologic: ' + file_name + line.suffix)
            elif identifier == 'vmp3':
                import_cell.vmp3(file_path, file_name, database.as_posix())
                support.print_cool('green', 'Converted from VMP3: ' + file_name + line.suffix)
            elif identifier == 'impedance':
                import_cell.vmp3(file_path, file_name, database.as_posix())
                support.print_cool('green', 'Converted from VMP3: ' + file_name + line.suffix)
            elif identifier == 'lanhe':
                import_cell.lanhe(file_path, file_name, database.as_posix())
                support.print_cool('green', 'Converted from Lanhe: ' + file_name + line.suffix)
            elif identifier == 'maccor':
                import_cell.maccor(file_path, file_name, database.as_posix())
                support.print_cool('green', 'Converted from Maccor: ' + file_name + line.suffix)
            else:
                support.print_cool('red', 'File not recognized: ' + file_path)

    elif response.lower() == 'no':
        support.print_cool('green','No files converted')
    else:
        support.print_cool('red', 'Input invalid')

    return
def merge_biologic(search_word, location):     #function takes a vector of dataframes an merged them into one dataframe based on the "cycle_nr, charge_spec, discharge_spec, QE" format.

    cell_database = Path(r'C:/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Database/cell_database/')   #Location where dataframes is stored.

    all_files = support.search_file(search_word, location)                                                        #Search for cells with the inputname in the given location

    response = input("\n Do you want to merge these files? yes/no:   ")                                 #Response from user

    if response.lower() == "yes":                                                                         #Starts mergning

        df_list = []                                                                                      #List of dataframes to be merged.

        for line in all_files:                                                                            #Creates a list of all dataframes to be merged.
            df_list.append(access_data.access_cell_data(line.stem))

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
            df_merged.to_pickle(cell_database.as_posix() + "/" + response + '.pkl')

            print("\n Database saved as: ",  response + '.pkl')

        else:
            print("\n New dataframe not saved")

        return df_merged

    else:
        print("\n Input invalid")

    return print("\n No merge conducted")

def merge_biologic2(search_word):     #function takes a vector of dataframes an merged them into one dataframe based on the "cycle_nr, charge_spec, discharge_spec, QE" format.

    database = user_setup.database

    all_files = support.find_files(search_word, database)  # Finds and returns files as list
    support.print_files_nr(all_files)  # prints files with nr
    #all_files = support.search_file(search_word, database)                                                        #Search for cells with the inputname in the given location

    response = input("\n Do you want to merge these files? yes/no:   ")                                 #Response from user

    if response.lower() == "yes":                                                                         #Starts mergning

        df_list = []                                                                                      #List of dataframes to be merged.

        for line in all_files:                                                                            #Creates a list of all dataframes to be merged.
            df_list.append(access_data.access_cell_data(line.stem))

        df_merged = pd.concat(df_list, axis=0)                                                            #Actual merging of dataframes.
        df_merged = df_merged.ix[:,['cycle_nr', "charge_spec", "discharge_spec", 'QE']]                   #Desides which colums are to be merged.
        df_merged = df_merged.dropna()                                                                    #Drop rows without input.

        #df_merged['cycle_nr'] = range(1, df_merged.shape[0] + 1)                                          #Renumber the cycling_nr column to go from 1--> x.
        df_merged['cycle_nr'] = range(1, len(df_merged.index)+1)
        #df_merged.set_index([list(range(df_merged.shape[0]))], inplace=True)                              #Renumber the index of the dataframe to go from 1 --> x.
        df_merged.set_index([list(range(len(df_merged.index)))], inplace=True)                              #Renumber the index of the dataframe to go from 1 --> x.

        plt.scatter(df_merged['cycle_nr'], df_merged['discharge_spec'], s=10, color='deepskyblue')        #Plots result, so that the user can see if it is satisfying.
        plt.show()

        response = input("\n Would you like to store the new file? yes/no:   ")

        if response.lower() == "yes":
            response = input("\n Please write file name:  ")
            df_merged.to_pickle(database.as_posix() + "/" + response)

            print("\n Database saved as: ",  response + '.pkl')

        else:
            print("\n New dataframe not saved")

        return df_merged

    else:
        print("\n Input invalid")

    return print("\n No merge conducted")


def auto_plot (search_word, **kwargs):

    import plot_support

    try:
        if kwargs['testing']==True:

            database = Path(r'..\PyBat2-master\testing\database')
            plots_folder = Path(r'..\PyBat2-master\testing\plots')
        else:
            database = Path(r'..\PyBat2-master\testing')
            plots_folder = user_setup.plots
    except:
        plots_folder = user_setup.plots
        database = user_setup.database

    # Identifying cells to plot
    cell_names = []  # Initiates list for cells that will be plotted.
    cell_paths = []  # Initiates list for paths to cells to be plotted.
    finished = False    # Determines if user is finished with input
    while finished == False:
        files = support.find_files(search_word, database)  # Finds and returns files as list
        support.print_files_nr(files)  # prints files with nr
        response = support.input_cool('yellow', 'Which of these cells do you want to plot? Write corresponding numbers, separated with "+" (Ex: 0+2+3):  ')
        c_response = response.split('+')  # Splits string by plus sign and stores new strings in list
        for i in range (0, len(c_response)):  # Loop through all cells to plot.
            cell_names.append((files[int(c_response[i])]).stem)  # Saves the cell name (.stem returns last path-element)
            cell_paths.append(str(files[int(c_response[i])]))    # Saves the full path to the cell

        response2 = support.input_cool('yellow', 'Search for more cells? (yes/any):   ')
        if response2 == 'yes':
            search_word = support.input_cool('yellow', 'Write new search word:   ')
        else:
            finished = True

    try:                # Checks legend and use cellnames if not found.
        legend_use = kwargs['legend']
    except:
        legend_use = cell_names

    x1, y1, xlabel, ylabel, xlim, ylim, xticks, yticks, markersize, legend_list, legend_loc, legend_color_list, custom_code, custom_code_first, save_path_png, save_path_tiff = plot_support.set_plot_specs(autolegend=legend_use, **kwargs)  # Sets specifications for plot
    pickle_name, df, cycles, color, color_list, legend_color_list = plot_support.set_pickle_specs(legend_color_list, pickle1=cell_paths[0], **kwargs)  # Sets specifications for first pickle
    plot_support.AddPickleToPlot(df, cycles, x1, y1, color_list, markersize, custom_code_first)       # Adds this pickle with specifications to plot

    for nr in range (2, len(cell_names)+1):
  #      try:
        next_pickle_response = cell_paths[nr-1]   # Looks up index in files given by the next cell in the response
        next_pickle_response_nr = 'pickle' + str(nr)
        next_pickle_name,next_y, next_cycles, next_color, next_color_scheme = plot_support.set_next_pickle(nr, override=next_pickle_response, **kwargs)
        pickle_name, df, cycles, color, color_list, legend_color_list = plot_support.set_pickle_specs(legend_color_list, pickle1=next_pickle_name, cycles1=next_cycles, x1=x1, y1=next_y, color1=next_color, color_scheme1=next_color_scheme)
        plot_support.AddPickleToPlot(df, cycles, x1, next_y, color_list, markersize)
#        except:
 #           continue  # Script moves to next iteration, checking for yet another pickle. (should not be needed here)

    plot_support.plot_plot(x1, y1, xlabel, ylabel, xlim, ylim, xticks, yticks, legend_list, legend_color_list,
                           legend_loc, custom_code, save_path_png, save_path_tiff)  # Add labels and legend, and shows plot

    return

def identify_file (suffix, file_path):
    identifier = None   # Initiates result variable
    if suffix == '.mpt':
        with open(file_path, 'r') as file_input:
            for line in file_input:  # Reads the data from the data_url line by line.
                if line.find('Ewe-Ece') != -1:  # -1 if not found, returns index if found
                    identifier = 'vmp3'
                elif line.find('Cyclic Voltammetry')!= -1:
                    identifier = 'vmp3'
                elif line.find('Re(Z)/Ohm') != -1:
                    identifier = 'impedance'
        file_input.close()
        if identifier == None:      # If suffix is mpt, but not vmp3-file, should be biologic file.
            identifier = 'biologic'
    elif suffix == '.xls':
        identifier = 'lanhe'
    elif suffix == '.txt' or suffix == '.TXT':
        identifier = 'maccor'

    return identifier

def change_cycle_def (search_word): # Rewrites cycle column according to first instance of discharge or charge
    import add_to_rawdata

    database = user_setup.database
    all_files = support.find_files(search_word, database)  # Finds and returns files as list
    support.print_files_nr(all_files)  # prints files with nr

    response = support.input_cool('yellow',"Which file do you want to change the cycle definition? Write nr:   ")  # Response from user
    file = all_files[int(response)]
    df_change = access_data.access_cell_data(file.stem)

    df_change = add_to_rawdata.add_cycle_incr(df_change)

    response2 = support.input_cool('yellow',"Overwrite existing file? (no/any):   ")  # Response from user
    if response2.lower() == 'no':
        new_name = support.input_cool('yellow','Write new cell name:   ')
        df_change.to_pickle(database.as_posix() + "/" + new_name)
        support.print_cool('green', new_name + ' saved to database.')
    else:
        df_change.to_pickle(database.as_posix() + "/" + file.stem)
        support.print_cool('green', 'Updated pickle saved to database.')

    return

def add_column (search_word, operation, new_variable_name=None, from_variable=None, scalar=None): # Add column with relation from excisting columns

    database = user_setup.database
    all_files = support.find_files(search_word, database)  # Finds and returns files as list
    support.print_files_nr(all_files)  # prints files with nr

    response = input("\n Which files do you want to add column to? Write nr separated with + here:   ")  # Response from user
    c_response = response.split('+')  # Splits string by plus sign and stores new strings in list
    for i in range(0, len(c_response)):  # Loop through all cells to plot.
        file = all_files[int(c_response[i])]
        df_add = access_data.access_cell_as_string(file.stem)

        if operation == 'multiply_scalar':
            df_add = multiply_scalar(df_add, new_variable_name, from_variable, scalar)
            df_add.to_pickle(database.as_posix() + "/" + file.stem)
            support.print_cool('green', 'New column added and saved')
        elif operation == 'CL+CCL':
            df_add = CCL(df_add)
            df_add.to_pickle(database.as_posix() + "/" + file.stem)
            support.print_cool('green', 'New column added and saved')
        else:
            support.print_cool('yellow','No columns added')

    return

def multiply_scalar(df, new_variable_name, from_variable, scalar):
    #df[new_variable_name] = df[from_variable].mul(scalar)
    df[new_variable_name] = [i * scalar for i in support.str_to_float(df[from_variable].tolist())]  # Multiplying each element in list that contains float numbers of column in df.
    return df

def CCL (df):
    CL = []
    CCL = []
    for i in range(0, len(df['discharge_spec'])):
        if i == 0:
            CL.append(float(df['charge_spec'][i]) - float(df['discharge_spec'][i]))
            CCL.append(CL[i])
        else:
            CL.append(float(df['charge_spec'][i]) - float(df['discharge_spec'][i]))
            CCL.append(CCL[i-1]+CL[i])
    df['CL'], df['CCL'] = CL, CCL
    return df