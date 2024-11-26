#%%
import os
import sys

import mne
import matplotlib.pyplot as plt
import numpy as np
import neurokit2 as nk
import scipy.signal as sc

#%% ANTES DE CORRER TODO, PONER EL DIRECTORIO DONDE VAS A QUERER LA CARPETA
# ARREGLAR EL SUBJECT, SESSION Y FNAME

dir_folder = 'C:/Users/dameliotomas/experiment_VR/'
results_folder = 'results'
subject = '06'
session = 'A'
data = 'task-experiment_vr_non_immersive_eeg.fif'
fname = os.path.join(f"sub-{subject}_" + f"ses-{session.lower()}_" + f"{data}")

full_path = os.path.join('../', results_folder, f"sub-{subject}", f"ses-{session.upper()}", 'eeg', fname)


#%%
# raw = mne.io.read_raw(os.path.join(results_folder, fname), verbose=True, preload = True)
raw = mne.io.read_raw(full_path, verbose=True, preload = True)

data = raw.load_data()

markers = raw.annotations

df_data = data.to_data_frame()
df_markers = markers.to_data_frame()
print(df_data.columns)
print(df_markers.columns)

#%% Separo los dataframes en arrays que pueda leer Neurokit, es decir, ECG, EDA, RSP

edap = df_data['GSR'] #EDA posta (para ponerlo despues sin problema) MicroSiemens
ecgp = df_data['ECG'] #ECG posta
resp = df_data['RESP'] #RESP


#%% Generalizo el intervalo de sampleo, pongo lo que tenga el instrumental para no perder info

######### ¿Me conviene el promedio, el max o el minimo? ##############

interv = []
for i in range(0, len(df_data['time'])-1):
    t = df_data['time'][i+1] - df_data['time'][i]
    interv.append(t)
    
dt = np.mean(interv)
### se que lo dice el vhdr pero no se si confiar en el sistema de primera

#%% Leo los datos con NeuroKit (aunque RSP analiza con Harrison 2021)

df_eda, info_eda = nk.eda_process(edap, sampling_rate=1/dt) #neurokit method
df_ecg, info_ecg = nk.ecg_process(ecgp, sampling_rate=1/dt) #neurokit method
df_resp, info_resp = nk.rsp_process(resp, sampling_rate=1/dt) #Harrison 2021 method


#%% Ploteo de cada señal con NeuroKit

plot_eda = nk.eda_plot(df_eda, info = info_eda)
plot_ecg = nk.ecg_plot(df_ecg, info = info_ecg)
plot_resp = nk.rsp_plot(df_resp, info = info_resp)

#%% SOLO HACER UNA VEZ, te pasa los marcadores a un txt


fdir = os.path.dirname(full_path)
df_markers.to_csv(os.path.join(fdir,'marcadores.txt'), sep = '\t', index = False)