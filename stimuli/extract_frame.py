import cv2

# Modality
modality = "2D"
# Ruta del video de entrada
video_path = f"instruction_{modality}_video.mp4"
# Ruta donde guardar la imagen
output_path = "instruction_frame.jpg"

# Abrir el video
cap = cv2.VideoCapture(video_path)

# Verificar que el video se abrió correctamente
if not cap.isOpened():
    print(f"Error: No se pudo abrir el video {video_path}")
    exit()

# Obtener información del video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
duration = total_frames / fps

print(f"El video tiene {total_frames} frames y dura {duration:.2f} segundos")

# Elegir el frame que quieres extraer (por ejemplo, el frame en el segundo 5)
# Puedes cambiar este valor según el frame específico que quieras
frame_time = 5  # segundos
frame_number = int(frame_time * fps)

# Posicionar el video en el frame deseado
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

# Leer el frame
ret, frame = cap.read()

# Verificar que se leyó correctamente
if ret:
    # Guardar el frame como imagen JPG
    cv2.imwrite(output_path, frame)
    print(f"Frame guardado como {output_path}")
else:
    print("Error: No se pudo leer el frame")

# Liberar recursos
cap.release() 