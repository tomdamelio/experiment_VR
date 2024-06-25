# -*- coding: utf-8 -*-
#%%


#%%

import os
import glob
import re
import matplotlib.pyplot as plt

import pyxdf

import mne
from mnelab.io.xdf import read_raw_xdf

#%%

results_folder = 'Results'
subject = '20'
session = 'a'
data = 'experiment_vr_non_inmersive_physio'
fname = os.path.join(f"sub-{subject}", f"ses-{session.upper()}", f"{data}")

# full_path = os.path.join('../',results_folder, fname)
full_path = "C:/Users/tomas/OneDrive/Desktop/Tesis de Licenciatura/Emociones/Results/sub-20/ses-A/physio/sub-20_ses-a_task-experiment_vr_non_immersive_physio.xdf"
xdf_files = glob.glob(full_path)

print([file for file in xdf_files])

# if os.path.exists(full_path):
#     xdf_files = glob.glob(full_path + "/*.xdf")
#     xdf_files = 
    
#     print([file for file in xdf_files])
# else:
#     print(f"The folder {full_path} does not exist.")

#%%

for file in xdf_files:
    match = re.search('task-(.*?)_physio', file)


    task = match.group(1)
    print(f'Task name: {task}')

    streams, header = pyxdf.load_xdf(file)
    
    for stream in streams:
        if  stream['info']['type'][0] == 'EEG':
            raw = read_raw_xdf(file, stream_ids=[stream['info']['stream_id']],preload=True)
            print(raw.info)

            # Downsample the data to 500 Hz
            raw.resample(500, npad="auto")

            # raw.plot()
            # plt.show()
            data = 'eeg'

            results_name = f"sub-{subject}/ses-{session.upper()}/{data}/sub-{subject}_ses-{session}_task-{task}_{data}.fif"
            os.makedirs(os.path.join('../', results_folder, f'sub-{subject}/ses-{session.upper()}/{data}/'), exist_ok=True)

            raw.save(os.path.join('../', results_folder, results_name), overwrite=True)
        
        elif stream['info']['type'][0] == 'gaze':
            raw = read_raw_xdf(file, stream_ids=[stream['info']['stream_id']],preload=True)
            print(raw.info)

            # raw.plot()
            # plt.show()
            data = 'gaze'

            results_name = f"sub-{subject}/ses-{session.upper()}/{data}/sub-{subject}_ses-{session}_task-{task}_{data}.fif"
            os.makedirs(os.path.join('../', results_folder, f'sub-{subject}/ses-{session.upper()}/{data}/'), exist_ok=True)

            raw.save(os.path.join('../', results_folder, results_name), overwrite=True)
            
        elif stream['info']['type'][0] == 'Markers':
            print('Shape Markers:', stream['time_stamps'].shape)
