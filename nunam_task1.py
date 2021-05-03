# Import necessary modules
import pandas as pd
import cProfile
import pstats
# Get paths of excel file into variables
xls_file1 = "D:\\Nunam\\Data\\data.xlsx"
xls_file2 = "D:\\Nunam\\Data\\data_1.xlsx"
# Function to combine the sheets of related names into one dataframe.
# It returns a list of 3 dataframes which are then converted to 3 csv files


def combine(f1, f2):
    data = pd.read_excel(f1, sheet_name=None)  # Dataframe of excel file f1
    data_1 = pd.read_excel(f2, sheet_name=None)  # Dataframe of excel file f2
    # Get names of sheets in file 1 into a list 'sheet_names'
    sheet_names = list(data.keys())
    # Get names of sheets in file 2 and add to 'sheet_names' list
    sheet_names += list(data_1.keys())
    # Create empty list to store data from sheets
    # starting with name like Detail_67_
    detail = []
    # Create empty list to store data from sheets
    # starting with name like DetailVol_67_
    detail_vol = []
    # Create empty list to store data from sheets
    # starting with name like DetailTemp_67_
    detail_temp = []
    # Iterate through sheet_names
    # if the sheet matches the starting sequence,
    # append its data to corresponding list initialized above
    for i in sheet_names:
        if i.startswith("Detail_67_"):
            if(i in data.keys()):
                detail.append(data[i])
            else:
                detail.append(data_1[i])
        if i.startswith("DetailVol_67_"):
            if(i in data.keys()):
                detail_vol.append(data[i])
            else:
                detail_vol.append(data_1[i])
        if i.startswith("DetailTemp_67_"):
            if(i in data.keys()):
                detail_temp.append(data[i])
            else:
                detail_temp.append(data_1[i])
    # Concatenate and store data from sheets with related names
    d = pd.concat(detail)
    dv = pd.concat(detail_vol)
    dt = pd.concat(detail_temp)
    # Return list of dataframes of data from sheets with related names
    l = [d, dv, dt]
    return l
# Call function combine() on the given excel files
# store its profile testing result in text file
prof = cProfile.Profile()  # Initialize a profile object
# Call combine() within run() method of profile object
# to generate profile report
# store list returned by combine() in 'l'
prof.run('l=combine(xls_file1,xls_file2)')
# Write results of profile report to 'output.prof'
prof.dump_stats('C:\\Users\\piyus\\AppData\\Local\\Programs\\Python\\Python38\\output.prof')
# Open text file with append mode so that new report can be written into it
# if profile reports from other functions already exist
stream = open('C:\\Users\\piyus\\AppData\\Local\\Programs\\Python\\Python38\\output.txt', 'a')
# Copy contents(profile report) of output.prof to output.txt
stats = pstats.Stats('C:\\Users\\piyus\\AppData\\Local\\Programs\\Python\\Python38\\output.prof', stream=stream)
# Finally convert dataframes to csv files
l[0].to_csv("D:\\Nunam\\Data\\detail.csv", index=False)
l[1].to_csv("D:\\Nunam\\Data\\detailVol.csv", index=False)
l[2].to_csv("D:\\Nunam\\Data\\detailTemp.csv", index=False)
