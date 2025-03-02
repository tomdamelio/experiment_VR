# %%
import pandas as pd
import os
import subprocess
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError

#%%
# Cargar el DataFrame desde un archivo Excel
df = pd.read_excel("df_with_validity_checks_2024_Tomi_selected_practice.xlsx")

# %%

def download_and_encode_videos(df):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "practice_videos")
    os.makedirs(output_dir, exist_ok=True)

    for index, row in df.iterrows():
        if row["Practice_video"] == "yes":
            yt = YouTube(row["link"], use_oauth=True, allow_oauth_cache=True)
            print(f"Downloading {row['Title']} with id {row['id']}...")
            # Download entire video
            for n, stream in enumerate(yt.streams):
                file_extension = stream.mime_type.split("/")[1]
                raw_output_file = os.path.join(
                    output_dir, f"{row['id']}_{row['Title']}-{n}_raw.{file_extension}"
                )
                encoded_output_file = os.path.join(
                    output_dir, f"{row['id']}_{row['Title']}-{n}.{file_extension}"
                )
                stream.download(filename=raw_output_file)
                # Re-encode the video using FFmpeg
                try:
                    subprocess.run(
                        [
                            "ffmpeg",
                            "-i",
                            raw_output_file,
                            "-c:v",
                            "libx264",
                            "-preset",
                            "medium",
                            "-c:a",
                            "aac",
                            "-strict",
                            "experimental",
                            "-b:a",
                            "192k",
                            "-y",
                            encoded_output_file,
                        ],
                        check=True,
                    )
                    os.remove(
                        raw_output_file
                    )  # Remove the original download if re-encoding is successful
                except subprocess.CalledProcessError:
                    print(f"Error re-encoding {row['Title']}.")
                print(f"Downloaded and re-encoded {row['Title']}.")


# %%
download_and_encode_videos(df)

# %%
import pandas as pd
import os
import subprocess
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError

def descargar_video_youtube(url, directorio=None):
    """
    Descarga un video de YouTube a partir de su URL y lo recodifica usando FFmpeg.
    
    Args:
        url (str): URL del video de YouTube
        directorio (str, optional): Directorio donde guardar el video. 
                                   Si es None, se guarda en el directorio actual.
    
    Returns:
        str: Ruta del archivo descargado o None si hubo un error
    """
    if directorio is None:
        directorio = os.getcwd()  # Directorio actual si no se especifica
    
    try:
        # Crear objeto YouTube con opciones adicionales para evitar el error 403
        yt = YouTube(
            url,
            use_oauth=True,
            allow_oauth_cache=True,
            # Añadir un encabezado de usuario para simular un navegador
            on_progress_callback=lambda stream, chunk, bytes_remaining: None
        )
        
        # Obtener el stream con mejor resolución
        stream = yt.streams.get_highest_resolution()
        
        if not stream:
            print("No se encontraron streams disponibles. Intentando con otro método...")
            stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
            
        if not stream:
            print("No se pudo encontrar ningún stream para descargar.")
            return None
            
        # Generar nombres de archivos
        nombre_base = f"{yt.title.replace(' ', '_').replace('/', '_').replace(':', '-')}"
        archivo_temporal = os.path.join(directorio, f"{nombre_base}_raw.mp4")
        archivo_final = os.path.join(directorio, f"{nombre_base}.mp4")
        
        print(f"Descargando: {yt.title}")
        print(f"Duración: {yt.length} segundos")
        print(f"Stream seleccionado: {stream.resolution}, {stream.mime_type}")
        
        # Descargar el video en archivo temporal
        stream.download(output_path=directorio, filename=f"{nombre_base}_raw.mp4")
        
        # Recodificar el video usando FFmpeg
        print("Recodificando el video con FFmpeg...")
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    archivo_temporal,
                    "-c:v",
                    "libx264",
                    "-preset",
                    "medium",
                    "-c:a",
                    "aac",
                    "-strict",
                    "experimental",
                    "-b:a",
                    "192k",
                    "-y",
                    archivo_final,
                ],
                check=True,
            )
            # Eliminar el archivo temporal si la recodificación fue exitosa
            os.remove(archivo_temporal)
            print(f"Video descargado y recodificado exitosamente en: {archivo_final}")
            return archivo_final
        except subprocess.CalledProcessError:
            print("Error al recodificar el video con FFmpeg.")
            print("Manteniendo el archivo original descargado.")
            return archivo_temporal
        
    except AgeRestrictedError:
        print("Error: El video tiene restricción de edad")
        return None
    except Exception as e:
        print(f"Error al descargar el video: {str(e)}")
        print("Intentando método alternativo con yt-dlp...")
        
        # Método alternativo usando yt-dlp (necesita estar instalado: pip install yt-dlp)
        try:
            import yt_dlp
            
            nombre_base = url.split("=")[-1]
            archivo_final = os.path.join(directorio, f"{nombre_base}.mp4")
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': archivo_final,
                'quiet': False,
                'no_warnings': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            print(f"Video descargado exitosamente con yt-dlp en: {archivo_final}")
            return archivo_final
        except Exception as e2:
            print(f"Error también con el método alternativo: {str(e2)}")
            return None

#%%

# Ejemplo de uso:
descargar_video_youtube("https://www.youtube.com/watch?v=AiVpdGIPgOw")

# %%
