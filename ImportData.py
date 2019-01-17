# About scrip:
#-Loads biologic data and returns a list Data and the characteristic mass. Data is a list of list with all data from the txt file.


import numpy as np                # Matrise pakke
import pandas as pd               # Database pakke
import matplotlib.pyplot as plt   # Plottepakke
import StrToFloat


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

    if len(char_mass) >= 1:             # If more then 1 characteristic mass is found, the user is proped to decide which to use.
        print("\nMultiple characteristic masses found:  ", char_mass)
        char_mass = input("\nPleas write the characteristic mass that whould be used for calaculating spesific capacity:    ")

    if not char_mass:
        char_mass = input("\n No characteristic mass found. Please input mass:  ")

    file_input.close()
    return Data, char_mass


# Function for importing data from Lanhe
def importLanhe(data_url):

    with open(data_url, 'r') as file_input:
        Data = []  # Initiates a list to hold all data
        counter = 1

        for line in file_input:  # Reads the data from the data_url line by line.
            line = line.replace(",",".")  # Replaces "," with "." so that it is possible to convert the data from a string to a float.
            line = line.rstrip()
            if counter > 1:  # Evaluates if the line contains data or
                Data.append(line.split("\t"))  # Appendas data from a give line to the Data list
            counter = counter + 1

    file_input.close()
    return Data

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
    file_input.close()
    return Data, char_mass


# # #Testing of functions
#
#data_url = '/Users/andnor/OneDrive - NTNU/Diatoma/Experimental/Experimental data/Data Transfers/180226, DataTransfer/Diatoma, Biologic/180214/180214_SiO2MSC1_35CB_ECDEC_17_Hold120_2mV_CE5.mpt'
#Data = importBiologic(data_url)
#print(Data[0][0])
















    ## Storing data in Pandas
    #col = Data[0][0:(len(Data[0])-1)]
    #
    # SiO2M_3 = pd.DataFrame(Data[1:],columns=col)
    # SiO2M_3.to_pickle('SiO2M_3_ECDEC.pkl')
    #
    # A  = SiO2M_3['Q charge/mA.h'].tolist()
    # print(A)
    #
    # x = strToFloat.strToFloat(SiO2M_3['time/s'].tolist())
    # y = strToFloat.strToFloat(SiO2M_3['Ecell/V'].tolist())
    #
    # print(type(x[1]))







    # Reading data from list of list (Will probably not be used)



    # #Initierer tom liste
    # x = []      # Time
    # y = []      # Potential
    #
    #
    # # Henter ut "time and potential" data fra txt fil.
    # for numb in range(2,len(Data)):
    #     x.append(float(Data[numb][7]))
    #     y.append(float(Data[numb][11]))








    #Plotter data som X og Y
    # plt.plot(x, y)
    # plt.xlabel('time [s]')
    # plt.ylabel('voltage [V]')
    # plt.title('About as simple as it gets, folks')
    # plt.grid(False)
    # plt.locator_params(axis='both', nbins=6)
    # plt.ylim(ymax=2.4)
    # plt.show()
    #





#Lukker filer for å spare minne.


