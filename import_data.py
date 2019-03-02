# About scrip:
#-Loads biologic data and returns a list Data and the characteristic mass. Data is a list of list with all data from the txt file.


import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import string_to_float
import support



# Function for importing data from Biologic
def importBiologic(data_url):                               #data_url is the location of data to be red.
    with open(data_url,'r') as file_input:
        Evaluater = False                                   # Evaluation variable used to determide where the data in the biologic tex file is. (We don't want to read all the junk in the begining of the document).
        char_mass = []
        Data = []                                           # Initiates a list to hold all data

        for line in file_input:                             # Reads the data from the data_url line by line.

            line = line.replace(",",".")  # Replaces "," with "." so that it is possible to convert the data from a string to a float.
            line = line.rstrip()                            # Removes all kind of trailing characters. Eks: Whitespace and \n at the end of a line

            if Evaluater == True:                           # Evaluates if the line contains data or

                    if line.find('mod') == 0 or line.find('ox/red')==0:

                        print("\n " ,line, "\n\n  Is not a int/float ")

                        response = input('\nDo you want to add the line anyway? (yes/no)  ')

                        if response.lower == 'yes':
                            Data.append(line.split("\t"))
                        else:
                            print("\n Line", line, " \n \n not added to dataframe")

                    else:
                        Data.append(line.split("\t"))  # Appendas data from a give line to the Data list

            elif line.find('Characteristic mass') == 0:     # Identifies the characteristic mass in the documet.
                if char_mass:
                    char_mass.append(float(line.split(' ')[3]))
                char_mass.append(line.split(' ')[3])
            else:
                if line.find('mod') == 0 and line.find('ox/red'):
                    Data.append(line.split("\t"))
                    Evaluater = True

    char_mass = check_char_mass(char_mass)

    file_input.close()

    return Data, char_mass


# Function for importing data from Lanhe
def importLanhe(data_url):

    df = pd.read_excel(data_url, skiprows=0)  # Reads all rows (first row becomes headers). https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html

    return df

# Function for importing data from Maccor
def importMaccor(data_url):
    with open(data_url,'r') as file_input:
        Evaluater = False  # Evaluation variable used to determine where the data in the text file is. (We don't want to read all the junk in the beginning of the document).
        char_mass = None
        Data = []  # Initiates a list to hold all data

        for line in file_input:  # Reads the data from the data_url line by line.
            line = line.replace(",", ".")       # Replaces "," with "." so that it is possible to convert the data from a string to a float.
            if Evaluater == True:  # Evaluates if the line contains data or
                Data.append(line.split("\t"))   # Appends data from a give line to the Data list
            elif line.find('SCap')==0:          # Identifies the characteristic mass in the document, as grams(!).
                char_mass = line.split("\t")[1] # The mass is found (zero element is 'Scap')
            else:
                if line.find('Rec')==0 and line.find('Cycle P')==4:     # Attempts to find variables at positions they're supposed to if text file is exported correctly
                    Data.append(line.split("\t"))   # Appends coloumn names
                    Evaluater = True                # Sets evaluater to true, will start read in data from next line

    char_mass = check_char_mass(char_mass)      # Verifies found char_mass with user.

    file_input.close()
    return Data, char_mass

def check_char_mass (found_mass):
    use_mass = None # value to be returned
    if found_mass!=None:
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


# # #Testing of functions
#
#data_url = '/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Experimental data/Data Transfers/180226, DataTransfer/Diatoma, Biologic/180214/180214_SiO2MSC1_35CB_ECDEC_17_Hold120_2mV_CE5.mpt'
#Data = importBiologic(data_url)
#print(Data[0][0])



