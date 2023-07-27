import pandas as pd
import numpy as np
import datetime as dt
from datetime import date
import calendar as cl

# Reading in the CSV
cakes = pd.read_csv('Data\\PD 2022 Wk 1 Input - Input.csv')

# Only bringing back the columns that I want to use
cakes = cakes[['id','pupil first name','pupil last name','gender','Date of Birth']]

# Concatenating first and last name to give a full name
cakes['pupil full name'] = cakes['pupil first name'] + ' ' + cakes['pupil last name']

# Converting the birthdays to a datetime
cakes['Date of Birth'] = pd.to_datetime(cakes['Date of Birth'], format = '%m/%d/%Y')

# Getting this years birthday (not sure how this works...)
cakes['This Years Birthday'] = cakes['Date of Birth'].apply(lambda cakes: cakes.replace(year = 2022))

# Getting the day of week for this years birthday
cakes['Cake Needed On'] = cakes['This Years Birthday'].dt.day_name()

# Replacing Saturday and Sunday with Friday
cakes['Cake Needed On'] = cakes['Cake Needed On'].replace('Saturday', 'Friday')
cakes['Cake Needed On'] = cakes['Cake Needed On'].replace('Sunday', 'Friday')

# Getting the month number from birth date
cakes['Month'] = pd.DatetimeIndex(cakes['Date of Birth']).month

# Getting the full month name
cakes['Month'] = cakes['Month'].apply(lambda x: cl.month_name[x])

# Group by Month and Day to count the number of IDs
group = cakes.groupby(['Month','Cake Needed On']).agg(
    BDs_per_weekday_and_month = ('id','count')
).reset_index()

# Joining cakes and group
df = pd.merge(cakes, group, how='inner',left_on = ('Month','Cake Needed On'),right_on=('Month','Cake Needed On'))

# Removing unwanted columns
df = df[['pupil full name','Date of Birth','This Years Birthday','Month','Cake Needed On','BDs_per_weekday_and_month']]

# Renaming the columns
df_new_columns = df.columns.values
df_new_columns = ['Pupil Name','Date of Birth',"This Year's Birthday",'Month','Cake Needed On','BDs per Weekday and Month']
df.columns = df_new_columns

# Output to csv
df.to_csv("Output\\Preppin Data W2 2022.csv")

print(df)