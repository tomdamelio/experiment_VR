
import subprocess
import os

# Directorio de videos de entrada y salida
#input_directory = 'C:/Users/Cocudata/test_videos_360'
input_directory = 'C:/Users/Cocudata/experiment_VR/stimuli/exp_videos/VR'
#output_directory = 'C:/Users/Cocudata/test_videos_2d'
output_directory = 'C:/Users/Cocudata/experiment_VR/stimuli/exp_videos/2D'

# Crear el directorio de salida si no existe
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Listar todos los archivos de video en el directorio de entrada
video_files = [f for f in os.listdir(input_directory) if f.endswith('.mp4')]

# Proceso de conversión para cada archivo de video
for video in video_files:
    input_path = os.path.join(input_directory, video)
    output_path = os.path.join(output_directory, video)
    
    # Comando ffmpeg para convertir el video
    command = [
        'ffmpeg',
        '-i', input_path, 
        '-vf', 'v360=input=e:output=flat', 
        output_path
    ]
    
    # Ejecutar el comando
    subprocess.run(command, check=True)

    print(f'Video converted and saved: {output_path}')
# %%
