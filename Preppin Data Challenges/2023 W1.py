import pandas as pd
import numpy as np
import datetime as dt
import calendar as cl

# Reading in the CSV files
bank = pd.read_csv('Data\\PD 2023 Wk 1 Input.csv')

# Split the transaction code into bank and code
newbank = bank['Transaction Code'].str.split("-", n=1, expand = True)

# Create the columns in the bank table for the split fields
bank['Bank'] = newbank[0]
bank['Code'] = newbank[1]

# Drop original Transaction Code
bank.drop(columns = ['Transaction Code'], inplace = True)

# Replace 1 and 2 values with Online and In-Person values
bank['Online or In-Person'] = bank['Online or In-Person'].replace(1, 'Online')
bank['Online or In-Person'] = bank['Online or In-Person'].replace(2, 'In-Person')

# Get the day of the week for given date
bank['Day of Week'] = pd.DatetimeIndex(bank['Transaction Date']).day_of_week
bank['Day of Week'] = bank['Day of Week'].apply(lambda x: cl.day_name[x])

print(bank)

# Output 1 is total number of transactions by Banks
output1 = bank.groupby('Bank')['Value'].sum()
print(output1)

# Output 2 is total number of transactions by Bank, day of week and type of transaction
output2 = bank.groupby(['Bank', 'Day of Week', 'Online or In-Person'])['Value'].sum().reset_index()
print(output2)

# Output 3 is total number of transactions by Bank and Customer Code
output3 = bank.groupby(['Bank', 'Customer Code'])['Value'].sum().reset_index()
print(output3)