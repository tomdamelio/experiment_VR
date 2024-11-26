#%%

import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Filtrar los datos para el participante 'sub-06', 'id' 9
filtered_data = data_all_resampled[(data_all_resampled['sub'] == 6) & 
                                   (data_all_resampled['id'] == 9)]

# Verificar el resultado
print(filtered_data)

# Asegurar que 'continuous_annotation' está en formato de listas
filtered_data['continuous_annotation'] = filtered_data['continuous_annotation'].apply(eval)

# Iterar sobre cada fila filtrada para generar gráficos separados
for index, row in filtered_data.iterrows():
    values = []
    times = []

    for value, time in row['continuous_annotation']:
        values.append(value)
        times.append(time)

    # Graficar la columna 'continuous_annotation'
    plt.figure(figsize=(10, 6))
    plt.plot(times, values, label='Continuous Annotation', color='#c08c94', linewidth=2)

    # Añadir títulos y etiquetas
    plt.title(f"Continuous Annotation for sub-06, id 9, {row['dimension']}", fontsize=14, fontweight='bold')
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Annotation Value', fontsize=12)
    plt.legend()

    # Mejorar la apariencia
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()

# %%

import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Filtrar los datos para el video con id 7 y dimension = 'arousal'
filtered_data = data_all_resampled[(data_all_resampled['id'] == 9) & (data_all_resampled['dimension'] == 'arousal')]

# Verificar el resultado
print(filtered_data)

# Asegurar que 'continuous_annotation' está en formato de listas
filtered_data['continuous_annotation'] = filtered_data['continuous_annotation'].apply(eval)

# Lista de colores para diferenciar los participantes
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

plt.figure(figsize=(10, 6))

# Iterar sobre cada participante (sub 1 al 6) para generar gráficos en el mismo plot
for i, sub in enumerate(range(1, 7)):
    participant_data = filtered_data[filtered_data['sub'] == sub]
    
    # Iterar sobre cada fila filtrada para generar gráficos separados
    for index, row in participant_data.iterrows():
        values = []
        times = []

        for value, time in row['continuous_annotation']:
            values.append(value)
            times.append(time)

        # Graficar la columna 'continuous_annotation'
        plt.plot(times, values, label=f'Participant {sub}', color=colors[i], linewidth=2)

# Añadir títulos y etiquetas
plt.title(f'Continuous Annotation for Video id 9 (Arousal) for Participants 1-6', fontsize=14, fontweight='bold')
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Annotation Value', fontsize=12)
plt.legend()

# Mejorar la apariencia
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Mostrar el gráfico
plt.show()

#%%


#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Filtrar los datos para el video con id 9 y dimension = 'arousal'
filtered_data = data_all_resampled[(data_all_resampled['id'] == 9) & (data_all_resampled['dimension'] == 'arousal')]

# Verificar el resultado
print(filtered_data)

# Asegurar que 'continuous_annotation' está en formato de listas
filtered_data['continuous_annotation'] = filtered_data['continuous_annotation'].apply(eval)

# Función para resamplear y obtener el promedio y el desvío estándar
def resample_and_aggregate(data, common_times):
    all_resampled_values = []

    for annotations in data:
        df = pd.DataFrame(annotations, columns=['value', 'time'])
        resampled_values = np.interp(common_times, df['time'], df['value'])
        all_resampled_values.append(resampled_values)

    all_resampled_values = np.array(all_resampled_values)
    mean_values = np.mean(all_resampled_values, axis=0)
    std_values = np.std(all_resampled_values, axis=0)
    return mean_values, std_values

# Recolectar todas las anotaciones continuas para los 6 participantes
continuous_annotations = []
for sub in range(1, 7):
    participant_data = filtered_data[filtered_data['sub'] == sub]
    for index, row in participant_data.iterrows():
        continuous_annotations.append(row['continuous_annotation'])

# Definir un rango de tiempos común
all_times = [time for annotations in continuous_annotations for value, time in annotations]
common_times = np.arange(min(all_times), max(all_times), 0.1)

# Resamplear y obtener el promedio y el desvío estándar
mean_values, std_values = resample_and_aggregate(continuous_annotations, common_times)

# Graficar el promedio y el desvío estándar
plt.figure(figsize=(10, 6))
plt.plot(common_times, mean_values, label='Mean Arousal', color='blue', linewidth=2)
plt.fill_between(common_times, mean_values - std_values, mean_values + std_values, color='blue', alpha=0.2)

# Añadir títulos y etiquetas
plt.title(f'Continuous Annotation for Video id 9 (Arousal) for Participants 1-6', fontsize=14, fontweight='bold')
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Annotation Value', fontsize=12)
plt.legend()

# Mejorar la apariencia
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Mostrar el gráfico
plt.show()



#%%

import os
import pandas as pd
import matplotlib.pyplot as plt

# Crear la carpeta de destino si no existe
output_dir = './figures/plot_per_video'
os.makedirs(output_dir, exist_ok=True)

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Verificar el resultado
print(data_all_resampled)

# Asegurar que 'continuous_annotation' está en formato de listas
data_all_resampled['continuous_annotation'] = data_all_resampled['continuous_annotation'].apply(eval)

# Lista de colores para diferenciar los participantes
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# Iterar sobre cada valor único de 'id' y 'dimension'
for video_id in data_all_resampled['id'].unique():
    for dimension in data_all_resampled['dimension'].unique():
        plt.figure(figsize=(10, 6))

        # Filtrar los datos para el video y dimensión actuales
        filtered_data = data_all_resampled[(data_all_resampled['id'] == video_id) & 
                                           (data_all_resampled['dimension'] == dimension)]
        
        # Iterar sobre cada participante (sub 1 al 6) para generar gráficos en el mismo plot
        for i, sub in enumerate(range(1, 7)):
            participant_data = filtered_data[filtered_data['sub'] == sub]
            
            # Iterar sobre cada fila filtrada para generar gráficos separados
            for index, row in participant_data.iterrows():
                values = []
                times = []

                for value, time in row['continuous_annotation']:
                    values.append(value)
                    times.append(time)

                # Graficar la columna 'continuous_annotation'
                plt.plot(times, values, label=f'Participant {sub}', color=colors[i], linewidth=2)

        # Añadir títulos y etiquetas
        plt.title(f'Continuous Annotation for Video id {video_id} ({dimension}) for Participants 1-6', fontsize=14, fontweight='bold')
        plt.xlabel('Time (s)', fontsize=12)
        plt.ylabel('Annotation Value', fontsize=12)
        plt.legend()

        # Mejorar la apariencia
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()

        # Guardar el gráfico
        filename = f'plot_video_{video_id}_dimension_{dimension}.png'
        plt.savefig(os.path.join(output_dir, filename), dpi=300)
        plt.close()

#%%

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Crear la carpeta de destino si no existe
output_dir = './figures'
os.makedirs(output_dir, exist_ok=True)

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Asegurar que 'continuous_annotation' está en formato de listas
data_all_resampled['continuous_annotation'] = data_all_resampled['continuous_annotation'].apply(eval)

# Lista de colores para diferenciar los participantes
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# Filtrar los datos para el video 9 y dimensión arousal
filtered_data = data_all_resampled[(data_all_resampled['id'] == 9) & 
                                   (data_all_resampled['dimension'] == 'arousal')]

plt.figure(figsize=(12, 8))  # Aumentar el tamaño de la figura

all_values = []
common_times = None

# Encontrar el tiempo final mínimo entre todos los participantes
min_final_time = float('inf')

# Iterar sobre cada participante (sub 1 al 6) para encontrar el tiempo final mínimo
for sub in range(1, 7):
    participant_data = filtered_data[filtered_data['sub'] == sub]
    for index, row in participant_data.iterrows():
        times = [time for value, time in row['continuous_annotation']]
        if times[-1] < min_final_time:
            min_final_time = times[-1]

print(f'Minimum final time: {min_final_time}')

# Crear una serie de tiempos comunes basada en el tiempo final mínimo
common_times = np.linspace(0, min_final_time, num=int(min_final_time*10) + 1)

# Iterar sobre cada participante (sub 1 al 6) para generar gráficos en el mismo plot
for i, sub in enumerate(range(1, 7)):
    participant_data = filtered_data[filtered_data['sub'] == sub]

    for index, row in participant_data.iterrows():
        values = []
        times = []

        for value, time in row['continuous_annotation']:
            if time <= min_final_time:
                values.append(value)
                times.append(time)

        print(f'Participant {sub} last time value after adjustment: {times[-1]}')  # Imprimir el último valor de tiempo ajustado
        print(f'Participant {sub} last annotation value after adjustment: {values[-1]}')

        # Interpolar valores para tener una longitud común
        interp_func = interp1d(times, values, kind='linear', bounds_error=False, fill_value='extrapolate')
        common_values = interp_func(common_times)  # Asegurar que los tiempos coinciden con los valores

        all_values.append(common_values)

        # Graficar la columna 'continuous_annotation' con alpha para translucidez
        plt.plot(common_times, common_values, label=f'Participant {sub}', color=colors[i], linewidth=2, alpha=0.5)

# Calcular el promedio de las anotaciones
mean_values = np.mean(np.array(all_values), axis=0)

# Graficar la línea del promedio
plt.plot(common_times, mean_values, color='black', linewidth=3, label='Mean')

# Añadir títulos y etiquetas con fuentes más grandes
plt.title('Continuous Annotation for Video id 9 (Arousal) for Participants 1-6', fontsize=20, fontweight='bold')
plt.xlabel('Time (s)', fontsize=18)
plt.ylabel('Annotation Value', fontsize=18)

# Aumentar el tamaño de las etiquetas de los ejes
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Añadir y mejorar la leyenda
plt.legend(fontsize=14, loc='upper right')

# Mejorar la apariencia de la cuadrícula
plt.grid(True, linestyle='--', alpha=0.6)

# Ajustar el diseño para evitar superposiciones
plt.tight_layout()

# Guardar el gráfico
filename = 'plot_video_9_dimension_arousal.png'
plt.savefig(os.path.join(output_dir, filename), dpi=300)
plt.close()


#%%
import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Filtrar los datos para el participante 'sub-06', 'id' 9
filtered_data = data_all_resampled[(data_all_resampled['sub'] == 6) & 
                                   (data_all_resampled['id'] == 9)]

# Verificar el resultado
print(filtered_data)

# Asegurar que 'continuous_annotation' está en formato de listas
filtered_data['continuous_annotation'] = filtered_data['continuous_annotation'].apply(eval)

# Extraer valores y tiempos de las listas internas para valence y arousal
valence_values = []
valence_times = []
arousal_values = []
arousal_times = []

for index, row in filtered_data.iterrows():
    if row['dimension'] == 'valence':
        for value, time in row['continuous_annotation']:
            if time > 5:
                valence_values.append(value)
                valence_times.append(time)
    elif row['dimension'] == 'arousal':
        for value, time in row['continuous_annotation']:
            if time > 5:
                arousal_values.append(value)
                arousal_times.append(time)

# Verificar que tenemos los datos de ambas dimensiones
if valence_values and arousal_values:
    # Encontrar la longitud de la lista más corta
    min_length = min(len(valence_values), len(arousal_values))
    
    # Truncar ambas listas a la longitud de la lista más corta
    valence_values = valence_values[:min_length]
    arousal_values = arousal_values[:min_length]

    # Graficar valence en el eje X y arousal en el eje Y
    plt.figure(figsize=(10, 6))
    plt.plot(valence_values, arousal_values, label='Valence vs Arousal', color='#c08c94', linewidth=2)

    # Añadir títulos y etiquetas
    plt.title(f'Valence vs Arousal for sub-06, id 9', fontsize=14, fontweight='bold')
    plt.xlabel('Valence', fontsize=12)
    plt.ylabel('Arousal', fontsize=12)
    plt.legend()

    # Establecer los límites de los ejes
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)

    # Mejorar la apariencia
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()
else:
    print("No se encontraron datos completos para 'valence' y 'arousal' en el sujeto 6, id 9.")

# %%

import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Filtrar los datos para el participante 'sub-06', 'id' 9
filtered_data = data_all_resampled[(data_all_resampled['sub'] == 6) & 
                                   (data_all_resampled['id'] == 10)]

# Verificar el resultado
print(filtered_data)

# Asegurar que 'continuous_annotation' está en formato de listas
filtered_data['continuous_annotation'] = filtered_data['continuous_annotation'].apply(eval)

# Extraer valores y tiempos de las listas internas para valence y arousal
valence_annotations = []
arousal_annotations = []

for index, row in filtered_data.iterrows():
    if row['dimension'] == 'valence':
        valence_annotations.append([(value, time) for value, time in row['continuous_annotation'] if time > 5])
    elif row['dimension'] == 'arousal':
        arousal_annotations.append([(value, time) for value, time in row['continuous_annotation'] if time > 5])

# Convertir las listas de listas en DataFrames
valence_df = pd.DataFrame([value for sublist in valence_annotations for value in sublist], columns=['value', 'time'])
arousal_df = pd.DataFrame([value for sublist in arousal_annotations for value in sublist], columns=['value', 'time'])

# Agrupar por intervalos de 5 segundos y calcular la media
valence_df['interval'] = (valence_df['time'] // 5) * 5
arousal_df['interval'] = (arousal_df['time'] // 5) * 5

valence_mean = valence_df.groupby('interval')['value'].mean()
arousal_mean = arousal_df.groupby('interval')['value'].mean()

# Asegurarse de que ambos tengan la misma longitud
common_intervals = valence_mean.index.intersection(arousal_mean.index)
valence_mean = valence_mean.loc[common_intervals]
arousal_mean = arousal_mean.loc[common_intervals]

# Graficar valence en el eje X y arousal en el eje Y
plt.figure(figsize=(10, 6))
plt.plot(valence_mean, arousal_mean, label='Valence vs Arousal', color='#c08c94', linewidth=2)

# Añadir títulos y etiquetas
plt.title(f'Valence vs Arousal for sub-06, id 9', fontsize=14, fontweight='bold')
plt.xlabel('Valence', fontsize=12)
plt.ylabel('Arousal', fontsize=12)
plt.legend()

# Establecer los límites de los ejes
plt.xlim(-1, 1)
plt.ylim(-1, 1)

# Mejorar la apariencia
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Mostrar el gráfico
plt.show()

# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
from moviepy.editor import VideoFileClip

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Crear la carpeta de salida si no existe
output_dir = './figures/videos_annotations_per_subject'
os.makedirs(output_dir, exist_ok=True)

# Definir una paleta de colores categórica
colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00', '#e6ab02', '#66a61e', '#e7298a', '#a6761d', '#666666']

# Crear una función para generar los gráficos
def generate_plots_for_subject(subject_id):
    # Filtrar los datos para el participante actual
    filtered_data = data_all_resampled[data_all_resampled['sub'] == subject_id]

    # Asegurar que 'continuous_annotation' está en formato de listas
    filtered_data['continuous_annotation'] = filtered_data['continuous_annotation'].apply(eval)

    # Extraer valores y tiempos de las listas internas para valence y arousal
    valence_annotations = []
    arousal_annotations = []

    for index, row in filtered_data.iterrows():
        if row['dimension'] == 'valence':
            valence_annotations.append([(value, time, row['id']) for value, time in row['continuous_annotation'] if time > 5])
        elif row['dimension'] == 'arousal':
            arousal_annotations.append([(value, time, row['id']) for value, time in row['continuous_annotation'] if time > 5])

    # Convertir las listas de listas en DataFrames
    valence_df = pd.DataFrame([value for sublist in valence_annotations for value in sublist], columns=['value', 'time', 'id'])
    arousal_df = pd.DataFrame([value for sublist in arousal_annotations for value in sublist], columns=['value', 'time', 'id'])

    # Agrupar por intervalos de 5 segundos y calcular la media
    valence_df['interval'] = (valence_df['time'] // 5) * 5
    arousal_df['interval'] = (arousal_df['time'] // 5) * 5

    valence_mean = valence_df.groupby(['interval', 'id'])['value'].mean().reset_index()
    arousal_mean = arousal_df.groupby(['interval', 'id'])['value'].mean().reset_index()

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)  # DPI alto para mejor calidad
    lines = {video_id: ax.plot([], [], lw=2, color=colors[video_id - 1], label=f'Video {video_id}')[0] for video_id in range(1, 15)}

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_xlabel('Valence', fontsize=12)
    ax.set_ylabel('Arousal', fontsize=12)
    ax.axhline(0, color='black', linestyle='--', linewidth=1)  # Línea punteada en Y=0
    ax.axvline(0, color='black', linestyle='--', linewidth=1)  # Línea punteada en X=0
    ax.set_title(f'Subject {subject_id}', fontsize=14)
    ax.legend()

    # Inicializar la función de animación
    def init():
        for line in lines.values():
            line.set_data([], [])
        return lines.values()

    # Función de animación
    def animate(i):
        video_id = (i // len(valence_mean['interval'].unique())) + 1
        frame = i % len(valence_mean['interval'].unique())

        if video_id > 14:
            return lines.values()

        valence_data = valence_mean[valence_mean['id'] == video_id]
        arousal_data = arousal_mean[arousal_mean['id'] == video_id]
        common_intervals = np.intersect1d(valence_data['interval'], arousal_data['interval'])
        valence_data = valence_data[valence_data['interval'].isin(common_intervals)]
        arousal_data = arousal_data[arousal_data['interval'].isin(common_intervals)]
        x = valence_data['value'].values[:frame+1]
        y = arousal_data['value'].values[:frame+1]
        lines[video_id].set_data(x, y)
        return lines.values()

    # Crear la animación
    total_frames = len(valence_mean['interval'].unique()) * 14
    ani = FuncAnimation(fig, animate, init_func=init, frames=total_frames, interval=200, blit=True)

    # Guardar la animación como video
    video_path = os.path.join(output_dir, f'valence_vs_arousal_sub-{subject_id}_all_videos.mp4')
    ani.save(video_path, fps=5, extra_args=['-vcodec', 'libx264'])

    plt.close(fig)  # Cerrar la figura para liberar memoria

    # Convertir el video a GIF
    gif_path = os.path.join(output_dir, f'valence_vs_arousal_sub-{subject_id}_all_videos.gif')
    clip = VideoFileClip(video_path)
    clip.write_gif(gif_path, fps=5)

# Generar los gráficos para todos los participantes
for subject_id in range(1, 7):
    generate_plots_for_subject(subject_id)

# %%
import os
from moviepy.editor import VideoFileClip

# Definir la carpeta de entrada y salida
input_dir = './figures/videos_annotations_per_subject'
output_dir = './figures/videos_annotations_per_subject'

# Convertir los videos a GIF
for filename in os.listdir(input_dir):
    if filename.endswith(".mp4"):
        video_path = os.path.join(input_dir, filename)
        gif_path = os.path.join(output_dir, filename.replace(".mp4", ".gif"))
        
        clip = VideoFileClip(video_path)
        clip.write_gif(gif_path, fps=5)
        print(f'Converted {filename} to GIF')

print("Conversion complete.")

# %%
import os
from moviepy.editor import VideoFileClip

# Definir la carpeta de entrada y salida
input_dir = './figures/videos_annotations_per_subject'
output_dir = './figures/compressed_gifs'
os.makedirs(output_dir, exist_ok=True)

# Convertir los GIFs a una versión comprimida
for filename in os.listdir(input_dir):
    if filename.endswith(".gif"):
        gif_path = os.path.join(input_dir, filename)
        compressed_gif_path = os.path.join(output_dir, filename.replace(".gif", "_compressed.gif"))
        
        clip = VideoFileClip(gif_path)

        # Reducir FPS a 2 para compresión
        clip = clip.set_fps(2)

        # Opción adicional: Redimensionar el GIF para compresión adicional
        # clip = clip.resize(height=240)  # Ajusta la altura a 240px, manteniendo el aspecto

        clip.write_gif(compressed_gif_path, fps=2)
        print(f'Compressed {filename} to {compressed_gif_path}')

print("Compression complete.")

# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Crear la carpeta de salida si no existe
output_dir = './figures/images_annotations_per_subject'
os.makedirs(output_dir, exist_ok=True)

# Definir una paleta de colores categórica
colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00', '#e6ab02', '#66a61e', '#e7298a', '#a6761d', '#666666']

# Crear una función para generar los gráficos
def generate_plots_for_subject(subject_id):
    # Filtrar los datos para el participante actual
    filtered_data = data_all_resampled[data_all_resampled['sub'] == subject_id]

    # Asegurar que 'continuous_annotation' está en formato de listas
    filtered_data['continuous_annotation'] = filtered_data['continuous_annotation'].apply(eval)

    # Extraer valores y tiempos de las listas internas para valence y arousal
    valence_annotations = []
    arousal_annotations = []

    for index, row in filtered_data.iterrows():
        if row['dimension'] == 'valence':
            valence_annotations.append([(value, time, row['id']) for value, time in row['continuous_annotation'] if time > 5])
        elif row['dimension'] == 'arousal':
            arousal_annotations.append([(value, time, row['id']) for value, time in row['continuous_annotation'] if time > 5])

    # Convertir las listas de listas en DataFrames
    valence_df = pd.DataFrame([value for sublist in valence_annotations for value in sublist], columns=['value', 'time', 'id'])
    arousal_df = pd.DataFrame([value for sublist in arousal_annotations for value in sublist], columns=['value', 'time', 'id'])

    # Agrupar por intervalos de 5 segundos y calcular la media
    valence_df['interval'] = (valence_df['time'] // 5) * 5
    arousal_df['interval'] = (arousal_df['time'] // 5) * 5

    valence_mean = valence_df.groupby(['interval', 'id'])['value'].mean().reset_index()
    arousal_mean = arousal_df.groupby(['interval', 'id'])['value'].mean().reset_index()

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)  # DPI alto para mejor calidad

    for video_id in range(1, 15):
        valence_data = valence_mean[valence_mean['id'] == video_id]
        arousal_data = arousal_mean[arousal_mean['id'] == video_id]
        common_intervals = np.intersect1d(valence_data['interval'], arousal_data['interval'])
        valence_data = valence_data[valence_data['interval'].isin(common_intervals)]
        arousal_data = arousal_data[arousal_data['interval'].isin(common_intervals)]
        x = valence_data['value'].values
        y = arousal_data['value'].values
        ax.plot(x, y, lw=2, color=colors[video_id - 1], label=f'Video {video_id}')

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_xlabel('Valence', fontsize=24)  # Aumentar el tamaño de la fuente
    ax.set_ylabel('Arousal', fontsize=24)  # Aumentar el tamaño de la fuente
    ax.axhline(0, color='black', linestyle='--', linewidth=1)  # Línea punteada en Y=0
    ax.axvline(0, color='black', linestyle='--', linewidth=1)  # Línea punteada en X=0
    ax.set_title(f'Subject {subject_id}', fontsize=30)  # Aumentar el tamaño de la fuente del título
    ax.legend(fontsize=12)  # Aumentar el tamaño de la fuente de la leyenda

    # Guardar la figura como imagen
    image_path = os.path.join(output_dir, f'valence_vs_arousal_sub-{subject_id}_all_videos.png')
    plt.savefig(image_path)
    plt.close(fig)  # Cerrar la figura para liberar memoria

# Generar los gráficos para todos los participantes
for subject_id in range(1, 7):
    generate_plots_for_subject(subject_id)

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurar estilo de seaborn para gráficos
sns.set(style="whitegrid")

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Crear la carpeta de salida si no existe
output_dir = './figures/images_annotations_per_subject'
os.makedirs(output_dir, exist_ok=True)

# Definir una paleta de colores categórica
colors = sns.color_palette("husl", 14)  # Usar una paleta de colores de seaborn

# Crear una figura con subplots
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(25, 12), dpi=300)  # Tamaño ajustado para mejor calidad y legibilidad
axes = axes.flatten()  # Aplanar el array de ejes para facilitar el acceso

# Crear una función para generar los gráficos en subplots
def generate_plots_for_subject(subject_id, ax):
    # Filtrar los datos para el participante actual
    filtered_data = data_all_resampled[data_all_resampled['sub'] == subject_id]

    # Asegurar que 'continuous_annotation' está en formato de listas
    filtered_data['continuous_annotation'] = filtered_data['continuous_annotation'].apply(eval)

    # Extraer valores y tiempos de las listas internas para valence y arousal
    valence_annotations = []
    arousal_annotations = []

    for index, row in filtered_data.iterrows():
        if row['dimension'] == 'valence':
            valence_annotations.append([(value, time, row['id']) for value, time in row['continuous_annotation'] if time > 5])
        elif row['dimension'] == 'arousal':
            arousal_annotations.append([(value, time, row['id']) for value, time in row['continuous_annotation'] if time > 5])

    # Convertir las listas de listas en DataFrames
    valence_df = pd.DataFrame([value for sublist in valence_annotations for value in sublist], columns=['value', 'time', 'id'])
    arousal_df = pd.DataFrame([value for sublist in arousal_annotations for value in sublist], columns=['value', 'time', 'id'])

    # Agrupar por intervalos de 5 segundos y calcular la media
    valence_df['interval'] = (valence_df['time'] // 5) * 5
    arousal_df['interval'] = (arousal_df['time'] // 5) * 5

    valence_mean = valence_df.groupby(['interval', 'id'])['value'].mean().reset_index()
    arousal_mean = arousal_df.groupby(['interval', 'id'])['value'].mean().reset_index()

    for video_id in range(1, 15):
        valence_data = valence_mean[valence_mean['id'] == video_id]
        arousal_data = arousal_mean[arousal_mean['id'] == video_id]
        common_intervals = np.intersect1d(valence_data['interval'], arousal_data['interval'])
        valence_data = valence_data[valence_data['interval'].isin(common_intervals)]
        arousal_data = arousal_data[arousal_data['interval'].isin(common_intervals)]
        x = valence_data['value'].values
        y = arousal_data['value'].values
        ax.plot(x, y, lw=2, color=colors[video_id - 1])

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_xlabel('Valence', fontsize=18)  # Ajustar el tamaño de la fuente
    ax.set_ylabel('Arousal', fontsize=18)  # Ajustar el tamaño de la fuente
    ax.axhline(0, color='black', linestyle='--', linewidth=1)  # Línea punteada en Y=0
    ax.axvline(0, color='black', linestyle='--', linewidth=1)  # Línea punteada en X=0
    ax.set_title(f'Subject {subject_id}', fontsize=22, fontweight='bold')  # Título en negrita

# Generar los gráficos para todos los participantes en subplots
for i, subject_id in enumerate(range(1, 7)):
    generate_plots_for_subject(subject_id, axes[i])

# Ajustar el diseño para evitar superposición y dejar espacio para la leyenda
plt.subplots_adjust(bottom=0.2, top=0.85, hspace=0.4, wspace=0.4)

# Añadir un título general a la figura
fig.suptitle('Valence vs Arousal for All Subjects', fontsize=28, fontweight='bold', y=0.95)

# Añadir una leyenda común para todos los subplots
handles = [plt.Line2D([0], [0], color=colors[i], lw=2, label=f'Video {i+1}') for i in range(14)]
fig.legend(handles=handles, loc='lower center', ncol=7, fontsize=20, frameon=False, bbox_to_anchor=(0.5, -0.05))

# Guardar la figura como imagen
image_path = os.path.join(output_dir, 'valence_vs_arousal_all_subjects.png')
plt.savefig(image_path, bbox_inches='tight')
plt.close(fig)  # Cerrar la figura para liberar memoria




# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurar estilo de seaborn para gráficos
sns.set(style="whitegrid")

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Crear la carpeta de salida si no existe
output_dir = './figures/images_annotations_per_video'
os.makedirs(output_dir, exist_ok=True)

# Definir una paleta de colores categórica
colors = sns.color_palette("husl", 14)  # Usar una paleta de colores de seaborn

# Crear una función para generar los gráficos por video
def generate_plots_for_video(video_id):
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(25, 12), dpi=300)  # Tamaño ajustado para mejor calidad y legibilidad
    axes = axes.flatten()  # Aplanar el array de ejes para facilitar el acceso

    for i, subject_id in enumerate(range(1, 7)):
        ax = axes[i]
        # Filtrar los datos para el participante actual y el video actual
        filtered_data = data_all_resampled[(data_all_resampled['sub'] == subject_id) & 
                                           (data_all_resampled['id'] == video_id)]

        # Asegurar que 'continuous_annotation' está en formato de listas
        filtered_data['continuous_annotation'] = filtered_data['continuous_annotation'].apply(eval)

        # Extraer valores y tiempos de las listas internas para valence y arousal
        valence_annotations = []
        arousal_annotations = []

        for index, row in filtered_data.iterrows():
            if row['dimension'] == 'valence':
                valence_annotations.append([(value, time) for value, time in row['continuous_annotation'] if time > 5])
            elif row['dimension'] == 'arousal':
                arousal_annotations.append([(value, time) for value, time in row['continuous_annotation'] if time > 5])

        # Convertir las listas de listas en DataFrames
        valence_df = pd.DataFrame([value for sublist in valence_annotations for value in sublist], columns=['value', 'time'])
        arousal_df = pd.DataFrame([value for sublist in arousal_annotations for value in sublist], columns=['value', 'time'])

        # Agrupar por intervalos de 5 segundos y calcular la media
        valence_df['interval'] = (valence_df['time'] // 5) * 5
        arousal_df['interval'] = (arousal_df['time'] // 5) * 5

        valence_mean = valence_df.groupby('interval')['value'].mean().reset_index()
        arousal_mean = arousal_df.groupby('interval')['value'].mean().reset_index()

        common_intervals = np.intersect1d(valence_mean['interval'], arousal_mean['interval'])
        valence_mean = valence_mean[valence_mean['interval'].isin(common_intervals)]
        arousal_mean = arousal_mean[arousal_mean['interval'].isin(common_intervals)]

        x = valence_mean['value'].values
        y = arousal_mean['value'].values
        ax.plot(x, y, lw=2, color=colors[video_id - 1])

        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_xlabel('Valence', fontsize=18)  # Ajustar el tamaño de la fuente
        ax.set_ylabel('Arousal', fontsize=18)  # Ajustar el tamaño de la fuente
        ax.axhline(0, color='black', linestyle='--', linewidth=1)  # Línea punteada en Y=0
        ax.axvline(0, color='black', linestyle='--', linewidth=1)  # Línea punteada en X=0
        ax.set_title(f'Subject {subject_id}', fontsize=22, fontweight='bold')  # Título en negrita

    # Ajustar el diseño para evitar superposición y dejar espacio para la leyenda
    plt.subplots_adjust(bottom=0.2, top=0.85, hspace=0.4, wspace=0.4)

    # Añadir un título general a la figura
    fig.suptitle(f'Valence vs Arousal for Video {video_id}', fontsize=28, fontweight='bold', y=0.95)

    # Añadir una leyenda común para todos los subplots
    handles = [plt.Line2D([0], [0], color=colors[video_id - 1], lw=2, label=f'Video {video_id}')]
    fig.legend(handles=handles, loc='lower center', ncol=1, fontsize=20, frameon=False, bbox_to_anchor=(0.5, -0.05))

    # Guardar la figura como imagen
    image_path = os.path.join(output_dir, f'valence_vs_arousal_video_{video_id}.png')
    plt.savefig(image_path, bbox_inches='tight')
    plt.close(fig)  # Cerrar la figura para liberar memoria

# Generar los gráficos por video
for video_id in range(1, 15):
    generate_plots_for_video(video_id)

# %%

import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Filtrar los datos para el participante 'sub-06', 'id' 9
filtered_data = data_all_resampled[(data_all_resampled['sub'] == 6) & 
                                   (data_all_resampled['id'] == 9)]

# Verificar el resultado
print(filtered_data)

# Asegurar que 'continuous_annotation' está en formato de listas
filtered_data['continuous_annotation'] = filtered_data['continuous_annotation'].apply(eval)

# Iterar sobre cada fila filtrada para generar gráficos separados
for index, row in filtered_data.iterrows():
    values = []
    times = []

    for value, time in row['continuous_annotation']:
        values.append(value)
        times.append(time)

    # Graficar la columna 'continuous_annotation'
    plt.figure(figsize=(10, 6))
    plt.plot(times, values, label='Continuous Annotation', color='#c08c94', linewidth=2)

    # Añadir títulos y etiquetas
    plt.title(f"Continuous Annotation for sub-06, id 9, {row['dimension']}", fontsize=14, fontweight='bold')
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Annotation Value', fontsize=12)
    plt.legend()

    # Mejorar la apariencia
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()

# %%

