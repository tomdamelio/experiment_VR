#%%
import pandas as pd
import os
from pytube import YouTube

# read the Excel file into a DataFrame
df = pd.read_excel('df_with_validity_checks_2024_Tomi.xlsx')

#%%
def download_videos(df):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, 'vr_videos')
    os.makedirs(output_dir, exist_ok=True)

    for index, row in df.iterrows():
        if row['Selected'] == 'yes':
            yt = YouTube(row['link'])
            # Download entire video
            stream = yt.streams.get_highest_resolution()
            if stream is not None:
                output_file = os.path.join(output_dir, f"{row['id']}_{row['Title']}.mp4")
                stream.download(filename=output_file)
                print(f"Downloaded {row['Title']}.")


#%%
# Check if function works
# Define a test DataFrame with one row
#df = pd.DataFrame({
#    'link': ['https://www.youtube.com/watch?v=dvQZH5xYg0Y'],
#    'valid_video': ['yes'],
#    'start_time': [0],
#    'end_time': [0],
#    'Title': ['Test_video']
#})
#%%
# Call the download_videos function with the first row of df
download_videos(df)

# %%
# SEGUIR DESDE ACA -> MODIFICAR ESTA FUNCION PARA CORTAR LOS VIDEOS
# DESPUES, BUSCAR ALGUNA FORMA PARA DESCARGAR LOS VIDEOS EN FORMATO 360, VR
from moviepy.video.io.VideoFileClip import VideoFileClip

def crop_videos(df):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir_cropped = os.path.join(base_dir, 'vr_videos_cropped')
    os.makedirs(output_dir, exist_ok=True)

    for index, row in df.iterrows():
        if row['Selected'] == 'yes':
            video_path = row['link']
            start_time = row['start_time']
            end_time = row['end_time']
            title = row['Title']

            # Load video clip
            video = VideoFileClip(video_path)

            # Crop video clip based on start and end times
            if start_time == 0 and end_time == 0:
                cropped_video = video
            else:
                cropped_video = video.subclip(start_time, end_time)

            # Save cropped video clip to output directory
            output_file = os.path.join(output_dir, f"{title}.mp4")
            cropped_video.write_videofile(output_file)

            print(f"Cropped {title} video.")