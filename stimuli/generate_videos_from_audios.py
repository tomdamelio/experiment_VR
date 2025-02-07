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

generate_instruction_videos(input_dir='./stimuli/instructions_audios/new_audio', output_dir='./stimuli/instructions_videos/new_video')