import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

cons_data = pd.read_csv("DSCodeTest/Consumption.csv")

# Two different data formats
# dd/mm/yyyy
# YYYYMMDD

# Split the data into two different dfs so te datetime can be converted without issue
normal_dateform = cons_data[cons_data["Date"].str.contains('/')]

normal_dateform['Date']= pd.to_datetime(normal_dateform['Date'], dayfirst=True)

different_dataform = cons_data[~cons_data["Date"].str.contains('/')]

different_dataform['Date'] = different_dataform['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

# merge the two dfs with matching datetime formats back into the same dataset

cons_merge = pd.concat([normal_dateform, different_dataform], axis=0)

cons_merge["Year"] = cons_merge['Date'].dt.year
cons_merge["DayMonth"] = cons_merge['Date'].dt.strftime('%m-%d')

cons_merge =cons_merge.set_index('DayMonth')

cons_merge.drop('Date', axis=1, inplace=True)

# Dataframe to show consumption of each year, with Year as column name and mm-dd as index
cons_merge

# create a new dataframe to make it easier to plot the data in the format needed when the index is not the date

remove_index = cons_merge.reset_index()

# Get average for each day
drop_yr = remove_index.drop('Year', axis = 1)
avrg_daily = drop_yr.groupby([cons_merge.index]).mean()

avrg_daily_drp = avrg_daily.reset_index()

# split into 2016-20
year1620 = cons_merge[cons_merge.Year == 2016]
year1620 = year1620.append(cons_merge[cons_merge.Year == 2017])
year1620 = year1620.append(cons_merge[cons_merge.Year == 2018])
year1620 = year1620.append(cons_merge[cons_merge.Year == 2019])
year1620 = year1620.append(cons_merge[cons_merge.Year == 2020])

# split into 2021-22
year2022 = cons_merge[cons_merge.Year == 2021]
year2022 = year2022.append(cons_merge[cons_merge.Year == 2022])

# drop reset index due to errors in plotting

year1620_drp = year1620.reset_index()

year2022_drp = year2022.reset_index()

# lineplot graph plot
fig, ax = plt.subplots(figsize=(30, 12))

palette1 = sns.color_palette("tab10")
palette2 = sns.color_palette("Paired")
palette3 = sns.color_palette("ch:9.5,-.2,dark=.9", 4)
ax = sns.lineplot(x=year1620_drp['DayMonth'],y= year1620_drp['Consumption'], hue=year1620_drp['Year'], palette=palette1, linestyle='dotted')
ax = sns.lineplot(x=year2022_drp['DayMonth'],y= year2022_drp['Consumption'], hue=year2022_drp['Year'], palette=palette2)
ax = sns.lineplot(x=avrg_daily_drp['DayMonth'],y= avrg_daily_drp['Consumption'], palette=palette3, linestyle='--', label = "Daily Average")
ax.set_title('Consumption of a Year', fontsize = 20, loc='center', fontdict=dict(weight='bold'))
ax.set_xlabel('Date', fontsize = 16, fontdict=dict(weight='bold'))
ax.set_ylabel('Consumption', fontsize = 16, fontdict=dict(weight='bold'))
plt.xticks(rotation=90, size= 2)
plt.show()

# From looking at the plot we can see the consumption is higher during the start and end of the year,
# with the lowest consumption being during the summer. The consumption is the highest during cold periods

# Was not sure what was meant by shaded for 2016-20 so I made them dotted