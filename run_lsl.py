import subprocess
import threading
import os
import time
import socket
import tkinter as tk
from tkinter import ttk
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from pylsl import StreamInfo, StreamOutlet

def execute_command(path, command):
    print(f'Executing proceess {command}')
    process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, cwd=path)

    if process.poll():
        error = process.stderr.read().decode()
        print(f"Error: {error}")
        raise subprocess.CalledProcessError(process.returncode, command)

def execute_lab_recorder(config_file=None):
    os.system("taskkill /IM LabRecorder.exe /F")
    command = "LabRecorder.exe"
    if config_file:
        command += f" -c {config_file}"
    execute_command("C:/Users/Cocudata/Desktop/LabRecorder", command)

def execute_game_controller():
    os.system("taskkill /IM GameController.exe /F")
    execute_command("C:/Users/Cocudata/GameController/", "GameController.exe")

def execute_brainamp_connector(config_file=None):
    os.system("taskkill /IM BrainAmpSeries.exe /F")
    command = "BrainAmpSeries.exe"
    if config_file:
        command += f" -c {config_file}"
    execute_command("C:/Users/Cocudata/BrainAmpSeries/bin/", command)

def setup_lsl_outlet():
    info = StreamInfo(name='markers', type='Markers', channel_count=1,
                     channel_format='string', source_id='vr-markers')
    outlet = StreamOutlet(info)
    return outlet

def create_bids_folders(info_dict):
    results_folder = "C:/Users/Cocudata/experiment_VR/results"
    
    subject_folder = os.path.join(results_folder, f"sub-{info_dict['ID']}")
    os.makedirs(subject_folder, exist_ok=True)
    
    session_folder = os.path.join(subject_folder, f"ses-{info_dict['Sesion']}")
    os.makedirs(session_folder, exist_ok=True)
    
    physio_folder = os.path.join(session_folder, "physio")
    os.makedirs(physio_folder, exist_ok=True)
    
    audio_folder = os.path.join(session_folder, "audio")
    os.makedirs(audio_folder, exist_ok=True)
    
    return physio_folder, audio_folder

def initialize_lsl_recording(info_dict, physio_file_name):
    modality = 'physio'
    command = f"filename {{root:C:/Users/Cocudata/experiment_VR/results/}} {{template:sub-%p/ses-%s/{modality}/{physio_file_name}.xdf}} {{participant:{info_dict['ID']}}} {{session:{info_dict['Sesion']}}} {{task:{info_dict['exp_name']}}} {{modality:{modality}}}\n"
    
    try:
        s = socket.create_connection(("localhost", 22345))
        s.sendall(b"update\n")
        s.sendall(b"select all\n")
        s.sendall(command.encode())
        s.sendall(b"start\n")
        return s
    except ConnectionRefusedError:
        print("Warning: Unable to connect to LSL server. Proceeding without LSL.")
        return None

def get_participant_info():
    def validate_id():
        try:
            id_num = int(id_entry.get())
            if 0 <= id_num <= 999:
                info['ID'] = f"{id_num:03d}"
                root.quit()
            else:
                raise ValueError
        except ValueError:
            error_label.config(text="Error: ID debe ser un número entre 000 y 999")
            return
        
    root = tk.Tk()
    root.title("Configuración de la sesión")
    
    info = {}
    
    # ID Entry
    tk.Label(root, text="ID (000-999):").grid(row=0, column=0, padx=5, pady=5)
    id_entry = tk.Entry(root)
    id_entry.grid(row=0, column=1, padx=5, pady=5)
    
    # Session Dropdown
    tk.Label(root, text="Sesión:").grid(row=1, column=0, padx=5, pady=5)
    session_var = tk.StringVar(value="A")
    session_dropdown = ttk.Combobox(root, textvariable=session_var, values=["A", "B"], state="readonly")
    session_dropdown.grid(row=1, column=1, padx=5, pady=5)
    
    # Condition Dropdown
    tk.Label(root, text="Condición:").grid(row=2, column=0, padx=5, pady=5)
    condition_var = tk.StringVar(value="VR")
    condition_dropdown = ttk.Combobox(root, textvariable=condition_var, values=["VR", "2D"], state="readonly")
    condition_dropdown.grid(row=2, column=1, padx=5, pady=5)
    
    # Error Label
    error_label = tk.Label(root, text="", fg="red")
    error_label.grid(row=3, column=0, columnspan=2, pady=5)
    
    # Submit Button
    submit_btn = tk.Button(root, text="Comenzar", command=validate_id)
    submit_btn.grid(row=4, column=0, columnspan=2, pady=10)
    
    root.mainloop()
    
    info['Sesion'] = session_var.get()
    info['Condicion'] = condition_var.get()
    
    root.destroy()
    return info

if __name__ == "__main__":
    # Get participant information
    info_dict = get_participant_info()
    
    # Setup experiment name and file names
    info_dict['exp_name'] = f"Experiment_{info_dict['Condicion']}"
    physio_file_name = f"sub-{info_dict['ID']}_ses-{info_dict['Sesion']}_task-{info_dict['exp_name']}_physio"
    audio_file_name = f"sub-{info_dict['ID']}_ses-{info_dict['Sesion']}_task-{info_dict['exp_name']}_audio.wav"

    # Create BIDS folders
    physio_folder, audio_folder = create_bids_folders(info_dict)
    
    # Setup LSL outlet
    outlet = setup_lsl_outlet()
    
    # Initialize LSL recording
    s = initialize_lsl_recording(info_dict, physio_file_name)
    
    # Start recording threads
    try:
        LRthread = threading.Thread(target=execute_lab_recorder, args=("LabRecorder - Copy.cfg",))
        GCthread = threading.Thread(target=execute_game_controller)
        BAthread = threading.Thread(target=execute_brainamp_connector, args=(["C:/Users/Cocudata/experiment_VR/mw_lsl_42chs.cfg"]))
   
        # Start the threads
        LRthread.start()
        time.sleep(5)
        GCthread.start()
        BAthread.start()

        # Send block start marker
        outlet.push_sample([f"BLOCK_{info_dict['Sesion']}_START"])

        # Setup audio recording
        samplerate = 44100
        channels = 1
        max_dur = 7200  # 2 hours max duration
        
        # Start audio recording
        recording = sd.rec(int(samplerate * max_dur), 
                         samplerate=samplerate, 
                         channels=channels, 
                         dtype='float64', 
                         blocking=False)
        
        recording_start_time = time.time()
        
        # Wait for 'p' key press
        print("Presione 'p' para finalizar la grabación")
        while True:
            if input() == 'p':
                break
        
        # Calculate recording duration
        recording_duration = time.time() - recording_start_time
        
        # Send end marker
        outlet.push_sample([f"SUPRABLOCK_{info_dict['Sesion']}_END"])
        
        # Stop LSL recording
        if s:
            s.sendall(b"stop\n")
            s.close()
        
        # Save audio recording
        actual_samples = int(recording_duration * samplerate)
        trimmed_recording = recording[:actual_samples]
        audio_path = os.path.join(audio_folder, audio_file_name)
        write(audio_path, samplerate, np.int16(trimmed_recording * 32767))
        
        print("Grabación finalizada y guardada")
        
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
    finally:
        # Cleanup
        if s:
            s.close()
