#%%
import pandas as pd

def check_resampled_data(file_path):
    # Cargar el archivo CSV
    data = pd.read_csv(file_path)

    # Verificar inconsistencias en el tipo de dato y longitud de las columnas
    columns_to_check = ['continuous_annotation', 'stim_value', 'continuous_annotation_luminance']
    
    inconsistencies = []
    for column in columns_to_check:
        lengths = data[column].apply(lambda x: len(eval(x)) if isinstance(x, str) else 0)
        types = data[column].apply(lambda x: type(eval(x)) if isinstance(x, str) else type(x))
        
        # Verificar si todas las longitudes son iguales
        if len(set(lengths)) != 1:
            inconsistencies.append(f'Inconsistent lengths in column: {column}')
        
        # Verificar si todos los tipos de datos son iguales
        if len(set(types)) != 1:
            inconsistencies.append(f'Inconsistent data types in column: {column}')
    
    if inconsistencies:
        print("Inconsistencies found:")
        for inconsistency in inconsistencies:
            print(inconsistency)
    else:
        print("No inconsistencies found.")

    # Obtener los últimos dos valores de las listas en las filas donde 'luminance' es 'yes'
    filtered_data = data[data['luminance'] == 'yes']
    
    for column in columns_to_check:
        print(f"\nLast two values of '{column}' for rows where 'luminance' is 'yes':")
        last_two_values = filtered_data[column].apply(lambda x: eval(x)[-2:] if isinstance(x, str) else [])
        print(last_two_values.tolist())

if __name__ == "__main__":
    file_path = 'data_all_subs_resampled.csv'
    check_resampled_data(file_path)

# %%
