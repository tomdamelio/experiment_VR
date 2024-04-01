#%%
import pandas as pd
import os
import subprocess
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError


# Cargar el DataFrame desde un archivo Excel
df = pd.read_excel('df_with_validity_checks_2024_Tomi_selected.xlsx')

#%%

def download_and_encode_videos(df):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, 'vr_videos')
    os.makedirs(output_dir, exist_ok=True)

    for index, row in df.iterrows():
        if row['Selected'] == 'yes':
            yt = YouTube(row['link'], use_oauth=True, allow_oauth_cache=True)
            print(f"Downloading {row['Title']} with id {row['id']}...")
            # Download entire video
            for n, stream in enumerate(yt.streams):
                file_extension = stream.mime_type.split('/')[1]
                raw_output_file = os.path.join(output_dir, f"{row['id']}_{row['Title']}-{n}_raw.{file_extension}")
                encoded_output_file = os.path.join(output_dir, f"{row['id']}_{row['Title']}-{n}.{file_extension}")
                stream.download(filename=raw_output_file)
                # Re-encode the video using FFmpeg
                try:
                    subprocess.run([
                        'ffmpeg', '-i', raw_output_file, 
                        '-c:v', 'libx264', '-preset', 'medium', 
                        '-c:a', 'aac', '-strict', 'experimental', 
                        '-b:a', '192k', '-y', 
                        encoded_output_file
                    ], check=True)
                    os.remove(raw_output_file)  # Remove the original download if re-encoding is successful
                except subprocess.CalledProcessError:
                    print(f"Error re-encoding {row['Title']}.")
                print(f"Downloaded and re-encoded {row['Title']}.")

#%%
#download_and_encode_videos(df)
