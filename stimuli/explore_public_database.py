#%%
import pandas as pd
# Create a Pandas dataframe to store the xlsx file
df = pd.read_excel("df_with_comments.xlsx")

#%%
df["valid_video"] = "no"
df.loc[(df["valid_link"] == "yes") & (df["language_barriers"].isin(["no", "no/partial", "doubt", "partial"])), "valid_video"] = "yes"

#%%
def time_to_seconds(time_str):
    """Converts a string in the format 'MM:SS' to seconds"""
    if time_str == '':
        return 0
    else:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds

# Convert good_track column to string and fill NaN values with an empty string
df['good_track'] = df['good_track'].astype(str).fillna('')

# Extract the first and second times from the good_track column and convert them to seconds
df['start_time'] = df['good_track'].apply(lambda x: x.split('-')[0].strip() if '-' in x else '')
df['end_time'] = df['good_track'].apply(lambda x: x.split('-')[1].strip() if '-' in x else '')
df['start_time'] = df['start_time'].apply(time_to_seconds)
df['end_time'] = df['end_time'].apply(time_to_seconds)

# Compute the net time based on the good_track column and the Total time column
df['net_time'] = df.apply(lambda x: x['Total time (s)'] if pd.isnull(x['start_time']) else x['end_time'] - x['start_time'], axis=1)

#%%
import numpy as np
df['net_time'] = np.where(df['net_time'] == 0, df['Total time (s)'], df['net_time'])

#%%
df['valid_video_plus_60'] = np.where((df['valid_video'] == 'yes') & (df['net_time'] >= 1), 'yes', 'no')
df['valid_video_plus_120'] = np.where((df['valid_video'] == 'yes') & (df['net_time'] >= 1), 'yes', 'no')


# %%
%matplotlib 
# Scatter plot valence vs arousal
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.widgets import TextBox, Button
from matplotlib import rcParams
from urllib.parse import quote
import webbrowser


# Extract the relevant columns
valence = df['Valence']
arousal = df['Arousal']
total_time = df['net_time']
valid_video = df['valid_video_plus_120']
video_title = df['Title']
video_link = df['link']

# Define the point size as a function of the total time
point_size = 800 * total_time / max(total_time)

# Map the valid_link column to colors
colors = valid_video.map({'yes': 'blue', 'no': 'gray'})

# Create the scatterplot
fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(valence, arousal, s=point_size, c=colors, alpha=0.5)


# Set the axis labels, limits and title
ax.set_xlabel('Valence')
ax.set_ylabel('Arousal')
ax.set_title('Valence-Arousal Scatterplot with Point Size Scaled by Total Time')

# Set the axis limits
ax.set_xlim([1, 9])
ax.set_ylim([1, 9])

# Add labels for the legend and point size reference
ax.text(8.5, 1.5, 'Valid Video (available + no language barriers) = Yes', color='blue', ha='right', va='center', fontsize=14)
ax.text(8.5, 1.2, 'Valid Video (available + no language barriers) = No', color='gray', ha='right', va='center', fontsize=14)
ax.text(8.5, 8.5, 'Point Size\n(Scaled by Total Time)', ha='right', va='center', fontsize=14)

# Add vertical and horizontal dashed lines at x=5 and y=5
ax.axvline(5, linestyle='--', color='gray', alpha=0.5)
ax.axhline(5, linestyle='--', color='gray', alpha=0.5)

# Use mplcursors to make the plot interactive and show information about each video
def show_info(sel):
    index = sel.target.index
    v = valence[index]
    a = arousal[index]
    t = total_time[index]
    l = video_link[index]
    title = video_title[index]
    link_html = f'<a href="{l}" target="_blank">{l}</a>'
    info = f'\nTitle: {title}\nValence: {v:.2f}\nArousal: {a:.2f}\nTotal time: {t:.0f} seconds\nLink: {l}'
    sel.annotation.set_text(info)

cursor = mplcursors.cursor(ax, hover=True)
cursor.connect('add', show_info)

# %%
df.loc[df['valid_video_plus_120'] == 'yes', 'net_time'].sum()

# %%
# Download df
#df.to_excel('df_with_validity_checks.xlsx', index=False)
# %%
