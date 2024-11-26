# -*- coding: utf-8 -*-
#%%
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats

base_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_dir)

#%% Junto los datos en 1 df para cada sujeto

subjects = ["02","03","04", "05","06"] #

dict_videos_sujetos = {}
for subject in subjects:
    df_videos_sujeto = pd.DataFrame()
    for bloque_n in range(1,9): # Por ahora no hubo sujetos que no tuvieran 8 bloques
        if subject == "05" and bloque_n == 3: # no tengo el fisio de este bloque porque crashea
            continue
        
        bloque = pd.read_csv(f'sub-{subject}/ses-A/df_sub-{subject}_block_{bloque_n}_final.csv').drop("Unnamed: 0",axis=1)
        
        if bloque_n > 4:
            bloque["video_rep"] = 2
        
        else:
            bloque["video_rep"] = 1
        
        
        df_videos_sujeto = pd.concat([df_videos_sujeto, bloque], axis=0)
    
    dict_videos_sujetos[subject] = df_videos_sujeto
    
#%% Comparar EDA_CLean entre primer y segunda pasada del video

for subject in subjects:
    df_videos_sujeto = dict_videos_sujetos[subject]
    
    for video in df_videos_sujeto.video_id.unique():
        data_video = df_videos_sujeto[df_videos_sujeto.video_id == video]
        primera_pasada = data_video[data_video["video_rep"]==1]
        segunda_pasada = data_video[data_video["video_rep"]==2]
    
        plt.figure()
        plt.plot(primera_pasada.time,stats.zscore(primera_pasada.EDA_Clean),color="red",label="Primer pasada")
        plt.plot(segunda_pasada.time,stats.zscore(segunda_pasada.EDA_Clean),color="blue",label="Segunda pasada")
        plt.title(f"EDA Clean Subject {subject} - Video {video}")
        plt.legend()
        plt.show()

#%% Comparar EDA_Phasic entre primer y segunda pasada del video

for subject in subjects:
    df_videos_sujeto = dict_videos_sujetos[subject]
    
    for video in df_videos_sujeto.video_id.unique():
        data_video = df_videos_sujeto[df_videos_sujeto.video_id == video]
        primera_pasada = data_video[data_video["video_rep"]==1]
        segunda_pasada = data_video[data_video["video_rep"]==2]
    
        plt.figure()
        plt.plot(primera_pasada.time,stats.zscore(primera_pasada.EDA_Phasic),color="red",label="Primer pasada")
        plt.plot(segunda_pasada.time,stats.zscore(segunda_pasada.EDA_Phasic),color="blue",label="Segunda pasada")
        plt.title(f"EDA Phasic Subject {subject} - Video {video}")
        plt.legend()
        plt.show()
        
# %% Comparar EDA_Tonic entre primer y segunda pasada

for subject in subjects:
    df_videos_sujeto = dict_videos_sujetos[subject]
    
    for video in df_videos_sujeto.video_id.unique():
        data_video = df_videos_sujeto[df_videos_sujeto.video_id == video]
        primera_pasada = data_video[data_video["video_rep"]==1]
        segunda_pasada = data_video[data_video["video_rep"]==2]
    
        plt.figure()
        plt.plot(primera_pasada.time,stats.zscore(primera_pasada.EDA_Tonic),color="red",label="Primer pasada")
        plt.plot(segunda_pasada.time,stats.zscore(segunda_pasada.EDA_Tonic),color="blue",label="Segunda pasada")
        plt.title(f"EDA Tonic Subject {subject} - Video {video}")
        plt.legend()
        plt.show()

# %% Comparar SMNA entre primer y segunda pasada

for subject in subjects:
    df_videos_sujeto = dict_videos_sujetos[subject]
    
    for video in df_videos_sujeto.video_id.unique():
        data_video = df_videos_sujeto[df_videos_sujeto.video_id == video]
        primera_pasada = data_video[data_video["video_rep"]==1]
        segunda_pasada = data_video[data_video["video_rep"]==2]
    
        plt.figure()
        plt.plot(primera_pasada.time,primera_pasada.SMNA,color="red",label="Primer pasada")
        plt.plot(segunda_pasada.time,segunda_pasada.SMNA,color="blue",label="Segunda pasada")
        plt.title(f"SMNA Subject {subject} - Video {video}")
        plt.legend()
        plt.show()

# %% Comparar ECG_Rate entre primer y segunda pasada

for subject in subjects:
    df_videos_sujeto = dict_videos_sujetos[subject]
    
    for video in df_videos_sujeto.video_id.unique():
        data_video = df_videos_sujeto[df_videos_sujeto.video_id == video]
        primera_pasada = data_video[data_video["video_rep"]==1]
        segunda_pasada = data_video[data_video["video_rep"]==2]
    
        plt.figure()
        plt.plot(primera_pasada.time,stats.zscore(primera_pasada.ECG_Rate),color="red",label="Primer pasada")
        plt.plot(segunda_pasada.time,stats.zscore(segunda_pasada.ECG_Rate),color="blue",label="Segunda pasada")
        plt.title(f"ECG Rate Subject {subject} - Video {video}")
        plt.legend()
        plt.show()

# %% Comparar HRV entre primer y segunda pasada

for subject in subjects:
    df_videos_sujeto = dict_videos_sujetos[subject]
    
    for video in df_videos_sujeto.video_id.unique():
        data_video = df_videos_sujeto[df_videos_sujeto.video_id == video]
        primera_pasada = data_video[data_video["video_rep"]==1]
        segunda_pasada = data_video[data_video["video_rep"]==2]
    
        plt.figure()
        plt.plot(primera_pasada.time,stats.zscore(primera_pasada.HRV),color="red",label="Primer pasada")
        plt.plot(segunda_pasada.time,stats.zscore(segunda_pasada.HRV),color="blue",label="Segunda pasada")
        plt.title(f"HRV Subject {subject} - Video {video}")
        plt.legend()
        plt.show()
        
# %% Comparar anotaciones entre primer y segunda pasada

for subject in subjects:
    df_videos_sujeto = dict_videos_sujetos[subject]
    
    for video in df_videos_sujeto.video_id.unique():
        data_video = df_videos_sujeto[df_videos_sujeto.video_id == video]
        arousal_annotated = data_video[data_video["dimension_annotated"]=="arousal"]
        valence_annotated = data_video[data_video["dimension_annotated"]=="valence"]

    
        plt.figure()
        plt.plot(arousal_annotated.time,arousal_annotated.annotation,color="red",label="Arousal")
        plt.plot(valence_annotated.time,valence_annotated.annotation,color="blue",label="Valencia")
        plt.title(f"Anotaciones Subject {subject} - Video {video}")
        plt.legend()
        plt.show()
# %% Ver señal X de cada sujeto por estimulo

sujetos_por_video = {}

for video_id in range(1,15):   
    primeras_pasadas = pd.DataFrame()
    segundas_pasadas = pd.DataFrame()
    
    for subject in subjects:
        df_videos_sujeto = dict_videos_sujetos[subject]
        
        data_video = df_videos_sujeto[df_videos_sujeto.video_id == video_id]
        primera_pasada = data_video[data_video["video_rep"]==1]
        segunda_pasada = data_video[data_video["video_rep"]==2]
        
        primeras_pasadas = pd.concat([primeras_pasadas,primera_pasada],axis=0)
        segundas_pasadas = pd.concat([segundas_pasadas,segunda_pasada],axis=0)        
        
    sujetos_por_video[f'video_{video_id}_primer_rep'] = primeras_pasadas
    sujetos_por_video[f'video_{video_id}_segundo_rep'] = segundas_pasadas
    
señal_objetivo = "ECG_Rate"

for video in sujetos_por_video.keys():
    for subject in range(2,7):
        df_primer_rep = sujetos_por_video[f'{video}']
        señal = df_primer_rep[df_primer_rep["subject_id"]==subject]
        
        plt.figure(1)
        plt.plot(señal.time,stats.zscore(señal[f'{señal_objetivo}']),label=f"Subject {subject}")
        plt.title(f'{señal_objetivo} Video {video}')
        plt.legend()
    plt.show()
    
# %%
    

# %%

for subject in subjects:
    df_videos_sujeto = dict_videos_sujetos[subject]
    
    for video in sujeto_2.video_id.unique():
        data_video = sujeto_2[sujeto_2.video_id == video]
        arousal_annotated = data_video[data_video["dimension_annotated"]=="arousal"]
        valence_annotated = data_video[data_video["dimension_annotated"]=="valence"]
    
        plt.figure()
        plt.plot(arousal_annotated.time,stats.zscore(arousal_annotated.EDA_Phasic),color="red",label="EDA")
        plt.plot(arousal_annotated.time,arousal_annotated.annotation,color="orange",label="Arousal")
        plt.title(f"EDA Subject {subject} - Video {video}")
        plt.legend()
        plt.show()
        
        plt.figure()
        plt.plot(valence_annotated.time,stats.zscore(valence_annotated.EDA_Phasic),color="blue",label="EDA")
        plt.plot(valence_annotated.time,valence_annotated.annotation,color="orange",label="Valence")
        plt.title(f"EDA Subject {subject} - Video {video}")
        plt.legend()
        plt.show()
        
        
#%%

        plt.figure()
        plt.plot(valence_annotated.time,stats.zscore(valence_annotated.EDA_Phasic),color="blue",label="EDA")
        plt.plot(valence_annotated.time,valence_annotated.annotation,color="orange",label="Valence")
        plt.title(f"Señal {subject} - Video {video}")
        plt.legend()
        plt.show()
        