
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

import os
import pandas as pd
import numpy as np
import random
from moviepy import *

def generate_countdown():
    """
    Crea un clip de 30 segundos (30s) que muestra una barra de progreso
    sobre un fondo negro. La barra comienza vacía (en t=0) y se llena
    progresivamente hasta completar todo su ancho (en t=30s).
    
    Además, se dibuja un contorno que muestra la posición máxima que
    alcanzará la barra al finalizar la cuenta.
    """

    duration_seconds = 30
    width, height = 1280, 720
    
    # Dimensiones y ubicación de la barra
    bar_max_width = int(width * 0.05)  # 10% del ancho total
    bar_height = 10
    # Centramos verticalmente
    bar_y1 = (height - bar_height) // 2
    bar_y2 = bar_y1 + bar_height
    # Dejamos 45% de espacio a la izquierda (x1), y la barra crece a la derecha
    bar_x1 = int(width * 0.475)
    # Coordenada final de la barra "completa"
    bar_x1_full = bar_x1 + bar_max_width

    def make_frame(t):
        # Calcula el porcentaje de la barra que se ha "llenado"
        fraction = t / duration_seconds  # valor entre 0 y 1
        current_bar_width = int(bar_max_width * fraction)
        
        # Creamos un fondo negro
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # ------------------ Pintar la parte llena de la barra ------------------
        bar_x2 = bar_x1 + current_bar_width
        # "Pintamos" la parte llena de la barra en color verde (0,255,0)
        frame[bar_y1:bar_y2, bar_x1:bar_x2] = (0, 255, 0)  
        
        # ------------------ Dibujar el contorno "final" de la barra ------------------
        # Top edge
        frame[bar_y1:bar_y1+1, bar_x1:bar_x1_full] = (0, 255, 0)
        # Bottom edge
        frame[bar_y2-1:bar_y2, bar_x1:bar_x1_full] = (0, 255, 0)
        # Left edge
        frame[bar_y1:bar_y2, bar_x1:bar_x1+1] = (0, 255, 0)
        # Right edge
        frame[bar_y1:bar_y2, bar_x1_full-1:bar_x1_full] = (0, 255, 0)

        return frame

    countdown_clip = VideoClip(
        make_frame,
        duration=duration_seconds
    ).with_fps(60)
    
    countdown_clip.write_videofile(
        "countdown_bar.mp4",
        codec='libx264',
        fps=60
    )
    
generate_countdown()



#%%

import os
import pandas as pd
import random
from moviepy import *

def resize_clip(clip, target_resolution):
    return clip.resized(target_resolution)

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
    """
    Lee todos los CSV en 'csv_directory', extrae los paths de videos (columna 'movie_path'),
    y de la primera fila de cada CSV, el path de luminancia (columna 'luminance').

    Devuelve un DataFrame en el orden ya mezclado donde cada fila es:
        - Una instrucción de inicio de bloque (path, block_num, description="audio_instruction")
        - Los videos mezclados de ese bloque (path, block_num, description="video")
        - Su respectivo post_stimulus (verbal o self_report)
    Finalmente, al terminar, añade (si corresponde) la instrucción y el path de luminancia.
    """
    csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
    random.shuffle(csv_files)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    sequence_rows = []

    last_luminance_path = None
    last_luminance_order_emojis = None

    for csv_file in csv_files:
        csv_path = os.path.join(csv_directory, csv_file)
        
        # Ajusta si tu naming real es distinto
        block_number = int(csv_file.split('_')[2])
        block_id_base = os.path.splitext(csv_file)[0]  # Nombre base, sin extensión

        df = pd.read_csv(csv_path).sample(frac=1).reset_index(drop=True)

        # Tomamos la info de la primera fila
        luminance_path = df['luminance'].iloc[0]
        luminance_order_emojis = df['order_emojis_slider'].iloc[0]
        audio_report_condition = df['audio_report'].iloc[0]

        last_luminance_path = luminance_path
        last_luminance_order_emojis = luminance_order_emojis

        # 1) Instrucción de inicio de bloque
        block_start_audio = f"./instructions_videos/block_{block_number}_text.mp4"
        sequence_rows.append({
            "path": block_start_audio,
            "block_num": block_number,
            "description": "audio_instruction"
        })
        
        ii = 0
        # 2) Videos mezclados del bloque y su post_stimulus
        for _, row in df.iterrows():
            # Pre-stim
            if ii > 0:
                stim_start_audio = f"./instructions_videos/block_{block_number}_text_reminder.mp4"
                sequence_rows.append({
                    "path": stim_start_audio,
                    "block_num": block_number,
                    "description": "audio_instruction"
                })
                
            movie_path = row['movie_path']
            dimension = row['dimension']
            order_emojis_slider = row['order_emojis_slider']
            video_id = os.path.splitext(os.path.basename(movie_path))[0]

            sequence_rows.append({
                "path": movie_path,
                "block_num": block_number,
                "dimension": dimension,
                "order_emojis_slider": order_emojis_slider,
                "description": "video",
                "video_id": video_id
            })

            # Post-stim
            if audio_report_condition == 'yes':
                report_path = './instructions_videos/post_stimulus_verbal_report.mp4'
                sequence_rows.append({
                    "path": report_path,
                    "block_num": block_number,
                    "description": "instruction_post_stimulus_verbal_report"
                })
                count_down_30 = './videos_fixation/countdown_bar.mp4'
                sequence_rows.append({
                    "path": count_down_30,
                    "block_num": block_number,
                    "description": "verbal_report"
                })
                
                black_screen_5 = './black_screen_5_sec.mp4'
                sequence_rows.append({
                    "path": black_screen_5,
                    "block_num": block_number,
                    "description": "black_screen_5_seconds"
                })
                
            else:
                report_path = './instructions_videos/post_stimulus_self_report.mp4'
                sequence_rows.append({
                    "path": report_path,
                    "block_num": block_number,
                    "description": "post_stimulus_self_report"
                })
                black_screen_5 = './black_screen_5_sec.mp4'
                sequence_rows.append({
                    "path": black_screen_5,
                    "block_num": block_number,
                    "description": "black_screen_5_seconds"
                })
                
            ii += 1

        # Tras recorrer todos los CSVs, añadimos las instrucciones de luminancia si corresponde
        if last_luminance_path != 'no':
            if last_luminance_order_emojis == 'direct':
                luminance_instructions = "./instructions_videos/luminance_instructions_direct.mp4"
            elif last_luminance_order_emojis == 'inverse':
                luminance_instructions = "./instructions_videos/luminance_instructions_inverse.mp4"
            else:
                luminance_instructions = "./instructions_videos/luminance_instructions_direct.mp4"

            sequence_rows.append({
                "path": luminance_instructions,
                "block_num": None,
                "description": "luminance_instructions"
            })

            sequence_rows.append({
                "path": last_luminance_path,
                "block_num": None,
                "description": "luminance",
                "dimension": "luminance",
                "order_emojis_slider": last_luminance_order_emojis,
            })

    df_final = pd.DataFrame(sequence_rows)
    return df_final


def generate_videos(
    subjects=['06'],
    modality=['VR'],
    sesion_A=True,       # Renombrado en vez de condition_A
    sesion_B=True,       # Renombrado en vez de condition_B
    output_resolution=(1280, 720)
):
    """
    Genera los videos y crea dos order_matrix (uno por cada sesión) si sesion_A y sesion_B son True.
    - 'order_presentation' solo se asigna a los estímulos (./stimuli/exp_videos).
    - Columns: 'participant', 'suprablock', 'order_presentation', 'modality', 'session', ...
    """
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(f'{base_dir}/output_videos', exist_ok=True)

    experiment_vr_dir = os.path.dirname(base_dir)
    cond_A_dir = os.path.join(experiment_vr_dir, 'conditions', 'A')
    cond_B_dir = os.path.join(experiment_vr_dir, 'conditions', 'B')

    # Cargar DF base para A o B (si se piden)
    video_files_df_A = None
    video_files_df_B = None
    if sesion_A:
        video_files_df_A = get_video_files_from_csvs(cond_A_dir)
    if sesion_B:
        video_files_df_B = get_video_files_from_csvs(cond_B_dir)

    # Iterar sobre cada participante
    for i, subject in enumerate(subjects):

        subject_dir = os.path.join(base_dir, "output_videos", subject)
        os.makedirs(subject_dir, exist_ok=True)

        # (Opcional) Podrías tener un directorio de results
        results_dir = os.path.join(
            base_dir, '..', 'results', f'sub-{subject}'
        )
        os.makedirs(results_dir, exist_ok=True)

        # Determinar la(s) modalidad(es) a generar
        subject_modality = modality[i] if i < len(modality) else modality[0]
        if subject_modality == 'both':
            modalities_to_generate = ['VR', '2D']
        else:
            modalities_to_generate = [subject_modality]

        for actual_modality in modalities_to_generate:
            
            # ===================== SESIÓN A =====================
            if sesion_A and video_files_df_A is not None:
                # 1) Modificamos paths (VR <-> 2D)
                df_A_mod = video_files_df_A.copy()
                df_A_mod['path'] = df_A_mod['path'].apply(
                    lambda p: p.replace('2D', actual_modality)
                )

                # 2) Armamos la lista final (como diccionarios)
                initial_relaxation = "./instructions_videos/initial_relaxation_video_text.mp4"
                calm_901_path = f"./calm_videos/{actual_modality}/901.mp4"
                rest_suprablock = "./instructions_videos/rest_suprablock_text.mp4"

                final_list_A = [
                    {
                        "path": initial_relaxation,
                        "block_num": None,
                        "description": "initial_relaxation"
                    },
                    {
                        "path": calm_901_path,
                        "block_num": None,
                        "description": "calm_901"
                    }
                ]
                # Extendemos con lo que vino de CSV
                final_list_A.extend(df_A_mod.to_dict('records'))
                # Añadimos la pausa final
                final_list_A.append({
                    "path": rest_suprablock,
                    "block_num": None,
                    "description": "rest_suprablock"
                })

                # 3) Convertimos a DataFrame
                df_A = pd.DataFrame(final_list_A)

                # 4) Asignamos columns fijas:
                df_A['participant'] = subject
                #df_A['suprablock'] = 'A'  # O "sesion_A", como prefieras
                df_A['modality'] = actual_modality
                df_A['session'] = 'A'    # Para que sea claro que es la sesión "A"

                # 5) Asignar 'order_presentation' solo a los estímulos
                #    Por ejemplo, contando videos de la carpeta ./stimuli/exp_videos
                counter_A = 0
                for idx, row in df_A.iterrows():
                    if "./stimuli/exp_videos" in row['path']:
                        counter_A += 1
                        df_A.at[idx, 'order_presentation'] = counter_A
                    else:
                        df_A.at[idx, 'order_presentation'] = None

                # 6) Reordenar columnas
                # Queremos que vayan primero: participant, suprablock, order_presentation, modality, session
                desired_order = [
                    'participant', 
                    'session', 
                    'modality', 
                    'order_presentation', 
                    'video_id'
                ]
                other_cols = [c for c in df_A.columns if c not in desired_order]
                df_A = df_A[desired_order + other_cols]

                # 7) Concatenar videos en un solo .mp4
                output_file_A = os.path.join(subject_dir, f"{subject}_A_{actual_modality}_output_video.mp4")
                paths_for_A = [item['path'] for item in final_list_A]
                #concatenate_videos(paths_for_A, output_resolution, output_file_A)

                # 8) Guardar order_matrix para la sesión A
                order_matrix_A_path = os.path.join(subject_dir, f"order_matrix_{subject}_A_{actual_modality}.xlsx")
                df_A.to_excel(order_matrix_A_path, index=False)

                # (Opcional) copia en results
                results_order_matrix_A_path = os.path.join(results_dir, f"order_matrix_{subject}_A_{actual_modality}.xlsx")
                df_A.to_excel(results_order_matrix_A_path, index=False)


            # ===================== SESIÓN B =====================
            if sesion_B and video_files_df_B is not None:
                # 1) Modificar paths
                df_B_mod = video_files_df_B.copy()
                df_B_mod['path'] = df_B_mod['path'].apply(
                    lambda p: p.replace('2D', actual_modality)
                )

                # 2) Secuencia
                final_relaxation = "./instructions_videos/final_relaxation_video_audio.mp4"
                calm_902_path = f"./calm_videos/{actual_modality}/902.mp4"
                experiment_end_task = "./instructions_videos/experiment_end_text.mp4"

                final_list_B = df_B_mod.to_dict('records')
                final_list_B.append({
                    "path": final_relaxation,
                    "block_num": None,
                    "description": "final_relaxation"
                })
                final_list_B.append({
                    "path": calm_902_path,
                    "block_num": None,
                    "description": "calm_902"
                })
                final_list_B.append({
                    "path": experiment_end_task,
                    "block_num": None,
                    "description": "experiment_end_task"
                })

                df_B = pd.DataFrame(final_list_B)

                # 3) Asignar columnas fijas
                df_B['participant'] = subject
                #df_B['suprablock'] = 'B'
                df_B['modality'] = actual_modality
                df_B['session'] = 'B'

                # 4) Asignar order_presentation solo para ./stimuli/exp_videos
                counter_B = 0
                for idx, row in df_B.iterrows():
                    if "./stimuli/exp_videos" in row['path']:
                        counter_B += 1
                        df_B.at[idx, 'order_presentation'] = counter_B
                    else:
                        df_B.at[idx, 'order_presentation'] = None

                # 5) Reordenar columnas
                desired_order = [
                    'participant', 
                    'session',
                    'modality', 
                    'order_presentation', 
                    'video_id',
                    'dimension',
                    'order_emojis_slider'
                ]
                other_cols = [c for c in df_B.columns if c not in desired_order]
                df_B = df_B[desired_order + other_cols]

                # 6) Concatenar videos
                output_file_B = os.path.join(subject_dir, f"{subject}_B_{actual_modality}_output_video.mp4")
                paths_for_B = [item['path'] for item in final_list_B]
                #concatenate_videos(paths_for_B, output_resolution, output_file_B)

                # 7) Guardar order_matrix en un archivo aparte
                order_matrix_B_path = os.path.join(subject_dir, f"order_matrix_{subject}_B_{actual_modality}.xlsx")
                df_B.to_excel(order_matrix_B_path, index=False)

                # (Opcional) copia en results
                results_order_matrix_B_path = os.path.join(results_dir, f"order_matrix_{subject}_B_{actual_modality}.xlsx")
                df_B.to_excel(results_order_matrix_B_path, index=False)

#%%
# Ejemplo de uso (solo si deseas llamarla directamente):
generate_videos(
    subjects=['07'],
    modality=['VR'],
    sesion_A=True,
    sesion_B=True
)

# %%
