import pandas as pd

# Import csv data
df = pd.read_csv("Absenteeism-data.csv", delimiter=",")

# Create backup
raw_csv_data = df.copy()

# Delete ID column as it is not needed for analysis
df = df.drop(["ID"], axis = 1)

# Get descriptive statistics of columns
print(df.describe())

# Explore values within "Reason for Abscence" column
print(df["Reason for Absence"].min())
print(df["Reason for Absence"].max())
print(df["Reason for Absence"].unique())
print(len(df["Reason for Absence"].unique()))
print(sorted(df["Reason for Absence"].unique()))

# Set categorical nominal values for "Reason for Absence" to dummy values
# where 1 = presence of categorical event
# where 0 = absence of categorical event
reason_columns = pd.get_dummies(df["Reason for Absence"], dtype = int)

# Check that their are no missing values for "Reason for Absence"
reason_columns["check"] = reason_columns.sum(axis = 1)
print(reason_columns["check"].unique())

# Remove check column
reason_columns = reason_columns.drop(["check"], axis = 1)

# Drop reason column 0, that represents records with 0 hours of 
# absenteeism as analysis is not concerned with records without absenteeism
reason_columns = reason_columns.drop([0], axis = 1)

# To avoid multicollinearity the "Reason for Abscence" column will be
# replaced with the grouping / classification of reason_columns columns
df = df.drop(["Reason for Absence"], axis = 1)

# Group absence reasons
reason_type1 = reason_columns.loc[:, 1:14].max(axis=1)
reason_type2 = reason_columns.loc[:, 15:17].max(axis=1)
reason_type3 = reason_columns.loc[:, 18:21].max(axis=1)
reason_type4 = reason_columns.loc[:, 22:].max(axis=1)

# Concatenate absence reason group columns to data frame
df = pd.concat([df, reason_type1, reason_type2, reason_type3, reason_type4], 
                axis = 1)

# Rename columns with names of 0, 1, 2, and 3 as Reason_1 ... Reason_4
# Get comma seperated list of column names that can be pasted into column_names
print([df.columns.values]) 
column_names = ["Date", "Transportation Expense", "Distance to Work", "Age",
                "Daily Work Load Average", "Body Mass Index", "Education",
                "Children", "Pets", "Absenteeism Time in Hours", "Reason_1", 
                "Reason_2", "Reason_3", "Reason_4"]     
# Assigned revised column_names list to data frame
df.columns = column_names
# Check column names
print(df.head())

# Reorder columns
column_names_reordered = ["Reason_1", "Reason_2", "Reason_3", "Reason_4",
                        "Date", "Transportation Expense", "Distance to Work",
                        "Age", "Daily Work Load Average", "Body Mass Index",
                        "Education", "Children", "Pets",
                        "Absenteeism Time in Hours"]
df = df[column_names_reordered]
# Check column names
print(df.head())

# Create backup
df_reason_mod = df.copy()

# Check data type
print(type(df["Date"][0]))
# Change string to timestamp
df["Date"] = pd.to_datetime(df["Date"], format = "%d/%m/%Y")
# Check date data type is datetime
print(df.info())

# Extract month from each record and store in months_list
months_list = []
for i in range(df.shape[0]):
    months_list.append(df["Date"][i].month)
# Update data frame with "Month" column
df["Month"] = months_list
# Check months
print(df.head(20))

# Extract day of week and update data frame with "Day of Week" column
df["Day of Week"] = df["Date"].apply(lambda d: d.weekday())
# Check day of week
print(df["Day of Week"].iloc[:5])

# Reorder "Month" and "Day of Week" columns
col = df.pop("Month")
df.insert(4, col.name, col)
col = df.pop("Day of Week")
df.insert(5, col.name, col)
# Check "Month" and "Day of Week"
print(df.head(20))

# Remove Date column
df = df.drop(["Date"], axis=1)

# Group education as binary variable 0 - high school, 1 - college
df["Education"].map({1:0, 2:1, 3:1, 4:1})
# Check "Education" values
df["Education"].unique()
df["Education"].value_counts()

# Save data frame to .csv file
df.to_csv("absenteeism-cleaned.csv", index=False)
