import pandas as pd

# Export data for e.g. plotting using other software.
from support import error_message


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