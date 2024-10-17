#%%

import os
import pandas as pd
import numpy as np

# Directorio de la carpeta y configuración inicial
dir_folder = 'C:/Users/dameliotomas/experiment_VR/'
results_folder = 'results'
session = 'A'
data_type = 'beh'
extension = '.csv'
task = 'experiment_vr_non_immersive'

# Ruta completa del directorio de resultados
results_path = os.path.join(dir_folder, results_folder)

# Lista para almacenar los datos de todos los participantes
all_data = []

# Obtener la lista de subdirectorios en el directorio de resultados
participants = [d for d in os.listdir(results_path) if os.path.isdir(os.path.join(results_path, d)) and d.startswith('sub-')]

print(participants)

#%%
# Función para resamplear una lista de listas
def resample_continuous_annotation(annotations, interval=0.1):
    if not isinstance(annotations, list) or not all(isinstance(i, list) and len(i) == 2 for i in annotations):
        print("Anotaciones no están en el formato correcto")
        return annotations  # Return original if it's not in the correct format
    
    # Convertir a un DataFrame para facilitar el resampleo
    df = pd.DataFrame(annotations, columns=['value', 'time'])
    
    # Definir un rango de tiempos con el intervalo deseado
    resampled_times = np.arange(df['time'].min(), df['time'].max(), interval)
    
    # Realizar el resampleo interpolando los valores
    resampled_values = np.interp(resampled_times, df['time'], df['value'])
    
    # Formatear los tiempos resampleados para que tengan un decimal
    resampled_times = np.round(resampled_times, 1)
    
    # Convertir de nuevo a una lista de listas
    resampled_annotations = list(zip(resampled_values, resampled_times))
    
    return resampled_annotations

# Función para modificar las anotaciones en función de 'order_emojis_slider'
def modify_annotations(row):
    annotations = row['continuous_annotation']
    if row['order_emojis_slider'] == 'inverse':
        annotations = [[-value, time] for value, time in annotations]
    return annotations

# Loop para cargar los datos de todos los participantes
for participant in participants:
    # Extraer el número del participante del nombre del directorio
    subject_str = participant.split('-')[1]
    
    # Crear el path completo para el archivo del participante
    full_path = os.path.join(results_path, participant, f"ses-{session.upper()}",
                             data_type, f"{participant}_ses-{session}_task-{task}_{data_type}{extension}") 
    
    # Verificar si el archivo existe antes de intentar leerlo
    if os.path.exists(full_path):
        # Leer el archivo CSV
        data = pd.read_csv(full_path)
        
        # Añadir la columna 'sub' con el número del participante
        data['sub'] = subject_str
        
        # Reordenar las columnas para que 'sub' sea la primera
        columns = ['sub'] + [col for col in data.columns if col != 'sub']
        data = data[columns]
        
        # Asegurar que las columnas están en formato de listas
        for col in ['continuous_annotation', 'continuous_annotation_luminance', 'stim_value']:
            data[col] = data[col].apply(lambda x: eval(x) if isinstance(x, str) else x)
        
        # Modificar las anotaciones en función de 'order_emojis_slider'
        data['continuous_annotation'] = data.apply(modify_annotations, axis=1)
        data['continuous_annotation_luminance'] = data.apply(modify_annotations, axis=1)
        
        # Resamplear las columnas
        for col in ['continuous_annotation', 'continuous_annotation_luminance', 'stim_value']:
            data[col] = data[col].apply(resample_continuous_annotation)
        
        # Añadir los datos a la lista
        all_data.append(data)
    else:
        print(f"Archivo no encontrado para {participant} en la ruta {full_path}")

# Concatenar todos los DataFrames en uno solo
data_all = pd.concat(all_data, ignore_index=True)

# Guardar el DataFrame concatenado en el directorio actual
data_all.to_csv('data_all_subs_resampled.csv', index=False)

# Verificar el resultado
print(f"Archivo guardado en el directorio actual: {os.getcwd()}/data_all_subs_resampled.csv")


#%%

filtered_data = data_all[(data_all['sub'] == '06') & (data_all['id'] == 9)]
# %%

# Obtener el tamaño de 'continuous_annotation' para cada fila
lengths = filtered_data['continuous_annotation'].apply(len)

# Mostrar los tamaños
for idx, length in enumerate(lengths):
    print(f"Length of continuous_annotation in row {idx}: {length}")

#%%

filtered_data_arousal = filtered_data[filtered_data['dimension'] == 'valence']

#%%
annotations_filtered_data_arousal = filtered_data_arousal['continuous_annotation']
# %%
for idx, annotations in enumerate(annotations_filtered_data_arousal.head(10)):
    print(f"Row {idx}: {annotations}")
# %%
