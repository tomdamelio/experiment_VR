#%%

# ESTO ME GENERA UN PLOT DE CADA UNO DE LOS ESTIMULOS Y DIMENSION PARA CADA PARTICIPANTE, CON LOS VALORES DE ANOTACIONES CONTINUAS

import os
import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV que contiene todos los participantes
data_all = pd.read_csv('data_all_subs.csv')

# Crear la carpeta de destino si no existe
output_dir = './figures/affective_reports_per_sub_id_dimension'
os.makedirs(output_dir, exist_ok=True)

# Iterar sobre todos los participantes, ids y dimensiones únicos
for sub in data_all['sub'].unique():
    for id_val in data_all['id'].unique():
        for dimension in data_all['dimension'].unique():
            # Filtrar los datos para el participante, id y dimensión actuales
            filtered_data = data_all[(data_all['sub'] == sub) & 
                                     (data_all['id'] == id_val) & 
                                     (data_all['dimension'] == dimension)]
            
            if filtered_data.empty:
                continue

            # Asegurar que 'continuous_annotation' está en formato de listas
            filtered_data['continuous_annotation'] = filtered_data['continuous_annotation'].apply(eval)

            # Extraer valores y tiempos de las listas internas
            values = []
            times = []

            for annotation in filtered_data['continuous_annotation']:
                for value, time in annotation:
                    values.append(value)
                    times.append(time)

            # Graficar la columna 'continuous_annotation'
            plt.figure(figsize=(10, 6))
            plt.plot(times, values, label='Continuous Annotation', color='#c08c94', linewidth=2)

            # Añadir títulos y etiquetas
            plt.title(f'Continuous Annotation for sub-{sub}, id {id_val} ({dimension})', fontsize=14, fontweight='bold')
            plt.xlabel('Time (s)', fontsize=12)
            plt.ylabel('Annotation Value', fontsize=12)
            plt.legend()

            # Mejorar la apariencia
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()

            # Guardar la figura
            filename = f'continuous_annotation_sub-{sub}_id-{id_val}_{dimension}.png'
            plt.savefig(os.path.join(output_dir, filename), dpi=300)


#%%
