#%%
from moviepy import *
import random
import os
import pandas as pd
#%%

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
        df = pd.read_csv(csv_path).sample(frac=1).reset_index(drop=True)
        video_paths = df['movie_path'].tolist()
        video_files.extend(video_paths)
        block_numbers.extend([block_number] * len(video_paths))
        video_ids.extend([video_id] * len(video_paths))
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    video_files = [os.path.abspath(os.path.join(base_dir, path)) for path in video_files]
    
    video_files_df = pd.DataFrame({'video_files': video_files, 'block_number': block_numbers, 'video_id': video_ids})
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

def generate_practice_videos():
    # Rutas de videos
    video_2d_path_1 = "./practice_videos/2D/991.mp4"
    video_2d_path_2 = "./practice_videos/2D/994.mp4"

    # Rutas de audios
    valencia_audio_991_path = "./valencia_audio_pre_991.wav"
    arousal_audio_994_path  = "./arousal_audio_pre_994.wav"

    # Cargar audio
    valencia_991_audio_clip = AudioFileClip(valencia_audio_991_path)
    arousal_994_audio_clip  = AudioFileClip(arousal_audio_994_path)

    # Cargar y redimensionar videos usando .resized(...) en lugar de .resize(...)
    video_2d_clip_1 = VideoFileClip(video_2d_path_1).resized((1280, 720))
    video_2d_clip_2 = VideoFileClip(video_2d_path_2).resized((1280, 720))

    # Crear clips de pantalla negra con audio
    black_screen_valencia_991 = (
        ColorClip(size=(1280, 720), color=(0, 0, 0))
        .with_duration(valencia_991_audio_clip.duration)
        .with_audio(valencia_991_audio_clip)
    )

    black_screen_arousal_994 = (
        ColorClip(size=(1280, 720), color=(0, 0, 0))
        .with_duration(arousal_994_audio_clip.duration)
        .with_audio(arousal_994_audio_clip)
    )

    # Concatenar en el orden deseado
    merged_2d = concatenate_videoclips([
        black_screen_valencia_991,
        video_2d_clip_1,
        black_screen_arousal_994,
        video_2d_clip_2
    ])

    # Exportar
    merged_2d_output = "./practice_videos/2D/merged_practice_video_practice_2D.mp4"
    merged_2d.write_videofile(
        merged_2d_output,
        codec="libx264",
        audio_codec="aac"
    )

generate_practice_videos()


#%%
# Ejemplo de llamado:
generate_videos(Subjects= ['03','04'],  
                 Modality=['VR','2D'], 
                 sesion=['A','A'],
                 condition_A=True, condition_B=True,)

#%%

