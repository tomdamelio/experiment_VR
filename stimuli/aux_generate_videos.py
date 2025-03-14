#%%
import os
import pandas as pd
import random
from moviepy import *


def generate_instruction(audio_path):
    """
    Pantalla negra con duración igual al audio + el audio embebido.
    """
    audio_clip = AudioFileClip(audio_path)
    black_screen_clip = (
        ColorClip(size=(3840, 2048), color=(0, 0, 0))
        .with_duration(audio_clip.duration)
        .with_audio(audio_clip)
    )
    return black_screen_clip

def generate_instruction_videos(input_dir, output_dir):
    """
    Genera videos .mp4 a partir de archivos de audio .wav en un directorio especificado.
    Cada video consiste en una pantalla negra con la duración del audio y el audio incorporado.

    Parámetros
    ----------
    input_dir : str
        Directorio que contiene los archivos de audio .wav.
    output_dir : str
        Directorio donde se guardarán los archivos de video .mp4 resultantes.
        Si no existe, se creará automáticamente.

    Ejemplo de uso
    --------------
    generate_instruction_videos(
        input_dir='./instructions_audios',
        output_dir='./instructions_videos'
    )
    """
    # Verificar si el directorio de entrada existe
    if not os.path.isdir(input_dir):
        raise ValueError(f"The input directory '{input_dir}' does not exist.")
    
    # Crear el directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Listar todos los archivos .wav en el directorio de entrada
    audio_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.wav')]
    
    if not audio_files:
        print(f"No se encontraron archivos .wav en el directorio '{input_dir}'.")
        return
    
    for audio_file in audio_files:
        input_audio_path = os.path.join(input_dir, audio_file)
        base_name = os.path.splitext(audio_file)[0]
        output_video_path = os.path.join(output_dir, f"{base_name}.mp4")
        
        try:
            # Generar el clip de video utilizando la función existente
            video_clip = generate_instruction(input_audio_path)
            
            # Escribir el video al directorio de salida
            video_clip.write_videofile(
                output_video_path,
                codec="libx264",
                audio_codec="aac",
                fps=60
            )
            
            # Cerrar los clips para liberar recursos
            video_clip.close()
            print(f"Video generado: {output_video_path}")
        
        except Exception as e:
            print(f"Error al procesar '{input_audio_path}': {e}")

#generate_instruction_videos(input_dir='./instructions_audios/new_audios', output_dir='./instructions_videos/new_videos')

#%%
def generate_practice_videos(modality="2D"):
    """
    Genera un video de práctica concatenando los siguientes elementos:
    1. welcome_text.mp4
    2. valence_practice_instructions_text.mp4
    3. Video 1
    4. post_stimulus_self_report_practice_new.wav
    5. arousal_practice_instructions_audio.wav
    6. Video 2
    7. post_stimulus_self_report.wav
    8. luminance_practice_instructions_audio.wav
    9. luminance video
    10.confidence_luminance_practice_instructions_text.wav
    11.end_practice.wav

    Parámetros:
    -----------
    modality : str
        "2D" o "VR" para especificar la carpeta de la que se toman los videos.
    """

    # ---------------------------
    # RUTAS A LOS VIDEOS
    # ---------------------------
    video_path_1            = f"./practice_videos/{modality}/991.mp4"
    video_path_2            = f"./practice_videos/{modality}/994.mp4"
    luminance_path_practice = f"./practice_videos/{modality}/green_intensity_video_1.mp4"
    #fixation_path           = "./final_videos_fixation/fixation_cross.mp4"
    countdown_bar_path      = "./final_videos_fixation/countdown_bar.mp4"

    # ---------------------------
    # RUTAS A LOS VIDEOS DE INSTRUCCIONES
    # ---------------------------
    welcome_path                       = "./instructions_videos/1_welcome_text.mp4"
    #baseline_path                      = "./instructions_videos/2_baseline_instructions_text.mp4"
    valence_practice_instruction_path  = f"./instructions_videos/{modality}/valence_practice_instructions_text.mp4"
    post_stimulus_self_report_path     = f"./instructions_videos/{modality}/post_stimulus_self_report_text_1.mp4"
    post_stimulus_self_report_2_path   = f"./instructions_videos/{modality}/post_stimulus_self_report_practice.mp4"
    arousal_practice_instructions_path = f"./instructions_videos/{modality}/arousal_practice_instructions_text.mp4"
    post_stimulus_verbal_report_path   = f"./instructions_videos/{modality}/post_stimulus_verbal_report.mp4"
    luminance_practice_path           = f"./instructions_videos/{modality}/luminance_practice_instructions_text.mp4"
    confidence_luminance_practice_path = f"./instructions_videos/{modality}/confidence_luminance_practice_instructions_text_2.mp4"
    confidence_verbal_report_path      = f"./instructions_videos/{modality}/confidence_verbal_report_text.mp4"
    end_practice_path                  = f"./instructions_videos/{modality}/end_practice.mp4"

    # ---------------------------
    # CARGAR VIDEOS
    # ---------------------------
    # Videos de estímulos
    video_1             = VideoFileClip(video_path_1).resized((3840, 2048))
    video_2             = VideoFileClip(video_path_2).resized((3840, 2048))
    luminance_practice  = VideoFileClip(luminance_path_practice).resized((3840, 2048))
    #fixation_clip       = VideoFileClip(fixation_path).resized((3840, 2048))
    countdown_bar       = VideoFileClip(countdown_bar_path).resized((3840, 2048))

    # Videos de instrucciones
    welcome_clip = VideoFileClip(welcome_path).resized((3840, 2048))
    #baseline_clip = VideoFileClip(baseline_path).resized((3840, 2048))
    valence_practice_clip    = VideoFileClip(valence_practice_instruction_path).resized((3840, 2048))
    post_stimulus_clip       = VideoFileClip(post_stimulus_self_report_path).resized((3840, 2048))
    post_stimulus_2_clip     = VideoFileClip(post_stimulus_self_report_2_path).resized((3840, 2048))
    arousal_instructions_clip = VideoFileClip(arousal_practice_instructions_path).resized((3840, 2048))
    post_stimulus_self_report = VideoFileClip(post_stimulus_verbal_report_path).resized((3840, 2048))
    luminance_practice_clip   = VideoFileClip(luminance_practice_path).resized((3840, 2048))
    confidence_luminance_practice_clip = VideoFileClip(confidence_luminance_practice_path).resized((3840, 2048))
    confidence_verbal_report_clip = VideoFileClip(confidence_verbal_report_path).resized((3840, 2048))
    end_practice_clip = VideoFileClip(end_practice_path).resized((3840, 2048))

    # ---------------------------
    # DEFINIR EL ORDEN DE CONCATENACIÓN
    # ---------------------------
    clips_in_order = [
        welcome_clip,                # 1
        #baseline_clip,               
        #fixation_clip,               
        valence_practice_clip,       # 2
        video_1,                     # 3
        post_stimulus_clip,          # 4
        post_stimulus_2_clip,        # 5
        arousal_instructions_clip,   # 6
        video_2,                     # 7
        post_stimulus_self_report,   # 8
        countdown_bar,               # 9
        confidence_verbal_report_clip, # 10
        luminance_practice_clip,     # 11
        luminance_practice,          # 12
        confidence_luminance_practice_clip, # 13
        end_practice_clip            # 15
    ]

    for idx, clip in enumerate(clips_in_order):
        print(f"Clip {idx}: size={clip.size}")
        if clip.mask:
            print(f"    Clip {idx} MASK size = {clip.mask.size}")

    # ---------------------------
    # CONCATENAR TODOS LOS CLIPS
    # ---------------------------
    final_clip = concatenate_videoclips(clips_in_order)

    # ---------------------------
    # EXPORTAR
    # ---------------------------
    output_path = f"./practice_videos/{modality}/S12_practice_{modality}.mp4"
    final_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

# Ejemplo de uso:
#generate_practice_videos("2D")         # Modalidad "2D" por defecto
generate_practice_videos("VR")     # Modalidad "VR"


#%%

import os
import cv2
import numpy as np
from scipy.io.wavfile import write
from moviepy import *


def generate_whistle_sound(duration_sec, sample_rate=44100, freq=500):
    # Generate time array
    t = np.linspace(0, duration_sec, int(duration_sec * sample_rate), endpoint=False)

    # Generate whistle signal
    whistle_signal = np.sin(2 * np.pi * freq * t)

    # Scale signal to 16-bit range
    whistle_signal = np.int16(whistle_signal * 32767)

    return sample_rate, whistle_signal

# Parameters for the whistle sound
duration_sec = 1
sample_rate, whistle_signal = generate_whistle_sound(duration_sec)
# Save whistle sound to file
write("whistle_sound.wav", sample_rate, whistle_signal)

#%%

def create_black_screen_video(duration_sec, output_file, fps=60, width=640, height=360):
    # Calculate number of frames
    num_frames = int(duration_sec * fps)

    # Create VideoWriter object
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Create black frame
    black_frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Write black frames to video
    for _ in range(num_frames):
        out.write(black_frame)

    # Release VideoWriter
    out.release()

#create_black_screen_video(30, "black_screen_30_sec.mp4", width=1280, height=720)



def create_flicker_screen_video(duration_sec, output_file, fps=60, width=640, height=360):
    num_frames = int(duration_sec * fps)
    # Crear VideoWriter
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    # Frames negros y blancos
    black_frame = np.zeros((height, width, 3), dtype=np.uint8)
    white_frame = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Calcular cuántos frames por medio ciclo
    cycles_per_second = 2
    frames_per_cycle = fps // cycles_per_second  # en este caso 30/5 = 6
    
    # Cada ciclo: mitad negro, mitad blanco
    half_cycle_frames = frames_per_cycle // 2  # 6/2 = 3
    
    # Generar los frames
    for i in range(num_frames):
        cycle_index = i % frames_per_cycle
        if cycle_index < half_cycle_frames:
            # Negro
            out.write(black_frame)
        else:
            # Blanco
            out.write(white_frame)
    
    out.release()


# Create black screen video of 1 second duration
#create_flicker_screen_video(1, "black_flicker_1_sec.mp4")


def add_audio_to_video(video_file, audio_file, output_file):
    # Load the video clip
    video_clip = VideoFileClip(video_file)

    # Load the audio clip
    audio_clip = AudioFileClip(audio_file)

    # Set audio duration to match video duration
    audio_clip = audio_clip.with_duration(video_clip.duration)

    # Add audio to video
    video_with_audio = video_clip.with_audio(audio_clip)

    # Write final video with audio
    video_with_audio.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=video_clip.fps)


# Add audio to the black screen video

#add_audio_to_video("black_screen_1_sec.mp4", "whistle_sound.wav", "black_screen_with_audio.mp4")

def append_videos(video1_file, video2_file, output_file, fps=60, codec="libx264", audio_codec='aac'):
    # Load video clips
    video1_clip = VideoFileClip(video1_file)
    video2_clip = VideoFileClip(video2_file)

    # Set the frame rate for the output video
    video2_clip = video2_clip.with_fps(fps)

    # Concatenate video clips
    final_clip = concatenate_videoclips([video1_clip, video2_clip, video1_clip])

    # Write final video to file, ensuring to specify both video and audio codecs
    final_clip.write_videofile(output_file, codec=codec, audio_codec=audio_codec)


# Append video_1.mp4 to the beginning of video_2.mp4


def process_videos_in_folder(modality="2D"):
    folder_path = f"videos_{modality}"
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4") or filename.endswith(".avi") or filename.endswith(".mov"):
            print("Processing video:", filename)
            
            video = cv2.VideoCapture(f'{folder_path}/{filename}')
            width_vid = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height_vid = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Crear flicker 1 seg con audio
            create_flicker_screen_video(1, "flicker_1_sec.mp4", width=width_vid, height=height_vid)
            add_audio_to_video("flicker_1_sec.mp4", "whistle_sound.wav", "flicker_1_sec_with_audio.mp4")

            # Crear flicker 1 seg final con audio
            create_flicker_screen_video(1, "flicker_1_sec_final.mp4", width=width_vid, height=height_vid)
            add_audio_to_video("flicker_1_sec_final.mp4", "whistle_sound.wav", "flicker_1_sec_final_with_audio.mp4")

            # Crear black screen 2 and 5 sec
            create_black_screen_video(2, "black_screen_2_sec.mp4", width=width_vid, height=height_vid)
            create_black_screen_video(5, "black_screen_5_sec.mp4", width=width_vid, height=height_vid)
            create_black_screen_video(30, "black_screen_30_sec.mp4", width=width_vid, height=height_vid)

            
            # Concatenar: black_screen_2_sec + flicker_1_sec_with_audio + video original + flicker_1_sec_final_with_audio + black_screen_5_sec
            black_2_clip = VideoFileClip("black_screen_2_sec.mp4")
            flicker_1_clip = VideoFileClip("flicker_1_sec_with_audio.mp4")
            original_clip = VideoFileClip(f'{folder_path}/{filename}')
            flicker_1_final_clip = VideoFileClip("flicker_1_sec_final_with_audio.mp4")
            #black_5_clip = VideoFileClip("black_screen_5_sec.mp4")
            #black_30_clip = VideoFileClip("black_screen_5_sec.mp4")


            final_clip = concatenate_videoclips([black_2_clip, flicker_1_clip, original_clip, flicker_1_final_clip, black_2_clip])
            final_clip.write_videofile(f'final_videos_{modality}/{filename}', codec='libx264', audio_codec='aac', fps=60)
            
            

#%%
process_videos_in_folder(modality='2D')

#%%
process_videos_in_folder(modality='VR')
#%%
process_videos_in_folder(modality='luminance')

# %%
process_videos_in_folder(modality='fixation')

# %%

def check_practice_videos_size(modality="2D"):
    """
    Loads practice videos and shows their original dimensions.

    Parameters:
    -----------
    modality : str
        "2D" or "VR" to specify the folder from which videos are taken.
    """
    # Rutas a los videos
    video_path_1 = f"./practice_videos/{modality}/991.mp4"
    video_path_2 = f"./practice_videos/{modality}/994.mp4"
    
    # Cargar los videos sin redimensionar
    video_1 = VideoFileClip(video_path_1)
    video_2 = VideoFileClip(video_path_2)
    
    # Imprimir dimensiones
    print(f"\nDimensiones de los videos de práctica ({modality}):")
    print(f"Video 991.mp4: {video_1.size}")
    print(f"Video 994.mp4: {video_2.size}")
    
    # Cerrar los clips para liberar recursos
    video_1.close()
    video_2.close()

# Ejemplo de uso:
#check_practice_videos_size("2D")
check_practice_videos_size("VR")

# %%

def get_video_files_from_csvs(csv_directory):
    """
    Reads all CSVs in 'csv_directory', extracts video paths (movie_path column),
    and from the first row of each CSV, the luminance path (luminance column).

    Returns a DataFrame in the already mixed order where each row is:
        - A block start instruction (path, block_num, description="audio_instruction")
        - The mixed videos of that block (path, block_num, description="video")
        - Their respective post_stimulus (verbal or self_report)
    Finally, when finished, adds (if applicable) the instruction and luminance path.
    """

# %%
