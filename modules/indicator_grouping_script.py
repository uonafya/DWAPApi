import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('HTS_POS_ALL_FACILITIES_OCT22_SEPT23.csv')
df.drop(columns=['datadescription','organisationunitdescription'],inplace=True)
# Iterate through the columns corresponding to months
months = ['October 2022', 'November 2022', 'December 2022',
       'January 2023', 'February 2023', 'March 2023', 'April 2023', 'May 2023',
       'June 2023', 'July 2023', 'August 2023', 'September 2023']

# Initialize a dictionary to store the running sum for each facility
facility_sums = {}

df =df.head(100)
for month in months:
    # Fill NaN values with 0 for the current month
    df[month] = df[month].fillna(0)

    # Convert the month column to a numeric data type
    df[month] = pd.to_numeric(df[month], errors='coerce')

    # Iterate through rows and sum values for each facility
    for index, row in df.iterrows():
        #print(row)
        facility_id = row['organisationunitid']
        dataname=row['dataname']
        if facility_id in facility_sums and dataname in facility_sums:
            facility_sums[facility_id] += row[month]
        else:
            facility_sums[facility_id] = row[month]
            facility_sums[dataname]=dataname
df.drop(columns=months,inplace=True)

# Create a new DataFrame to store the final sums
final_sum_df = pd.DataFrame(list(facility_sums.items()), columns=['organisationunitid', 'total'])

# Merge the final sum DataFrame with the original DataFrame on 'organisationunitid'
df = df.merge(final_sum_df, on='organisationunitid', how='left')
df.to_csv('PROCCESSED_HTS_POS_ALL_FACILITIES_OCT22_SEPT23.csv', index=False)

