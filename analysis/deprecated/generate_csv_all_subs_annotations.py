#%%
import os
import pandas as pd

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
        
        # Añadir los datos a la lista
        all_data.append(data)
    else:
        print(f"Archivo no encontrado para {participant} en la ruta {full_path}")

# Concatenar todos los DataFrames en uno solo
data_all = pd.concat(all_data, ignore_index=True)

# Guardar el DataFrame concatenado en el directorio actual
data_all.to_csv('data_all_subs.csv', index=False)

# Verificar el resultado
print(f"Archivo guardado en el directorio actual: {os.getcwd()}/data_all_subs.csv")

#%%


















