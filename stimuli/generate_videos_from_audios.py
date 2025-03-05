#%%
import os
import pandas as pd
import random
from moviepy import *
import concurrent.futures
from pydub import AudioSegment
import concurrent.futures

def convert_m4a_to_wav(input_dir, output_dir=None, max_workers=8):
    """
    Convierte todos los archivos .m4a en un directorio a formato .wav.
    
    Parámetros
    ----------
    input_dir : str
        Directorio que contiene los archivos .m4a a convertir.
    output_dir : str, opcional
        Directorio donde se guardarán los archivos .wav convertidos.
        Si es None, se guardarán en el mismo directorio de entrada.
    max_workers : int, opcional
        Número máximo de hilos paralelos a utilizar. Por defecto es 8.
    
    Ejemplo de uso
    --------------
    convert_m4a_to_wav(
        input_dir='./instructions_audios/m4a_files',
        output_dir='./instructions_audios/wav_files',
        max_workers=8
    )
    """
    # Verificar si el directorio de entrada existe
    if not os.path.isdir(input_dir):
        raise ValueError(f"El directorio de entrada '{input_dir}' no existe.")
    
    # Si no se especifica un directorio de salida, usar el mismo que el de entrada
    if output_dir is None:
        output_dir = input_dir
    else:
        # Crear el directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
    
    # Listar todos los archivos .m4a en el directorio de entrada
    m4a_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.m4a')]
    
    if not m4a_files:
        print(f"No se encontraron archivos .m4a en el directorio '{input_dir}'.")
        return
    
    print(f"Convirtiendo {len(m4a_files)} archivos .m4a a .wav con {max_workers} trabajadores paralelos...")
    
    def process_m4a_file(m4a_file):
        """Procesa un único archivo m4a y lo convierte a wav."""
        try:
            input_path = os.path.join(input_dir, m4a_file)
            base_name = os.path.splitext(m4a_file)[0]
            output_path = os.path.join(output_dir, f"{base_name}.wav")
            
            # Cargar el archivo m4a y exportarlo como wav
            audio = AudioSegment.from_file(input_path, format="m4a")
            audio.export(output_path, format="wav")
            
            return f"Convertido: {m4a_file} -> {os.path.basename(output_path)}"
        except Exception as e:
            return f"Error al convertir '{m4a_file}': {e}"
    
    # Utilizar ThreadPoolExecutor para procesar archivos en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_m4a_file, m4a_file) for m4a_file in m4a_files]
        
        for future in concurrent.futures.as_completed(futures):
            try:
                print(future.result())
            except Exception as e:
                print(f"Error en el procesamiento: {e}")
    
    print("Conversión completada.")

# Ejecutar la función con las carpetas especificadas
#convert_m4a_to_wav(
#    input_dir='./instructions_audios/audio_files/old',
#    output_dir='./instructions_audios/audio_files/new',
#    max_workers=8
#)
#%%
def generate_instruction(audio_path):
    """
    Pantalla negra con duración igual al audio + el audio embebido.
    """
    audio_clip = AudioFileClip(audio_path)
    image_clip = (
        ImageClip('./instruction_frame.jpg')
        .with_duration(audio_clip.duration)
        .with_audio(audio_clip)
    )
    return image_clip

def process_audio_file(audio_file, input_dir, output_dir):
    """
    Procesa un único archivo de audio y genera el video correspondiente.
    
    Parámetros
    ----------
    audio_file : str
        Nombre del archivo de audio a procesar.
    input_dir : str
        Directorio que contiene los archivos de audio.
    output_dir : str
        Directorio donde se guardarán los videos generados.
    
    Returns
    -------
    str
        Mensaje indicando el resultado del procesamiento.
    """
    input_audio_path = os.path.join(input_dir, audio_file)
    base_name = os.path.splitext(audio_file)[0]
    output_video_path = os.path.join(output_dir, f"{base_name}.mp4")
    
    try:
        # Generar el clip de video utilizando la función existente
        video_clip = generate_instruction(input_audio_path)
        
        # Escribir el video al directorio de salida con configuración optimizada
        video_clip.write_videofile(
            output_video_path,
            codec="libx264",
            audio_codec="aac",
            fps=1,  # Reducido de 60 a 1 fps
            bitrate="1000k",  # Bitrate fijo para video
            audio_bitrate="128k"  # Bitrate fijo para audio
        )
        
        # Cerrar los clips para liberar recursos
        video_clip.close()
        return f"Video generado: {output_video_path}"
    
    except Exception as e:
        return f"Error al procesar '{input_audio_path}': {e}"

def generate_instruction_videos(input_dir, output_dir, max_workers=8):
    """
    Genera videos .mp4 a partir de archivos de audio .wav en un directorio especificado.
    Cada video consiste en una pantalla negra con la duración del audio y el audio incorporado.
    Utiliza paralelización para procesar múltiples archivos simultáneamente.

    Parámetros
    ----------
    input_dir : str
        Directorio que contiene los archivos de audio .wav.
    output_dir : str
        Directorio donde se guardarán los archivos de video .mp4 resultantes.
        Si no existe, se creará automáticamente.
    max_workers : int, opcional
        Número máximo de hilos paralelos a utilizar. Por defecto es 8.

    Ejemplo de uso
    --------------
    generate_instruction_videos(
        input_dir='./instructions_audios',
        output_dir='./instructions_videos',
        max_workers=8
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
    
    print(f"Procesando {len(audio_files)} archivos de audio con {max_workers} trabajadores paralelos...")
    
    # Utilizar ThreadPoolExecutor en lugar de ProcessPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Crear una lista de futuros
        futures = [
            executor.submit(process_audio_file, audio_file, input_dir, output_dir)
            for audio_file in audio_files
        ]
        
        # Procesar los resultados a medida que se completan
        for future in concurrent.futures.as_completed(futures):
            try:
                print(future.result())
            except Exception as e:
                print(f"Error en el procesamiento: {e}")
    
    print("Procesamiento completado.")

#%%

generate_instruction_videos(input_dir='./instructions_audios/new_audio', output_dir='./instructions_videos/new_video')
# %%
