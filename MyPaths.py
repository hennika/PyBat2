# Set your own paths, that is forever yours (will not be changed with updates on other scripts)

from pathlib import Path

# ----------------------------------------------------------------------------------------------
# Fill in the locations of your folders using the variables below (Henning's files as examples)
# ----------------------------------------------------------------------------------------------
# Raw data (text files):
raw_data = Path(r'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Raw_files')

# Database where the imported cells will be (when saved as pickle)
database = Path(r'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Pickles')

# (Default) Location to where the exported data will be (possible to override)
exported_data = Path(r'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Exported')

# (Default) Location to where plots will be saved (possible to override)
plots = Path(r'C:/Users/hennika/OneDrive - NTNU/PhD/Results/Cycling/Plots')