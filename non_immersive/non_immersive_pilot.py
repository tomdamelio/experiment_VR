# Experiment VR: Non Immersive Task
# Author: Tomas D'Amelio

from psychopy import core, visual, data, event, constants
from psychopy.hardware import keyboard

import random
import os
import time 

from params import params
import instructions

import numpy as np


# Get the absolute path of the currently executing script
current_script_path = os.path.abspath(__file__)

# Extract the directory from the absolute path
current_script_dir = os.path.dirname(current_script_path)

# Change the current working directory to the script's directory
os.chdir(current_script_dir)

# Confirm the current working directory has been changed
print("Current working directory:", os.getcwd())

# GUI for subject information

# Form
info_dict = {
    'Subject_id': 'S6',
    'Age': 21,
    'Gender': ['Male', 'Female', 'Non-binary', 'Rather not say'],
    'Group': ['Test', 'Control'],
}

# Order of forms
order = ['Subject_id', 'Age', 'Gender', 'Group']

### UNCOMMENT THIS TO USE THE FORMS. It's commented for practicity.###
# Instantiate dialog boxqq
# my_dlg = gui.DlgFromDict(info_dict, title=params.exp_name,
#                          order=order)
# if my_dlg.OK == False:
#     core.quit()  # user pressed cancel

info_dict['date'] = data.getDateStr()

##########################################################################
# Experiment data settings

# create folder to save experiment data for each subject
subject_folder = params['results_folder'] + f"{info_dict['Subject_id']}/"

os.makedirs(subject_folder, exist_ok=True)

# Name of .csv file to save the data
file_name = info_dict['Subject_id'] + '_' + \
            params['exp_name'] + '_' + info_dict['date']

#########################################################################
# Create experiment handler
exp = data.ExperimentHandler(name=params['exp_name'],
                                # version='0.1',
                                extraInfo=info_dict,
                                runtimeInfo=True,
                                originPath='./non_immersive_experiment.py',
                                savePickle=True,
                                saveWideText=True,
                                dataFileName=subject_folder + file_name)

##########################################################################

# Diccionario para definir los sliders y su configuración
sliders_dict = {
    "valence": {
        "slider_position": (0, 7),
        "left_image_path": './images_scale/valence_left.png',
        "right_image_path": './images_scale/valence_right.png',
        "left_text": '',
        "right_text": '' 
    },
    "arousal": {
        "slider_position": (0, 4),
        "left_image_path": './images_scale/arousal_left.png',
        "right_image_path": './images_scale/arousal_right.png',
        "left_text": '',
        "right_text": '' 
    },
    "preference": {
        "slider_position": (0, 1),
        "left_image_path": './images_scale/preference_left.png',
        "right_image_path": './images_scale/preference_right.png',
        "left_text": "Completo desagrado",
        "right_text": "Completo agrado",
    },
    "engagement": {
        "slider_position": (0, -2),
        "left_image_path": None,
        "right_image_path": None,
        "left_text": "No presté atención",
        "right_text": "Presté completa atención",
    },
    "familiarity": {
        "slider_position": (0, -5),
        "left_image_path": None,
        "right_image_path": None,
        "left_text": "Nunca habia visto este video antes",
        "right_text": "Conozco este video muy bien",
    },
    "luminance": {
        "slider_position": None,
        "left_image_path": './images_scale/non_bright_left.png',
        "right_image_path": './images_scale/bright_right.png',
        "left_text": '',
        "right_text": '',}
}

def mostrar_sliders_y_recoger_respuestas(win, sliders_dict, trials, params):

    import params

    sliders = []

    # Crear y dibujar los sliders y las imágenes asociadas
    for slider_name, slider_info in sliders_dict.items():
        if slider_name == "luminance":
            continue
        #print(slider_name)
        #print(slider_info)
        # Crear el slider
        slider_info['slider'] = visual.Slider(win=win, name=slider_name, ticks=(-1, 1), 
                                            pos=slider_info["slider_position"], size=(8, 0.25),
                                            labels = [slider_info["left_text"],' ', slider_info["right_text"]],
                                            labelHeight = 0.5,
                                            style=['slider'], granularity=0.1, color='white',
                                            font='HelveticaBold', lineColor='white', fillColor='white',
                                            borderColor='white', markerColor='white')
        sliders.append(slider_info['slider'])

        #print(slider_info["left_image_path"])
        #print(slider_info["slider_position"][1])

        # Determinar si se debe cargar una imagen o usar texto para cada lado
        slider_info['left_image'] = visual.ImageStim(win, image=slider_info["left_image_path"],
                                                        pos=(-5, slider_info["slider_position"][1]), size=1.3)

        slider_info['right_image'] = visual.ImageStim(win, image=slider_info["right_image_path"],
                                                        pos=(-5, slider_info["slider_position"][1]), size=1.3)

    # Inicializa la ventana gráfica
    win.flip()

    # Define las posiciones de las casillas de verificación en la parte inferior de la pantalla
    checkbox_positions = [(x, -9) for x in range(-10, 10, 3)]  # Genera posiciones a lo largo del eje x con un espaciado de 3

    # Define las emociones básicas y su estado inicial (no seleccionado)
    basic_emotions = ['Neutral', 'Asco', 'Felicidad', 'Sorpresa', 'Ira', 'Miedo', 'Tristeza']
    emotion_states = {emotion: False for emotion in basic_emotions}

    # Crea rectángulos y etiquetas para las casillas de verificación
    checkbox_rects = []
    checkbox_labels = []
    for pos, emotion in zip(checkbox_positions, basic_emotions):
        rect = visual.Rect(win, width=0.5, height=0.5, pos=pos, lineColor='white', fillColor=None)
        checkbox_rects.append(rect)
        label = visual.TextStim(win, text=emotion, pos=(pos[0], pos[1] - 0.7), height=0.5)
        checkbox_labels.append(label)

    # Crear un slider_thumb para cada slider antes del bucle
    for slider_name, slider_info in sliders_dict.items():
        if slider_name == "luminance":
            continue
        slider_info['left_image'] = visual.ImageStim(win, image=slider_info["left_image_path"], pos=(-5, slider_info["slider_position"][1]+0.5), size=1.3)
        slider_info['right_image'] = visual.ImageStim(win, image=slider_info["right_image_path"], pos=(5, slider_info["slider_position"][1]+0.5), size=1.3)
        slider_y = slider_info['slider_position'][1]
        slider_info['slider_thumb'] = visual.Circle(win, radius=0.30, fillColor='white', lineColor='black', edges=32, pos=(0, slider_y))

    # Iniciar el bucle de evento para la interacción del usuario
    mouse = event.Mouse(win=win)
    event.clearEvents()

    win.flip()

    user_interacting = True  # Una nueva variable para controlar la interacción del usuario

    while user_interacting:
        # Obtener la posición actual del ratón en cada iteración del bucle
        mouse_x, mouse_y = mouse.getPos()
        iteration_counter = 0  # Inicializa el contador

        for slider_name, slider_info in sliders_dict.items():
            if slider_name == "luminance":
                continue
            slider = slider_info['slider']
            slider.draw()
            slider_thumb = slider_info['slider_thumb']
            slider_x, slider_y = slider.pos
            slider_width, slider_height = slider.size
            slider_start = slider_x - slider_width / 2
            slider_end = slider_x + slider_width / 2

            # Condición para dibujar intensity_cue_image solo en las dos primeras iteraciones
            if iteration_counter < 2:
                intensity_cue_image_scale = visual.ImageStim(win, image='./images_scale/AS_intensity_cue.png', pos=(0, -8.7), size=(8, 0.6))
                intensity_cue_image_scale.pos = (0, slider_y - 1.0)
                intensity_cue_image_scale.draw()

            # Dibujar la imagen o el texto izquierdo
            if "left_image" in slider_info:
                slider_info['left_image'].draw()
            else:
                slider_info['left_text'].draw()

            # Dibujar la imagen o el texto derecho
            if "right_image" in slider_info:
                slider_info['right_image'].draw()
            else:
                slider_info['right_text'].draw()
            
            iteration_counter += 1

            # Dibujar el thumb del slider
            slider_thumb.draw()

            if mouse.getPressed()[0]:
                #mouse_x, mouse_y = mouse.getPos()
                # Comprobar si el ratón está sobre el slider o su thumb
                if slider_x - slider_width / 2 <= mouse_x <= slider_x + slider_width / 2 and \
                slider_y - slider_height / 2 <= mouse_y <= slider_y + slider_height / 2:
                    if mouse.getPressed()[0]:  # Si se presiona el botón izquierdo del ratón
                        norm_pos = (mouse_x - slider_start) / slider_width
                        slider_value = norm_pos * (slider.ticks[-1] - slider.ticks[0]) + slider.ticks[0]
                        slider.markerPos = slider_value
                        # Asegurarse de que la posición del thumb refleje la posición del marcador
                        thumb_pos_x = (slider.markerPos - slider.ticks[0]) / (slider.ticks[-1] - slider.ticks[0]) * slider_width + slider_start
                        slider_thumb.setPos((thumb_pos_x, slider_y))

        mensaje = "Por favor indicá cómo te sentiste al ver este video"
        text_stim = visual.TextStim(win, text=mensaje, height= 0.6, pos=(0,10))

        # Para dibujar el estímulo de texto
        text_stim.draw()

        # Dibujar las casillas de verificación y sus etiquetas
        for rect, label in zip(checkbox_rects, checkbox_labels):
            rect.draw()   
            label.draw()
        
        # Detectar clics del ratón
        if mouse.getPressed()[0]:  # Verifica si el botón izquierdo del ratón está presionado
            mouse_click_position = mouse.getPos()
            for i, rect in enumerate(checkbox_rects):
                if rect.contains(mouse_click_position):
                    emotion = basic_emotions[i]
                    emotion_states[emotion] = not emotion_states[emotion]  # Cambia el estado de la emoción
                    rect.fillColor = 'grey' if emotion_states[emotion] else None  # Retroalimentación visual
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
    
    # Una vez finalizada la interacción del usuario, recoger y guardar los datos
    for slider_name, slider_info in sliders_dict.items():
        if slider_name == "luminance":
            continue
        slider_value = slider_info['slider'].getRating()
        trials.addData(f'{slider_name}_value', slider_value)

    # Guardar los estados de las casillas de verificación
    for emotion, rect in zip(basic_emotions, checkbox_rects):
        trials.addData(f'checkbox_{emotion}', emotion_states[emotion])

    # Inter Trial Interval(ITI) con pantalla en blanco
    win.flip()

def presentar_instrucciones(dimension, hand, win, params, sliders_dict, order_emojis_slider="normal"):
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
    
    instruction_trial = (f"Ahora vas a reportar continuamente {dimension_traducida} mientras ves el video. \n\n"
                        f"Vas a usar tu mano {mano} para indicar esto en la escala de abajo. \n\n"
                        "Por favor, presioná la barra espaciadora para comenzar.")

    # Crear y presentar las instrucciones generales
    instruction_general = visual.TextStim(win, height=params['text_height'], pos=[0, 0.5], text=instruction_trial, wrapWidth=80)
    instruction_general.draw()

    # Determinar las rutas de las imágenes basadas en la 'dimension'
    slider_info = sliders_dict.get(dimension, {})
    
    # Preparar las imágenes de la escala para mostrar
    if order_emojis_slider == "inverse":
        left_image_path = slider_info.get('right_image_path')
        right_image_path = slider_info.get('left_image_path')
    else:
        left_image_path = slider_info.get('left_image_path')
        right_image_path = slider_info.get('right_image_path')
    
    if left_image_path and right_image_path:  # Asegurar que ambas rutas estén definidas
        left_image = visual.ImageStim(win, image=left_image_path, pos=(-5, -8.4), size=1.3)
        right_image = visual.ImageStim(win, image=right_image_path, pos=(5, -8.4), size=1.3)
        left_image.draw()
        right_image.draw()

    dimension_slider = visual.Slider(win=win, name='dimension', ticks=(-1, 1), labels=None, pos=(0, -8.1), size=(8, 0.25),
                        style=['slider'], granularity=0.1, color='white', font='Helvetica',
                        lineColor='white', fillColor='white', borderColor='white', markerColor='white')
    
    dimension_slider.draw()

    ## Create a custom white circle as the slider thumb
    slider_thumb = visual.Circle(win, pos=(0, -8.1), radius=0.30, fillColor='white', lineColor='black', edges=32)
    slider_thumb.draw()

    intensity_cue_image = visual.ImageStim(win, image='./images_scale/AS_intensity_cue.png', pos=(0, -8.7), size=(8, 0.6))
    intensity_cue_image.draw()

    # Flip the front and back buffers para mostrar las instrucciones y las imágenes
    win.flip()

    # To begin the Experimetn with Spacebar or RightMouse Click
    press_button = True
    while press_button:
        keys = event.getKeys(keyList=['space'])

        mouse = event.Mouse(visible=True, win=win)
        mouse_click = mouse.getPressed()

        if 'space' in keys or 1 in mouse_click:
            press_button = False
    
    return left_image, right_image




##########################################################################
# Create a window
win = visual.Window(allowGUI=None,
                    size=params['display_size'],
                    monitor='testMonitor',
                    winType='pyglet',
                    useFBO=True,
                    # units='pix',Fpg
                    units='deg',
                    fullscr=params['fullscreen'],
                    color='black')

info_dict['frame_rate'] = win.getActualFrameRate()

exp_info = {'fullscreen': params['fullscreen'],
            'main_screen': params['main_screen'],
            'display_size': params['display_size'],
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

# Create practice instructions ('text' visual stimuli)
# for _, value in list(instructions.non_immersive_instructions_text.items())[:1]:
#     instruction_practice = visual.TextStim(win,
#                                             height=params['text_height'],
#                                             pos=[0, 0],
#                                             text=value,
#                                             wrapWidth=80)
#     instruction_practice.draw()
#     # Flip the front and back buffers
#     win.flip()

#     # To begin the Experimetn with Spacebar or RightMouse Click
#     press_button = True
#     while press_button:
#         keys = event.getKeys(keyList=['space'])

#         mouse = event.Mouse(visible=False, win=win)
#         mouse_click = mouse.getPressed()

#         if 'space' in keys or 1 in mouse_click:
#             press_button = False

# # Create trial handler
# practice_trials = data.TrialHandler(
# trialList=data.importConditions('./conditions/non_immersive_practice_conditions.csv'),
# originPath=-1, nReps=1, method='sequential', name='practice')

# exp.addLoop(practice_trials)
# #
# # Cargar imágenes para los extremos y el marcador del slider
# intensity_cue_image = visual.ImageStim(win, image='./images_scale/AS_intensity_cue.png', pos=(0, -8.7), size=(8, 0.6))

# ## Initialize the slider
# dimension_slider = visual.Slider(win=win, name='dimension', ticks=(-1, 1), labels=None, pos=(0, -8.1), size=(8, 0.25),
#                             style=['slider'], granularity=0.1, color='white', font='Helvetica',
#                             lineColor='white', fillColor='white', borderColor='white', markerColor='white')

# ## Create a custom white circle as the slider thumb
# slider_thumb = visual.Circle(win, radius=0.30, fillColor='white', lineColor='black', edges=32)

# green_screen_variation = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0073615047716684145, 0.0073615047716684145, 0.0073615047716684145, 0.0073615047716684145, 0.0073615047716684145, 0.0073615047716684145, 0.0073615047716684145, 0.0073615047716684145, 0.0073615047716684145, 0.0073615047716684145, 0.0073615047716684145, 0.014723009543337051, 0.014723009543337051, 0.014723009543337051, 0.014723009543337051, 0.014723009543337051, 0.014723009543337051, 0.014723009543337051, 0.014723009543337051, 0.014723009543337051, 0.014723009543337051, 0.014723009543337051, 0.014723009543337051, 0.014723009543337051, 0.014723009543337051, 0.029446019086674102, 0.029446019086674102, 0.03680752385834252, 0.03680752385834252, 0.03680752385834252, 0.03680752385834252, 0.05153053340167957, 0.05889203817334798, 0.05889203817334798, 0.05889203817334798, 0.05889203817334798, 0.05889203817334798, 0.05889203817334798, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.07361504771668503, 0.06625354294501662, 0.05889203817334798, 0.0073615047716684145, -0.04416902863001104, -0.06625354294501651, -0.10306106680335902, -0.161953104976707, -0.18403761929171258, -0.21348363837838658, -0.23556815269339204, -0.2576526670083975, -0.27237567655173445, -0.27237567655173445, -0.27237567655173445, -0.27237567655173445, -0.27237567655173445, -0.27237567655173445, -0.27237567655173445, -0.27237567655173445, -0.27237567655173445, -0.27237567655173445, -0.27237567655173445, -0.27237567655173445, -0.279737181323403, -0.29446019086674, -0.30182169563840844, -0.30182169563840844, -0.30182169563840844, -0.30182169563840844, -0.30182169563840844, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3165447051817455, -0.3239062099534139, -0.3239062099534139, -0.3239062099534139, -0.3239062099534139, -0.3239062099534139, -0.3239062099534139, -0.33862921949675096, -0.3459907242684195, -0.3459907242684195, -0.3459907242684195, -0.3459907242684195, -0.3459907242684195, -0.3607137338117564, -0.3607137338117564, -0.3607137338117564, -0.3607137338117564, -0.3607137338117564, -0.3607137338117564, -0.3607137338117564, -0.36807523858342495, -0.36807523858342495, -0.36807523858342495, -0.36807523858342495, -0.36807523858342495, -0.36807523858342495, -0.36807523858342495, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347, -0.37543674335509347]

# # Loop over trials handler
# for trial in practice_trials:
#     practice_value = trial['dimension'] + "_practice_instructions_text"
#     instruction_practice = visual.TextStim(win,
#                                             height=params['text_height'],
#                                             pos=[0, 0],
#                                             text=instructions.non_immersive_instructions_text[practice_value],
#                                             wrapWidth=80)
#     instruction_practice.draw()
#     # Flip the front and back buffers
#     win.flip()

#     # To begin the Experimetn with Spacebar or RightMouse Click
#     press_button = True
#     while press_button:
#         keys = event.getKeys(keyList=['space'])

#         mouse = event.Mouse(visible=False, win=win)
#         mouse_click = mouse.getPressed()

#         if 'space' in keys or 1 in mouse_click:
#             press_button = False

#     # Crear cruz de fijación
#     fixation = visual.GratingStim(win, color=1, colorSpace='rgb', tex=None, mask='cross', size=2)
#     fixation.draw()
#     win.flip()
#     core.wait(params['fixation_time'])

#     # Limpiar buffers y reloj
#     kb.clearEvents()
#     kb.clock.reset()

#     # Usar 'Dimension' del trial para determinar las rutas de las imágenes
#     if trial['dimension'] in sliders_dict:
#         slider_info = sliders_dict[trial['dimension']]
        
#         # Verificar si hay rutas de imagen definidas y crear los estímulos de imagen correspondientes
#         if slider_info['left_image_path'] is not None:
#             left_image = visual.ImageStim(win, image=slider_info['left_image_path'], pos=(-5, -8.4), size=1.3)
#             left_image.draw()
#         if slider_info['right_image_path'] is not None:
#             right_image = visual.ImageStim(win, image=slider_info['right_image_path'], pos=(5, -8.4), size=1.3)
#             right_image.draw()
#     else:
#         print("La dimensión del trial no está definida en sliders_dict:", trial['dimension'])
#         continue  #

#     # Inicializar lista para almacenar anotaciones continuas para este ensayo
#     mouse_annotation = []
    
#     # Restablecer el deslizador de valencia para el nuevo ensayo
#     dimension_slider.reset()
#     dimension_slider.markerPos = 0  # Establecer la posición inicial del marcador

#     # Obtener objeto del ratón y hacerlo visible
#     mouse = event.Mouse(visible=True, win=win)
#     mouse.setPos(newPos=(0, dimension_slider.pos[1]))

#     # Calculate the range in pixels for the slider
#     slider_start = dimension_slider.pos[0] - (dimension_slider.size[0] / 2)
#     slider_end = dimension_slider.pos[0] + (dimension_slider.size[0] / 20)

#     dimension_slider.name = trial['dimension']

#     # Si el ensayo es el especial para mostrar la pantalla verde
#     if trial['movie_path'] == 'green_screen':
        
        # # Tiempo de inicio para el ensayo de pantalla verde
        # green_screen_start_time = core.getTime()

        # # Calcular el número total de frames basado en la duración y el frame rate de la ventana
        # num_frames = len(green_screen_variation)

        # for frame in range(num_frames):
        #     # Calcular el valor de intensidad verde para el frame actual
        #     # Ajustando el rango de -1 a 1 para mapearlo a 25 a 255
        #     green_intensity = ((green_screen_variation[frame] + 1) / 2) * (255 - 25) + 25
            
        #     # Establecer el color de la ventana usando el valor calculado (manteniendo rojo y azul constantes)
        #     win.setColor([20, green_intensity, 12], 'rgb255')
            
        #     # Dibujar todo lo necesario en este frame
        #     win.flip()
            
        #     # Manejar interacción con el deslizador en cada frame
        #     if mouse.getPressed()[0]:  # Si se presiona el botón izquierdo del ratón
        #         mouse_x, _ = mouse.getPos()
        #         if slider_start <= mouse_x <= slider_end:  # Si la posición del ratón está dentro del rango del deslizador
        #             norm_pos = (mouse_x - slider_start) / dimension_slider.size[0]
        #             slider_value = norm_pos * (dimension_slider.ticks[-1] - dimension_slider.ticks[0]) + dimension_slider.ticks[0]
        #             dimension_slider.markerPos = round(slider_value, 2)
        #             mouse_annotation.append([slider_value, core.getTime() - green_screen_start_time])  # Añadir valor al registro de anotaciones junto con el timestamp

        #     left_image.draw()
        #     right_image.draw()
        #     intensity_cue_image.draw()
        #     dimension_slider.draw()
        #     slider_thumb.draw()

        #     # Actualizar posición del pulgar en el deslizador
        #     thumb_pos_x = (dimension_slider.markerPos - dimension_slider.ticks[0]) / (dimension_slider.ticks[-1] - dimension_slider.ticks[0]) * dimension_slider.size[0] - (dimension_slider.size[0] / 2)
        #     slider_thumb.setPos([thumb_pos_x, dimension_slider.pos[1]])

        # # Restablecer el color de fondo a negro al final del ensayo
        # win.setColor('black')
        # win.flip()
        # # Añadir anotaciones continuas al final del ensayo
        # exp.addData('continuous_annotation', mouse_annotation)
        # #continue
#     else:
#         video_start_time = core.getTime()
#         # Procesamiento para ensayos que involucran la presentación de un video
#         mov = visual.MovieStim3(win=win, filename=trial['movie_path'], size=(1024, 768), pos=[0, 0], noAudio=True)
#         while mov.status != constants.FINISHED:
#             mov.draw()
#             left_image.draw()
#             right_image.draw()
#             intensity_cue_image.draw()
#             dimension_slider.draw()
#             slider_thumb.draw()

#             if mouse.getPressed()[0]:
#                 mouse_x, _ = mouse.getPos()
#                 if slider_start <= mouse_x <= slider_end:
#                     norm_pos = (mouse_x - slider_start) / dimension_slider.size[0]
#                     slider_value = norm_pos * (dimension_slider.ticks[-1] - dimension_slider.ticks[0]) + dimension_slider.ticks[0]
#                     dimension_slider.markerPos = round(slider_value, 2)
#                     mouse_annotation.append([slider_value, core.getTime() - video_start_time])

#             thumb_pos_x = (dimension_slider.markerPos - dimension_slider.ticks[0]) / (dimension_slider.ticks[-1] - dimension_slider.ticks[0]) * dimension_slider.size[0] - (dimension_slider.size[0] / 2)
#             slider_thumb.setPos([thumb_pos_x, dimension_slider.pos[1]])
#             win.flip()

#             # Manejar la salida anticipada
#             keys = event.getKeys()  
#             if 'escape' in keys:
#                 win.close()
#                 core.quit()

#         # Añadir anotaciones continuas al final del ensayo
#         exp.addData('continuous_annotation', mouse_annotation)

#         ############### SCALES ################
#         mostrar_sliders_y_recoger_respuestas(win, sliders_dict, practice_trials, params)

#     # Siguiente entrada del registro de datos
#     core.wait(params['iti'])
#     exp.nextEntry()

###########################################################################
########                        TEST BLOCK                        ########
##########################################################################

# Función para cargar los bloques desde un archivo CSV
def cargar_bloques(nombre_archivo):
    return data.importConditions(nombre_archivo)

# Función para ejecutar los trials de un bloque específico
def ejecutar_trials(win, archivo_bloque, sliders_dict):

    # Cargar imágenes para los extremos y el marcador del slider
    intensity_cue_image = visual.ImageStim(win, image='./images_scale/AS_intensity_cue.png', pos=(0, -8.7), size=(8, 0.6))

    ## Initialize the slider
    dimension_slider = visual.Slider(win=win, name='dimension', ticks=(-1, 1), labels=None, pos=(0, -8.1), size=(8, 0.25),
                                style=['slider'], granularity=0.1, color='white', font='Helvetica',
                                lineColor='white', fillColor='white', borderColor='white', markerColor='white')
    
    condiciones = data.importConditions(archivo_bloque)
    print(archivo_bloque)
    trials = data.TrialHandler(trialList=condiciones, nReps=1, method='random', name = 'trials')

    exp.addLoop(trials)

    for trial in trials:
        left_image, right_image = presentar_instrucciones(trial['dimension'], trial['hand'], win, params, sliders_dict,
                                                            order_emojis_slider=trial['order_emojis_slider'])
        
        # Usar 'Dimension' del trial para determinar las rutas de las imágenes
        if trial['dimension'] in sliders_dict:
            slider_info = sliders_dict[trial['dimension']]            
        
        # Invertir las imágenes si 'order_emojis_slider' es 'inverse'
        if 'order_emojis_slider' in trial and trial['order_emojis_slider'] == "inverse":
            # Verificar si hay rutas de imagen definidas y crear los estímulos de imagen invertidos
            if slider_info['right_image_path'] is not None and slider_info['left_image_path'] is not None:
                left_image = visual.ImageStim(win, image=slider_info['right_image_path'], pos=(-5, -8.4), size=1.3)
                right_image = visual.ImageStim(win, image=slider_info['left_image_path'], pos=(5, -8.4), size=1.3)
        else:
            # Verificar si hay rutas de imagen definidas y crear los estímulos de imagen normales
            if slider_info['left_image_path'] is not None:
                left_image = visual.ImageStim(win, image=slider_info['left_image_path'], pos=(-5, -8.4), size=1.3)
            if slider_info['right_image_path'] is not None:
                right_image = visual.ImageStim(win, image=slider_info['right_image_path'], pos=(5, -8.4), size=1.3)
        
        # Dibujar las imágenes
        if slider_info['left_image_path'] is not None:
            left_image.draw()
        if slider_info['right_image_path'] is not None: 
            right_image.draw()
        else:
            print("La dimensión del trial no está definida en sliders_dict:", trial['dimension'])
            continue  #

        # Inicializar lista para almacenar anotaciones continuas para este ensayo
        mouse_annotation = []
        mouse_annotation_aux = []

        # Restablecer el deslizador de valencia para el nuevo ensayo
        dimension_slider.reset()
        dimension_slider.markerPos = 0  # Establecer la posición inicial del marcador

        # Obtener objeto del ratón y hacerlo visible
        mouse = event.Mouse(visible=True, win=win)
        mouse.setPos(newPos=(0, dimension_slider.pos[1]))

        # Calculate the range in pixels for the slider
        slider_start = dimension_slider.pos[0] - (dimension_slider.size[0] / 2)
        slider_end = dimension_slider.pos[0] + (dimension_slider.size[0] / 2)

        dimension_slider.name = trial['dimension']

        left_image.draw()
        right_image.draw()
        intensity_cue_image.draw()
        dimension_slider.draw()

        ## Create a custom white circle as the slider thumb
        slider_thumb = visual.Circle(win, pos=(0, -8.4), radius=0.30, fillColor='white', lineColor='black', edges=32)
        slider_thumb.draw()

        print(trial['movie_path'])
        
        # Procesamiento para ensayos que involucran la presentación de un video
        mov = visual.MovieStim3(win=win, filename=trial['movie_path'], size=(1024, 768), pos=[0, 0], noAudio=True)

        video_start_time = core.getTime()
        while mov.status != constants.FINISHED:
            mov.draw()
            left_image.draw()
            right_image.draw()
            intensity_cue_image.draw()
            dimension_slider.draw()
            slider_thumb.draw()

            win.flip()

            #if mouse.getPressed()[0]:
            mouse_x, _ = mouse.getPos()
            if slider_start <= mouse_x <= slider_end:
                norm_pos = (mouse_x - slider_start) / dimension_slider.size[0]
                slider_value = norm_pos * (dimension_slider.ticks[-1] - dimension_slider.ticks[0]) + dimension_slider.ticks[0]
                dimension_slider.markerPos = round(slider_value, 2)
                mouse_annotation.append([slider_value, core.getTime() - video_start_time])
                mouse_annotation_aux.append(slider_value) 

            thumb_pos_x = (dimension_slider.markerPos - dimension_slider.ticks[0]) / (dimension_slider.ticks[-1] - dimension_slider.ticks[0]) * dimension_slider.size[0] - (dimension_slider.size[0] / 2)
            slider_thumb.setPos([thumb_pos_x, dimension_slider.pos[1]])

            # Manejar la salida anticipada
            keys = event.getKeys()  
            if 'escape' in keys:
                win.close()
                core.quit()
            # if 'space' in keys:  # Verificar si se presionó la tecla "space"
                # break  # Salir del bucle while, finalizando la reproducción del video

        # Añadir anotaciones continuas al final del ensayo
        exp.addData('continuous_annotation', mouse_annotation)
        exp.addData('video_duration', mov.duration)
        
        mostrar_sliders_y_recoger_respuestas(win, sliders_dict, trials, params)

        # Siguiente entrada del registro de datos
        core.wait(params['iti'])
        
        # Instrucciones luminancia
        left_image, right_image = presentar_instrucciones('luminance', trial['hand'], win, params, sliders_dict,
                                                            order_emojis_slider=trial['order_emojis_slider'])
        # Cambiar las posiciones a (0, 1)
        left_image.pos = (-5, -8.4)
        right_image.pos = (5, -8.4)
        slider_thumb.pos=(0, -8.1)

        green_screen_variation = mouse_annotation_aux

        # Restablecer el deslizador de valencia para el nuevo ensayo
        dimension_slider.reset()
        dimension_slider.markerPos = 0  # Establecer la posición inicial del marcador

        # Obtener objeto del ratón y hacerlo visible
        mouse = event.Mouse(visible=True, win=win)
        mouse.setPos(newPos=(0, dimension_slider.pos[1]))

        # Calculate the range in pixels for the slider
        slider_start = dimension_slider.pos[0] - (dimension_slider.size[0] / 2)
        slider_end = dimension_slider.pos[0] + (dimension_slider.size[0] / 2)

        # Calcular el número total de frames basado en la duración y el frame rate de la ventana
        num_frames = len(green_screen_variation)

        mouse_annotation_green = []

        # Tiempo de inicio para el ensayo de pantalla verde
        green_screen_start_time = core.getTime()

        for frame in range(num_frames):
            # Calcular el valor de intensidad verde para el frame actual

            # Ajustando el rango de -1 a 1 para mapearlo a 25 a 255
            green_intensity = ((green_screen_variation[frame] + 1) / 2) * (255 - 25) + 25
            
            #green_intensity = green_screen_variation[frame] 
            #green_intensity_normalized = (green_screen_variation[frame] + 1) / 2
            
            # Establecer el color de la ventana usando el valor calculado (manteniendo rojo y azul constantes)
            win.setColor([20, green_intensity, 12], 'rgb255')

            left_image.draw()
            right_image.draw()
            intensity_cue_image.draw()
            dimension_slider.draw()
            slider_thumb.draw()
            
            # Dibujar todo lo necesario en este frame
            win.flip()

            # Manejar interacción con el deslizador en cada frame
            #if mouse.getPressed()[0]:  # Si se presiona el botón izquierdo del ratón
            mouse_x, _ = mouse.getPos()
            if slider_start <= mouse_x <= slider_end:  # Si la posición del ratón está dentro del rango del deslizador
                norm_pos = (mouse_x - slider_start) / dimension_slider.size[0]
                slider_value_green = norm_pos * (dimension_slider.ticks[-1] - dimension_slider.ticks[0]) + dimension_slider.ticks[0]
                dimension_slider.markerPos = round(slider_value_green, 2)
                mouse_annotation_green.append([slider_value_green, core.getTime() - green_screen_start_time])  # Añadir valor al registro de anotaciones junto con el timestamp

            # Actualizar posición del pulgar en el deslizador
            thumb_pos_x = (dimension_slider.markerPos - dimension_slider.ticks[0]) / (dimension_slider.ticks[-1] - dimension_slider.ticks[0]) * dimension_slider.size[0] - (dimension_slider.size[0] / 2)
            slider_thumb.setPos([thumb_pos_x, dimension_slider.pos[1]])

        # Restablecer el color de fondo a negro al final del ensayo
        win.setColor('black')
        win.flip()
        # Añadir anotaciones continuas al final del ensayo
        exp.addData('continuous_annotation_luminance', mouse_annotation_green)

        exp.nextEntry()  # Finalizar la entrada actual y prepararse para la siguiente

# Cargar los subbloques de cada suprabloque
        
subbloques_A = cargar_bloques('./conditions/Blocks_A.csv')
subbloques_B = cargar_bloques('./conditions/Blocks_B.csv')

# Función para ejecutar todos los subbloques de un suprabloque
def ejecutar_suprabloque(win, subbloques):  
    random.shuffle(subbloques)  # Aleatorizar el orden de los subbloques
    for subbloque in subbloques:
        ruta_subbloque = subbloque['condsFile']
        ejecutar_trials(win, ruta_subbloque, sliders_dict)

# Asignar bloque inicial basado en alguna condición externa (ejemplo)
bloque_inicial = 'B'  # o 'A'

# Ejecutar los suprabloques en el orden determinado por bloque_inicial
if bloque_inicial == 'A':
    ejecutar_suprabloque(win, subbloques_A)
    ejecutar_suprabloque(win, subbloques_B)
else:
    ejecutar_suprabloque(win, subbloques_B)
    ejecutar_suprabloque(win, subbloques_A)

win.close()


##########################################################################
###################### Feedback + Goodbye message ######################## 
kb.clearEvents()
n_corr = np.count_nonzero(trials.data['response'] == 'correct')
if n_corr == 1:
    msg_trial = 'trial'
else:
    msg_trial = 'trials'
msg = "You got %i %s correct!" % (n_corr, msg_trial)

feedback_msg = visual.TextStim(win,
                                height=params['text_height'],
                                pos=[0, +6],
                                text=msg,
                                wrapWidth=80)

goodbye_msg = visual.TextStim(win,
                                height=params['text_height'],
                                pos=[0, -6],
                                text=instructions.non_immersive_instructions_text['5_goodbye_text'],
                                wrapWidth=80)

feedback_msg.draw()
goodbye_msg.draw()
win.flip()

event.waitKeys(maxWait=params['stim_time'], keyList=['space'])

# Task shutdown
#pg.exit()git
win.close()
#pg.exit(show_metadata=params['show_metadata'])

############ OPTIONAL: Converting BDF file to CSV #############
# Clock to quit bdf before trying to open it
# Some computers take more or less time in closing the file.
# change it accordingly if error "file has already been opened"
time.sleep(60)

#ReadPurpleGaze(pg.subject_id + '.bdf', pg.subject_id, subject_folder)
csv_file = subject_folder + info_dict['Subject_id'] + '_.csv'
#MakeReport(csv_file, report_path=subject_folder, subject_id=pg.subject_id)
################################################################

# Finish psychopy thread
core.quit()
