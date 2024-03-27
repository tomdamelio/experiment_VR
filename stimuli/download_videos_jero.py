#%%
import pandas as pd
import os
from pytube import YouTube

# read the Excel file into a DataFrame
df = pd.read_excel('df_with_validity_checks_2024_Tomi.xlsx')


#%%
def download_videos(df):
    base_dir = os.path.dirname(os.path.abspath(_file_))
    output_dir = os.path.join(base_dir, 'vr_videos')
    os.makedirs(output_dir, exist_ok=True)

    for index, row in df.iterrows():
        if row['Selected'] == 'yes':
            if row['id'] == 104:
                print(f"Skipping video with id {row['id']} named {row['Title']}.")
                continue  # Skip the rest of the loop for video with id 104

            yt = YouTube(row['link'])
            # Obtener todos los streams de video disponibles
            video_streams = yt.streams.order_by('resolution').desc()

            for stream in video_streams:
                file_extension = stream.mime_type.split('/')[-1]  # Extract the file extension from the mime_type
                output_file = os.path.join(output_dir, f"{row['id']}{stream.resolution}{stream.fps}fps_{row['Title'].replace('/', '_')}.{file_extension}")
                
                # Check if the file already exists
                if not os.path.exists(output_file):
                    stream.download(output_path=output_dir, filename=output_file)
                    print(f"Downloaded {row['Title']} in {stream.resolution} at {stream.fps}fps with extension {file_extension}.")
                else:
                    print(f"Video with id {row['id']} named {row['Title']} in {stream.resolution} at {stream.fps}fps already downloaded.")

#%%
download_videos(df)