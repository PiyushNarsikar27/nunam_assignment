# Import necessary modules
import pandas as pd
import cProfile
import pstats
"""Function for downsampling
4 arguments:
1.df: dataframe of data that is to be downsampled
2.cols_dict: dictionary with column names as keys
and aggregate functions to be applied on those columns for resampling as values
3.timestamp_col: name of column with timestamp observations
based on which we want to carry out resampling
4.record_index: name of column which should act as indexing column
"""


def downsample(df, cols_dict, timestamp_col, record_index):
    # Convert type of timestamp column to datetime
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    # Downsample 'df' to 1 sample per minute and store in 'df_ds'
    df_ds = df.resample("1min", on=timestamp_col).agg(cols_dict)
    # Add an index column
    df_ds[record_index] = range(1, len(df_ds)+1)
    # Return downsampled dataframe
    return df_ds
# Get path of csv file that is to be downsampled
detail = pd.read_csv("D:\\Nunam\\Data\\detail.csv")
"""Create dictionary with column names as keys
and aggregate functions to be applied on those columns for resampling as values
Here, for each column, first() is chosen as aggregate function
because every observation would be noted by the sensor
at the start of every minute had the sampling rate be 1 sample per minute"""
detail_ds_cols = {'Status': 'first', 'JumpTo': 'first', 'Cycle': 'first', 'Step': 'first', 'Cur(mA)': 'first', 'CapaCity(mAh)': 'first', 'Energy(mWh)': 'first', 'Voltage(V)': 'first'}
# Initialize a profile object
prof1 = cProfile.Profile()
# Call downsample() within run() method of profile object
# to generate profile report
# store resulting downsampled dataframe in 'detail_ds'
prof1.run('detail_ds = downsample(detail,detail_ds_cols,\'Absolute Time\',\'Record Index\')')
# Write results of profile report to 'output.prof'
prof1.dump_stats('output.prof')
# Open text file with append mode
# so that new report can be written into it
# if profile reports from other functions already exist
stream = open('output.txt', 'a')
# Copy contents(profile report) of output.prof to output.txt
stats = pstats.Stats('output.prof', stream=stream)
# Repeat same procedure for remaining two csv files
detailVol = pd.read_csv("D:\\Nunam\\Data\\detailVol.csv")
detailVol_ds_cols = {'Step Name': 'first', 'Auxiliary channel TU1 U(V)': 'first', 'Gap of Voltage': 'first', 'Realtime': 'first'}
prof2 = cProfile.Profile()
prof2.run('detailVol_ds = downsample(detailVol, detailVol_ds_cols, \'Realtime\', \'Record ID\')')
prof2.dump_stats('output.prof')
stream = open('output.txt', 'a')
stats = pstats.Stats('output.prof', stream=stream)


detailTemp = pd.read_csv("D:\\Nunam\\Data\\detailTemp.csv")
detailTemp_ds_cols = {'Step Name': 'first', 'Auxiliary channel TU1 T(°C)': 'first', 'Gap of Temperature': 'first', 'Realtime': 'first'}
prof3 = cProfile.Profile()
prof3.run('detailTemp_ds=downsample(detailTemp,detailTemp_ds_cols,\'Realtime\',\'Record ID\')')
prof3.dump_stats('output.prof')
stream = open('output.txt', 'a')
stats = pstats.Stats('output.prof', stream=stream)

# Finally convert downsampled dataframes to csv files
detail_ds.to_csv("D:\\Nunam\\Data\\detailDownsampled.csv", index=False)
detailVol_ds.to_csv("D:\\Nunam\\Data\\detailVolDownsampled.csv", index=False)
detailTemp_ds.to_csv("D:\\Nunam\\Data\\detailTempDownsampled.csv", index=False)
