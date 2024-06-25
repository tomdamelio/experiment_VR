#%%
import os

# Print the current working directory
print("Current Working Directory:", os.getcwd())

#%%

import pandas as pd
from moviepy.editor import VideoFileClip
import os

# Cargar los datos desde el archivo Excel
df = pd.read_excel('df_with_validity_checks_final_selection.xlsx')

df['id'] = df['id'].astype(int).astype(str)

# Directorio de los videos originales y el directorio destino para los videos recortados
src_directory = 'C:/Users/Cocudata/videos_360'
dest_directory = 'C:/Users/Cocudata/experiment_VR/stimuli/exp_videos/VR'

# Crear el directorio destino si no existe
if not os.path.exists(dest_directory):
    os.makedirs(dest_directory)

# Función para convertir tiempo 'mm:ss' a segundos
def time_to_seconds(t):
    min, sec = map(int, t.split(':'))
    return min * 60 + sec

# Procesar cada fila del DataFrame
for index, row in df.iterrows():
    video_id = row['id']
    good_track = row['good_track']
    if '-' in good_track:  # Asegurarse de que el formato es correcto
        start_time, end_time = good_track.split('-')
        start_seconds = time_to_seconds(start_time.strip())
        end_seconds = time_to_seconds(end_time.strip())

        # Nombre del archivo de video
        video_filename = f"{video_id}.mp4"
        video_path = os.path.join(src_directory, video_filename)
        output_path = os.path.join(dest_directory, video_filename)

        # Cargar el video y recortarlo
        if os.path.exists(video_path):
            clip = VideoFileClip(video_path).subclip(start_seconds, end_seconds)
            clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
            print(f"Video {video_filename} processed and saved to {output_path}")
        else:
            print(f"Video file {video_filename} not found.")
    else:
        print(f"No valid 'good_track' data for video {video_id}.")

# %%
