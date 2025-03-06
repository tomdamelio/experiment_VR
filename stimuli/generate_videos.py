#%%
import cv2
import numpy as np
import pandas as pd
import ast
import os
import random
from moviepy import *
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import threading
import time
from datetime import datetime
#%%

# Obtener el directorio del script actual
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Crear directorios necesarios
os.makedirs('./videos_fixation', exist_ok=True)
os.makedirs('./videos_luminance', exist_ok=True)

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
        print(f"The CSV file was not found at the path: {csv_path}")
        return
    except pd.errors.EmptyDataError:
        print(f"The CSV file is empty: {csv_path}")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
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
            print(f"Error parsing 'continuous_annotation': {e}")
            return
        
        # Crear un DataFrame con las anotaciones
        df_annotations = pd.DataFrame(annotations, columns=["annotation", "time"])
        
        # Limitar la duración del video a max_duration
        actual_duration = min(df_annotations["time"].max(), max_duration)
        
        # Configuración del video
        width, height = 3840, 2048  # Resolución del video
        fps = 60  # Frames por segundo
        frames = int(fps * actual_duration)  # Total de frames
        
        # Configurar el nombre del archivo de salida
        if output_filename is None:
            output_filename = f'./videos_luminance/green_intensity_video_{id_value}.mp4'
        
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
                print(f"Processed {idx + 1}/{frames} frames ({progress:.2f}%)")
        
        # Liberar el objeto VideoWriter
        out.release()
        
        print(f"Video generated successfully as '{output_filename}' with a duration of {actual_duration:.2f} seconds.")
    
    else:
        if len(filtered_beh) == 0:
            print(f"No row found with id={id_value} and hand='right'.")
        else:
            print(f"Found {len(filtered_beh)} rows with id={id_value} and hand='right'. Expected only one.")

#%%
# Parámetros principales
#subject = "02"
#id_values = [1, 3, 7, 9, 12]  # IDs para los cuales se generarán los videos
#max_duration = 60.0  # Duración máxima del video en segundos
#
## Generar videos para cada id_value en la lista
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
        ColorClip(size=(3840, 2048), color=(0, 0, 0))
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
            size=(3840, 2048)  # ensures the textclip has a 1280x720 canvas
        )
        .with_duration(duration_seconds)
        .with_position(('center', 'center'))
    )

    # Generamos la composición del clip (pantalla + texto)
    compo = CompositeVideoClip(
        [black_screen_clip, cross_text],
        size=(3840, 2048)  # force the final size
    )

    compo.write_videofile('./videos_fixation/fixation_cross.mp4', codec='libx264', audio_codec='aac', fps=60)
    
    return compo

#generate_fixation_cross()

#%%

def generate_countdown():
    """
    Crea un clip de 45 segundos (45s) que muestra una barra de progreso
    sobre un fondo negro. La barra comienza vacía (en t=0) y se llena
    progresivamente hasta completar todo su ancho (en t=45s).
    
    Además, se dibuja un contorno que muestra la posición máxima que
    alcanzará la barra al finalizar la cuenta.
    """

    duration_seconds = 45
    width, height = 3840, 2048
    
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
        "./videos_fixation/countdown_bar.mp4",
        codec='libx264',
        fps=60
    )
    
#generate_countdown()



#%%

def resize_clip(clip, target_resolution):
    return clip.resized(target_resolution)

def process_videos(video_paths, output_resolution):
    video_clips = []
    for video in video_paths:
        # Si el path no es absoluto, convertirlo
        if not os.path.isabs(video):
            video = os.path.join(SCRIPT_DIR, video)
        try:
            clip = VideoFileClip(video)
            clip = clip.resized(output_resolution)
            video_clips.append(clip)
        except Exception as e:
            print(f"Error processing video {video}: {e}")
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
    suprablock_count = 1

    for block_order, csv_file in enumerate(csv_files):
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
            "block_order": block_order,
            "suprablock_count": suprablock_count,
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
                    "block_order": block_order,
                    "suprablock_count": suprablock_count,
                    "description": "audio_instruction"
                })
                
            movie_path = row['movie_path']
            dimension = row['dimension']
            order_emojis_slider = row['order_emojis_slider']
            video_id = os.path.splitext(os.path.basename(movie_path))[0]

            sequence_rows.append({
                "path": movie_path,
                "block_num": block_number,
                "block_order": block_order,
                "suprablock_count": suprablock_count,
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
                    "block_order": block_order,
                    "suprablock_count": suprablock_count,
                    "description": "instruction_post_stimulus_verbal_report"
                })
                count_down_30 = './videos_fixation/countdown_bar.mp4'
                sequence_rows.append({
                    "path": count_down_30,
                    "block_num": block_number,
                    "block_order": block_order,
                    "suprablock_count": suprablock_count,
                    "description": "verbal_report"
                })

                confidence_verbal_report_instructions_text_path = "./instructions_videos/confidence_verbal_report_text.mp4"
                sequence_rows.append({
                    "path": confidence_verbal_report_instructions_text_path,
                    "block_num": block_number,
                    "block_order": block_order,
                    "suprablock_count": suprablock_count,
                    "description": "confidence_verbal_report"
                })
                
                sequence_rows.append({
                    "path": './instructions_videos/mareo.mp4',
                    "block_num": block_number,
                    "block_order": block_order,
                    "suprablock_count": suprablock_count,
                    "description": "motion_sickness"
                })
                
            else:
                report_path = './instructions_videos/post_stimulus_self_report.mp4'
                sequence_rows.append({  
                    "path": report_path,
                    "block_num": block_number,
                    "block_order": block_order,
                    "suprablock_count": suprablock_count,
                    "description": "post_stimulus_self_report"
                })

                sequence_rows.append({
                    "path": './instructions_videos/mareo.mp4',
                    "block_num": block_number,
                    "block_order": block_order,
                    "suprablock_count": suprablock_count,
                    "description": "motion_sickness"
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
                "block_order": block_order,
                "suprablock_count": suprablock_count,
                "description": "luminance_instructions"
            })

            sequence_rows.append({
                "path": last_luminance_path,
                "block_num": None,
                "block_order": block_order,
                "suprablock_count": suprablock_count,
                "description": "luminance",
                "dimension": "luminance",
                "order_emojis_slider": last_luminance_order_emojis,
            })

            sequence_rows.append({
                "path": "./instructions_videos/confidence_luminance_practice_instructions_text.mp4",
                "block_num": None,
                "block_order": block_order,
                "suprablock_count": suprablock_count,
                "description": "confidence_luminance_instructions"
            })

        # Agregar pausa de descanso después de procesar los dos primeros archivos CSV
        if block_order == 1:
            sequence_rows.append({
                "path": "./instructions_videos/rest_suprablock_text.mp4",
                "block_num": None,
                "block_order": block_order,
                "suprablock_count": suprablock_count,
                "description": "rest_suprablock"
            })
            suprablock_count += 1

    # Mover esta línea fuera del bucle para que procese todos los bloques
    df_final = pd.DataFrame(sequence_rows)
    return df_final

def process_session(session_params):
    """
    Procesa una sesión individual
    """
    subject, actual_modality, session, df_session, subject_dir, results_dir, test = session_params
    
    thread_id = threading.current_thread().name
    start_time = datetime.now()
    print(f"\n[{start_time}] Iniciando sesión {session} en thread {thread_id}")
    
    # Determinar si es bloque 1 o bloque 2
    is_block1 = 'block1' in session
    is_block2 = 'block2' in session
    
    # Iniciar la lista con elementos específicos según el bloque
    final_list = []
    
    # Elementos específicos para el bloque 1
    if is_block1:
        initial_relaxation = "./instructions_videos/initial_relaxation_video_text.mp4"
        calm_video_path_initial = f"./calm_videos/{actual_modality}/901.mp4"
        
        final_list.extend([
            {
                "path": initial_relaxation,
                "block_num": None,
                "block_order": 0,
                "suprablock_count": 1,
                "description": "initial_relaxation"
            },
            {
                "path": calm_video_path_initial,
                "block_num": None,
                "block_order": 0,
                "suprablock_count": 1,
                "description": "calm_901"
            }
        ])
    
    # Añadir los elementos específicos de la sesión (contenido principal)
    final_list.extend(df_session.to_dict('records'))
    
    # Elementos específicos para el bloque 2
    if is_block2:
        final_relaxation = "./instructions_videos/final_relaxation_video_text.mp4"
        calm_video_path_final = f"./calm_videos/{actual_modality}/902.mp4"
        
        final_list.extend([
            {
                "path": final_relaxation,
                "block_num": None,
                "block_order": 4,
                "suprablock_count": 2,
                "description": "final_relaxation"
            },
            {
                "path": calm_video_path_final,
                "block_num": None,
                "block_order": 4,
                "suprablock_count": 2,
                "description": "calm_902"
            },
            {
                "path": "./instructions_videos/experiment_end_text.mp4",
                "block_num": None,
                "block_order": 4,
                "suprablock_count": 2,
                "description": "experiment_end_task"
            }
        ])

    # Crear DataFrame y procesar
    df = pd.DataFrame(final_list)
    df['participant'] = subject
    df['modality'] = actual_modality
    df['session'] = session

    # Asignar order_presentation
    counter = 0
    for idx, row in df.iterrows():
        if isinstance(row['path'], str) and "./stimuli/exp_videos" in row['path']:
            counter += 1
            df.at[idx, 'order_presentation'] = counter
        else:
            df.at[idx, 'order_presentation'] = None

    # Reordenar columnas
    desired_order = [
        'participant', 
        'session',
        'modality', 
        'order_presentation', 
        'video_id',
        'dimension',
        'order_emojis_slider'
    ]
    other_cols = [c for c in df.columns if c not in desired_order]
    df = df[desired_order + other_cols]

    # Concatenar videos solo si no estamos en modo test
    if not test:
        output_file = os.path.join(subject_dir, f"{subject}_{session}_{actual_modality}_output_video.mp4")
        paths = [item['path'] for item in final_list]
        concatenate_videos(paths, (3840, 2048), output_file)
    else:
        print(f"[MODO TEST] Omitiendo generación de video para {subject}_{session}_{actual_modality}")

    # Asegurarse de que los directorios existen
    os.makedirs(subject_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    try:
        # Guardar order_matrix en subject_dir
        order_matrix_path = os.path.join(subject_dir, f"order_matrix_{subject}_{session}_{actual_modality}.xlsx")
        df.to_excel(order_matrix_path, index=False)
        print(f"Archivo Excel guardado en: {order_matrix_path}")
        
        # Guardar en results_dir
        results_order_matrix_path = os.path.join(results_dir, f"order_matrix_{subject}_{session}_{actual_modality}.xlsx")
        df.to_excel(results_order_matrix_path, index=False)
        print(f"Archivo Excel guardado en: {results_order_matrix_path}")
    except Exception as e:
        print(f"Error al guardar archivos Excel: {e}")

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"[{end_time}] Finalizada sesión {session} en thread {thread_id}")
    print(f"Duración total de sesión {session}: {duration}")

def generate_videos(
    subjects=['06'],
    modality=['VR'],
    sesion_A=True,
    sesion_B=True,
    output_resolution=(3840, 2048),
    test=False
):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(f'{base_dir}/output_videos', exist_ok=True)

    experiment_vr_dir = os.path.dirname(base_dir)
    cond_A_dir = os.path.join(experiment_vr_dir, 'conditions', 'A')
    cond_B_dir = os.path.join(experiment_vr_dir, 'conditions', 'B')

    # Cargar DFs base
    video_files_df_A = get_video_files_from_csvs(cond_A_dir) if sesion_A else None
    video_files_df_B = get_video_files_from_csvs(cond_B_dir) if sesion_B else None

    # Imprimir información de diagnóstico
    if video_files_df_A is not None:
        print(f"DataFrame A: {len(video_files_df_A)} filas")
        print(f"Valores únicos de suprablock_count en A: {video_files_df_A['suprablock_count'].unique()}")
    
    if video_files_df_B is not None:
        print(f"DataFrame B: {len(video_files_df_B)} filas")
        print(f"Valores únicos de suprablock_count en B: {video_files_df_B['suprablock_count'].unique()}")

    for i, subject in enumerate(subjects):
        subject_dir = os.path.join(base_dir, "output_videos", subject)
        os.makedirs(subject_dir, exist_ok=True)

        results_dir = os.path.join(base_dir, '..', 'results', f'sub-{subject}')
        os.makedirs(results_dir, exist_ok=True)

        subject_modality = modality[i] if i < len(modality) else modality[0]
        modalities_to_generate = ['VR', '2D'] if subject_modality == 'both' else [subject_modality]

        for actual_modality in modalities_to_generate:
            print(f"\nProcesando modalidad: {actual_modality}")
            if test:
                print(f"[MODO TEST] Solo se generarán archivos .xlsx, no videos")
                
            session_params = []
            
            if sesion_A and video_files_df_A is not None:
                df_A_mod = video_files_df_A.copy()
                df_A_mod['path'] = df_A_mod['path'].apply(lambda p: p.replace('2D', actual_modality) if isinstance(p, str) else p)
                
                # Verificar si hay datos para ambos bloques
                suprablock_values = df_A_mod['suprablock_count'].unique()
                print(f"Valores de suprablock en sesión A: {suprablock_values}")
                
                # Separar en dos bloques
                df_A_block1 = df_A_mod[df_A_mod['suprablock_count'] == 1].copy() if 1 in suprablock_values else pd.DataFrame()
                df_A_block2 = df_A_mod[df_A_mod['suprablock_count'] == 2].copy() if 2 in suprablock_values else pd.DataFrame()
                
                print(f"Sesión A - Bloque 1: {len(df_A_block1)} filas")
                print(f"Sesión A - Bloque 2: {len(df_A_block2)} filas")
                
                if not df_A_block1.empty:
                    session_params.append((subject, actual_modality, 'A_block1', df_A_block1, subject_dir, results_dir, test))
                if not df_A_block2.empty:
                    session_params.append((subject, actual_modality, 'A_block2', df_A_block2, subject_dir, results_dir, test))
            
            if sesion_B and video_files_df_B is not None:
                df_B_mod = video_files_df_B.copy()
                df_B_mod['path'] = df_B_mod['path'].apply(lambda p: p.replace('2D', actual_modality) if isinstance(p, str) else p)
                
                # Verificar si hay datos para ambos bloques
                suprablock_values = df_B_mod['suprablock_count'].unique()
                print(f"Valores de suprablock en sesión B: {suprablock_values}")
                
                # Separar en dos bloques
                df_B_block1 = df_B_mod[df_B_mod['suprablock_count'] == 1].copy() if 1 in suprablock_values else pd.DataFrame()
                df_B_block2 = df_B_mod[df_B_mod['suprablock_count'] == 2].copy() if 2 in suprablock_values else pd.DataFrame()
                
                print(f"Sesión B - Bloque 1: {len(df_B_block1)} filas")
                print(f"Sesión B - Bloque 2: {len(df_B_block2)} filas")
                
                if not df_B_block1.empty:
                    session_params.append((subject, actual_modality, 'B_block1', df_B_block1, subject_dir, results_dir, test))
                if not df_B_block2.empty:
                    session_params.append((subject, actual_modality, 'B_block2', df_B_block2, subject_dir, results_dir, test))

            print(f"Iniciando procesamiento paralelo de {len(session_params)} bloques...")
            
            start_time_total = datetime.now()
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(process_session, params) for params in session_params]
                concurrent.futures.wait(futures)
            end_time_total = datetime.now()
            
            print(f"\nTiempo total de procesamiento: {end_time_total - start_time_total}")

#%%
# Ejemplo de uso (solo si deseas llamarla directamente):
generate_videos(
    subjects=['12'],
    modality=['VR'],
    sesion_A=True,
    sesion_B=True,
    test=False  # Cambiar a True para ejecutar en modo test
)

# %%

def generate_instruction(audio_path):
    """
    Black screen with duration equal to audio + embedded audio.
    """

def generate_instruction_videos(input_dir, output_dir):
    """
    Generates .mp4 videos from .wav audio files in a specified directory.
    Each video consists of a black screen with the audio duration and embedded audio.

    Parameters
    ----------
    input_dir : str
        Directory containing .wav audio files.
    output_dir : str
        Directory where resulting .mp4 video files will be saved.
        If it doesn't exist, it will be created automatically.

    Usage example
    --------------
    generate_instruction_videos(
        input_dir='./instructions_audios',
        output_dir='./instructions_videos'
    )
    """

def generate_practice_videos(modality="2D"):
    """
    Generates a practice video by concatenating the following elements:
    1. welcome_and_baseline_audio.wav
    2. fixation_cross (5 minutes)
    3. valence_practice_instruction_audio.wav
    4. Video 1
    5. post_stimulus_self_report_practice.wav
    6. arousal_practice_instructions_audio.wav
    7. Video 2
    8. post_stimulus_self_report.wav
    9. luminance_practice_instructions_audio.wav
    10.luminance video
    11. end_practice.wav

    Parameters:
    -----------
    modality : str
        "2D" or "VR" to specify the folder from which videos are taken.
    """
