import pandas as pd

# Load the HTS_TST and HTS_POS Excel files
hts_pos = pd.read_csv('processed\HTS_POS_2023_processed.csv')
hts_pos.drop_duplicates(inplace=True)
hts_tst = pd.read_csv('processed\HTS_TST_2023_proccessed.csv')
hts_tst.drop_duplicates(inplace=True)
# Merge the two DataFrames on 'facilityid' to compare values
merged_df = pd.merge_ordered(hts_pos, hts_tst, on='organisationunitid', suffixes=('_pos', '_tst'),how='inner')
merged_df.to_csv('cleaned/Merged_df_tst_pos.csv')
print(merged_df.columns)
# Calculate the difference between corresponding 'total' columns
merged_df['difference'] = merged_df['Total_tst'] - merged_df['Total_pos']

# Filter rows where the difference is greater than or equal to 0
filtered_df = merged_df[merged_df['difference'] >= 0]
filtered_df.drop_duplicates(subset=['dataname_tst','dataname_pos','organisationunitid'],inplace=True)
less_zero_df = merged_df[merged_df['difference'] <0]
less_zero_df.drop_duplicates(subset=['dataname_tst','dataname_pos','organisationunitid'],inplace=True)
# Drop the 'difference' column as it's no longer needed
#filtered_df = filtered_df.drop(columns=['difference'])

# Save the filtered DataFrame to a new Excel file (HTS_POS_CLEANED.xlsx)
less_zero_df.to_csv('cleaned/LESS_ZERO_HTS_X-Y_2023.csv', index=False)
filtered_df = filtered_df[[col for col in filtered_df.columns if not col.endswith('_tst')]]
filtered_df.columns=filtered_df.columns.str.replace('_pos', '')
#filtered_df=pd.concat([hts_tst, filtered_df],ignore_index=True)
filtered_df.to_csv('cleaned/CLEANED_HTS_POS_2023.csv', index=False)

