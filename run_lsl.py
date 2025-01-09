# Importaciones estándar
import os
import sys
import time
import socket
import threading
import subprocess
import argparse

# Importaciones de terceros
import tkinter as tk
from tkinter import ttk
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from pylsl import StreamInfo, StreamOutlet
import pyautogui

# Funciones de ejecución de procesos

def execute_command(path, command):
    """Ejecuta un comando en un directorio específico y maneja errores."""
    print(f'Executing process {command}')
    process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, cwd=path)

    if process.poll():
        error = process.stderr.read().decode()
        print(f"Error: {error}")
        raise subprocess.CalledProcessError(process.returncode, command)


def execute_lab_recorder(config_file=None):
    """Ejecuta el LabRecorder con un archivo de configuración opcional."""
    os.system("taskkill /IM LabRecorder.exe /F")
    command = "LabRecorder.exe"
    if config_file:
        command += f" -c {config_file}"
    execute_command("C:/Users/Cocudata/Desktop/LabRecorder", command)


def execute_game_controller():
    """Ejecuta el GameController."""
    os.system("taskkill /IM GameController.exe /F")
    execute_command("C:/Users/Cocudata/GameController/", "GameController.exe")


def execute_brainamp_connector(config_file=None):
    """Ejecuta el BrainAmpSeries con un archivo de configuración opcional."""
    os.system("taskkill /IM BrainAmpSeries.exe /F")
    command = "BrainAmpSeries.exe"
    if config_file:
        command += f" -c {config_file}"
    process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, 
                               cwd="C:/Users/Cocudata/BrainAmpSeries/bin/")
    if process.poll():
        error = process.stderr.read().decode()
        print(f"Error: {error}")
        raise subprocess.CalledProcessError(process.returncode, command)
    return process

# Funciones de configuración y grabación

def setup_lsl_outlet():
    """Configura y devuelve un StreamOutlet para LSL."""
    info = StreamInfo(name='markers', type='Markers', channel_count=1,
                      channel_format='string', source_id='vr-markers')
    return StreamOutlet(info)


def create_bids_folders(info_dict):
    """Crea las carpetas necesarias para almacenar los resultados en formato BIDS."""
    results_folder = "C:/Users/Cocudata/experiment_VR/results"
    subject_folder = os.path.join(results_folder, f"sub-{info_dict['ID']}")
    os.makedirs(subject_folder, exist_ok=True)
    session_folder = os.path.join(subject_folder, f"ses-{info_dict['session']}")
    os.makedirs(session_folder, exist_ok=True)
    physio_folder = os.path.join(session_folder, "physio")
    os.makedirs(physio_folder, exist_ok=True)
    audio_folder = os.path.join(session_folder, "audio")
    os.makedirs(audio_folder, exist_ok=True)
    return physio_folder, audio_folder


def initialize_lsl_recording(info_dict, physio_file_name):
    """Inicializa la grabación LSL con los parámetros proporcionados."""
    modality = 'physio'
    # Nombre de archivo simplificado
    physio_file_name = (f"sub-{info_dict['ID']}_ses-{info_dict['session'].lower()}_"
                       f"task-{info_dict['block'].lower()}_physio")
    
    command = (f"filename {{root:C:/Users/Cocudata/experiment_VR/results/}} "
              f"{{template:sub-%p/ses-%s/{modality}/{physio_file_name}.xdf}} "
              f"{{participant:{info_dict['ID']}}} "
              f"{{session:{info_dict['session'].lower()}}} "
              f"{{task:{info_dict['block'].lower()}}} "
              f"{{modality:{modality}}}\n")
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

# Funciones de interfaz de usuario

def get_participant_info():
    """Obtiene la información del participante y maneja la interfaz de grabación."""
    def start_recording():
        try:
            id_num = int(id_entry.get())
            if 0 <= id_num <= 99:
                info['ID'] = f"{id_num:02d}"
                info['block'] = block_var.get()
                info['session'] = session_var.get()
                info['exp_name'] = f"Experiment_{info['session']}"
                start_actual_recording()
                id_entry.config(state='disabled')
                block_dropdown.config(state='disabled')
                session_dropdown.config(state='disabled')
                start_btn.grid_forget()
                stop_btn.grid(row=4, column=0, columnspan=2, pady=10, sticky='nsew')
                status_label.config(text="Grabando...", fg="green")
                root.recording_active = True
            else:
                error_label.config(text="Error: ID debe ser un número entre 00 y 99")
                return
        except ValueError:
            error_label.config(text="Error: ID debe ser un número entre 00 y 99")
            return

    def start_actual_recording():
        physio_folder, audio_folder = create_bids_folders(info)
        root.physio_folder = physio_folder
        root.audio_folder = audio_folder
        root.outlet = setup_lsl_outlet()
        if not args.test:
            root.brainamp_process = execute_brainamp_connector(
                "C:/Users/Cocudata/experiment_VR/mw_lsl_42chs.cfg")
            GCthread = threading.Thread(target=execute_game_controller)
            GCthread.start()
            link_instructions_label = tk.Label(root, 
                text="Por favor, realiza las siguientes acciones y marca las casillas cuando estén listas:")
            link_instructions_label.grid(row=6, column=0, columnspan=2, pady=5)
            brainamp_var = tk.BooleanVar()
            brainamp_check = tk.Checkbutton(root, 
                text="He hecho clic en 'Link' en BrainAmp", 
                variable=brainamp_var)
            brainamp_check.grid(row=7, column=0, columnspan=2, pady=2)
            gamecontroller_var = tk.BooleanVar()
            gamecontroller_check = tk.Checkbutton(root, 
                text="He hecho clic en 'Link' en GameController", 
                variable=gamecontroller_var)
            gamecontroller_check.grid(row=8, column=0, columnspan=2, pady=2)
            start_btn.config(state='disabled')
            def on_links_confirmed():
                if brainamp_var.get() and gamecontroller_var.get():
                    link_instructions_label.grid_remove()
                    brainamp_check.grid_remove()
                    gamecontroller_check.grid_remove()
                    confirm_links_btn.grid_remove()
                    LRthread = threading.Thread(target=execute_lab_recorder, 
                                             args=("LabRecorder - Copy.cfg",))
                    LRthread.start()
                    time.sleep(5)
                    id_entry.config(state='disabled')
                    block_dropdown.config(state='disabled')
                    session_dropdown.config(state='disabled')
                    start_btn.grid_forget()
                    stop_btn.grid(row=4, column=0, columnspan=2, pady=10, sticky='nsew')
                    status_label.config(text="Grabando...", fg="green")
                    root.recording_active = True
                    root.s = initialize_lsl_recording(info, 
                        f"sub-{info['ID']}_ses-{info['session']}_task-{info['exp_name']}_physio")
                    root.outlet.push_sample([f"BLOCK_{info['session']}_START"])
                    root.samplerate = 44100
                    root.channels = 1
                    root.max_dur = 7200
                    root.recording = sd.rec(int(root.samplerate * root.max_dur),
                                          samplerate=root.samplerate,
                                          channels=root.channels,
                                          dtype='float64',
                                          blocking=False)
                    root.recording_start_time = time.time()
                else:
                    status_label.config(
                        text="Por favor, confirma ambos Links antes de continuar", 
                        fg="red")
            confirm_links_btn = tk.Button(root, 
                text="Confirmar y Continuar", 
                command=on_links_confirmed)
            confirm_links_btn.grid(row=9, column=0, columnspan=2, pady=5)

    def stop_recording():
        if root.recording_active:
            # Detener la grabación de audio
            recording_duration = time.time() - root.recording_start_time
            root.outlet.push_sample([f"SUPRABLOCK_{info['session']}_END"])
            
            # Detener Lab Recorder usando socket
            try:
                lab_recorder_socket = socket.create_connection(("localhost", 22345))
                lab_recorder_socket.sendall(b"stop\n")
                lab_recorder_socket.close()
                time.sleep(2)  # Esperar a que Lab Recorder procese el comando
            except Exception as e:
                print(f"Error al detener Lab Recorder: {e}")
            
            # Detener LSL
            if root.s:
                root.s.sendall(b"stop\n")
                root.s.close()
            
            # Guardar grabación de audio
            actual_samples = int(recording_duration * root.samplerate)
            trimmed_recording = root.recording[:actual_samples]
            audio_file_name = (f"sub-{info['ID']}_ses-{info['session'].lower()}_"
                              f"task-{info['block'].lower()}_audio.wav")
            audio_path = os.path.join(root.audio_folder, audio_file_name)
            write(audio_path, root.samplerate, np.int16(trimmed_recording * 32767))
            print(f"Grabación finalizada y guardada en {audio_path}")
            
            # Cerrar procesos
            os.system("taskkill /IM LabRecorder.exe /F")
            os.system("taskkill /IM BrainAmpSeries.exe /F")
            os.system("taskkill /IM GameController.exe /F")
            
        root.recording_active = False
        root.quit()

    root = tk.Tk()
    root.title("Configuración de la sesión")
    root.recording_active = False
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    info = {}
    # ID
    tk.Label(root, text="ID (00-99):").grid(row=0, column=0, padx=5, pady=5)
    id_entry = tk.Entry(root)
    id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
    
    # Sesión (ahora primero)
    tk.Label(root, text="Sesión:").grid(row=1, column=0, padx=5, pady=5)
    session_var = tk.StringVar(value="VR")
    session_dropdown = ttk.Combobox(root, textvariable=session_var, 
                                  values=["VR", "2D"], 
                                  state="readonly")
    session_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
    
    # Bloque (ahora segundo)
    tk.Label(root, text="Bloque:").grid(row=2, column=0, padx=5, pady=5)
    block_var = tk.StringVar(value="A")
    block_dropdown = ttk.Combobox(root, textvariable=block_var, 
                                values=["A", "B"], 
                                state="readonly")
    block_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
    
    error_label = tk.Label(root, text="", fg="red")
    error_label.grid(row=3, column=0, columnspan=2, pady=5)
    
    status_label = tk.Label(root, text="", fg="green")
    status_label.grid(row=4, column=0, columnspan=2, pady=5)
    
    start_btn = tk.Button(root, text="Comenzar Grabación", command=start_recording)
    start_btn.grid(row=6, column=0, columnspan=2, pady=10, sticky='nsew')
    stop_btn = tk.Button(root, text="Detener Grabación", command=stop_recording, bg="red", fg="white")
    root.mainloop()
    return info, root.recording_active

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', help='Run in test mode without hardware connections')
    args = parser.parse_args()
    info_dict, recording_active = get_participant_info()
    if not recording_active:
        print("Grabación finalizada")
        sys.exit()
