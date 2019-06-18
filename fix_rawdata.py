import pandas as pd
import support


def biologic(df, char_mass):
    # Deletes unnecessary columns:
    del df['mode'], df['control changes'], df['Ns changes'], df['counter inc.'], df['Ns'], df['(Q-Qo)/mA.h'], df['control/V/mA'], df['Q charge/discharge/mA.h'], df['x'], df['control/V']  # Deletes row that we do not want.

    # Replaces the name of the colums with standard names:
    df = df.rename(
        columns={'ox/red': 'redox', 'time/s': 'time', 'dq/mA.h': 'dq', 'Ecell/V': 'potential', 'Ewe/V': 'potential',
                 'half cycle': 'halfcycle', 'Energy charge/W.h': 'energy_char', 'Energy discharge/W.h': 'energy_dis',
                 'Capacitance charge/µF': 'capacitance_char', 'Capacitance discharge/µF': 'capacitance_dis',
                 '<I>/mA': 'current', 'Q discharge/mA.h': 'discharge_incr', 'Q charge/mA.h': 'charge_incr',
                 'Capacity/mA.h': 'cap_incr', 'Efficiency/%': 'QE', 'control/mA': 'current_aim',
                 'cycle number': 'cycle', 'P/W': 'power'})

    # Verifies characteristic mass from user:
    char_mass = check_char_mass(char_mass)

    return df, char_mass

def vmp3_CV (df, char_mass):
    # Seems like exported file can either contain <> or not, remove it anyway:
    df.columns = df.columns.str.replace('<', '')
    df.columns = df.columns.str.replace('>', '')

    # Deletes unnecessary columns:
    # Column names from CV-file:  ['mode', 'ox/red', 'error', 'control changes', 'counter inc.', 'time/s', 'control/V', 'Ewe/V', '<I>/mA', 'cycle number', '(Q-Qo)/C', '<Ece>/V', 'P/W', 'Ewe-Ece/V']
    del df['mode'], df['control changes'], df['control/V'], df['counter inc.']  # Deletes row that we do not want.
    # Renames to standard names:
    df = df.rename(columns={'ox/red':'redox', 'time/s':'time','Ewe/V':'Ew','I/mA':'current', 'cycle number':'cycle', '(Q-Qo)/C':'(Q-Qo)/C', 'Ece/V': 'Ec', 'P/W': 'power', 'Ewe-Ece/V':'Ew-Ec'}) # Renaming.

    # Verifies characteristic mass from user:
    char_mass = check_char_mass(char_mass)

    return df, char_mass

def vmp3_cycling(df, char_mass):

    # Seems like exported file can either contain <> or not, remove it anyway:
    df.columns = df.columns.str.replace('<', '')
    df.columns = df.columns.str.replace('>', '')

    # Deletes unnecessary columns:
    del df['mode'], df['control changes'], df['Ns changes'], df['Ns'], df['(Q-Qo)/mA.h'], df['control/V/mA'], df['Q charge/discharge/mA.h'], df['x']
    # Renames to standard names:
    df = df.rename(
        columns={'ox/red': 'redox', 'time/s':'time','Ewe/V':'Ew','I/mA':'current', 'cycle number':'cycle', '(Q-Qo)/C':'(Q-Qo)/C', 'Ece/V': 'Ec', 'P/W': 'power', 'Ewe-Ece/V':'Ew-Ec', 'dq/mA.h': 'dq', 'half cycle': 'halfcycle', 'Energy charge/W.h': 'energy_char',
                 'Energy discharge/W.h': 'energy_dis', 'Capacitance charge/µF': 'capacitance_char',
                 'Capacitance discharge/µF': 'capacitance_dis', 'Q discharge/mA.h': 'discharge_incr',
                 'Q charge/mA.h': 'charge_incr', 'Capacity/mA.h': 'cap_incr', 'Efficiency/%': 'QE',
                 'control/mA': 'current_aim'})

    # Verifies characteristic mass from user:
    char_mass = check_char_mass(char_mass)

    return df, char_mass

def vmp3_impedance(df, char_mass):
    # Seems like exported file can either contain <> or not, remove it anyway:
    df.columns = df.columns.str.replace('<', '')
    df.columns = df.columns.str.replace('>', '')

    # Now columns are:
    # freq/Hz', 'Re(Z)/Ohm', '-Im(Z)/Ohm', '|Z|/Ohm', 'Phase(Z)/deg', 'time/s', 'Ewe/V', 'I/mA', 'Cs/µF', 'Cp/µF', 'cycle number', 'I Range', '|Ewe|/V', '|I|/A', 'Ece/V', '|Ece|/V', 'Phase(Zce)/deg', '|Zce|/Ohm',
    # 'Re(Zce)/Ohm', '-Im(Zce)/Ohm', 'Phase(Zwe-ce)/deg', '|Zwe-ce|/Ohm', 'Re(Zwe-ce)/Ohm', '-Im(Zwe-ce)/Ohm', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Re(Y)/Ohm-1', 'Im(Y)/Ohm-1', '|Y|/Ohm-1', 'Phase(Y)/deg'

    try:    # This only applies to 3-electrode cells I think, except statement is for coin cell impedance
        # Deletes unnecessary columns:
        del df['Unknown']   # Deletets all "Unknown" columns.
        # Renames to standard names:
        df = df.rename(
            columns={'freq/Hz':'freq', 'Re(Z)/Ohm':'Re_Z', '-Im(Z)/Ohm':'-Im_Z', '|Z|/Ohm':'|Z|', 'Phase(Z)/deg':'phase_Z',
                     'time/s':'time', 'Ewe/V':'Ew', 'I/mA':'current', 'Cs/µF':'Cs', 'Cp/µF':'Cp', 'cycle number': 'cycle', 'I Range':'current_range',
                     '|Ewe|/V':'|Ew|', '|I|/A':'|I|', 'Ece/V':'Ec', '|Ece|/V':'|Ec|', 'Phase(Zce)/deg':'phase_Zce', '|Zce|/Ohm':'|Zce|',
                     'Re(Zce)/Ohm':'Re_Zce', '-Im(Zce)/Ohm':'-Im_Zce', 'Phase(Zwe-ce)/deg':'phase_Zwe-ce', '|Zwe-ce|/Ohm':'|Zwe-ce|',
                     'Re(Zwe-ce)/Ohm':'Re_Zwe-ce', '-Im(Zwe-ce)/Ohm':'-Im_Zwe-ce', 'Re(Y)/Ohm-1':'Re_Y', 'Im(Y)/Ohm-1':'Im_Y', '|Y|/Ohm-1':'|Y|', 'Phase(Y)/deg':'phase_Y'
                     })
    except:
        # For coin cells, coloumns are: 'freq/Hz', 'Re(Z)/Ohm', '-Im(Z)/Ohm', '|Z|/Ohm', 'Phase(Z)/deg','time/s', 'Ewe/V', 'I/mA', 'Cs/µF', 'Cp/µF', 'cycle number', 'I Range',
        # '|Ewe|/V', '|I|/A', 'Re(Y)/Ohm-1', 'Im(Y)/Ohm-1', '|Y|/Ohm-1','Phase(Y)/deg'
        df = df.rename(
            columns={'freq/Hz':'freq', 'Re(Z)/Ohm':'Re_Z', '-Im(Z)/Ohm':'-Im_Z', '|Z|/Ohm':'|Z|', 'Phase(Z)/deg':'phase_Z',
        'time/s':'time', 'Ewe/V':'Ew', 'I/mA':'current', 'Cs/µF':'Cs', 'Cp/µF':'Cp', 'cycle number':'cycle', 'I Range':'current_range',
        '|Ewe|/V':'|Ew|', '|I|/A':'|I|', 'Re(Y)/Ohm-1':'Re_Y', 'Im(Y)/Ohm-1':'Im_Y', '|Y|/Ohm-1':'|Y|','Phase(Y)/deg':'phase_Y'})

        print(df.columns)
    # Verifies characteristic mass from user:
    char_mass = check_char_mass(char_mass)

    return  df, char_mass

def lanhe (df):

    del df['Index'], df['Energy/mWh'], df['SEnergy/Wh/kg'], df['SysTime'], df['Unnamed: 10']  # Deletes row that we do not want/need.
    df = df.rename(columns={'TestTime/Sec.': 'time', 'StepTime/Sec.': 'step_time', 'Voltage/V': 'potential',
                            'Current/mA': 'current', 'Capacity/mAh': 'cap_incr', 'SCapacity/mAh/g': 'cap_incr_spec',
                            'State': 'mode'})

    return df

def maccor (df, char_mass):
    # Now column names are: ['Rec', 'Cycle P', 'Cycle C', 'Step', 'TestTime', 'StepTime', 'Cap. [Ah]', 'Ener. [Wh]', 'Current [A]', 'Voltage [V]', 'Md', 'ES', 'DPT Time', 'AUX1 [V]', 'VAR1', 'VAR2', 'VAR3', 'VAR4', 'VAR5', 'VAR6', 'VAR7', 'VAR8', 'VAR9', 'VAR10', 'VAR11', 'VAR12', 'VAR13', 'VAR14', 'VAR15\n', 'NA']
    del df['ES'], df['AUX1 [V]'], df['VAR1'], df['VAR2'], df['VAR3'], df['VAR4'], df['VAR5'], df['VAR6'], df['VAR7'], \
    df['VAR8'], df['VAR9'], df['VAR10'], df['VAR11'], df['VAR12'], df['VAR13'], df['VAR14'], df['VAR15\n'], df[
        'NA']  # Deletes row that we do not want.
    # Now they are: ['Rec', 'Cycle P', 'Cycle C', 'Step', 'TestTime', 'StepTime', 'Cap. [Ah]', 'Ener. [Wh]', 'Current [A]', 'Voltage [V]', 'Md', 'DPT Time']
    # Replaces the name of the colums with standard names.
    df = df.rename(columns={'Rec': 'rec', 'Cycle P': 'cycle_p', 'Cycle C': 'cycle', 'Step': 'program_seq',
                            'TestTime': 'time', 'StepTime': 'program_seq_time',
                            'Cap. [Ah]': 'cap_incr', 'Ener. [Wh]': 'energy',
                            'Current [A]': 'current', 'Voltage [V]': 'potential',
                            'Md': 'mode', 'DPT Time': 'date'})
    # Now they are: ['rec', 'cycle_p', 'cycle', 'program_seq', 'time', 'program_seq_time', 'cap_incr', 'energy', 'current', 'potential', 'mode', 'date']

    char_mass = check_char_mass(char_mass)

    return df, char_mass


def check_char_mass (found_mass):
    use_mass = None # value to be returned
    if found_mass:
        support.print_cool('blue', 'Found this/these characteristic mass (mg): ', found_mass)
        response = support.input_cool('yellow', '\nUse this? (enter/no):   \n(If multiple masses, will use first)   ')
        if response == 'no':
            use_mass = support.input_cool('yellow', 'Please write desired mass (mg):   ')
        elif type(found_mass)==list:
            use_mass = found_mass[0]
        else:
            use_mass = found_mass
    else:
        use_mass = support.input_cool('yellow', 'No characteristic mass found. Please write desired mass (mg):   ')

    return use_mass