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

        if isinstance(search_word, list):   # User should then have specified cells so that only one pickle  matches each instance in the list of plotted cells
            support.print_cool('green', 'Assumes all cells are specified in search word list, skipping more searching')
            for i in range(0, len(search_word)):
                file = support.find_single_file(search_word[i], database)
                cell_names.append(file.stem)
                cell_paths.append(str(file))
            finished = True
        else:
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

    x1, y1, xlabel, ylabel, xlim, ylim, xticks, yticks, type, markersize, legend_list, legend_loc, legend_color_list, custom_code, custom_code_first, save_path_png, save_path_tiff = plot_support.set_plot_specs(autolegend=legend_use, **kwargs)  # Sets specifications for plot
    pickle_name, df, cycles, color, color_list, legend_color_list, marker, markerfill, linestyle = plot_support.set_pickle_specs(legend_color_list, pickle1=cell_paths[0], **kwargs)  # Sets specifications for first pickle
    plot_support.AddPickleToPlot(df, cycles, x1, y1, color_list, type, marker, markerfill, markersize, linestyle, custom_code_first)       # Adds this pickle with specifications to plot

    for nr in range (2, len(cell_names)+1):
  #      try:
        next_pickle_response = cell_paths[nr-1]   # Looks up index in files given by the next cell in the response
        next_pickle_response_nr = 'pickle' + str(nr)
        next_pickle_name,next_x, next_y, next_cycles, next_color, next_color_scheme, next_marker, next_markerfill, next_linestyle = plot_support.set_next_pickle(nr, override=next_pickle_response, **kwargs)
        pickle_name, df, cycles, color, color_list, legend_color_list, marker, markerfill, linestyle = plot_support.set_pickle_specs(legend_color_list, pickle1=next_pickle_name, cycles1=next_cycles, x1=next_x, y1=next_y, color1=next_color, color_scheme1=next_color_scheme, marker1=next_marker, markerfill1=next_markerfill, linestyle1=next_linestyle)
        plot_support.AddPickleToPlot(df, cycles, next_x, next_y, color_list, type, marker, markerfill, markersize, linestyle)
#        except:
 #           continue  # Script moves to next iteration, checking for yet another pickle. (should not be needed here)

    plot_support.plot_plot(x1, y1, xlabel, ylabel, xlim, ylim, xticks, yticks, legend_list, legend_color_list,
                           legend_loc, custom_code, save_path_png, save_path_tiff)  # Add labels and legend, and shows plot

    return

def batch_plot (search_word, **kwargs):

    import plot_support
    plots_folder = user_setup.plots
    database = user_setup.database
    colors_qual = user_setup.colors_qual

    # Identifying cells to plot
    cell_names = []  # Initiates list for cells that will be plotted.
    cell_paths = []  # Initiates list for paths to cells to be plotted.
    finished = False    # Determines if user is finished with input
    while finished == False:
        files = support.find_files(search_word, database)  # Finds and returns files as list
        if len(files) == 1:
            support.print_cool ('green',"Found only one file, using this.")
            cell_names.append(files[0].stem)  # Saves the cell name (.stem returns last path-element)
            cell_paths.append(str(files[0]))  # Saves the full path to the cell
            finished = True
            continue
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

    for nr in range (0, len(cell_names)):
        list = access_data.columns(cell_paths[nr], ['cycle_nr', 'discharge_spec', 'charge_spec', 'cap_incr_spec', 'potential', 'cycle'])
        df = access_data.access_cell_as_string(cell_names[nr])
        cycles, discharge, charge, capacity_incr, potential, cycle_incr = list[0][0], list[1][0], list[2][0], list[3][0], list[4][0], list[5][0]
        CE = [float(ai)/bi*100 for ai,bi in zip(discharge,charge)]  # Obtaining Coulombic efficiencies

        fontsize = 10
        fig, axs = plt.subplots(3,2, figsize=(7,7))
        """     Capacity vs cycle nr    """
        axs[0,0].scatter(cycles, discharge, color=colors_qual[0])
        axs[0,0].scatter(cycles, charge, marker='D', color=colors_qual[1])
        axs[0,0].set_xlabel('Cycle number', size=fontsize)
        axs[0,0].set_ylabel('Capacity (mAh/g)', size=fontsize)
        axs[0,0].tick_params(axis='both', which='major', labelsize=fontsize) # Setting ticks size equally enlarged to fontsize
        axs[0,0].tick_params(direction='in')     # Ticks pointing inwards.
        axs[0,0].legend(['Discharge', 'Charge'], prop={'size': fontsize})
        #plt.savefig((str('C:\\Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Plots\MP1H') + '\\' + 'MP1H_D1_16_100-250mA_capacity-cycle-nr' + '.png'),format='png', dpi=1000)  # > 300 DPI is recommended by NTNU in master theses.
        """     Coulombic efficiency    """
        axs[0,1].scatter(cycles, CE, color=colors_qual[0])
        axs[0,1].set_xlabel('Cycle number', size=fontsize)
        axs[0,1].set_ylabel('Coulombic efficiency (%)', size=fontsize)
        axs[0,1].tick_params(axis='both', which='major',labelsize=fontsize)  # Setting ticks size equally enlarged to fontsize
        axs[0,1].tick_params(direction='in')  # Ticks pointing inwards.
        axs[0,1].legend(['C.E.'], prop={'size': fontsize})
        # plt.savefig((str('C:\\Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Plots\MP1H') + '\\' + 'MP1H_D1_16_100-250mA_capacity-cycle-nr' + '.png'),format='png', dpi=1000)  # > 300 DPI is recommended by NTNU in master theses.
        """     Voltage profiles (all)    """
        color_list = plot_support.get_colors(cycle_incr, color_scheme='Blues')
        last_cycle = df['cycle'].as_matrix().astype(int)[-1]  # Converts cycle column to int, and get last element (last cycle nr).
        cycles = range(0,last_cycle,1)  # Makes variable with cycles to plot (all)
        for i in range (0, last_cycle,1):  # Iterates through all cycles
                df_cycle_x = df[df['cycle'].astype(float) == cycles[i]]  # Make new data frame for given cycle
                axs[1, 0].scatter(df_cycle_x['cap_incr_spec'].astype(float), df_cycle_x['potential'].astype(float), s=1, c=color_list[i])
        axs[1,0].set_xlabel('Capacity (mAh/g)', size=fontsize)
        axs[1,0].set_ylabel('Voltage', size=fontsize)
        axs[1,0].tick_params(axis='both', which='major',labelsize=fontsize)  # Setting ticks size equally enlarged to fontsize
        axs[1,0].tick_params(direction='in')  # Ticks pointing inwards.
        axs[1,0].legend(['All cycles'], prop={'size': fontsize})
        #axs[1,0].legend(['Voltage profile'], prop={'size': fontsize})
        # plt.savefig((str('C:\\Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Plots\MP1H') + '\\' + 'MP1H_D1_16_100-250mA_capacity-cycle-nr' + '.png'),format='png', dpi=1000)  # > 300 DPI is recommended by NTNU in master theses.
        """     Voltage profiles (selected)    """
        cycles = [1,2,10,50,100] # Makes variable with cycles to plot
        color_list = plot_support.get_colors(cycle_incr, cycles=cycles, color_scheme='Qualitative')
        for i in range(0, len(cycles), 1):  # Iterates through all cycles
            df_cycle_x = df[df['cycle'].astype(float) == cycles[i]]  # Make new data frame for given cycle
            axs[1, 1].scatter(df_cycle_x['cap_incr_spec'].astype(float), df_cycle_x['potential'].astype(float), s=1,
                              c=color_list[i], label='%s' %cycles[i])
        axs[1, 1].set_xlabel('Capacity (mAh/g)', size=fontsize)
        axs[1, 1].set_ylabel('Voltage', size=fontsize)
        axs[1, 1].tick_params(axis='both', which='major',
                              labelsize=fontsize)  # Setting ticks size equally enlarged to fontsize
        axs[1, 1].tick_params(direction='in')  # Ticks pointing inwards.
        axs[1, 1].legend(prop={'size': fontsize})
        # plt.savefig((str('C:\\Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Plots\MP1H') + '\\' + 'MP1H_D1_16_100-250mA_capacity-cycle-nr' + '.png'),format='png', dpi=1000)  # > 300 DPI is recommended by NTNU in master theses.

        """     Differential capacity (selected cycles)    """
        cycles = [1, 2, 10, 50, 100]  # Makes variable with cycles to plot
        color_list = plot_support.get_colors(cycle_incr, cycles=cycles, color_scheme='Qualitative')
        for i in range(0, len(cycles), 1):  # Iterates through all cycles
            df_cycle_x = df[df['cycle'].astype(float) == cycles[i]]  # Make new data frame for given cycle
            axs[2, 0].scatter(df_cycle_x['potential_diff_cap'].astype(float), df_cycle_x['diff_cap'].astype(float), s=1,
                              c=color_list[i], label='%s' % cycles[i])
        axs[2, 0].set_xlabel('Potential (V)', size=fontsize)
        axs[2, 0].set_ylabel('Diff. capacity (mAh/g/V)', size=fontsize)
        axs[2, 0].tick_params(axis='both', which='major',
                              labelsize=fontsize)  # Setting ticks size equally enlarged to fontsize
        axs[2, 0].tick_params(direction='in')  # Ticks pointing inwards.
        axs[2, 0].legend(prop={'size': fontsize})
        # plt.savefig((str('C:\\Users\hennika\OneDrive - NTNU\PhD\Results\Cycling\Plots\MP1H') + '\\' + 'MP1H_D1_16_100-250mA_capacity-cycle-nr' + '.png'),format='png', dpi=1000)  # > 300 DPI is recommended by NTNU in master theses.

        """     Add more here   """
        axs[2, 1].text(0.35,0.5, 'Awesome!')

        fig.tight_layout()  # Makes sure everything is within figure

        """     Saving figures      """
        from pathlib import Path
        Path(str(plots_folder)+'\\'+cell_names[nr]).mkdir(parents=True, exist_ok=True)   # Make new folder for cell if it doesn't exist already
        resolution = 500

        extent = axs[0, 0].get_window_extent().transformed(fig.dpi_scale_trans.inverted())  # Collecting subplot to save
        fig.savefig(str(plots_folder) + '\\' + cell_names[nr] + '\\' + 'capacity_vs_cycles.png',
                    dpi=resolution, bbox_inches=extent.expanded(1.45, 1.5))  # Saving subplot

        extent = axs[1, 1].get_window_extent().transformed(fig.dpi_scale_trans.inverted())  # Collecting subplot to save
        fig.savefig(str(plots_folder)+'\\'+cell_names[nr]+'\\'+'Voltage_profiles_cycle_1-2-10-50-100.png',dpi=resolution, bbox_inches=extent.expanded(1.4, 1.42))   # Saving subplot

        plt.show()



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

def add_columns_from_textfile (search_word_pickle, textfile_url, list_of_vars_to_import): # Add data to existing dataframe from textfile containing variable name as header in first row.

    with open(textfile_url,'r') as file_input:
        data = [] # initiates variable to contain variables as columns

        for line in file_input:                             # Reads the data from the data_url line by line.
            line = line.replace(",",".")  # Replaces "," with "." so that it is possible to convert the data from a string to a float.
            line = line.rstrip()                            # Removes all kind of trailing characters. Eks: Whitespace and \n at the end of a line
            data.append(line.split("\t"))
        df_textfile = pd.DataFrame(data[1:],columns=data[0][0:(len(data[0]))])  # Creates the dataframe, with column names from first row.

    database = user_setup.database
    all_files = support.find_files(search_word_pickle, database)  # Finds and returns files as list
    support.print_files_nr(all_files)  # prints files with nr

    response = input("\n Which files do you want to add columns to? Write nr separated with + here:   ")  # Response from user
    c_response = response.split('+')  # Splits string by plus sign and stores new strings in list
    for i in range(0, len(c_response)):  # Loop through all cells to plot.
        file = all_files[int(c_response[i])]
        df_add = access_data.access_cell_as_string(file.stem)

        for i in range(0, len(list_of_vars_to_import)):
            df_add[list_of_vars_to_import[i]] = df_textfile[list_of_vars_to_import[i]]
        df_add.to_pickle(database.as_posix() + "/" + file.stem)
        support.print_cool('green', 'New column(s) added and saved')

    return