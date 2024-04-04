import pandas as pd

# Load the HTS_TST and HTS_POS Excel files
pmtct_df = pd.read_csv('processed\PMTCT_STAT_2023_processed.csv')
pmtct_init_test=pmtct_df.query(f"dataname == 'MOH 731 Initial test at ANC HV02-04'")
pmtct_pos_results=pmtct_df.query(f"dataname == 'MOH 731 Positive Results_ANC HV02-11'")
pmtct_know_pos=pmtct_df.query(f"dataname == 'MOH 731 Known Positive at 1st ANC HV02-03'")
# Merge the two DataFrames on 'facilityid' to compare values
merged_df = pd.merge(pmtct_init_test, pmtct_pos_results, on='organisationunitid', suffixes=('_tst', '_pos'))

# Calculate the difference between corresponding 'total' columns
merged_df['difference'] = merged_df['Total_tst'] - merged_df['Total_pos']

# Filter rows where the difference is greater than or equal to 0
filtered_df = merged_df[merged_df['difference'] >= 0]
filtered_df_final=pd.concat([filtered_df,pmtct_know_pos],ignore_index=True)
filtered_df_final.drop_duplicates(inplace=True)
unmatched_df = merged_df[merged_df['difference'] <0]


# Drop the 'difference' column as it's no longer needed
#filtered_df = filtered_df.drop(columns=['difference'])

# Save the filtered DataFrame to a new Excel file (HTS_POS_CLEANED.xlsx)
unmatched_df.to_csv('cleaned/NEGATIVE_PMTCT_STAT_2023.csv', index=False)
filtered_df_final = filtered_df_final[[col for col in filtered_df.columns if not col.endswith('_tst')]]
filtered_df.columns=filtered_df.columns.str.replace('_pos', '')
filtered_df_final.to_csv('cleaned/CLEANED_PMTCT_STAT_2023.csv', index=False)

