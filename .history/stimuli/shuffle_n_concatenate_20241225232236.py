
#%%
import cv2
import numpy as np
import pandas as pd
import ast

def generate_green_intensity_video(subject, id_value, max_duration, output_filename=None):
    """
    Genera un video donde la intensidad del canal verde está determinada por anotaciones continuas.

    Parámetros:
    ----------
    subject (str): Identificador del sujeto (e.g., "02").
    id_value (int): Valor de la columna 'id' para filtrar los datos.
    max_duration (float): Duración máxima del video en segundos (e.g., 30.0).
    output_filename (str, opcional): Nombre del archivo de video de salida.
                                     Si no se proporciona, se generará automáticamente como 'green_intensity_video_<id_value>.mp4'.

    Retorna:
    -------
    None
    """

    # Ruta al archivo de anotaciones
    csv_path = f'../results/sub-{subject}/ses-A/beh/sub-{subject}_ses-A_task-Experiment_VR_non_immersive_beh.csv'
    
    try:
        # Leer datos de anotaciones
        df_beh = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"El archivo CSV no se encontró en la ruta: {csv_path}")
        return
    except pd.errors.EmptyDataError:
        print(f"El archivo CSV está vacío: {csv_path}")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo CSV: {e}")
        return

    # Filtrar la fila donde 'id' es id_value y 'hand' es 'right'
    filtered_beh = df_beh[(df_beh["id"] == id_value) & (df_beh["hand"] == "right")]
    
    # Verificar si se encontró exactamente una fila
    if len(filtered_beh) == 1:
        # Obtener el contenido de 'continuous_annotation'
        continuous_annotation = filtered_beh.iloc[0]["continuous_annotation"]
        
        try:
            # Convertir la cadena a una lista de listas utilizando ast.literal_eval
            annotations = ast.literal_eval(continuous_annotation)
        except (ValueError, SyntaxError) as e:
            print(f"Error al parsear 'continuous_annotation': {e}")
            return
        
        # Crear un DataFrame con las anotaciones
        df_annotations = pd.DataFrame(annotations, columns=["annotation", "time"])
        
        # Limitar la duración del video a max_duration
        actual_duration = min(df_annotations["time"].max(), max_duration)
        
        # Configuración del video
        width, height = 1280, 720  # Resolución del video
        fps = 60  # Frames por segundo
        frames = int(fps * actual_duration)  # Total de frames
        
        # Configurar el nombre del archivo de salida
        if output_filename is None:
            output_filename = f'green_intensity_video_{id_value}.mp4'
        
        # Crear el escritor de video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))
        
        # Interpolar anotaciones a la frecuencia de cuadros
        time_new = np.linspace(0, actual_duration, frames)
        annotations_interp = np.interp(time_new, df_annotations["time"], df_annotations["annotation"])
        
        # Función para escalar la intensidad de verde
        def green_intensity_function(value):
            """
            Escala un valor entre -1 y 1 a una intensidad de verde entre 25 y 255.

            Parámetros:
            ----------
            value (float): Valor de anotación entre -1 y 1.

            Retorna:
            -------
            int: Intensidad de verde escalada entre 25 y 255.
            """
            return int(((value + 1) / 2) * (255 - 25) + 25)
        
        # Generar los frames del video
        for idx, annotation_value in enumerate(annotations_interp):
            # Obtener la intensidad del verde en el frame actual
            green_intensity = green_intensity_function(annotation_value)
        
            # Crear una imagen completamente verde con la intensidad calculada
            green_frame = np.zeros((height, width, 3), dtype=np.uint8)
            green_frame[:, :, 1] = green_intensity  # Canal verde
        
            # Escribir el frame en el archivo de video
            out.write(green_frame)
            
            # Opcional: Mostrar progreso cada 5 segundos
            if (idx + 1) % (fps * 5) == 0 or (idx + 1) == frames:
                progress = (idx + 1) / frames * 100
                print(f"Procesado {idx + 1}/{frames} frames ({progress:.2f}%)")
        
        # Liberar el objeto VideoWriter
        out.release()
        
        print(f"Video generado exitosamente como '{output_filename}' con una duración de {actual_duration:.2f} segundos.")
    
    else:
        if len(filtered_beh) == 0:
            print(f"No se encontró ninguna fila con id={id_value} y hand='right'.")
        else:
            print(f"Se encontraron {len(filtered_beh)} filas con id={id_value} y hand='right'. Se esperaba solo una.")

#%%
# Parámetros principales
subject = "02"
id_values = [1, 3, 7, 9, 12]  # IDs para los cuales se generarán los videos
max_duration = 60.0  # Duración máxima del video en segundos

# Generar videos para cada id_value en la lista
#for id_val in id_values:
#    generate_green_intensity_video(subject, id_val, max_duration)


#%%

def generate_fixation_cross():
    """
    Crea un clip de 5 minutos de duración (300s) consistente en
    una pantalla negra con un signo '+' en el centro.
    
    Retorna
    -------
    CompositeVideoClip
        Un clip compuesto por la pantalla negra y el texto '+'.
    """
    # Duración en segundos (5 minutos = 300s)
    duration_seconds = 300

    # Creamos el clip de pantalla negra con la duración deseada
    black_screen_clip = (
        ColorClip(size=(1280, 720), color=(0, 0, 0))
        .with_duration(duration_seconds)
    )

    font = "C:/Windows/Fonts/arial.ttf"

    # Creamos el TextClip con el signo '+'
    cross_text = (
        TextClip(
            text="+",
            color="white",
            font_size=50,
            font="C:/Windows/Fonts/arial.ttf",
            method='caption',
            size=(1280, 720)  # ensures the textclip has a 1280x720 canvas
        )
        .with_duration(duration_seconds)
        .with_position(('center', 'center'))
    )

    # Generamos la composición del clip (pantalla + texto)
    compo = CompositeVideoClip(
        [black_screen_clip, cross_text],
        size=(1280, 720)  # force the final size
    )

    #compo.write_videofile('fixation_cross.mp4', codec='libx264', audio_codec='aac', fps=60)
    
    return compo

#generate_fixation_cross()

#%%

from moviepy import *
import random
import os
import pandas as pd

def generate_instruction(audio_path):
    """
    Crea un clip de 'pantalla negra' que dura lo mismo que el audio
    y contiene el audio especificado en 'audio_path'.

    Parámetro
    ---------
    audio_path : str
        Ruta al archivo de audio .wav, .mp3, etc.
    
    Retorna
    -------
    ColorClip
        Clip de pantalla negra con la duración y el audio cargado.
    """
    audio_clip = AudioFileClip(audio_path)
    black_screen_clip = (
        ColorClip(size=(1280, 720), color=(0, 0, 0))
        .with_duration(audio_clip.duration)
        .with_audio(audio_clip)
    )
    return black_screen_clip

def generate_practice_videos(modality="2D"):
    """
    Genera un video de práctica concatenando los siguientes elementos:
    1. welcome_and_baseline_audio.wav
    2. fixation_cross (5 minutos)
    3. valence_practice_instruction_audio.wav
    4. Video 1
    5. post_stimulus_self_report_practice.wav
    6. arousal_practice_instructions_audio.wav
    7. Video 2
    8. post_stimulus_self_report.wav
    9. luminance_practice_instructions_audio.wav
    10.luminance video
    11. end_practice.wav

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
    fixation_path           = "./fixation_cross_final.mp4"
    
    # Cargar y redimensionar los videos
    video_1             = VideoFileClip(video_path_1).resized((1280, 720))
    video_2             = VideoFileClip(video_path_2).resized((1280, 720))
    luminance_practice  = VideoFileClip(luminance_path_practice).resized((1280, 720))
    fixation_clip       = VideoFileClip(fixation_path).resized((1280, 720))

    # ---------------------------
    # RUTAS A LOS AUDIOS
    # (TODOS en ./instructions_audios)
    # ---------------------------
    welcome_and_baseline_audio_path          = "./instructions_audios/welcome_and_baseline_audio.wav"
    valence_practice_instruction_audio_path  = "./instructions_audios/valence_practice_instruction_audio.wav"
    post_stimulus_self_report_practice_path  = "./instructions_audios/post_stimulus_self_report_practice.wav"
    arousal_practice_instructions_audio_path = "./instructions_audios/arousal_practice_instructions_audio.wav"
    post_stimulus_self_report_path           = "./instructions_audios/post_stimulus_self_report.wav"  
    luminance_practice_instructions_path     = "./instructions_audios/luminance_practice_instructions_audio.wav"
    end_practice_audio_path                  = "./instructions_audios/end_practice.wav"

    # ---------------------------
    # CREAR CLIPS
    # ---------------------------
    # 1) Clip de bienvenida
    welcome_and_baseline_clip = generate_instruction(welcome_and_baseline_audio_path)
    
    # 2) Pantalla con cruz de fijación durante 5 minutos
    #fixation_clip = generate_fixation_cross()
    
    # 3) Resto de audios en pantallas negras
    valence_practice_clip     = generate_instruction(valence_practice_instruction_audio_path)
    post_stimulus_clip        = generate_instruction(post_stimulus_self_report_practice_path)
    arousal_instructions_clip = generate_instruction(arousal_practice_instructions_audio_path)
    post_stimulus_self_report = generate_instruction(post_stimulus_self_report_path)
    luminance_practice_clip   = generate_instruction(luminance_practice_instructions_path)
    end_practice_clip         = generate_instruction(end_practice_audio_path)

    # ---------------------------
    # DEFINIR EL ORDEN DE CONCATENACIÓN
    # ---------------------------
    clips_in_order = [
        welcome_and_baseline_clip,   # 1
        fixation_clip,               # 2 
        valence_practice_clip,       # 3
        video_1,                     # 4
        post_stimulus_clip,          # 5
        arousal_instructions_clip,   # 6
        video_2,                     # 7
        post_stimulus_self_report,   # 8
        luminance_practice_clip,     # 9
        luminance_practice,          # 10 
        end_practice_clip            # 11
    ]

    for idx, clip in enumerate(clips_in_order):
        # clip.size --> tamaño (width, height)
        # clip.mask  --> la máscara del clip si existe
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
    output_path = f"./practice_videos/{modality}/merged_practice_{modality}_25_12.mp4"
    final_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

# Ejemplo de uso:
#generate_practice_videos("2D")         # Modalidad "2D" por defecto
#generate_practice_videos("VR")     # Modalidad "VR"


#%%

from moviepy import *
import random
import os
import pandas as pd


def resize_clip(clip, target_resolution):
    return clip.resize(target_resolution)

def process_videos(video_paths, output_resolution):
    video_clips = []
    for i, video in enumerate(video_paths):
        try:
            clip = VideoFileClip(video)
            clip = resize_clip(clip, output_resolution)
            video_clips.append(clip)
        except Exception as e:
            print(f"Failed to process video: {video}, Error: {e}")
    return video_clips

def concatenate_videos(video_paths, output_resolution, output_path):
    video_clips = process_videos(video_paths, output_resolution)
    if not video_clips:
        print("No videos processed successfully.")
        return
    
    final_video = concatenate_videoclips(video_clips)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

def get_video_files_from_csvs(csv_directory):
    video_files = []
    block_numbers = []
    video_ids = []
    csv_files = [csv_file for csv_file in os.listdir(csv_directory) if csv_file.endswith('.csv')]
    random.shuffle(csv_files)
    
    for csv_file in csv_files:
        csv_path = os.path.join(csv_directory, csv_file)
        block_number = int(csv_file.split('_')[2])
        video_id = os.path.splitext(csv_file)[0]

        # Leemos y mezclamos el DataFrame
        df = pd.read_csv(csv_path).sample(frac=1).reset_index(drop=True)
        
        # Obtenemos la columna 'movie_path' como lista
        video_paths = df['movie_path'].tolist()

        # Agregamos *inmediatamente* al final el valor de df['luminance'] en la primera fila
        luminosidad_primera_fila = df['luminance'].iloc[0]
        video_paths.append(luminosidad_primera_fila)

        # Extendemos las listas
        video_files.extend(video_paths)
        block_numbers.extend([block_number] * len(video_paths))
        video_ids.extend([video_id] * len(video_paths))
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    video_files = [os.path.abspath(os.path.join(base_dir, path)) for path in video_files]
    
    video_files_df = pd.DataFrame({
        'video_files': video_files,
        'block_number': block_numbers,
        'video_id': video_ids
    })
    return video_files_df

def modify_paths_for_modality(video_list, modality):
    if modality == 'VR':
        new_list = [v.replace('2D', 'VR') for v in video_list]
        return new_list
    elif modality == '2D':
        return video_list
    else:
        return video_list

def generate_videos(Subjects=['06'], Modality=['VR'], sesion=['A'], condition_A=True, condition_B=True , output_resolution=(1280, 720)):
    """
    Ejemplo:
    Subjects = ['01','02']
    Modality = ['VR','both']
    sesion = ['A','B']  # Sujeto '01' = sesion A, Sujeto '02' = sesion B
    """
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(f'{base_dir}/output_videos', exist_ok=True)

    experiment_vr_dir = os.path.dirname(base_dir)
    cond_A_dir = os.path.join(experiment_vr_dir, 'conditions', 'A')
    cond_B_dir = os.path.join(experiment_vr_dir, 'conditions', 'B')

    # Cargar videos según las condiciones
    if condition_A:
        video_files_df_A = get_video_files_from_csvs(cond_A_dir)
        video_files_A = video_files_df_A['video_files'].tolist()
        
    if condition_B:
        video_files_df_B = get_video_files_from_csvs(cond_B_dir)
        video_files_B = video_files_df_B['video_files'].tolist()
    
    # Iterar sobre cada sujeto
    for i, subject in enumerate(Subjects):
        # Obtener la sesión para este sujeto
        subject_sesion = sesion[i]
        
        subject_dir = f'{base_dir}/output_videos/{subject}'
        os.makedirs(subject_dir, exist_ok=True)
        
        # También crear la carpeta en results/sub-{subject}/ses-{sesion}
        results_dir = os.path.join(base_dir, '..', 'results', f'sub-{subject}', f'ses-{subject_sesion}')
        os.makedirs(results_dir, exist_ok=True)

        # order_matrix por sujeto
        order_matrix = pd.DataFrame()

        # Determinar la(s) modalidad(es) a generar
        subject_modality = Modality[i]
        if subject_modality == 'both':
            modalities_to_generate = ['VR', '2D']
        else:
            modalities_to_generate = [subject_modality]

        for actual_modality in modalities_to_generate:
            
            # Generar videos para A
            if condition_A:
                video_files_A_mod = modify_paths_for_modality(video_files_A, actual_modality)
                calm_901_path = f"./calm_videos/{actual_modality}/901.mp4"
                final_list_A = [calm_901_path] + video_files_A_mod
                
                output_file_A = f"{subject_dir}/{subject}_A_{actual_modality}_output_video.mp4"
                concatenate_videos(final_list_A, output_resolution, output_file_A)
                
                df_A = pd.DataFrame({'video_files': final_list_A})
                df_A['Participant'] = subject
                df_A['Block'] = 'A'
                df_A['Orden_de_presentacion'] = range(1, len(final_list_A) + 1)
                df_A['Modality'] = actual_modality
                df_A['Session'] = subject_sesion
                
                df_A = df_A.merge(video_files_df_A, on='video_files', how='left')
                order_matrix = pd.concat([order_matrix, df_A], ignore_index=True)
            
            # Generar videos para B
            if condition_B:
                video_files_B_mod = modify_paths_for_modality(video_files_B, actual_modality)
                calm_902_path = f"./calm_videos/{actual_modality}/902.mp4"
                final_list_B = video_files_B_mod + [calm_902_path]
                
                output_file_B = f"{subject_dir}/{subject}_B_{actual_modality}_output_video.mp4"
                concatenate_videos(final_list_B, output_resolution, output_file_B)
                
                df_B = pd.DataFrame({'video_files': final_list_B})
                df_B['Participant'] = subject
                df_B['Block'] = 'B'
                df_B['Orden_de_presentacion'] = range(1, len(final_list_B) + 1)
                df_B['Modality'] = actual_modality
                df_B['Session'] = subject_sesion
                
                df_B = df_B.merge(video_files_df_B, on='video_files', how='left')
                order_matrix = pd.concat([order_matrix, df_B], ignore_index=True)
        
        # Guardar el order_matrix por sujeto en su carpeta de output_videos
        subject_order_matrix_path = f'{subject_dir}/order_matrix.xlsx'
        order_matrix.to_excel(subject_order_matrix_path, index=False)
        
        # Guardar una copia en ../results/sub-{subject}/ses-{subject_sesion}/
        results_order_matrix_path = os.path.join(results_dir, 'order_matrix.xlsx')
        os.makedirs(os.path.dirname(results_order_matrix_path), exist_ok=True)
        order_matrix.to_excel(results_order_matrix_path, index=False)


#%%
# Ejemplo de llamado:
generate_videos(Subjects= ['04'],  
                 Modality=['VR'], 
                 sesion=['A'],
                 condition_A=True, condition_B=True,)

#%%

