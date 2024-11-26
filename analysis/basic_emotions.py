#%%
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
df = pd.read_csv('data_all_subs_resampled.csv')

# Filtrar los datos para filas con True o False en 'checkbox_Neutral' y id entre 1 y 14
filtered_df = df[(df['checkbox_Neutral'].isin([True, False])) & (df['id'].between(1, 14))]

# Seleccionar solo las columnas relevantes
relevant_columns = ['checkbox_Neutral', 'checkbox_Asco', 'checkbox_Felicidad', 'checkbox_Sorpresa', 'checkbox_Enojo', 'checkbox_Miedo', 'checkbox_Tristeza']
filtered_df = filtered_df[relevant_columns]

# Reemplazar True con 1 y False con 0
binary_df = filtered_df.replace({True: 1, False: 0})

# Crear la matriz de adyacencia basada en coapariciones
adj_matrix_dim = binary_df.T.dot(binary_df)
np.fill_diagonal(adj_matrix_dim.values, 0)

# Calcular el número total de conexiones para cada emoción en adj_matrix_dim
total_connections = adj_matrix_dim.sum(axis=1)

# Traducir las etiquetas al inglés
translation = {
    'Neutral': 'Neutral',
    'Asco': 'Disgust',
    'Felicidad': 'Happiness',
    'Sorpresa': 'Surprise',
    'Enojo': 'Anger',
    'Miedo': 'Fear',
    'Tristeza': 'Sadness'
}

# Crear el grafo desde la matriz de adyacencia
Gd = nx.from_numpy_array(adj_matrix_dim.values)
labels = adj_matrix_dim.columns

# Renombrar los nodos para que coincidan con los nombres traducidos
translated_labels = {i: translation[labels[i].replace('checkbox_', '').capitalize()] for i in range(len(labels))}
Gd = nx.relabel_nodes(Gd, translated_labels)

# Obtener pesos de las aristas
weights2 = nx.get_edge_attributes(Gd, 'weight').values()

# Actualizar el tamaño del nodo basado en el número total de conexiones
node_size = [total_connections[labels[i]] * 500 for i in range(len(labels))]  # Factor incrementado para exagerar

# Plotear el grafo con tamaños de nodos actualizados y etiquetas
fig, ax = plt.subplots(figsize=(30, 25))

# Usar disposición circular para los nodos
pos = nx.circular_layout(Gd)

# Dibujar el grafo con tamaños de nodos actualizados
nx.draw(Gd, pos,
        edgecolors="black",
        node_color='white',
        node_size=node_size,
        width=[i / 1.1 for i in weights2],
        font_weight="bold",
        arrows=False,
        edge_cmap=plt.cm.copper)

# Crear etiquetas que incluyan el nombre y el número total de relaciones
labels_with_counts = {node: f"{node}\n{int(total_connections[labels[i]])}" for i, node in enumerate(translated_labels.values())}
boxes = dict(facecolor='white', alpha=1)

# Dibujar etiquetas dentro de los nodos
pos_nodes = {k: (v[0], v[1]) for k, v in pos.items()}
nx.draw_networkx_labels(Gd, pos=pos_nodes, labels=labels_with_counts, font_size=40, font_color='k',
                        font_family='sans serif', font_weight='normal', alpha=None, bbox=boxes,
                        horizontalalignment='center', verticalalignment='center', ax=None, clip_on=True)

plt.tight_layout()
plt.show()





# %%

# SEGUIR DESDE ACA. Quiero qeu el nodo se dibuje mas grande si tiene mas conexiones totales
# Los labels deberian ser mucho mas grandes y no tener la palabra "checkbox_" en el nombre.
#  Y deberian estar en ingles
# Despues voy a querer crear uno de estos para cada participantec


# %%
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
df = pd.read_csv('data_all_subs_resampled.csv')

# Traducir las etiquetas al inglés
translation = {
    'Neutral': 'Neutral',
    'Asco': 'Disgust',
    'Felicidad': 'Happiness',
    'Sorpresa': 'Surprise',
    'Enojo': 'Anger',
    'Miedo': 'Fear',
    'Tristeza': 'Sadness'
}

# Crear una función para plotear el grafo para un subconjunto de datos
def plot_graph(ax, filtered_df, sub_value):
    # Reemplazar True con 1 y False con 0
    binary_df = filtered_df.replace({True: 1, False: 0})

    # Crear la matriz de adyacencia basada en coapariciones
    adj_matrix_dim = binary_df.T.dot(binary_df)
    np.fill_diagonal(adj_matrix_dim.values, 0)

    # Calcular el número total de conexiones para cada emoción en adj_matrix_dim
    total_connections = adj_matrix_dim.sum(axis=1)

    # Crear el grafo desde la matriz de adyacencia
    Gd = nx.from_numpy_array(adj_matrix_dim.values)
    labels = adj_matrix_dim.columns

    # Renombrar los nodos para que coincidan con los nombres traducidos
    translated_labels = {i: translation[labels[i].replace('checkbox_', '').capitalize()] for i in range(len(labels))}
    Gd = nx.relabel_nodes(Gd, translated_labels)

    # Obtener pesos de las aristas
    edge_weights = nx.get_edge_attributes(Gd, 'weight')

    # Actualizar el tamaño del nodo basado en el número total de conexiones
    node_size = [total_connections[labels[i]] * 2000 for i in range(len(labels))]  # Factor incrementado aún más

    # Actualizar el grosor de las aristas basado en el peso (cantidad de relaciones)
    edge_widths = [weight * 10 for weight in edge_weights.values()]  # Factor incrementado para exagerar

    # Usar disposición circular para los nodos
    pos = nx.circular_layout(Gd)

    # Dibujar el grafo con tamaños de nodos y grosores de aristas actualizados
    nx.draw(Gd, pos,
            ax=ax,
            edgecolors="black",
            node_color='white',
            node_size=node_size,
            width=edge_widths,
            font_weight="bold",
            arrows=False,
            edge_cmap=plt.cm.copper)

    # Crear etiquetas que incluyan el nombre y el número total de relaciones
    labels_with_counts = {node: f"{node}\n{int(total_connections[labels[i]])}" for i, node in enumerate(translated_labels.values())}
    boxes = dict(facecolor='white', alpha=1)

    # Dibujar etiquetas dentro de los nodos
    pos_nodes = {k: (v[0], v[1]) for k, v in pos.items()}
    nx.draw_networkx_labels(Gd, pos=pos_nodes, labels=labels_with_counts, font_size=40, font_color='k',
                            font_family='sans serif', font_weight='normal', alpha=None, bbox=boxes,
                            horizontalalignment='center', verticalalignment='center', ax=ax, clip_on=True)

    # Título del subplot
    ax.set_title(f'Subject {sub_value}', fontsize=60)

# Crear el plot con 6 subplots
fig, axes = plt.subplots(3, 2, figsize=(35, 45))

# Generar plots para cada valor de 'sub' de 1 a 6
for sub_value, ax in zip(range(1, 7), axes.flatten()):
    filtered_df_sub = df[(df['sub'] == sub_value) & (df['checkbox_Neutral'].isin([True, False])) & (df['id'].between(1, 14))]
    filtered_df_sub = filtered_df_sub[relevant_columns]
    plot_graph(ax, filtered_df_sub, sub_value)

plt.tight_layout()
plt.show()


# %%
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Cargar el archivo CSV que contiene todos los participantes ya resampleados
df = pd.read_csv('data_all_subs_resampled.csv')

# Traducir las etiquetas al inglés
translation = {
    'Neutral': 'Neutral',
    'Asco': 'Disgust',
    'Felicidad': 'Happiness',
    'Sorpresa': 'Surprise',
    'Enojo': 'Anger',
    'Miedo': 'Fear',
    'Tristeza': 'Sadness'
}

# Filtrar los datos para filas con True o False en 'checkbox_Neutral' y id entre 1 y 14
filtered_df = df[(df['checkbox_Neutral'].isin([True, False])) & (df['id'].between(1, 14))]

# Seleccionar solo las columnas relevantes
relevant_columns = ['checkbox_Neutral', 'checkbox_Asco', 'checkbox_Felicidad', 'checkbox_Sorpresa', 'checkbox_Enojo', 'checkbox_Miedo', 'checkbox_Tristeza']
filtered_df = filtered_df[relevant_columns]

# Reemplazar True con 1 y False con 0
binary_df = filtered_df.replace({True: 1, False: 0})

# Crear la matriz de adyacencia basada en coapariciones
adj_matrix_dim = binary_df.T.dot(binary_df)
np.fill_diagonal(adj_matrix_dim.values, 0)

# Calcular el número total de conexiones para cada emoción en adj_matrix_dim
total_connections = adj_matrix_dim.sum(axis=1)

# Crear el grafo desde la matriz de adyacencia
Gd = nx.from_numpy_array(adj_matrix_dim.values)
labels = adj_matrix_dim.columns

# Renombrar los nodos para que coincidan con los nombres traducidos
translated_labels = {i: translation[labels[i].replace('checkbox_', '').capitalize()] for i in range(len(labels))}
Gd = nx.relabel_nodes(Gd, translated_labels)

# Obtener pesos de las aristas
edge_weights = nx.get_edge_attributes(Gd, 'weight')

# Actualizar el tamaño del nodo basado en el número total de conexiones
node_size = [total_connections[labels[i]] * 500 for i in range(len(labels))]  # Reducir el tamaño de los nodos

# Actualizar el grosor de las aristas basado en el peso (cantidad de relaciones)
edge_widths = [weight * 2 for weight in edge_weights.values()]  # Menos exagerado

# Plotear el grafo con tamaños de nodos actualizados y etiquetas
fig, ax = plt.subplots(figsize=(30, 25))

# Usar disposición circular para los nodos
pos = nx.circular_layout(Gd)

# Dibujar el grafo con tamaños de nodos y grosores de aristas actualizados
nx.draw(Gd, pos,
        edgecolors="black",
        node_color='white',
        node_size=node_size,
        width=edge_widths,
        font_weight="bold",
        arrows=False,
        edge_cmap=plt.cm.copper)

# Crear etiquetas que incluyan el nombre y el número total de relaciones
labels_with_counts = {node: f"{node}\n{int(total_connections[labels[i]])}" for i, node in enumerate(translated_labels.values())}
boxes = dict(facecolor='white', alpha=1)

# Dibujar etiquetas dentro de los nodos
pos_nodes = {k: (v[0], v[1]) for k, v in pos.items()}
nx.draw_networkx_labels(Gd, pos=pos_nodes, labels=labels_with_counts, font_size=40, font_color='k',
                        font_family='sans serif', font_weight='normal', alpha=None, bbox=boxes,
                        horizontalalignment='center', verticalalignment='center', ax=ax, clip_on=True)

plt.tight_layout()
plt.title('Combined Relationships of All Subjects', fontsize=30)
plt.show()
