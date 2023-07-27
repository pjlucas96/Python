import pandas as pd
import numpy as np

# Reading in the CSV files
pupils = pd.read_csv('Data\\PD 2022 Wk 1 Input - Input.csv')
grades = pd.read_csv('Data\\PD 2022 WK 3 Grades.csv')

# Removing unwanted columns
pupils = pupils[['id','pupil first name','pupil last name','gender','Date of Birth']]

# Joining files together
a = pd.merge(pupils, grades, how = 'inner', left_on = ('id'), right_on = ('Student ID'))

# Pivoting using melt function
a = pd.melt(a,
            id_vars=['Student ID','pupil first name', 'pupil last name', 'gender', 'Date of Birth'],
            value_vars=['Maths', 'English', 'Spanish', 'Science', 'Art', 'History', 'Geography'],
            var_name="Subject",
            value_name="Score")

# Creating a new table that gives each student's avg score
b = a.groupby('Student ID')['Score'].mean()

# Joining the avg score back to the initial table
df = pd.merge(a, b, on = 'Student ID')

# Defining a pass / fail column
def pass_fail(Score_x):
    if Score_x < 75:
        return "Failed"
    elif Score_x >= 75:
        return "Passed"
df['pass_fail'] = df['Score_x'].map(pass_fail)

# Creating a new Data Frame to include only Passed rows
passed = df.loc[(df['pass_fail'] == "Passed")]

# Counting the number of passes per student
passed = passed.groupby('Student ID')['pass_fail'].count()

# Joining the data frame with number of passes back to original
data = pd.merge(df, passed, how='left', on='Student ID')

# Keeping only required columns
data = data[['Student ID', 'gender', 'Score_y', 'pass_fail_y']]

# Rounding
data['Score_y'] = data['Score_y'].round(decimals=1)

# Renaming the columns
data_new_columns = data.columns.values
data_new_columns = ['Student ID','Gender',"Student's Avg Score",'Passed Subjects']
data.columns = data_new_columns

# Dropping duplicate rows to get one row per student
data = data.drop_duplicates()

# Making the null value in Passed Subjects = 0
data['Passed Subjects'] = data['Passed Subjects'].fillna(0)

# Output to csv
data.to_csv("Output\\Preppin Data W3 2022.csv")

print(data)