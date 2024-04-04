import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_excel('final_merged_second_half - Processed - 2130hrs_file-3.xlsx')

# Convert the 'datecollected' column to datetime format
df['datecollected'] = pd.to_datetime(df['datecollected'], format='%m/%d/%Y')

# Sort the DataFrame by 'datecollected' in descending order
df = df.sort_values(by=['patient', 'datecollected'], ascending=[True, False])

# Drop duplicate 'patient' values, keeping the first occurrence (most recent date)
df = df.drop_duplicates(subset='patient', keep='first')

# Custom function to validate and create a new column
def validate_gender(gender):
    if gender.lower() == 'male':
        return 'Male'
    elif gender.lower() == 'female':
        return 'Female'
    else:
        return 'Unknown'

df['Sex'] = df['gender_description'].apply(validate_gender)

#<15 and 15+ except 95+
df['gender_description'].fillna(0, inplace=True)
# Convert a gender_description to float
df['age'] = df['age'].astype(float)
df['Age_recorded'] = df['age'].apply(lambda x: '<15' if x < 15 else '15+')
#Suppression
df['Suppression'] = df['result'].apply(lambda x: 'Suppressed' if (x == '< LDL copies/ml' or x == '< 40 Copies/ mL' or (isinstance(x, (int, float)) and x < 1000)) else 'Unsuppressed')
# Save the modified DataFrame to a new CSV file
df.to_excel('final_merged_second_half - Processed - 2130hrs_file-3.1.xlsx', index=False)
# sc_df=pd.read_excel('final_merged_second_half - Processed - 2130hrs.xlsx')
# print(sc_df.shape)
# new_df=pd.read_excel('eid_test_first_half_COP_20_38pm_file_1.xlsx')
# print(new_df.shape)
# merged_df=pd.concat([sc_df,new_df],ignore_index=True)
# merged_df.to_excel('master_merged - Processed - 2130hrs.xlsx')

