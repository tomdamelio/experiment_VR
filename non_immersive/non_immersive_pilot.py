# Experiment VR: Non Immersive Task
# Author: Tomas D'Amelio


from psychopy import core, visual, data, event, constants
from psychopy.hardware import keyboard

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
# Instantiate dialog box
# my_dlg = gui.DlgFromDict(info_dict, title=params.exp_name,
#                          order=order)
# if my_dlg.OK == False:
#     core.quit()  # user pressed cancel

info_dict['date'] = data.getDateStr()

##########################################################################
# Experiment data settings

# create folder to save experiment data for each subject
subject_folder = subject_folder = params['results_folder'] + f"{info_dict['Subject_id']}/"

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
# Set stimuli
# Basic emotion names
basic_emotions = {'1': '1. Anger', '2': '2. Fear', '3': '3. Disgust',
                    '4': '4. Joy', '5': '5. Sadness', '6': '6. Surprise'}

# Basic emotion positions
pos_basic_emotions = [(-7.0, 4.0), (0.0, 4.0), (7.0, 4.0),
                        (-7.0, -4.0), (0.0, -4.0), (7.0, -4.0)]

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
for _, value in sorted(instructions.non_immersive_instructions_text.items())[:3]:
    instruction_practice = visual.TextStim(win,
                                            height=params['text_height'],
                                            pos=[0, 0],
                                            text=value,
                                            wrapWidth=80)
    instruction_practice.draw()
    # Flip the front and back buffers
    win.flip()

    # To begin the Experimetn with Spacebar or RightMouse Click
    press_button = True
    while press_button:
        keys = event.getKeys(keyList=['space'])

        mouse = event.Mouse(visible=False, win=win)
        mouse_click = mouse.getPressed()

        if 'space' in keys or 1 in mouse_click:
            press_button = False

# Create trial handler
practice_trials = data.TrialHandler(
    trialList=data.importConditions('non_immersive_practice_conditions.csv'),
    originPath=-1, nReps=1, method='random', name='practice')

exp.addLoop(practice_trials)

#pg.log('Annotation', txt='Practice Block begun')
scr_idlog = 0
trial_idlog = 0

# Cargar imágenes para los extremos y el marcador del slider
unhappy_image = visual.ImageStim(win, image='./images_scale/AS_unhappy_final.png', pos=(-5, -8.4), size=1.3)
happy_image = visual.ImageStim(win, image='./images_scale/AS_happy_final.png', pos=(5, -8.4), size=1.3)
intensity_cue_image = visual.ImageStim(win, image='./images_scale/AS_intensity_cue.png', pos=(0, -8.7), size=(8, 0.6))

# Initialize the slider
valence_slider = visual.Slider(win=win, name='valence', ticks=(-1, 1), labels=None, pos=(0, -8.1), size=(8, 0.25),
                            style=['slider'], granularity=0.1, color='white', font='HelveticaBold',
                            lineColor='white', fillColor='white', borderColor='white', markerColor='white')

# Create a custom white circle as the slider thumb
slider_thumb = visual.Circle(win, radius=0.30, fillColor='white', lineColor='black', edges=32)

# Loop over trials handler
for trial in practice_trials:

    # Initialize a list to store continuous annotations for this trial
    mouse_annotation = []
    
    # Create fixation cross 2
    fixation = visual.GratingStim(win, color=1, colorSpace='rgb',
                                    tex=None, mask='cross', size=2)

    # Create visual stimulus for emotional faces
    mov = visual.MovieStim3(win=win, filename=trial['movie_path'],
                            size=(1024, 768), pos=[0, 0], noAudio=True)

    # Draw fixation
    fixation.draw()
    win.flip()
    core.wait(params['fixation_time'])

    # Flush the buffers
    kb.clearEvents()

    # Clock reset
    kb.clock.reset()

    # Reset the valence_slider for the new trial
    valence_slider.reset()
    valence_slider.markerPos = 0  # Set the initial position of the marker

    # Get the mouse object
    mouse = event.Mouse(visible=True, win=win)  # Make the mouse visible
    mouse.setPos(newPos=(0, valence_slider.pos[1]))  # Start the mouse at the center of the slider

    # Calculate the range in pixels for the slider
    slider_start = valence_slider.pos[0] - (valence_slider.size[0] / 2)
    slider_end = valence_slider.pos[0] + (valence_slider.size[0] / 2)

    while mov.status != constants.FINISHED:
        # Dibuja el video
        mov.draw()

        unhappy_image.draw()
        happy_image.draw()
        intensity_cue_image.draw()

        # Draw the slider (without the default marker)
        valence_slider.draw()

        # Draw the slider thumb
        slider_thumb.draw()

        # Check for mouse button press and position
        if mouse.getPressed()[0]:  # If left mouse button is pressed
            mouse_x, _ = mouse.getPos()
            if slider_start <= mouse_x <= slider_end:  # If the mouse x position is within the slider
                # Normalize the mouse position to a slider value
                norm_pos = (mouse_x - slider_start) / valence_slider.size[0]
                slider_value = norm_pos * (valence_slider.ticks[-1] - valence_slider.ticks[0]) + valence_slider.ticks[0]
                valence_slider.markerPos = round(slider_value, 2) 
                # Add the current slider value to the continuous annotations
                mouse_annotation.append(slider_value)


        # Draw the custom thumb on the slider
        thumb_pos_x = (valence_slider.markerPos - valence_slider.ticks[0]) / (valence_slider.ticks[-1] - valence_slider.ticks[0]) * valence_slider.size[0] - (valence_slider.size[0] / 2)
        slider_thumb.setPos([thumb_pos_x, valence_slider.pos[1]])

        # Actualiza la ventana
        win.flip()

        # Revisa si se ha presionado 'escape' para terminar el experimento
        if 'escape' in keys:
            win.close()
            core.quit()

        # Limpia el buffer de eventos de ratón que ya se han procesado
        mouse.getWheelRel()  # This is a trick to prevent mouse wheel buffer from filling up

        # Limpia el buffer de teclas que ya se han procesado
        kb.clearEvents()

        # At the end of the trial, add the continuous annotations to the trial data
        practice_trials.addData('continuous_annotation', mouse_annotation)

    # Draw visual stimulus for emotional faces
    for emotion, position in zip(basic_emotions.values(), pos_basic_emotions):
        emotion_response = visual.TextStim(
            win, text=str(emotion), height=params['text_height'],
            pos=position)
        emotion_response.draw()

    win.flip()

    # Get key response
    key, rt = event.waitKeys(keyList=basic_emotions.keys(),
                                timeStamped=core.Clock())[0]
    practice_trials.addData('emotion_key', key)
    practice_trials.addData('emotion_rt', rt)

    # Get correct/incorrect response
    if str(key) == str(trial['correct_response']):
        response = 'correct'
    else:
        response = 'incorrect'
    practice_trials.addData('response', response)

    # Inter Trial Interval(ITI) with blank screen
    win.flip()
    core.wait(params['iti'])

    scr_idlog += 1
    trial_idlog += 1
    exp.nextEntry()


##########################################################################
########                        TEST BLOCK                        ########
##########################################################################

# Create test instructions ('text' visual stimulus)
instruction_test = visual.TextStim(win,
                                    height=params['text_height'],
                                    pos=[0, 0],
                                    text=instructions.non_immersive_instructions_text['4_test_text'],
                                    wrapWidth=80)

# Draw test instructions
instruction_test.draw()

# Flip the front and back buffers
win.flip()

# To begin the Experimetn with Spacebar or LeftMouse Click
press_button = True
while press_button:
    keys = event.getKeys(keyList=['space'])

    mouse = event.Mouse(visible=False, win=win)
    mouse_click = mouse.getPressed()

    if 'space' in keys or 1 in mouse_click:
        press_button = False

# Wait until 'space' is pressed
# event.waitKeys(keyList=['space',], timeStamped=False)

# Create trial handler
trials = data.TrialHandler(
    trialList=data.importConditions('./non_immersive_conditions.csv'),
    originPath=-1, nReps=1, method='random', name='test')

exp.addLoop(trials)

#pg.log('Annotation', txt='Test Block begun')
scr_idlog = 0
trial_idlog = 0

# Loop over trials handler
for trial in trials:
    
    # Create fixation cross 2
    fixation = visual.GratingStim(win, color=1, colorSpace='rgb',
                                    tex=None, mask='cross', size=2)

    # Create visual stimulus for emotional faces
    mov = visual.MovieStim3(win=win, filename=trial['movie_path'], size=(
        1024, 768), pos=[0, 0], noAudio=True)

    # Draw fixation
    #pg.log("ScreenIn", screenname=f'Fixation: {scr_idlog}', screenid=scr_idlog, trialname=f'trial_{trial_idlog}',
    #       stims=[['fixation_cross', [int(fixation.size[0]), int(fixation.size[1])],
    #               [int(fixation.pos[0]), int(fixation.pos[1])]]])
    fixation.draw()
    win.flip()
    core.wait(params['fixation_time'])
    # log fixation
    #pg.log("ScreenOut", screenname=f'Fixation: {scr_idlog}')


    # Flush the buffers
    kb.clearEvents()

    # Clock reset
    kb.clock.reset()
    valence_slider.reset()

    # log information of the stimuli to the eytracker BDF file
    #pg.log("ScreenIn", screenname=f"{trial['movie_path']}: {scr_idlog}", screenid=scr_idlog,
    #       condition=trial['emotion'],
    #       duration=params['stim_time'], trialname=f'trial_{trial_idlog}',
    #       stims=[[trial['movie_path'], [int(mov.size[0]), int(mov.size[1])], [int(mov.pos[0]), int(mov.pos[1])]]])

    valence_slider.markerPos = 5

    while mov.status != constants.FINISHED:
        # Dibuja el video
        mov.draw()

        # Dibuja el slider
        valence_slider.draw()

        # Actualiza la ventana
        win.flip()

        # Revisa las teclas presionadas
        keys = kb.getKeys(['left', 'right', 'escape'], waitRelease=False)
        for key in keys:
            if key.name == 'left':
                # Disminuye la valencia
                valence_slider.markerPos = max(1, valence_slider.markerPos - 0.25)
            elif key.name == 'right':
                # Aumenta la valencia
                valence_slider.markerPos = min(9, valence_slider.markerPos + 0.25)
            elif key.name == 'escape':
                # Termina el experimento si se presiona 'escape'
                win.close()
                core.quit()

        # Limpia el buffer de teclas que ya se han procesado
        kb.clearEvents()

    # Write BDF and metadata
    #pg.log("ScreenOut", screenname=f"{trial['movie_path']}: {scr_idlog}")

    # Draw visual stimulus for emotional faces
    #pg.log('Annotation', txt='Emotions presented')
    for emotion, position in zip(basic_emotions.values(), pos_basic_emotions):
        emotion_response = visual.TextStim(
            win, text=str(emotion), height=params['text_height'],
            pos=position)
        emotion_response.draw()

    win.flip()

    # Get key response
    key, rt = event.waitKeys(keyList=basic_emotions.keys(),
                                timeStamped=core.Clock())[0]
    #pg.log('Annotation', txt='Response key and rt'+str(key)+','+str(rt))

    trials.addData('emotion_key', key)
    trials.addData('emotion_rt', rt)

    # Get correct/incorrect response
    if str(key) == str(trial['correct_response']):
        response = 'correct'
    else:
        response = 'incorrect'
    trials.addData('response', response)
    trials.addData('final_valence_rating', valence_slider.markerPos)

    # Inter Trial Interval(ITI) with blank screen
    win.flip()
    core.wait(params['iti'])
    scr_idlog += 1
    trial_idlog += 1
    exp.nextEntry()

#pg.log('Annotation', txt='Test Block ended')

# trials.saveAsText(fileName= subject_folder + file_name + '.csv')

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
#pg.exit()
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