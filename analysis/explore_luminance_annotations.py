#%%
import os
import pandas as pd
import matplotlib.pyplot as plt

# Asegurarse de que el directorio de figuras exista
figures_dir = './figures/luminance_per_sub_and_trial'
os.makedirs(figures_dir, exist_ok=True)

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
data_all_resampled = pd.read_csv('data_all_subs_resampled.csv')

# Iterar sobre los sujetos del 1 al 6
for sub in range(1, 7):
    # Filtrar los datos para el sujeto actual, 'luminance' yes
    filtered_data = data_all_resampled[(data_all_resampled['sub'] == sub) &
                                       (data_all_resampled['luminance'] == 'yes')]

    # Verificar si el DataFrame filtrado no está vacío
    if not filtered_data.empty:
        # Asegurar que 'continuous_annotation_luminance' y 'stim_value' están en formato de listas
        filtered_data['continuous_annotation_luminance'] = filtered_data['continuous_annotation_luminance'].apply(eval)
        filtered_data['stim_value'] = filtered_data['stim_value'].apply(eval)

        # Iterar sobre cada fila filtrada para generar gráficos combinados
        for index, row in filtered_data.iterrows():
            luminance_values = []
            luminance_times = []

            for value, time in row['continuous_annotation_luminance']:
                luminance_values.append(value)
                luminance_times.append(time)

            stim_values = [value for value, time in row['stim_value']]  # Separar los valores de los tiempos en 'stim_value'

            # Obtener la longitud mínima
            min_length = min(len(luminance_values), len(stim_values))

            # Acortar las listas a la longitud mínima
            luminance_values = luminance_values[:min_length]
            luminance_times = luminance_times[:min_length]
            stim_values = stim_values[:min_length]

            # Obtener el ID del video
            video_id = row['id']

            # Graficar 'continuous_annotation_luminance' y 'stim_value' en el mismo gráfico
            plt.figure(figsize=(10, 6))
            plt.plot(luminance_times, luminance_values, label='Continuous Annotation Luminance', color='#c08c94', linewidth=2)
            plt.plot(luminance_times, stim_values, label='Stim Value', color='#377eb8', linewidth=2)
            plt.title(f"Annotations for sub-{sub:02d}, Video ID: {video_id}", fontsize=14, fontweight='bold')
            plt.xlabel('Time (s)', fontsize=12)
            plt.ylabel('Annotation Value', fontsize=12)
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()

            # Guardar el gráfico en el directorio especificado
            fig_path = os.path.join(figures_dir, f'sub-{sub:02d}_video-{video_id}.png')
            plt.savefig(fig_path)
            plt.close()

            print(f'Gráfico guardado en: {fig_path}')
    else:
        print(f"No hay datos para sub-{sub:02d} con 'luminance' == 'yes'.")

# %%
