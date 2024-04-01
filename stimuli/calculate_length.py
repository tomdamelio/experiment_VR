
#%%
import pandas as pd

# Load the data from an Excel file
file_path = 'df_with_validity_checks_2024_Tomi_selected.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path)

# Filter rows where 'VR and 2D available' is 'yes'
filtered_df = df[df['Selected'] == 'yes']

# Exclude rows with 'id' values 28 and 70
filtered_df_no_ids = filtered_df[~filtered_df['id'].isin([28, 70])]

#%%
# Asumimos que 'df' es tu DataFrame ya cargado

def time_to_seconds(time_str):
    """Convert 'mm:ss' format time string to seconds."""
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

# Apply the conversion to 'start_time' and 'end_time'
filtered_df_no_ids['start_time'] = filtered_df_no_ids['good_track'].apply(lambda x: time_to_seconds(x.split('-')[0].strip()))
filtered_df_no_ids['end_time'] = filtered_df_no_ids['good_track'].apply(lambda x: time_to_seconds(x.split('-')[1].strip()))

# Calculate 'net_time' as the difference between 'end_time' and 'start_time'
filtered_df_no_ids['net_time'] = filtered_df_no_ids['end_time'] - filtered_df_no_ids['start_time']

# Your DataFrame 'df' now has the updated columns



#%%

# Calculate the total 'net_time' in seconds grouped by 'Class'
total_time_per_class_no_ids = filtered_df_no_ids.groupby('Class')['net_time'].sum().reset_index()

# Calculate the sum of 'net_time' for HV classes (HVHA and HVLA)
hv_sum = total_time_per_class_no_ids[total_time_per_class_no_ids['Class'].str.contains('HV')]['net_time'].sum()

# Calculate the sum of 'net_time' for LV classes (LVHA and LVLA)
lv_sum = total_time_per_class_no_ids[total_time_per_class_no_ids['Class'].str.contains('LV')]['net_time'].sum()

# Output the sums
print(f'Sum of HV classes (HVHA and HVLA): {hv_sum} seconds')
print(f'Sum of LV classes (LVHA and LVLA): {lv_sum} seconds')
# %%

