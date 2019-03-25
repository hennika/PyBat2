# About script:
# -Takes a biologic/Lanhe/Maccor txt file and convert the data into a pandas dataframe. The name of the colums is changed to global standard.
# -Saves as pickle.
import pandas as pd
import fix_rawdata
import import_rawdata as id
import fix_rawdata as fix
import add_to_rawdata as add
import support

def biologic(data_url, cell_key, database):

    # Imports raw data:
    df, char_mass = id.import_biologic(data_url)      # imports data and the characteristic mass from a bilogic txt file.

    # Clean up raw data:
    df, char_mass = fix.biologic(df, char_mass)

    # Add wanted columns to raw data:
    df = add.specific_capacity_incremental(df, char_mass)
    df = add.specific_capacity_cycle(df, char_mass)
    df = add.diffcap(df)
    df = add.cell_info(df, char_mass, cell_key)

    df.to_pickle((database + "/" + cell_key))  # OBS! Removed .pkl to avoid error. For storing data as a Pickle

    return df

def vmp3 (data_url, cell_key, database):
    df, char_mass = id.import_biologic(data_url)     # use ID:import_biologic to import data and the characteristic mass from a biologic txt file.

    if 'Ns changes' in df.columns:  # This should be a cycling file
        print ('Importing as VMP3 cycling file\n')
        df, char_mass = fix.vmp3_cycling(df, char_mass)
        df = add.specific_capacity_incremental(df, char_mass)
        df = add.specific_capacity_cycle(df, char_mass)
    else:
        print('Importing as VMP3 CV file, specific capacity not added.\n')
        df, char_mass = fix.vmp3_CV(df, char_mass)
        if not 'cycle' in df.columns:
            df = add.incremental_cycle_charge_discharge(df)
            print('Cycle, discharge and charge variable added from currents.')
        else:
            print()

    df.to_pickle((database + "/" + cell_key))  # Storing data as a Pickle

    return df

def lanhe(data_url, cell_key, database):

    # Imports raw data:
    df = id.import_lanhe(data_url)

    # Clean up raw data:
    df = fix.lanhe(df)

    # Tries to calculate characteristic mass and verifies with user / input from user:
    try:
        last_cap_incr = df['cap_incr'].iloc[-1]
        last_cap_incr_spec = df['cap_incr_spec'].iloc[-1]
        char_mass = last_cap_incr/last_cap_incr_spec*1000
        char_mass = fix_rawdata.check_char_mass(char_mass)
    except:
        char_mass = support.input_cool('yellow', 'No characteristic mass found. Please input mass:   ')

    #Add additional variables to pandas
    # First, need incremental cycle, discharge_incr and charge_incr (have cap_incr) to use AddSpecificCapacity functions:
    df = add.incremental_cycle_charge_discharge(df)
    # Then, can add specific incremental capacity (not really necessary, is in fact exported from Lanhe) and cyclebased:
    df = add.specific_capacity_incremental(df, char_mass)
    df = add.specific_capacity_cycle(df, char_mass)
    df = add.diffcap(df)
    df = add.cell_info(df, char_mass, cell_key)

    df.to_pickle((database + "/" + cell_key))  # Store data as a Pickle

    return df

def maccor(data_url, cell_key, database):
    # Imports raw data:
    df, char_mass = id.import_maccor(data_url)  # use ID:import_maccor to import data and the characteristic mass from a Maccor txt file.

    # Clean up raw data:
    df, char_mass = fix.maccor(df, char_mass)

    # Add wanted columns to raw data:
    df = add.incremental_charge_discharge_from_cap(df)
    df = add.specific_capacity_incremental(df, char_mass)
    df = add.specific_capacity_cycle(df, char_mass)
    df = add.diffcap(df)
    df = add.cell_info(df, char_mass, cell_key)

    df.to_pickle((database +"/" + cell_key))                                   #Store data as a Pickle

    return df






