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

# create a new dataframe to make it easier to plot the data in the format needed

remove_index = cons_merge.reset_index()
remove_index['DayMonth']= pd.to_datetime(remove_index['DayMonth'], dayfirst=True, format='%d%m')

plot = sns.lineplot(x = cons_merge.index, y = 'Consumption', hue='Year', data  = cons_merge)
#plot = sns.set(style='dark',)
#plt.plot()
plt.plot(cons_merge.index, cons_merge.Consumption)


fig, ax = plt.subplots()

for key, grp in remove_index.groupby(['Year']):
    if key==2016 or key==2017 or key==2018 or key==2019 or key==2020:
        ax = grp.plot(ax=ax, kind='line', x = "DayMonth", y='Consumption', label=key, linestyle='shaded')
plt.legend(loc='best')
plt.show()
