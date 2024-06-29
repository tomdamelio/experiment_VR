# Experiment VR: Non Immersive Tas
# Author: Tomas D'Amelio

import csv
import os
import random

#for lsl control
import socket
import time

import instructions
import numpy as np
import sounddevice as sd
from exp_params import ExperimentParameters
from psychopy import constants, core, data, event, gui, visual
from psychopy.hardware import keyboard
from psychopy.preferences import prefs
from pylsl import StreamInfo, StreamOutlet
from scipy.io.wavfile import write

    
ExperimentParameters = ExperimentParameters()

# prefs.hardware['audioLib'] = ['PTB']
prefs.hardware['audioLatencyMode'] = 3 

# Get the absolute path of the currently executing script
current_script_path = os.path.abspath(__file__)

# Extract the directory from the absolute path
current_script_dir = os.path.dirname(current_script_path)

# Change the current working directory to the script's directory
os.chdir(current_script_dir)

# Confirm the current working directory has been changed
print("Current working directory:", os.getcwd())

##########################################################################
# Set up LabStreamingLayer stream.
##########################################################################
info = StreamInfo(name='markers', type='Markers', channel_count=1,
                     channel_format='string', source_id='vr-markers')
outlet = StreamOutlet(info)  # Broadcast the stream.

# This is not necessary but can be useful to keep track of markers and the
# events they correspond to.

# Send triggers to test communication.
for _ in range(5):
    outlet.push_sample(['test'])
    core.wait(0.5)

##########################################################################
# GUI for subject information
##########################################################################
info_dict = {
    "ID": "",
    "Sesion": ["A", "B"],
    "Tarea": ["non_immersive", "immersive"],
    "Consumo de sustancias psicoactivas en las últimas 24 hs": ["No", "Sí"],
    "Horas de sueño la noche anterior": ""
}

# Orden de los campos en el formulario
order = [
    "ID", 
    "Sesion", 
    "Consumo de sustancias psicoactivas en las últimas 24 hs", 
    "Horas de sueño la noche anterior"
]

### Para usar el formulario, descomente la siguiente sección. Está comentado para practicidad. ###
# Instantiate dialog box
my_dlg = gui.DlgFromDict(info_dict, title="Experimento sobre Experiencia Emocional", order=order)
if my_dlg.OK is False:
    core.quit()  # El usuario presionó cancelar

info_dict["date"] = data.getDateStr()
exp_name = f"Experiment_VR_{info_dict['Tarea']}"
info_dict['exp_name'] = exp_name

##########################################################################
# Experiment data settings
##########################################################################

# create folder to save experiment data for each subject in BIDS format
subject_folder = os.path.join(ExperimentParameters.results_folder, f"sub-{info_dict['ID']}")
os.makedirs(subject_folder, exist_ok=True)
session_folder = os.path.join(subject_folder,f"ses-{info_dict['Sesion']}")
os.makedirs(session_folder, exist_ok=True)
physio_folder = os.path.join(session_folder,"physio")
os.makedirs(physio_folder, exist_ok=True)
behavioral_folder = os.path.join(session_folder,"beh")
os.makedirs(behavioral_folder, exist_ok=True)
audio_folder =  os.path.join(behavioral_folder, 'audios')
os.makedirs(audio_folder, exist_ok=True)

# Name of .csv file to save the data
beh_file_name = f"sub-{info_dict['ID']}_ses-{info_dict['Sesion']}_task-{exp_name}_beh"
physio_file_name = f"sub-{info_dict['ID']}_ses-{info_dict['Sesion']}_task-{exp_name}_physio"
#audio_file_name = f"sub-{info_dict['ID']}_ses-{info_dict['Sesion']}_task-{exp_name}_audio"


##########################################################################
# Initialize LSL recording
##########################################################################
# Construct the command to send to LSL App Recorder
# Note: You might need to adjust the path to match your exact folder structure
modality = 'physio'
command = f"filename {{root:C:/Users/Cocudata/experiment_VR/results/}} {{template:sub-%p/ses-%s/{modality}/{physio_file_name}.xdf}}  {{participant:{info_dict['ID']}}} {{session:{info_dict['Sesion']}}} {{task:{exp_name}}} {{modality: {modality}}}\n"
# Send commands to LSL App Recorder
#s = socket.create_connection(("localhost", 135))
s = socket.create_connection(("localhost", 22345))
s.sendall(b"update\n")
s.sendall(b"select all\n")
s.sendall(command.encode())  # Convert the command string to bytes
s.sendall(b"start\n")

#########################################################################
# Create experiment handler
exp = data.ExperimentHandler(name= exp_name,
                            extraInfo=info_dict,
                            runtimeInfo=True,
                            originPath='./non_immersive_experiment.py',
                            savePickle=True,
                            saveWideText=True,
                            dataFileName= os.path.join(behavioral_folder, beh_file_name)
)


#%%

##########################################################################

# Diccionario para definir los sliders y su configuración
sliders_dict = {
    "valence": {
        "slider_position": (0, 10),
        "left_image_path": "./images_scale/valence_left.png",
        "right_image_path": "./images_scale/valence_right.png",
        "left_text": "",
        "right_text": "",
    },
    "arousal": {
        "slider_position": (0, 7),
        "left_image_path": "./images_scale/arousal_left.png",
        "right_image_path": "./images_scale/arousal_right.png",
        "left_text": "",
        "right_text": "",
    },
    "preference": {
        "slider_position": (0, 4),
        "left_image_path": "./images_scale/preference_left.png",
        "right_image_path": "./images_scale/preference_right.png",
        "left_text": "Completo desagrado",
        "right_text": "Completo agrado",
    },
    "engagement": {
        "slider_position": (0, 1),
        "left_image_path": None,
        "right_image_path": None,
        "left_text": "No presté atención",
        "right_text": "Presté completa atención",
    },
    "familiarity": {
        "slider_position": (0, -2),
        "left_image_path": None,
        "right_image_path": None,
        "left_text": "Nunca habia visto este video antes",
        "right_text": "Conozco este video muy bien",
    },
    "FMS": {
        "slider_position": (0, -5),
        "left_image_path": None,
        "right_image_path": None,
        "left_text": "sin síntomas de mareo",
        "right_text": "síntomas extremadamente severos de mareo",
    },
    "luminance": {
        "slider_position": None,
        "left_image_path": "./images_scale/non_bright_left.png",
        "right_image_path": "./images_scale/bright_right.png",
        "left_text": "",
        "right_text": "",
    },
}


def mostrar_sliders_y_recoger_respuestas(win, outlet, sliders_dict, trials):
    sliders = []

    # Crear y dibujar los sliders y las imágenes asociadas
    for slider_name, slider_info in sliders_dict.items():
        if slider_name == "luminance":
            continue
        # print(slider_name)
        # print(slider_info)
        # Crear el slider
        slider_info["slider"] = visual.Slider(
            win=win,
            name=slider_name,
            ticks=(-1, 1),
            pos=slider_info["slider_position"],
            size=(8, 0.25),
            labels=[slider_info["left_text"], " ", slider_info["right_text"]],
            labelHeight=0.5,
            style=["slider"],
            granularity=0.1,
            color="white",
            font="Helvetica",
            lineColor="white",
            fillColor="white",
            borderColor="white",
            markerColor="white",
        )
        sliders.append(slider_info["slider"])

        # print(slider_info["left_image_path"])
        # print(slider_info["slider_position"][1])

        # Determinar si se debe cargar una imagen o usar texto para cada lado
        slider_info["left_image"] = visual.ImageStim(
            win,
            image=slider_info["left_image_path"],
            pos=(-5, slider_info["slider_position"][1]),
            size=1.3,
        )

        slider_info["right_image"] = visual.ImageStim(
            win,
            image=slider_info["right_image_path"],
            pos=(-5, slider_info["slider_position"][1]),
            size=1.3,
        )

    # Inicializa la ventana gráfica
    win.flip()

    # Define las posiciones de las casillas de verificación en la parte inferior de la pantalla
    checkbox_positions = [
        (x, -9) for x in range(-10, 10, 3)
    ]  # Genera posiciones a lo largo del eje x con un espaciado de 3

    # Define las emociones básicas y su estado inicial (no seleccionado)
    basic_emotions = [
        "Neutral",
        "Asco",
        "Felicidad",
        "Sorpresa",
        "Enojo",
        "Miedo",
        "Tristeza",
    ]
    emotion_states = {emotion: False for emotion in basic_emotions}

    # Crea rectángulos y etiquetas para las casillas de verificación
    checkbox_rects = []
    checkbox_labels = []
    for pos, emotion in zip(checkbox_positions, basic_emotions):
        rect = visual.Rect(
            win, width=0.5, height=0.5, pos=pos, lineColor="white", fillColor=None
        )
        checkbox_rects.append(rect)
        label = visual.TextStim(
            win, text=emotion, pos=(pos[0], pos[1] - 0.7), height=0.5
        )
        checkbox_labels.append(label)

    # Crear un slider_thumb para cada slider antes del bucle
    for slider_name, slider_info in sliders_dict.items():
        if slider_name == "luminance":
            continue
        slider_info["left_image"] = visual.ImageStim(
            win,
            image=slider_info["left_image_path"],
            pos=(-5, slider_info["slider_position"][1] + 0.5),
            size=1.3,
        )
        slider_info["right_image"] = visual.ImageStim(
            win,
            image=slider_info["right_image_path"],
            pos=(5, slider_info["slider_position"][1] + 0.5),
            size=1.3,
        )
        slider_y = slider_info["slider_position"][1]
        slider_info["slider_thumb"] = visual.Circle(
            win,
            radius=0.30,
            fillColor="white",
            lineColor="black",
            edges=32,
            pos=(0, slider_y),
        )

    # Iniciar el bucle de evento para la interacción del usuario
    mouse = event.Mouse(win=win)
    event.clearEvents()

    win.flip()
    outlet.push_sample(["self_report_post_start"])

    user_interacting = (
        True  # Una nueva variable para controlar la interacción del usuario
    )

    while user_interacting:
        # Obtener la posición actual del ratón en cada iteración del bucle
        mouse_x, mouse_y = mouse.getPos()
        iteration_counter = 0  # Inicializa el contador

        for slider_name, slider_info in sliders_dict.items():
            if slider_name == "luminance":
                continue
            slider = slider_info["slider"]
            slider.draw()
            slider_thumb = slider_info["slider_thumb"]
            slider_x, slider_y = slider.pos
            slider_width, slider_height = slider.size
            slider_start = slider_x - slider_width / 2
            #slider_end = slider_x + slider_width / 2

            # Condición para dibujar intensity_cue_image solo en las dos primeras iteraciones
            if iteration_counter < 2:
                intensity_cue_image_scale = visual.ImageStim(
                    win,
                    image="./images_scale/AS_intensity_cue.png",
                    pos=(0, -8.7),
                    size=(8, 0.6),
                )
                intensity_cue_image_scale.pos = (0, slider_y - 1.0)
                intensity_cue_image_scale.draw()

            # Dibujar la imagen o el texto izquierdo
            if "left_image" in slider_info:
                slider_info["left_image"].draw()
            else:
                slider_info["left_text"].draw()

            # Dibujar la imagen o el texto derecho
            if "right_image" in slider_info:
                slider_info["right_image"].draw()
            else:
                slider_info["right_text"].draw()

            iteration_counter += 1

            # Dibujar el thumb del slider
            slider_thumb.draw()

            if mouse.getPressed()[0]:
                # mouse_x, mouse_y = mouse.getPos()
                # Comprobar si el ratón está sobre el slider o su thumb
                if (
                    slider_x - slider_width / 2
                    <= mouse_x
                    <= slider_x + slider_width / 2
                    and slider_y - slider_height / 2
                    <= mouse_y
                    <= slider_y + slider_height / 2
                ):
                    if mouse.getPressed()[
                        0
                    ]:  # Si se presiona el botón izquierdo del ratón
                        norm_pos = (mouse_x - slider_start) / slider_width
                        slider_value = (
                            norm_pos * (slider.ticks[-1] - slider.ticks[0])
                            + slider.ticks[0]
                        )
                        slider.markerPos = slider_value
                        # Asegurarse de que la posición del thumb refleje la posición del marcador
                        thumb_pos_x = (slider.markerPos - slider.ticks[0]) / (
                            slider.ticks[-1] - slider.ticks[0]
                        ) * slider_width + slider_start
                        slider_thumb.setPos((thumb_pos_x, slider_y))

        mensaje = "Por favor indicá cómo te sentiste al ver este video"
        text_stim = visual.TextStim(win, text=mensaje, height=0.6, pos=(0, 13))

        # Para dibujar el estímulo de texto
        text_stim.draw()

        # Dibujar las casillas de verificación y sus etiquetas
        for rect, label in zip(checkbox_rects, checkbox_labels):
            rect.draw()
            label.draw()

        # Detectar clics del ratón
        if mouse.getPressed()[
            0
        ]:  # Verifica si el botón izquierdo del ratón está presionado
            mouse_click_position = mouse.getPos()
            for i, rect in enumerate(checkbox_rects):
                if rect.contains(mouse_click_position):
                    emotion = basic_emotions[i]
                    emotion_states[emotion] = not emotion_states[
                        emotion
                    ]  # Cambia el estado de la emoción
                    rect.fillColor = (
                        "grey" if emotion_states[emotion] else None
                    )  # Retroalimentación visual
                    break  # Procesar un solo clic a la vez

            # Reinicia el estado del clic del ratón para evitar detecciones múltiples del mismo clic
            while any(mouse.getPressed()):
                pass  # Espera hasta que todos los botones del ratón se liberen

        # Asegurarse de actualizar la ventana para reflejar los cambios
        win.flip()

        # Verificar si se presiona una tecla para finalizar la interacción del usuario
        keys = event.getKeys()
        if keys:
            user_interacting = False  # El usuario ha terminado de interactuar

        #   
    #        # Antes de finalizar la interacción del usuario, comprueba que se cumplan las condiciones
    #        all_sliders_rated = all(slider.getRating() is not None for slider in sliders)  # Verifica si todos los sliders tienen una valoración
    #        any_emotion_checked = any(emotion_states.values())  # Verifica si al menos una emoción está marcada
    #
    #        if all_sliders_rated and any_emotion_checked:
    #            user_interacting = False  # El usuario ha completado la interacción requerida
    #
    #        # Verificar si se presiona una tecla para finalizar la interacción del usuario
    #        keys = event.getKeys()
    #
    #        if not all_sliders_rated:
    #            print("Por favor, proporciona una valoración para cada dimensión.")
    #        elif not any_emotion_checked:
    #            print("Por favor, selecciona al menos una emoción.")
    #        else:
    #            user_interacting = False
    #
    #    # To begin the Experimetn with Spacebar or RightMouse Click
    #    press_space = True
    #    while press_space:
    #        keys = event.getKeys(keyList=['space'])
    #        if 'space' in keys:
    #            press_space = False

    # Una vez finalizada la interacción del usuario, recoger y guardar los datos
    for slider_name, slider_info in sliders_dict.items():
        if slider_name == "luminance":
            continue
        slider_value = slider_info["slider"].getRating()
        trials.addData(f"{slider_name}_value", slider_value)

    # Guardar los estados de las casillas de verificación
    for emotion, rect in zip(basic_emotions, checkbox_rects):
        trials.addData(f"checkbox_{emotion}", emotion_states[emotion])

    # Inter Trial Interval(ITI) con pantalla en blanco
    win.flip()
    outlet.push_sample(["self_report_post_end"])


def show_instructions_relative_trial(
    dimension, outlet, hand, win, params, sliders_dict, order_emojis_slider="normal"
):
    """
    Presenta las instrucciones al participante basadas en la dimensión, la mano usada, y muestra la escala correspondiente.

    :param dimension: La dimensión de la emoción o sensación a reportar (e.g., "arousal", "valence").
    :param hand: La mano que el participante usará para reportar, "left" o "right".
    :param win: La ventana de PsychoPy donde se presentarán las instrucciones.
    :param params: Diccionario de parámetros, incluyendo 'text_height' para la altura del texto.
    :param sliders_dict: Diccionario con información sobre los sliders, incluidas las rutas de las imágenes.
    :param order_emojis_slider: Orden de los emojis en el slider, puede ser "normal" o "inverse".
    """

    # Traducir "left" y "right" a "izquierda" y "derecha"
    mano = "izquierda" if hand == "left" else "derecha"
    # Traducir "left" y "right" a "izquierda" y "derecha"
    if dimension == "valence":
        dimension_traducida = "tu valencia"
    elif dimension == "arousal":
        dimension_traducida = "tu activación"
    elif dimension == "luminance":
        dimension_traducida = "el brillo"

    instruction_trial = (
        f"Ahora vas a reportar continuamente {dimension_traducida} mientras ves el video. \n\n"
        f"Vas a usar tu mano {mano} para indicar esto en la escala de abajo. \n\n"
        "Por favor, presioná la barra espaciadora para comenzar."
    )

    # Crear y presentar las instrucciones generales
    instruction_general = visual.TextStim(
        win,
        height=ExperimentParameters.text_height,
        pos=[0, 0.5],
        text=instruction_trial,
        wrapWidth=80,
    )
    instruction_general.draw()

    # Determinar las rutas de las imágenes basadas en la 'dimension'
    slider_info = sliders_dict.get(dimension, {})

    # Preparar las imágenes de la escala para mostrar
    if order_emojis_slider == "inverse":
        left_image_path = slider_info.get("right_image_path")
        right_image_path = slider_info.get("left_image_path")
    else:
        left_image_path = slider_info.get("left_image_path")
        right_image_path = slider_info.get("right_image_path")

    if left_image_path and right_image_path:  # Asegurar que ambas rutas estén definidas
        left_image = visual.ImageStim(
            win, image=left_image_path, pos=(-5, -8.4), size=1.3
        )
        right_image = visual.ImageStim(
            win, image=right_image_path, pos=(5, -8.4), size=1.3
        )
        left_image.draw()
        right_image.draw()

    dimension_slider = visual.Slider(
        win=win,
        name="dimension",
        ticks=(-1, 1),
        labels=None,
        pos=(0, -8.1),
        size=(8, 0.25),
        style=["slider"],
        granularity=0.1,
        color="white",
        font="Helvetica",
        lineColor="white",
        fillColor="white",
        borderColor="white",
        markerColor="white",
    )

    dimension_slider.draw()

    ## Create a custom white circle as the slider thumb
    slider_thumb = visual.Circle(
        win, pos=(0, -8.1), radius=0.30, fillColor="white", lineColor="black", edges=32
    )
    slider_thumb.draw()

    intensity_cue_image = visual.ImageStim(
        win, image="./images_scale/AS_intensity_cue.png", pos=(0, -8.7), size=(8, 0.6)
    )
    intensity_cue_image.draw()

    second_word = (
        dimension_traducida.split()[1]
        if len(dimension_traducida.split()) > 1
        else dimension_traducida
    )
    dimension_text = visual.TextStim(
        win, height=params.text_height, pos=[0, -9.4], text=second_word, wrapWidth=50
    )
    dimension_text.draw()

    hand_image_path = (
        "./images_scale/right_hand.png"
        if hand == "right"
        else "./images_scale/left_hand.png"
    )
    hand_image_pos = (
        (10, -10) if hand == "right" else (-10, -10)
    )  # Cambiar el '5' por el valor que se ajuste a tu pantalla
    hand_image = visual.ImageStim(
        win, image=hand_image_path, pos=hand_image_pos, size=(5, 5)
    )
    hand_image.draw()

    # Flip the front and back buffers para mostrar las instrucciones y las imágenes
    win.flip()
    outlet.push_sample(["instruction_start"])

    # To begin the Experimetn with Spacebar or RightMouse Click
    press_button = True
    while press_button:
        keys = event.getKeys(keyList=["space"])

        mouse = event.Mouse(visible=True, win=win)
        mouse_click = mouse.getPressed()

        if "space" in keys or 1 in mouse_click:
            press_button = False
            outlet.push_sample(["instruction_end"])
            

    return left_image, right_image


def show_instructions_absolute(
    value="valence_practice_instructions_text", outlet=outlet, params=ExperimentParameters, dimension=None
):
    """
    Displays instructions on the screen and waits for the user to press the spacebar
    to continue.

    Parameters:
    - win: The window object where the instructions will be displayed.
    - params: A dictionary containing parameters like text height.
    - value: indicates the text to be desplayed.
    """

    win.flip()
    
    # Traducir "left" y "right" a "izquierda" y "derecha"
    if dimension == "valence":
        dimension_traducida = "tu valencia"
    elif dimension == "arousal":
        dimension_traducida = "tu activación"
    elif dimension == "luminance":
        dimension_traducida = "el brillo"

    # Access the specific instruction text for verbal reports
    instruction_text = instructions.non_immersive_instructions_text[value]

    # Create a text stimulus for the verbal report instructions
    instructions_txt = visual.TextStim(
        win,
        height=params.text_height,
        pos=[0, 2],
        text=instruction_text,
        wrapWidth=80,
    )

    # Draw the text on the window
    instructions_txt.draw()
    outlet.push_sample(["instruction_start"])

    if dimension is not None:
        # Determinar las rutas de las imágenes basadas en la 'dimension'
        slider_info = sliders_dict.get(dimension, {})

        left_image_path = slider_info.get("left_image_path")
        right_image_path = slider_info.get("right_image_path")

        if (
            left_image_path and right_image_path
        ):  # Asegurar que ambas rutas estén definidas
            left_image = visual.ImageStim(
                win, image=left_image_path, pos=(-5, -8.4), size=1.3
            )
            right_image = visual.ImageStim(
                win, image=right_image_path, pos=(5, -8.4), size=1.3
            )
            left_image.draw()
            right_image.draw()

        dimension_slider = visual.Slider(
            win=win,
            name="dimension",
            ticks=(-1, 1),
            labels=None,
            pos=(0, -8.1),
            size=(8, 0.25),
            style=["slider"],
            granularity=0.1,
            color="white",
            font="Helvetica",
            lineColor="white",
            fillColor="white",
            borderColor="white",
            markerColor="white",
        )

        dimension_slider.draw()

        ## Create a custom white circle as the slider thumb
        slider_thumb = visual.Circle(
            win,
            pos=(0, -8.1),
            radius=0.30,
            fillColor="white",
            lineColor="black",
            edges=32,
        )
        slider_thumb.draw()

        intensity_cue_image = visual.ImageStim(
            win,
            image="./images_scale/AS_intensity_cue.png",
            pos=(0, -8.7),
            size=(8, 0.6),
        )
        intensity_cue_image.draw()

        second_word = (
            dimension_traducida.split()[1]
            if len(dimension_traducida.split()) > 1
            else dimension_traducida
        )
        dimension_text = visual.TextStim(
            win,
            height=params.text_height,
            pos=[0, -9.4],
            text=second_word,
            wrapWidth=50,
        )
        dimension_text.draw()

    # Update the display to show the drawn text
    win.flip()
    
    user_interacting = (
        True  # Una nueva variable para controlar la interacción del usuario
    )

    while user_interacting:
        # Wait for the user to press the spacebar
        event.waitKeys(keyList=["space"])
        
    user_interacting = False
    outlet.push_sample(["instruction_end"])


##########################################################################
# Create a window
win = visual.Window(
    allowGUI=None,
    size=ExperimentParameters.display_size,
    monitor="testMonitor",
    winType="pyglet",
    useFBO=True,
    # units='pix',Fpg
    units="deg",
    fullscr=ExperimentParameters.fullscreen,
    color="black",
)

info_dict["frame_rate"] = win.getActualFrameRate()

exp_info = {
    "fullscreen": ExperimentParameters.fullscreen,
#    "main_screen": ExperimentParameters["main_screen"],
    "display_size": ExperimentParameters.display_size,
}
exp_info.update(info_dict)

# setting keyboard for experiment
kb = keyboard.Keyboard()

############## TO RUN IN MAC AND LINUX ##############
# if os.name == 'posix':
#     launchHubServer(window=win)

#####################################################

##########################################################################
########                    PRACTICE BLOCK                        ########
##########################################################################

def log_mouse_and_time(mov, outlet=outlet ,first_iteration_aux=False):
    global mouse_x, current_time, video_start_time  # Define globales que se manipulan
    mov.draw()  # Asegúrate de que mov es un objeto que se pueda dibujar
    if first_iteration_aux:
        video_start_time = core.getTime()
        outlet.push_sample(['video_start'])  # Marca el inicio del video
    mouse_x, _ = mouse.getPos()
    current_time = core.getTime() - video_start_time


# Create practice instructions ('text' visual stimuli)
show_instructions_absolute("welcome_text")

win.flip()

show_instructions_absolute("baseline_instructions_text")

# Crear la cruz de fijación
fixation = visual.TextStim(win, text='+', pos=(0, 0), color='white')

# Limpiar todos los eventos acumulados
event.clearEvents()

# Marcar el inicio de la recolección de datos
outlet.push_sample(['baseline_start'])

# Mostrar la cruz de fijación y comenzar el período de baseline
fixation.draw()
win.flip()  # Actualizar la ventana para mostrar la cruz

# Esperar 10 segundos de manera precisa
core.wait(3)

# Marcar el fin de la recolección de datos
outlet.push_sample(['baseline_end'])

# Limpiar la pantalla (opcional, dependiendo de lo que necesites a continuación)
win.flip()


# Cargar imágenes para los extremos y el marcador del slider
intensity_cue_image = visual.ImageStim(
    win, image="./images_scale/AS_intensity_cue.png", pos=(0, -8.7), size=(8, 0.6)
)

## Initialize the slider
dimension_slider = visual.Slider(
    win=win,
    name="dimension",
    ticks=(-1, 1),
    labels=None,
    pos=(0, -8.1),
    size=(8, 0.25),
    style=["slider"],
    granularity=0.1,
    color="white",
    font="Helvetica",
    lineColor="white",
    fillColor="white",
    borderColor="white",
    markerColor="white",
)

# Check if the file exists
file_path = "../conditions/non_immersive_practice_conditions.csv"
#file_path = "../conditions_test_2/non_immersive_practice_conditions.csv"

try:
    with open(file_path, mode="r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        trialList = list(reader)
        print(f"Successfully read {len(trialList)} trials from the file.")
        # If successfully read, proceed to create the trial handler
        practice_trials = data.TrialHandler(
            trialList=trialList, nReps=1, method="sequential", name="practice"
        )
except Exception as e:
    print(f"Failed to read CSV file: {e}")
exp.addLoop(practice_trials)

practice_trial_number = 1

for trial in practice_trials:
    
    # Inicialización de elementos visuales
    mov = visual.MovieStim3(
            win=win,
            filename=trial["movie_path"],
            size=(1920, 1080),
            pos=[0, 0],
            noAudio=False,
    )
    
    if practice_trial_number == 1:
        show_instructions_absolute(
            "valence_practice_instructions_text", outlet, dimension=trial["dimension"]
        )
    elif practice_trial_number == 2:
        show_instructions_absolute(
            "arousal_practice_instructions_text", outlet, dimension=trial["dimension"]
        )
    elif practice_trial_number == 3:
        show_instructions_absolute("left_right_alternance_instructions_text")

    
    left_image, right_image = show_instructions_relative_trial(
        trial["dimension"],
        outlet,
        trial["hand"],
        win,
        ExperimentParameters,
        sliders_dict,
        order_emojis_slider=trial["order_emojis_slider"],
    )

    # Usar 'Dimension' del trial para determinar las rutas de las imágenes
    if trial["dimension"] in sliders_dict:
        slider_info = sliders_dict[trial["dimension"]]

    # Invertir las imágenes si 'order_emojis_slider' es 'inverse'
    if "order_emojis_slider" in trial and trial["order_emojis_slider"] == "inverse":
        # Verificar si hay rutas de imagen definidas y crear los estímulos de imagen invertidos
        if (
            slider_info["right_image_path"] is not None
            and slider_info["left_image_path"] is not None
        ):
            left_image = visual.ImageStim(
                win, image=slider_info["right_image_path"], pos=(-5, -8.4), size=1.3
            )
            right_image = visual.ImageStim(
                win, image=slider_info["left_image_path"], pos=(5, -8.4), size=1.3
            )
    else:
        # Verificar si hay rutas de imagen definidas y crear los estímulos de imagen normales
        if slider_info["left_image_path"] is not None:
            left_image = visual.ImageStim(
                win, image=slider_info["left_image_path"], pos=(-5, -8.4), size=1.3
            )
        if slider_info["right_image_path"] is not None:
            right_image = visual.ImageStim(
                win, image=slider_info["right_image_path"], pos=(5, -8.4), size=1.3
            )

    # Dibujar las imágenes
    if slider_info["left_image_path"] is not None:
        left_image.draw()
    if slider_info["right_image_path"] is not None:
        right_image.draw()
    else:
        print(
            "La dimensión del trial no está definida en sliders_dict:",
            trial["dimension"],
        )
        continue  #

    # Restablecer el deslizador de valencia para el nuevo ensayo
    dimension_slider.reset()
    dimension_slider.markerPos = 0  # Establecer la posición inicial del marcador

    # Obtener objeto del ratón y hacerlo visible
    mouse = event.Mouse(visible=True, win=win)
    mouse.setPos(newPos=(0, dimension_slider.pos[1]))

    # Calculate the range in pixels for the slider
    slider_start = dimension_slider.pos[0] - (dimension_slider.size[0] / 2)
    #slider_end = dimension_slider.pos[0] + (dimension_slider.size[0] / 2)

    dimension_slider.name = trial["dimension"]

    left_image.draw()
    right_image.draw()
    intensity_cue_image.draw()
    dimension_slider.draw()

    ## Create a custom white circle as the slider thumb
    slider_thumb = visual.Circle(
        win,
        pos=(0, -8.4),
        radius=0.30,
        fillColor="white",
        lineColor="black",
        edges=32,
    )
    slider_thumb.draw()

    print(trial["movie_path"])

    event.clearEvents()
    
    # Inicializar el array de NumPy para anotaciones del ratón
    mouse_annotation = np.empty((0, 2), dtype=float)  # Array vacío con dos columnas
    
    first_iteration = True
    
    while mov.status != constants.FINISHED:
                    
        left_image.draw()
        right_image.draw()
        intensity_cue_image.draw()
        dimension_slider.draw()
        slider_thumb.draw()
        
        win.callOnFlip(log_mouse_and_time, mov, outlet, first_iteration_aux=first_iteration)
        win.flip()
        
        if first_iteration:
            first_iteration = False
        
        if mouse_x < -4:
            slider_value = -1
        elif mouse_x > 4:
            slider_value = 1
        else:
            norm_pos = (mouse_x - slider_start) / dimension_slider.size[0]
            slider_value = norm_pos * (dimension_slider.ticks[-1] - dimension_slider.ticks[0]) + dimension_slider.ticks[0]
            dimension_slider.markerPos = round(slider_value, 2)
        
        # Agregar datos al array de NumPy
        new_data = np.array([[slider_value, current_time]])
        mouse_annotation = np.vstack((mouse_annotation, new_data))
        
        last_time_reported = current_time

        thumb_pos_x = (dimension_slider.markerPos - dimension_slider.ticks[0]) / (dimension_slider.ticks[-1] - dimension_slider.ticks[0]) * dimension_slider.size[0] - (dimension_slider.size[0] / 2)
        slider_thumb.setPos([thumb_pos_x, dimension_slider.pos[1]])

        keys = event.getKeys(keyList=["escape", "p"])
        if "escape" in keys:
            win.close()
            core.quit()
        if "p" in keys:
            mov.stop()
            break  # Salir del bucle
    
    outlet.push_sample(['video_end'])
    core.wait(0.5)
    # Convertir el array de NumPy a una lista de listas
    mouse_annotation_list = mouse_annotation.tolist()
    exp.addData("continuous_annotation", mouse_annotation_list)
    exp.addData("video_duration", mov.duration)

    if practice_trial_number <= 3:
        if practice_trial_number == 1:
            show_instructions_absolute("post_stimulus_self_report_text_1")
            show_instructions_absolute("post_stimulus_self_report_text_2")
            show_instructions_absolute("post_stimulus_self_report_text_3")

        win.flip()
        # Crear el estímulo de texto para el mensaje de carga
        loading_text_stim = visual.TextStim(
            win, text="Cargando escalas...", height=ExperimentParameters.text_height, pos=[0, 0]
        )

        # Dibujar el estímulo de texto en la ventana
        loading_text_stim.draw()

        # Mostrar la ventana con el mensaje de carga
        win.flip()

        # Mantener el mensaje en pantalla por 0.5 segundos
        core.wait(0.5)

        mostrar_sliders_y_recoger_respuestas(win, outlet, sliders_dict, practice_trials)

        # Siguiente entrada del registro de datos
        core.wait(ExperimentParameters.iti)

        if practice_trial_number == 1:
            show_instructions_absolute(
                "luminance_practice_instructions_text", outlet, dimension="luminance"
            )

        left_image, right_image = show_instructions_relative_trial(
            "luminance",
            outlet,
            trial["hand"],
            win,
            ExperimentParameters,
            sliders_dict,
            order_emojis_slider=trial["order_emojis_slider"],
        )
        # Cambiar las posiciones a (0, 1)
        left_image.pos = (-5, -8.4)
        right_image.pos = (5, -8.4)
        slider_thumb.pos = (0, -8.1)

        # Restablecer el deslizador de valencia para el nuevo ensayo
        dimension_slider.reset()
        dimension_slider.markerPos = 0  # Establecer la posición inicial del marcador
        
        # Convertir mouse_annotation_aux a una matriz de numpy para facilitar las búsquedas
        mouse_annotation_aux_np = mouse_annotation

        # Inicialización
        mouse_annotation_green = np.empty((0, 2), dtype=float) 
        stim_value = np.empty((0, 2), dtype=float) 
        stim_value_green = np.empty((0, 2), dtype=float) 
    
        # Obtener objeto del ratón y hacerlo visible
        mouse = event.Mouse(visible=True, win=win)
        mouse.setPos(newPos=(0, dimension_slider.pos[1]))

        # Calculate the range in pixels for the slider
        slider_start = dimension_slider.pos[0] - (dimension_slider.size[0] / 2)
        #slider_end = dimension_slider.pos[0] + (dimension_slider.size[0] / 2)

        event.clearEvents()                   
                                    
        cronometro = core.Clock()
        green_screen_start_time = cronometro.getTime()
        
        outlet.push_sample(['luminance_start'])
        
        # Bucle hasta que el tiempo transcurrido sea mayor que la duración del video
        while cronometro.getTime() - green_screen_start_time <= last_time_reported:
            tiempo_actual = cronometro.getTime() - green_screen_start_time

            # Encontrar el índice del valor de tiempo más cercano en mouse_annotation_aux
            idx = np.abs(mouse_annotation_aux_np[:, 1] - tiempo_actual).argmin()
            valor_cercano, _ = mouse_annotation_aux_np[idx]

            if trial["order_emojis_slider"] == "inverse":
                valor_cercano = -valor_cercano

            # Ajustar valor de intensidad verde según el valor más cercano encontrado
            green_intensity = ((valor_cercano + 1) / 2) * (255 - 25) + 25

            # Establecer el color de la ventana y dibujar todos los elementos
            win.setColor([20, green_intensity, 12], "rgb255")
            left_image.draw()
            right_image.draw()
            intensity_cue_image.draw()
            dimension_slider.draw()
            slider_thumb.draw()

            mouse_x, _ = mouse.getPos()
            tiempo_actual_real = cronometro.getTime() - green_screen_start_time

            # Verificar si mouse_x está fuera del rango a la izquierda (-4)
            if mouse_x < -4:
                slider_value_green = -1
            # Verificar si mouse_x está fuera del rango a la derecha (4)
            elif mouse_x > 4:
                slider_value_green = 1
            else:
                # Calcular norm_pos dentro del rango permitido
                norm_pos = (mouse_x - slider_start) / dimension_slider.size[0]
                # Calcular slider_value basado en norm_pos dentro del rango permitido
                slider_value_green = (
                    norm_pos
                    * (dimension_slider.ticks[-1] - dimension_slider.ticks[0])
                    + dimension_slider.ticks[0]
                )
                dimension_slider.markerPos = round(slider_value_green, 2)

            # Manejar la salida anticipada
            keys = event.getKeys()
            if "escape" in keys:
                win.close()
                core.quit()
            if "p" in keys:  # Verificar si se presionó la tecla "p"
                break  # Salir del bucle while, finalizando la reproducción del video
            
            # Agregar datos al array de NumPy
            new_data_mouse_annotation_green = np.array([[slider_value_green, tiempo_actual_real]])
            mouse_annotation_green = np.vstack((mouse_annotation_green, new_data_mouse_annotation_green))
            
            # Agregar datos al array de NumPy
            new_data_stim_value_green = np.array([[green_intensity, tiempo_actual_real]])
            stim_value_green = np.vstack((stim_value_green, new_data_stim_value_green))
            
            # Agregar datos al array de NumPy
            new_data_stim_value = np.array([[valor_cercano, tiempo_actual_real]])
            stim_value = np.vstack((stim_value, new_data_stim_value))

            thumb_pos_x = (
                dimension_slider.markerPos - dimension_slider.ticks[0]
            ) / (
                dimension_slider.ticks[-1] - dimension_slider.ticks[0]
            ) * dimension_slider.size[0] - (dimension_slider.size[0] / 2)
            slider_thumb.setPos([thumb_pos_x, dimension_slider.pos[1]])

            win.flip()

        outlet.push_sample(['luminance_end'])
        
        # Continuar con el código para restablecer el color de fondo y guardar las anotaciones
        win.setColor("black")
        win.flip()

        # Guardar anotaciones interpoladas al final del ensayo
        # Convertir el array de NumPy a una lista de listas
        mouse_annotation_green_list = mouse_annotation_green.tolist()
        exp.addData("continuous_annotation_luminance", mouse_annotation_green_list)
        stim_value_green_list = stim_value_green.tolist()
        exp.addData("stim_value_green", stim_value_green_list)
        stim_value_list = stim_value.tolist()
        exp.addData("stim_value", stim_value_list)


    elif practice_trial_number == 4:
        # how_instructions_absolute("post_stimulus_verbal_report_practice")
        show_instructions_absolute("post_stimulus_verbal_report")
        
        # Wait until ' space ' is pressed
        event.waitKeys(keyList=['space'])
        time_resp_clock = core.Clock()
                
        samplerate=44100
        channels=1
        max_dur = 120
        
        outlet.push_sample(['audio_response_start'])
        recording = sd.rec(int(samplerate * max_dur), samplerate=samplerate, channels=channels, dtype='float64', blocking=False)
        
        # Flush the buffers
        event.clearEvents()
        
        win.flip()
        
        grabando_audio_text = visual.TextStim(
            win,
            text="Grabando audio...",
            height=ExperimentParameters.text_height,
            pos=[0, 0],
        )

        # Para dibujar el estímulo de texto
        grabando_audio_text.draw()
        win.flip()

        # Wait until 'space' is pressed
        response = event.waitKeys(maxWait = max_dur, keyList=['space'], timeStamped=time_resp_clock)
        outlet.push_sample(['audio_response_end'])
        
        if not response:
            recording_dur = max_dur
        else:
            recording_dur = response[0][1]
        exp.addData('recording_dur', recording_dur)
        win.flip()
        
        # Calculate the actual number of samples recorded based on the recording time
        try:
            actual_samples_recorded = int((recording_dur + 1) * samplerate)
        except Exception as e:
            actual_samples_recorded = int((max_dur + 1) * samplerate)
            print(f"Error occurred during calculation of actual_samples_recorded: {e}")
        
        # Trim the recording to the actual size and save
        trimmed_recording = recording[:actual_samples_recorded]
    
        path_movie = trial["movie_path"]
        video_name = path_movie.split("/")[-1].split(".mp3")[0]
        audio_file_name = os.path.join(audio_folder, f"sub-{info_dict['ID']}_ses_{info_dict['Sesion']}_task-{exp_name}_probe-{video_name}_run-{practice_trial_number}.wav")

        write(audio_file_name, samplerate, np.int16(trimmed_recording * 32767))

        show_instructions_absolute("end_practice")
        print("Termino la practica")

    practice_trial_number += 1

    exp.nextEntry()


###########################################################################
########                        TEST BLOCK                        ########
##########################################################################
def ejecutar_calm_video(
    win,
    #path_video="../stimuli/calm_videos/2D/28.0_Maldives beach and resort-1-2d_cropped.mp4",
    path_video="../amsterdam_dynamic_facial_expression_set/28.0_Maldives beach and resort-1-2d_cropped.mp4",
    instruction_txt_calm=None,
):
    """
    Reproduce un video tranquilo en pantalla completa y espera hasta que el video termine
    o el usuario cierre el experimento presionando 'escape'.

    Parameters:
    - win: La ventana de PsychoPy donde se reproducirá el video.
    - path_video: El camino hacia el archivo de video que se va a reproducir.
    """
    
    win.flip()
    
    show_instructions_absolute(instruction_txt_calm)

    event.clearEvents()

    mov = visual.MovieStim3(
        win=win, filename=path_video, size=(1920, 1080), pos=[0, 0], noAudio=False
    )
    continue_playing = True  # Variable de control para continuar la reproducción
    
    outlet.push_sample(['calm_video_start'])
    
    while mov.status != constants.FINISHED and continue_playing:
        mov.draw()
        win.flip()

        keys = event.getKeys()
        # if 'escape' in keys:
        #    break  # Salir del bucle y luego cerrar la ventana y finalizar el experimento.
        if "p" in keys:
            mov.stop()
            continue_playing = False  # Detener la reproducción de manera controlada

    outlet.push_sample(['calm_video_end'])
    
    # if 'escape' in keys:  # Si la salida fue por 'escape', limpiar y cerrar.
    #    win.close()
    #    core.quit()
    # Si no, el programa continuará sin cerrar la ventana ni finalizar el experimento.

# Función para cargar los bloques desde un archivo CSV
def cargar_bloques(nombre_archivo):
    return data.importConditions(nombre_archivo)


def ejecutar_trials(win, exp, archivo_bloque, sliders_dict, subbloque_number_aux):
    global mouse_x, current_time, video_start_time  # Asegura que estas variables son tratadas como globales

    # Continúa con el resto de tu función ejecutar_trials
    condiciones = data.importConditions(archivo_bloque)
    trials = data.TrialHandler(
        trialList=condiciones, nReps=1, method="random", name="trials"
    )

    exp.addLoop(trials)

    for trial in trials:
        show_instructions_absolute("left_right_alternance_instructions_text")
        
        # Inicialización de elementos visuales
        mov = visual.MovieStim3(
            win=win,
            filename=trial["movie_path"],
            size=(1920, 1080),
            pos=[0, 0],
            noAudio=False,
        )
        
        left_image, right_image = show_instructions_relative_trial(
            trial["dimension"],
            outlet,
            trial["hand"],
            win,
            ExperimentParameters,
            sliders_dict,
            order_emojis_slider=trial["order_emojis_slider"],
        )

        # Usar 'Dimension' del trial para determinar las rutas de las imágenes
        if trial["dimension"] in sliders_dict:
            slider_info = sliders_dict[trial["dimension"]]

        # Invertir las imágenes si 'order_emojis_slider' es 'inverse'
        if "order_emojis_slider" in trial and trial["order_emojis_slider"] == "inverse":
            # Verificar si hay rutas de imagen definidas y crear los estímulos de imagen invertidos
            if (
                slider_info["right_image_path"] is not None
                and slider_info["left_image_path"] is not None
            ):
                left_image = visual.ImageStim(
                    win, image=slider_info["right_image_path"], pos=(-5, -8.4), size=1.3
                )
                right_image = visual.ImageStim(
                    win, image=slider_info["left_image_path"], pos=(5, -8.4), size=1.3
                )
        else:
            # Verificar si hay rutas de imagen definidas y crear los estímulos de imagen normales
            if slider_info["left_image_path"] is not None:
                left_image = visual.ImageStim(
                    win, image=slider_info["left_image_path"], pos=(-5, -8.4), size=1.3
                )
            if slider_info["right_image_path"] is not None:
                right_image = visual.ImageStim(
                    win, image=slider_info["right_image_path"], pos=(5, -8.4), size=1.3
                )

        # Dibujar las imágenes
        if slider_info["left_image_path"] is not None:
            left_image.draw()
        if slider_info["right_image_path"] is not None:
            right_image.draw()
        else:
            print(
                "La dimensión del trial no está definida en sliders_dict:",
                trial["dimension"],
            )
            continue  #

        # Restablecer el deslizador de valencia para el nuevo ensayo
        dimension_slider.reset()
        dimension_slider.markerPos = 0  # Establecer la posición inicial del marcador

        # Obtener objeto del ratón y hacerlo visible
        mouse = event.Mouse(visible=True, win=win)
        mouse.setPos(newPos=(0, dimension_slider.pos[1]))

        # Calculate the range in pixels for the slider
        slider_start = dimension_slider.pos[0] - (dimension_slider.size[0] / 2)
        #slider_end = dimension_slider.pos[0] + (dimension_slider.size[0] / 2)

        dimension_slider.name = trial["dimension"]

        left_image.draw()
        right_image.draw()
        intensity_cue_image.draw()
        dimension_slider.draw()

        ## Create a custom white circle as the slider thumb
        slider_thumb = visual.Circle(
            win,
            pos=(0, -8.4),
            radius=0.30,
            fillColor="white",
            lineColor="black",
            edges=32,
        )
        slider_thumb.draw()

        print(trial["movie_path"])

        event.clearEvents()
        
        # Inicializar el array de NumPy para anotaciones del ratón
        mouse_annotation = np.empty((0, 2), dtype=float)  # Array vacío con dos columnas
        
        first_iteration = True
        
        while mov.status != constants.FINISHED:
                        
            left_image.draw()
            right_image.draw()
            intensity_cue_image.draw()
            dimension_slider.draw()
            slider_thumb.draw()
            
            win.callOnFlip(log_mouse_and_time, mov, outlet, first_iteration_aux=first_iteration)
            win.flip()
            
            if first_iteration:
                first_iteration = False
            
            if mouse_x < -4:
                slider_value = -1
            elif mouse_x > 4:
                slider_value = 1
            else:
                norm_pos = (mouse_x - slider_start) / dimension_slider.size[0]
                slider_value = norm_pos * (dimension_slider.ticks[-1] - dimension_slider.ticks[0]) + dimension_slider.ticks[0]
                dimension_slider.markerPos = round(slider_value, 2)
            
            # Agregar datos al array de NumPy
            new_data = np.array([[slider_value, current_time]])
            mouse_annotation = np.vstack((mouse_annotation, new_data))
            
            last_time_reported = current_time

            thumb_pos_x = (dimension_slider.markerPos - dimension_slider.ticks[0]) / (dimension_slider.ticks[-1] - dimension_slider.ticks[0]) * dimension_slider.size[0] - (dimension_slider.size[0] / 2)
            slider_thumb.setPos([thumb_pos_x, dimension_slider.pos[1]])

            keys = event.getKeys(keyList=["escape", "p"])
            if "escape" in keys:
                win.close()
                core.quit()
            if "p" in keys:
                mov.stop()
                break  # Salir del bucle
        
        outlet.push_sample(['video_end'])
        # Convertir el array de NumPy a una lista de listas
        mouse_annotation_list = mouse_annotation.tolist()
        exp.addData("continuous_annotation", mouse_annotation_list)
        exp.addData("video_duration", mov.duration)
        exp.addData("subbloque_number", subbloque_number_aux)

        if subbloque_number_aux <= 4:
            # Crear el estímulo de texto para el mensaje de carga
            win.flip()
            loading_text_stim = visual.TextStim(
                win,
                text="Cargando escalas...",
                height=ExperimentParameters.text_height,
                pos=[0, 0],
            )

            # Dibujar el estímulo de texto en la ventana
            loading_text_stim.draw()

            # Mostrar la ventana con el mensaje de carga
            win.flip()

            # Mantener el mensaje en pantalla por 0.5 segundos
            core.wait(0.5)

            mostrar_sliders_y_recoger_respuestas(win, outlet, sliders_dict, trials)

            # Siguiente entrada del registro de datos
            core.wait(ExperimentParameters.iti)
            
            if trial["luminance"] == "yes":
                
                # Instrucciones luminancia
                left_image, right_image = show_instructions_relative_trial(
                    "luminance",
                    outlet,
                    trial["hand"],
                    win,
                    ExperimentParameters,
                    sliders_dict,
                    order_emojis_slider=trial["order_emojis_slider"],
                )
                # Cambiar las posiciones a (0, 1)
                left_image.pos = (-5, -8.4)
                right_image.pos = (5, -8.4)
                slider_thumb.pos = (0, -8.1)

                # Restablecer el deslizador de valencia para el nuevo ensayo
                dimension_slider.reset()
                dimension_slider.markerPos = (
                    0  # Establecer la posición inicial del marcador
                )

                # Convertir mouse_annotation_aux a una matriz de numpy para facilitar las búsquedas
                mouse_annotation_aux_np = mouse_annotation

                # Inicialización
                mouse_annotation_green = np.empty((0, 2), dtype=float) 
                stim_value = np.empty((0, 2), dtype=float) 
                stim_value_green = np.empty((0, 2), dtype=float) 
                
                # Obtener objeto del ratón y hacerlo visible
                mouse = event.Mouse(visible=True, win=win)
                mouse.setPos(newPos=(0, dimension_slider.pos[1]))

                # Calculate the range in pixels for the slider
                slider_start = dimension_slider.pos[0] - (dimension_slider.size[0] / 2)
                #slider_end = dimension_slider.pos[0] + (dimension_slider.size[0] / 2)

                event.clearEvents()                   
                                            
                cronometro = core.Clock()
                green_screen_start_time = cronometro.getTime()
                
                outlet.push_sample(['luminance_start'])
                
                # Bucle hasta que el tiempo transcurrido sea mayor que la duración del video
                while cronometro.getTime() - green_screen_start_time <= last_time_reported:
                    tiempo_actual = cronometro.getTime() - green_screen_start_time

                    # Encontrar el índice del valor de tiempo más cercano en mouse_annotation_aux
                    idx = np.abs(mouse_annotation_aux_np[:, 1] - tiempo_actual).argmin()
                    valor_cercano, _ = mouse_annotation_aux_np[idx]

                    if trial["order_emojis_slider"] == "inverse":
                        valor_cercano = -valor_cercano

                    # Ajustar valor de intensidad verde según el valor más cercano encontrado
                    green_intensity = ((valor_cercano + 1) / 2) * (255 - 25) + 25
    
                    # Establecer el color de la ventana y dibujar todos los elementos
                    win.setColor([20, green_intensity, 12], "rgb255")
                    left_image.draw()
                    right_image.draw()
                    intensity_cue_image.draw()
                    dimension_slider.draw()
                    slider_thumb.draw()

                    mouse_x, _ = mouse.getPos()
                    tiempo_actual_real = cronometro.getTime() - green_screen_start_time

                    # Verificar si mouse_x está fuera del rango a la izquierda (-4)
                    if mouse_x < -4:
                        slider_value_green = -1
                    # Verificar si mouse_x está fuera del rango a la derecha (4)
                    elif mouse_x > 4:
                        slider_value_green = 1
                    else:
                        # Calcular norm_pos dentro del rango permitido
                        norm_pos = (mouse_x - slider_start) / dimension_slider.size[0]
                        # Calcular slider_value basado en norm_pos dentro del rango permitido
                        slider_value_green = (
                            norm_pos
                            * (dimension_slider.ticks[-1] - dimension_slider.ticks[0])
                            + dimension_slider.ticks[0]
                        )
                        dimension_slider.markerPos = round(slider_value_green, 2)

                    # Manejar la salida anticipada
                    keys = event.getKeys()
                    if "escape" in keys:
                        win.close()
                        core.quit()
                    if "p" in keys:  # Verificar si se presionó la tecla "p"
                        break  # Salir del bucle while, finalizando la reproducción del video
                    
                    # Agregar datos al array de NumPy
                    new_data_mouse_annotation_green = np.array([[slider_value_green, tiempo_actual_real]])
                    mouse_annotation_green = np.vstack((mouse_annotation_green, new_data_mouse_annotation_green))
                    
                    # Agregar datos al array de NumPy
                    new_data_stim_value_green = np.array([[green_intensity, tiempo_actual_real]])
                    stim_value_green = np.vstack((stim_value_green, new_data_stim_value_green))
                    
                    # Agregar datos al array de NumPy
                    new_data_stim_value = np.array([[valor_cercano, tiempo_actual_real]])
                    stim_value = np.vstack((stim_value, new_data_stim_value))

                    thumb_pos_x = (
                        dimension_slider.markerPos - dimension_slider.ticks[0]
                    ) / (
                        dimension_slider.ticks[-1] - dimension_slider.ticks[0]
                    ) * dimension_slider.size[0] - (dimension_slider.size[0] / 2)
                    slider_thumb.setPos([thumb_pos_x, dimension_slider.pos[1]])

                    win.flip()

                outlet.push_sample(['luminance_end'])
                
                # Continuar con el código para restablecer el color de fondo y guardar las anotaciones
                win.setColor("black")
                win.flip()

                # Guardar anotaciones interpoladas al final del ensayo
                # Convertir el array de NumPy a una lista de listas
                mouse_annotation_green_list = mouse_annotation_green.tolist()
                exp.addData("continuous_annotation_luminance", mouse_annotation_green_list)
                stim_value_green_list = stim_value_green.tolist()
                exp.addData("stim_value_green", stim_value_green_list)
                stim_value_list = stim_value.tolist()
                exp.addData("stim_value", stim_value_list)

        elif subbloque_number_aux > 4:
            win.flip()
            show_instructions_absolute("post_stimulus_verbal_report")

            # Wait until ' space ' is pressed
            event.waitKeys(keyList=['space'])
            time_resp_clock = core.Clock()
                    
            samplerate=44100
            channels=1
            max_dur = 120
            
            outlet.push_sample(['audio_response_start'])
            recording = sd.rec(int(samplerate * max_dur), samplerate=samplerate, channels=channels, dtype='float64', blocking=False)
            
            # Flush the buffers
            event.clearEvents()
            
            win.flip()
            
            
            grabando_audio_text = visual.TextStim(
                win,
                text= "Grabando audio... \n\n Presioná 'espacio' para detener la grabación.",
                height=ExperimentParameters.text_height,
                pos=[0, 0],
            )

            # Para dibujar el estímulo de texto
            grabando_audio_text.draw()
            win.flip()

            # Wait until 'space' is pressed
            response = event.waitKeys(maxWait = max_dur, keyList=['space'], timeStamped=time_resp_clock)
            outlet.push_sample(['audio_response_end'])
            
            if not response:
                recording_dur = max_dur
            else:
                recording_dur = response[0][1]
            exp.addData('recording_dur', recording_dur)
            win.flip()
            
            # Calculate the actual number of samples recorded based on the recording time
            try:
                actual_samples_recorded = int((recording_dur + 1) * samplerate)
            except Exception as e:
                actual_samples_recorded = int((max_dur + 1) * samplerate)
                print(f"Error occurred during calculation of actual_samples_recorded: {e}")
            
            # Trim the recording to the actual size and save
            trimmed_recording = recording[:actual_samples_recorded]
        
            path_movie = trial["movie_path"]
            video_name = path_movie.split("/")[-1].split(".mp3")[0]
            audio_file_name = os.path.join(audio_folder, f"sub-{info_dict['ID']}_ses_{info_dict['Sesion']}_task-{exp_name}_probe-{video_name}_run-{subbloque_number_aux}.wav")

            write(audio_file_name, samplerate, np.int16(trimmed_recording * 32767))

            show_instructions_absolute("post_stimulus_stop_verbal_report")

            core.wait(0.5)  # Buffer for stopping the recording


        exp.nextEntry()

ejecutar_calm_video(
    win=win,
    path_video="../stimuli/calm_videos/2D/901.mp4",
    #path_video="../amsterdam_dynamic_facial_expression_set/28.0_Maldives beach and resort-1-2d_cropped.mp4",
    instruction_txt_calm="initial_relaxation_video_text",
)


show_instructions_absolute("post_stimulus_stop_verbal_report")

# Cargar los subbloques de cada suprabloque

subbloques_A = cargar_bloques("../conditions/Blocks_A.csv")
#subbloques_A = cargar_bloques("../conditions_test_2/Blocks_A.csv")

subbloques_B = cargar_bloques("../conditions/Blocks_B.csv")
#subbloques_B = cargar_bloques("../conditions_test_2/Blocks_B.csv")


subbloque_number = 1


# Función para ejecutar todos los subbloques de un suprabloque
def ejecutar_suprabloque(win, exp, subbloques):
    global subbloque_number  # Declarar que vamos a usar la variable global
    outlet.push_sample(["SUPRABLOCK_START"])
    core.wait(0.5)
    random.shuffle(subbloques)  # Aleatorizar el orden de los subbloques
    for subbloque in subbloques:
        print(subbloque)
        outlet.push_sample(["BLOCK_START"])
        core.wait(0.5)
        ruta_subbloque = subbloque["condsFile"]
        ejecutar_trials(win, exp, ruta_subbloque, sliders_dict, subbloque_number)
        outlet.push_sample(["BLOCK_END"])
        core.wait(0.5)
        show_instructions_absolute("rest_block_text")
        win.flip()
        
        subbloque_number += 1
    outlet.push_sample(["SUPRABLOCK_END"])
    win.flip()


# Asignar bloque inicial basado en alguna condición externa (ejemplo)
bloque_inicial = info_dict["Sesion"]

# Ejecutar los suprabloques en el orden determinado por bloque_inicial
if bloque_inicial == "A":
    ejecutar_suprabloque(win, exp, subbloques_A)
    show_instructions_absolute("rest_suprablock_text")
    ejecutar_suprabloque(win, exp, subbloques_B)
else:
    ejecutar_suprabloque(win, exp, subbloques_B)
    show_instructions_absolute("rest_suprablock_text")
    ejecutar_suprabloque(win, exp, subbloques_A)

ejecutar_calm_video(win=win,
                    path_video="../stimuli/calm_videos/2D/902.mp4",
                    #path_video="../amsterdam_dynamic_facial_expression_set/70.0_Tahiti Surf-1-2d_cropped.mp4",
                    instruction_txt_calm = 'final_relaxation_video_text')

##########################################################################
###################### Feedback + Goodbye message ########################
kb.clearEvents()
show_instructions_absolute("experiment_end_text")

event.waitKeys(maxWait=10, keyList=["space"])

#stop recording
s.sendall(b"stop\n")

time.sleep(3)

# Task shutdown
win.close()

# Finish psychopy thread
core.quit()

#%%