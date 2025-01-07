
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
        ColorClip(size=(1280, 720), color=(0, 0, 0))
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
        raise ValueError(f"El directorio de entrada '{input_dir}' no existe.")
    
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

generate_instruction_videos(input_dir='./instructions_audios', output_dir='./instructions_videos')


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
#duration_sec = 1
#sample_rate, whistle_signal = generate_whistle_sound(duration_sec)

# Save whistle sound to file
#write("whistle_sound.wav", sample_rate, whistle_signal)



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

create_black_screen_video(30, "black_screen_30_sec.mp4", width=1280, height=720)

#%%

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

#%%

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

#%%

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


#%%

def process_videos_in_folder(modality="2D"):
    folder_path = f"videos_{modality}"
    # Crea la carpeta de salida si no existe
    output_folder = f'final_videos_{modality}'
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith((".mp4", ".avi", ".mov")):
            print("Processing video:", filename)

            video_path = os.path.join(folder_path, filename)
            video = cv2.VideoCapture(video_path)
            width_vid = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height_vid = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Crear flicker 1 seg con audio
            #create_flicker_screen_video(1, "flicker_1_sec.mp4", width=width_vid, height=height_vid)
            #add_audio_to_video("flicker_1_sec.mp4", "whistle_sound.wav", "flicker_1_sec_with_audio.mp4")

            # Crear flicker 1 seg final con audio
            #create_flicker_screen_video(1, "flicker_1_sec_final.mp4", width=width_vid, height=height_vid)
            #add_audio_to_video("flicker_1_sec_final.mp4", "whistle_sound.wav", "flicker_1_sec_final_with_audio.mp4")

            # Crear black screen 2 and 7 sec
            #create_black_screen_video(2, "black_screen_2_sec.mp4", width=width_vid, height=height_vid)
            #create_black_screen_video(5, "black_screen_5_sec.mp4", width=width_vid, height=height_vid)

            # Clips de entrada
            black_2_clip = VideoFileClip("black_screen_2_sec.mp4") 
            flicker_1_clip = VideoFileClip("flicker_1_sec_with_audio.mp4")
            original_clip = VideoFileClip(video_path)
            flicker_1_final_clip = VideoFileClip("flicker_1_sec_final_with_audio.mp4")
            black_5_clip = VideoFileClip("black_screen_5_sec.mp4")
            black_30_clip = VideoFileClip("black_screen_30_sec.mp4")
            
            # Seleccionar el último clip según el filename
            if filename == "6_post_stimulus_self_report_practice.mp4":
                last_clip = black_5_clip
            elif filename == "7_post_stimulus_self_report.mp4":
                last_clip = black_30_clip
            else:
                last_clip = black_2_clip

            # Construir la concatenación final
            final_clip = concatenate_videoclips([
                black_2_clip, 
                flicker_1_clip, 
                original_clip, 
                flicker_1_final_clip, 
                last_clip
            ])

            # Guardar el video final
            output_path = os.path.join(output_folder, filename)
            final_clip.write_videofile(
                output_path, 
                codec='libx264',
                audio_codec='aac',
                fps=60
            )

            # Cerrar los VideoFileClips para liberar recursos
            black_2_clip.close()
            flicker_1_clip.close()
            original_clip.close()
            flicker_1_final_clip.close()
            black_5_clip.close()
            black_30_clip.close()
            final_clip.close()
            


            


#%%
process_videos_in_folder(modality='2D')

#%%
process_videos_in_folder(modality='VR')
#%%
process_videos_in_folder(modality='luminance')

# %%
process_videos_in_folder(modality='fixation')
# %%
