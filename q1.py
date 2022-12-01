import pandas as pd
import numpy as np
# read in csv
merge_data = pd.read_csv("DSCodeTest/Merge.csv")

# check data
merge_data.head()

merge_data.describe()

merge_data.set_index(['Datetime'], inplace = True)

merge_data.index= pd.to_datetime(merge_data.index, dayfirst=True, format="%Y-%m-%d %H:%M:%S")

# check nulls
merge_data.isnull().sum()

merge_data.notnull().sum()

merge_data['Price'].mean()
merge_data['Price'].median()
merge_data['Price'].mode()

# split into 3 different dfs

mins = merge_data[merge_data['Resolution'] == "10MIN"]
hour = merge_data[merge_data['Resolution'] == "1H"]
day = merge_data[merge_data['Resolution'] == "D"]

# Fill in the NULL data with mean

mins['Price'] = mins['Price'].replace(np.nan,mins['Price'].mean())
hour['Price'] = hour['Price'].replace(np.nan,hour['Price'].mean())
day['Price'] = day['Price'].replace(np.nan,day['Price'].mean())

# look at hour data
hour.dtypes
data_drop = hour.drop('Resolution', axis = 1)

two_hour = hour.resample('2h', origin='start').mean()
two_hour.dropna(inplace=True)
# This is a dataframe with 2-hour resolution between 7:00 - 17:00 only as index
two_hour
# this will then
two_hour['Resolution'] = "2H"

# DF merged together with original data
two_hour_merged = pd.concat([merge_data, two_hour], axis=0)

# this dataframe takes the average of the two-hour windows and resamples them into
# 1 day resolution and then forward fills the empty days
two_hour_one_day = two_hour.resample('1d', origin='start').mean()

two_hour_one_day_ffill = two_hour_one_day[['Price']].ffill()

two_hour_one_day_ffill

