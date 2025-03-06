#%%
import os

# Directorio a listar (puedes cambiarlo aquí)
directorio = "./instructions_videos/"

# Si el directorio especificado no existe, usar el directorio actual
if not os.path.exists(directorio):
    print(f"Aviso: El directorio {directorio} no existe. Usando el directorio actual.")
    directorio = "./"

# Obtener la lista de archivos
archivos = [f for f in os.listdir(directorio) if os.path.isfile(os.path.join(directorio, f))]

# Guardar los nombres en un archivo de texto
with open("lista_archivos.txt", "w") as archivo_salida:
    for nombre_archivo in archivos:
        archivo_salida.write(nombre_archivo + "\n")

print(f"Se han listado {len(archivos)} archivos en 'lista_archivos.txt'")
# %%
