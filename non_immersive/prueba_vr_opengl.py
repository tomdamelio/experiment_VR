import sys
import cv2
import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import os

# Inicializar Pygame y OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, pygame.OPENGL | pygame.DOUBLEBUF)

# Configurar OpenGL
glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)
glMatrixMode(GL_PROJECTION)
gluPerspective(90, (display[0] / display[1]), 0.1, 100.0)
glMatrixMode(GL_MODELVIEW)

# Crear la esfera para mapear el video equirectangular
def create_sphere(radius, slices, stacks):
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)

# Especifica la ruta absoluta al video 360 equirectangular
video_path = 'C:/Users/Cocudata/experiment_VR/stimuli/calm_videos/VR/901.mp4'  # Reemplaza con la ruta a tu video

# Verificar si el archivo de video existe
if not os.path.isfile(video_path):
    print(f"El archivo de video no existe en la ruta especificada: {video_path}")
    sys.exit()
else:
    print(f"Archivo de video encontrado: {video_path}")

# Cargar el video 360 equirectangular
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error al abrir el video.")
    sys.exit()

# Configurar la textura
texture_id = glGenTextures(1)

def update_texture(frame):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    frame = cv2.flip(frame, 0)  # Voltear verticalmente
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_data = frame.tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, frame.shape[1], frame.shape[0],
                 0, GL_RGB, GL_UNSIGNED_BYTE, frame_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# Variables para el control de rotación
yaw, pitch = 0, 0
mouse_speed = 0.1
last_mouse_pos = None

# Bucle principal
running = True
while running:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame del video. Terminando reproducción.")
        break  # Terminar si no hay más frames

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break

    # Obtener movimiento del ratón para simular rotación de la cabeza
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # Si se mantiene presionado el botón izquierdo
        mouse_pos = pygame.mouse.get_pos()
        if last_mouse_pos is not None:
            dx = mouse_pos[0] - last_mouse_pos[0]
            dy = mouse_pos[1] - last_mouse_pos[1]
            yaw += dx * mouse_speed
            pitch += dy * mouse_speed
        last_mouse_pos = mouse_pos
    else:
        last_mouse_pos = None

    # Limitar el pitch para evitar giros extremos
    pitch = max(-90, min(90, pitch))

    # Actualizar la textura con el frame actual
    update_texture(frame)

    # Limpiar la pantalla y el buffer de profundidad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Aplicar las rotaciones basadas en el movimiento del ratón
    glRotatef(-pitch, 1, 0, 0)
    glRotatef(-yaw, 0, 1, 0)

    # Invertir la esfera para que la textura sea visible desde el interior
    glPushMatrix()
    glScalef(-1.0, 1.0, 1.0)

    # Dibujar la esfera con la textura del frame actual
    glBindTexture(GL_TEXTURE_2D, texture_id)
    create_sphere(radius=50, slices=50, stacks=50)

    glPopMatrix()

    # Actualizar la pantalla
    pygame.display.flip()
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps > 0:
        pygame.time.wait(int(1000 / fps))
    else:
        pygame.time.wait(10)  # Espera 10 ms si no se puede obtener FPS

# Liberar recursos y cerrar el programa
cap.release()
pygame.quit()
sys.exit()
